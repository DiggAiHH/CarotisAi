"""Tests for model signing and verification pipeline.

Run with:
    pytest code/tests/test_model_signing.py -v
"""

from __future__ import annotations

import json
import sys
import tarfile
from pathlib import Path

import pytest

# scripts/ is not on PYTHONPATH (only backend/ is), so inject it temporarily.
SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from sign_model import _has_cosign, _has_gpg, _sha256_file, sign_bundle  # noqa: E402
from verify_model import verify_bundle  # noqa: E402


@pytest.fixture
def dummy_model(tmp_path: Path) -> Path:
    """Create a minimal dummy ONNX-like file."""
    model = tmp_path / "dummy.onnx"
    model.write_bytes(b"\x00\x01\x02ONNX")
    return model


@pytest.fixture
def dummy_meta(tmp_path: Path) -> Path:
    """Create a minimal metadata JSON."""
    meta = tmp_path / "meta.json"
    meta.write_text(
        json.dumps({"model_version": "v0.0.0", "description": "test"}),
        encoding="utf-8",
    )
    return meta


class TestSignVerifyRoundtrip:
    def test_sign_and_verify_sha256_fallback(
        self, tmp_path: Path, dummy_model: Path, dummy_meta: Path
    ) -> None:
        """Sha256 fallback roundtrip: sign -> verify -> valid."""
        bundle = tmp_path / "signed.tar.gz"
        sig = sign_bundle(
            model_path=dummy_model,
            meta_path=dummy_meta,
            output_path=bundle,
            signer="test@carotis-ai.local",
        )
        assert sig["method"] == "sha256_timestamp"
        assert sig["model_sha256"] == _sha256_file(dummy_model)

        report = verify_bundle(bundle)
        assert report["valid"] is True
        assert report["checks"]["sha256_match"]["ok"] is True
        assert report["checks"]["signature"]["ok"] is True

    def test_tampered_model_rejected(
        self, tmp_path: Path, dummy_model: Path, dummy_meta: Path
    ) -> None:
        """If model.onnx inside the bundle is modified, verification fails."""
        bundle = tmp_path / "signed.tar.gz"
        sign_bundle(
            model_path=dummy_model,
            meta_path=dummy_meta,
            output_path=bundle,
            signer="test@carotis-ai.local",
        )

        # Tamper: extract, modify model, repack
        extract_dir = tmp_path / "tamper"
        extract_dir.mkdir()
        with tarfile.open(bundle, "r:gz") as tar:
            tar.extractall(path=extract_dir, filter="data")

        tampered_model = extract_dir / "model.onnx"
        tampered_model.write_bytes(b"TAMPERED")

        tampered_bundle = tmp_path / "tampered.tar.gz"
        with tarfile.open(tampered_bundle, "w:gz") as tar:
            tar.add(tampered_model, arcname="model.onnx")
            tar.add(extract_dir / "meta.json", arcname="meta.json")
            tar.add(extract_dir / "signature.json", arcname="signature.json")

        report = verify_bundle(tampered_bundle)
        assert report["valid"] is False
        assert report["checks"]["sha256_match"]["ok"] is False

    def test_missing_meta_rejected(self, tmp_path: Path, dummy_model: Path) -> None:
        """Signing must raise FileNotFoundError when meta.json is missing."""
        missing_meta = tmp_path / "nonexistent.json"
        with pytest.raises(FileNotFoundError):
            sign_bundle(
                model_path=dummy_model,
                meta_path=missing_meta,
                output_path=tmp_path / "signed.tar.gz",
                signer="test@carotis-ai.local",
            )

    def test_missing_model_rejected(self, tmp_path: Path, dummy_meta: Path) -> None:
        """Signing must raise FileNotFoundError when model is missing."""
        missing_model = tmp_path / "nonexistent.onnx"
        with pytest.raises(FileNotFoundError):
            sign_bundle(
                model_path=missing_model,
                meta_path=dummy_meta,
                output_path=tmp_path / "signed.tar.gz",
                signer="test@carotis-ai.local",
            )

    def test_missing_bundle_file_rejected(self, tmp_path: Path) -> None:
        """Verification must raise FileNotFoundError when bundle is missing."""
        missing_bundle = tmp_path / "missing.tar.gz"
        with pytest.raises(FileNotFoundError):
            verify_bundle(missing_bundle)

    def test_timestamp_expiry(
        self, tmp_path: Path, dummy_model: Path, dummy_meta: Path
    ) -> None:
        """Signatures older than max_age_days must be rejected."""
        bundle = tmp_path / "signed.tar.gz"
        sign_bundle(
            model_path=dummy_model,
            meta_path=dummy_meta,
            output_path=bundle,
            signer="test@carotis-ai.local",
        )

        # max_age_days=0 should reject a freshly created signature because
        # the age is > 0 seconds (tiny but non-zero).
        report = verify_bundle(bundle, max_age_days=0)
        assert report["valid"] is False
        assert report["checks"]["timestamp"]["ok"] is False

        # max_age_days=1 should accept a fresh signature.
        report = verify_bundle(bundle, max_age_days=1)
        assert report["valid"] is True
        assert report["checks"]["timestamp"]["ok"] is True

    def test_bundle_integrity_missing_meta(
        self, tmp_path: Path, dummy_model: Path
    ) -> None:
        """A bundle without meta.json must raise FileNotFoundError."""
        bad_bundle = tmp_path / "bad.tar.gz"
        with tarfile.open(bad_bundle, "w:gz") as tar:
            tar.add(dummy_model, arcname="model.onnx")

        with pytest.raises(FileNotFoundError, match="meta.json"):
            verify_bundle(bad_bundle)

    def test_bundle_integrity_missing_sig(
        self, tmp_path: Path, dummy_model: Path, dummy_meta: Path
    ) -> None:
        """A bundle without signature.json must raise FileNotFoundError."""
        bad_bundle = tmp_path / "bad.tar.gz"
        with tarfile.open(bad_bundle, "w:gz") as tar:
            tar.add(dummy_model, arcname="model.onnx")
            tar.add(dummy_meta, arcname="meta.json")

        with pytest.raises(FileNotFoundError, match="signature.json"):
            verify_bundle(bad_bundle)


