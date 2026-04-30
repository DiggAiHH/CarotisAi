"""Verify a signed Carotis-AI model bundle.

Extracts a .tar.gz signed bundle and validates:
  - All expected files are present (model.onnx, meta.json, signature.json)
  - SHA-256 of model.onnx matches the value recorded in meta.json
  - Signature is valid (cosign, gpg, or sha256_timestamp fallback)
  - Optional: signature timestamp is not older than --max-age-days

Usage:
    python scripts/verify_model.py \
        --bundle data/models/mfsd_unet_signed.tar.gz \
        --format json
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def _sha256_file(path: Path) -> str:
    """Compute SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _extract_bundle(bundle_path: Path, dest: Path) -> tuple[Path, Path, Path]:
    """Extract tar.gz and return paths to model, meta, signature."""
    with tarfile.open(bundle_path, "r:gz") as tar:
        tar.extractall(path=dest, filter="data")

    model = dest / "model.onnx"
    meta = dest / "meta.json"
    sig = dest / "signature.json"

    if not model.exists():
        raise FileNotFoundError("Bundle missing model.onnx")
    if not meta.exists():
        raise FileNotFoundError("Bundle missing meta.json")
    if not sig.exists():
        raise FileNotFoundError("Bundle missing signature.json")

    return model, meta, sig


def _verify_cosign(model_path: Path, sig_b64: str) -> dict[str, Any]:
    """Verify a cosign signature blob."""
    sig_path = model_path.with_suffix(".sig")
    sig_path.write_bytes(base64.b64decode(sig_b64))
    try:
        cmd = [
            "cosign",
            "verify-blob",
            str(model_path),
            "--key",
            "cosign.pub",
            "--signature",
            str(sig_path),
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        return {"valid": True, "detail": "cosign verify succeeded"}
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.decode("utf-8", errors="ignore") if exc.stderr else ""
        return {"valid": False, "detail": f"cosign verify failed: {stderr}"}
    finally:
        sig_path.unlink(missing_ok=True)


def _verify_gpg(model_path: Path, sig_b64: str) -> dict[str, Any]:
    """Verify a GPG detached signature."""
    sig_path = model_path.with_suffix(".asc")
    sig_path.write_bytes(base64.b64decode(sig_b64))
    try:
        cmd = [
            "gpg",
            "--batch",
            "--yes",
            "--verify",
            str(sig_path),
            str(model_path),
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        return {"valid": True, "detail": "gpg verify succeeded"}
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.decode("utf-8", errors="ignore") if exc.stderr else ""
        return {"valid": False, "detail": f"gpg verify failed: {stderr}"}
    finally:
        sig_path.unlink(missing_ok=True)


def verify_bundle(
    bundle_path: Path,
    max_age_days: int | None = None,
) -> dict[str, Any]:
    """Verify a signed model bundle and return a structured report."""
    if not bundle_path.exists():
        raise FileNotFoundError(f"Bundle not found: {bundle_path}")

    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)
        model_path, meta_path, sig_path = _extract_bundle(bundle_path, tmpdir)

        meta: dict[str, Any] = json.loads(meta_path.read_text(encoding="utf-8"))
        sig: dict[str, Any] = json.loads(sig_path.read_text(encoding="utf-8"))

        report: dict[str, Any] = {
            "bundle": str(bundle_path),
            "valid": True,
            "checks": {},
            "model_sha256": "",
            "signed_at": sig.get("timestamp"),
            "signer": sig.get("signer"),
            "method": sig.get("method"),
        }

        # ---- SHA-256 check ----
        actual_sha = _sha256_file(model_path)
        report["model_sha256"] = actual_sha
        expected_sha = meta.get("model_sha256") or sig.get("model_sha256")
        if expected_sha and actual_sha == expected_sha:
            report["checks"]["sha256_match"] = {
                "ok": True,
                "detail": "SHA-256 matches",
            }
        else:
            report["checks"]["sha256_match"] = {
                "ok": False,
                "detail": (
                    f"SHA-256 mismatch: expected {expected_sha}, got {actual_sha}"
                ),
            }
            report["valid"] = False

        # ---- Timestamp age check ----
        if max_age_days is not None and sig.get("timestamp"):
            signed_at = datetime.fromisoformat(sig["timestamp"])
            age = datetime.now(timezone.utc) - signed_at
            if age <= timedelta(days=max_age_days):
                report["checks"]["timestamp"] = {
                    "ok": True,
                    "detail": f"Signature age {age.days}d <= {max_age_days}d",
                }
            else:
                report["checks"]["timestamp"] = {
                    "ok": False,
                    "detail": f"Signature age {age.days}d > {max_age_days}d",
                }
                report["valid"] = False
        else:
            report["checks"]["timestamp"] = {
                "ok": True,
                "detail": "No max_age check",
            }

        # ---- Signature validity check ----
        method = sig.get("method", "unknown")
        if method == "cosign":
            result = _verify_cosign(model_path, sig.get("signature_b64", ""))
            report["checks"]["signature"] = result
            if not result["valid"]:
                report["valid"] = False
        elif method == "gpg":
            result = _verify_gpg(model_path, sig.get("signature_b64", ""))
            report["checks"]["signature"] = result
            if not result["valid"]:
                report["valid"] = False
        elif method == "sha256_timestamp":
            report["checks"]["signature"] = {
                "ok": True,
                "detail": "SHA-256+Timestamp fallback (no cryptographic signature)",
            }
        else:
            report["checks"]["signature"] = {
                "ok": False,
                "detail": f"Unknown signing method: {method}",
            }
            report["valid"] = False

    return report


def _format_markdown(report: dict[str, Any]) -> str:
    """Render report as Markdown."""
    lines = [
        "# Carotis-AI Model Verification Report",
        "",
        f"- **Bundle:** `{report['bundle']}`",
        f"- **Valid:** {'✅ YES' if report['valid'] else '❌ NO'}",
        f"- **Method:** {report['method']}",
        f"- **Signer:** {report['signer']}",
        f"- **Signed at:** {report['signed_at']}",
        f"- **Model SHA-256:** `{report['model_sha256']}`",
        "",
        "## Checks",
        "",
    ]
    for name, check in report["checks"].items():
        icon = "✅" if check.get("ok") else "❌"
        lines.append(f"### {name}")
        lines.append(f"{icon} {check.get('detail', '')}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify a signed Carotis-AI model bundle"
    )
    parser.add_argument(
        "--bundle", required=True, help="Path to the signed .tar.gz bundle"
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Output format",
    )
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=None,
        help="Reject signatures older than N days",
    )
    args = parser.parse_args()

    root = Path(__file__).parent.parent
    bundle_path = Path(args.bundle)
    if not bundle_path.is_absolute():
        bundle_path = root / bundle_path

    report = verify_bundle(bundle_path, max_age_days=args.max_age_days)

    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(_format_markdown(report))

    sys.exit(0 if report["valid"] else 1)


if __name__ == "__main__":
    main()
