"""Sign an ONNX model bundle for Carotis-AI.

Creates a signed .tar.gz containing:
  - model.onnx   (the model file)
  - meta.json    (metadata enriched with SHA-256 and signer info)
  - signature.json (signature payload)

Signing hierarchy (local-first, no cloud upload):
  1. Sigstore / cosign (if cosign binary is available)
  2. GPG detached signature (if gpg binary is available)
  3. SHA-256 + Timestamp fallback (audit-trail only, no crypto signature)

Usage:
    python scripts/sign_model.py \
        --model data/models/mfsd_unet.onnx \
        --meta data/models/mfsd_unet_meta.json \
        --output data/models/mfsd_unet_signed.tar.gz \
        --signer lou@diggai.de
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import subprocess
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _sha256_file(path: Path) -> str:
    """Compute SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _has_cosign() -> bool:
    """Return True if the cosign CLI is installed."""
    try:
        subprocess.run(
            ["cosign", "version"],
            capture_output=True,
            check=True,
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def _has_gpg() -> bool:
    """Return True if the gpg CLI is installed."""
    try:
        subprocess.run(
            ["gpg", "--version"],
            capture_output=True,
            check=True,
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def _sign_cosign(blob_path: Path, _signer: str) -> dict[str, Any]:
    """Sign a blob with cosign (requires pre-generated cosign.key)."""
    sig_path = blob_path.with_suffix(".sig")
    cmd = [
        "cosign",
        "sign-blob",
        str(blob_path),
        "--key",
        "cosign.key",
        "--output-signature",
        str(sig_path),
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    sig_data = sig_path.read_bytes()
    sig_path.unlink(missing_ok=True)
    return {
        "method": "cosign",
        "signature_b64": base64.b64encode(sig_data).decode("ascii"),
    }


def _sign_gpg(blob_path: Path, _signer: str) -> dict[str, Any]:
    """Create an ASCII-armored detached GPG signature."""
    cmd = [
        "gpg",
        "--batch",
        "--yes",
        "--armor",
        "--detach-sign",
        "--output",
        "-",
        str(blob_path),
    ]
    result = subprocess.run(cmd, capture_output=True, check=True)
    return {
        "method": "gpg",
        "signature_b64": base64.b64encode(result.stdout).decode("ascii"),
    }


def _sign_sha256(blob_path: Path, _signer: str) -> dict[str, Any]:
    """Fallback: SHA-256 digest + timestamp (no cryptographic signature)."""
    sha = _sha256_file(blob_path)
    return {
        "method": "sha256_timestamp",
        "signature_b64": "",
        "sha256": sha,
    }


def sign_bundle(
    model_path: Path,
    meta_path: Path,
    output_path: Path,
    signer: str,
) -> dict[str, Any]:
    """Create a signed bundle (.tar.gz) from model + metadata.

    Returns the signature payload dict.
    """
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not meta_path.exists():
        raise FileNotFoundError(f"Meta file not found: {meta_path}")

    meta: dict[str, Any] = json.loads(meta_path.read_text(encoding="utf-8"))
    model_sha = _sha256_file(model_path)
    meta["model_sha256"] = model_sha
    meta["signed_at"] = datetime.now(timezone.utc).isoformat()
    meta["signer"] = signer

    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)
        tmp_model = tmpdir / "model.onnx"
        tmp_meta = tmpdir / "meta.json"
        tmp_sig = tmpdir / "signature.json"

        tmp_model.write_bytes(model_path.read_bytes())
        tmp_meta.write_text(json.dumps(meta, indent=2), encoding="utf-8")

        sig_info: dict[str, Any] | None = None
        if _has_cosign():
            try:
                sig_info = _sign_cosign(tmp_model, signer)
            except subprocess.CalledProcessError:
                sig_info = None
        if sig_info is None and _has_gpg():
            try:
                sig_info = _sign_gpg(tmp_model, signer)
            except subprocess.CalledProcessError:
                sig_info = None
        if sig_info is None:
            sig_info = _sign_sha256(tmp_model, signer)

        signature_payload = {
            "signer": signer,
            "timestamp": meta["signed_at"],
            "method": sig_info["method"],
            "signature_b64": sig_info.get("signature_b64", ""),
            "model_sha256": model_sha,
        }
        if "sha256" in sig_info:
            signature_payload["sha256"] = sig_info["sha256"]

        tmp_sig.write_text(
            json.dumps(signature_payload, indent=2),
            encoding="utf-8",
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with tarfile.open(output_path, "w:gz") as tar:
            tar.add(tmp_model, arcname="model.onnx")
            tar.add(tmp_meta, arcname="meta.json")
            tar.add(tmp_sig, arcname="signature.json")

    return signature_payload


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sign an ONNX model bundle for Carotis-AI"
    )
    parser.add_argument("--model", required=True, help="Path to the .onnx model file")
    parser.add_argument("--meta", required=True, help="Path to the metadata .json file")
    parser.add_argument(
        "--output",
        required=True,
        help="Output path for the signed .tar.gz bundle",
    )
    parser.add_argument(
        "--signer",
        default="unknown@carotis-ai.local",
        help="Identity of the signer (email or name)",
    )
    args = parser.parse_args()

    root = Path(__file__).parent.parent
    model_path = Path(args.model)
    meta_path = Path(args.meta)
    output_path = Path(args.output)

    if not model_path.is_absolute():
        model_path = root / model_path
    if not meta_path.is_absolute():
        meta_path = root / meta_path
    if not output_path.is_absolute():
        output_path = root / output_path

    print(f"Signing model: {model_path}")
    print(f"Meta:          {meta_path}")
    print(f"Output:        {output_path}")

    sig = sign_bundle(model_path, meta_path, output_path, args.signer)
    print(f"Method:        {sig['method']}")
    print(f"SHA-256:       {sig['model_sha256']}")
    print(f"Signed at:     {sig['timestamp']}")
    print(f"Signer:        {sig['signer']}")
    print("Done.")


if __name__ == "__main__":
    main()