class TestFallbackSigning:
    def test_sha256_fallback_deterministic(
        self, tmp_path: Path, dummy_model: Path, dummy_meta: Path
    ) -> None:
        """Fallback signing produces identical SHA-256 for identical input."""
        bundle1 = tmp_path / "signed1.tar.gz"
        bundle2 = tmp_path / "signed2.tar.gz"

        sig1 = sign_bundle(
            model_path=dummy_model,
            meta_path=dummy_meta,
            output_path=bundle1,
            signer="test@carotis-ai.local",
        )
        sig2 = sign_bundle(
            model_path=dummy_model,
            meta_path=dummy_meta,
            output_path=bundle2,
            signer="test@carotis-ai.local",
        )

        # method must be fallback when cosign/gpg unavailable
        if not _has_cosign() and not _has_gpg():
            assert sig1["method"] == "sha256_timestamp"
            assert sig2["method"] == "sha256_timestamp"

        assert sig1["model_sha256"] == sig2["model_sha256"]

    def test_signer_recorded_in_payload(
        self, tmp_path: Path, dummy_model: Path, dummy_meta: Path
    ) -> None:
        """Signer identity is preserved in signature payload."""
        bundle = tmp_path / "signed.tar.gz"
        sig = sign_bundle(
            model_path=dummy_model,
            meta_path=dummy_meta,
            output_path=bundle,
            signer="lou@diggai.de",
        )
        assert sig["signer"] == "lou@diggai.de"

        report = verify_bundle(bundle)
        assert report["signer"] == "lou@diggai.de"
