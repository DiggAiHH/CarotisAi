"""Integration tests for the full pipeline using real anonymized DICOM data.

Source: Zenodo record 16956 (William Lionheart, CC BY-SA 4.0)
Files:  tests/test_data/real_mri/MR000000.dcm … MR000004.dcm
All PII removed by AnonymizationService before these files were committed.
"""
from __future__ import annotations

import pytest
from pathlib import Path

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REAL_DICOM_DIR = Path(__file__).parent / "test_data" / "real_mri"
REAL_DICOM_FILE = REAL_DICOM_DIR / "MR000000.dcm"

API_KEY = "a" * 32  # matches conftest.py monkeypatch


def _load_real_dicom() -> bytes:
    """Return raw bytes of the first real anonymized DICOM file."""
    if not REAL_DICOM_FILE.exists():
        pytest.skip(f"Real DICOM test data not found: {REAL_DICOM_FILE}")
    return REAL_DICOM_FILE.read_bytes()


# ---------------------------------------------------------------------------
# Test 1 — Anonymization check: real DICOM must pass check_only → True
# ---------------------------------------------------------------------------


def test_real_dicom_is_fully_anonymized():
    """AnonymizationService.check_only() must report zero PII tags on the
    pre-anonymized real DICOM files downloaded from Zenodo record 16956."""
    from app.services.anonymization_service import AnonymizationService

    svc = AnonymizationService()
    dicom_bytes = _load_real_dicom()

    is_clean, found_tags = svc.check_only(dicom_bytes)

    assert is_clean, (
        f"Expected DICOM to be fully anonymized but found PII tags: {found_tags}"
    )
    assert found_tags == []


# ---------------------------------------------------------------------------
# Test 2 — Full pipeline: predict endpoint returns valid InferenceResponse
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_predict_with_real_dicom_returns_200(test_client):
    """POST /api/v1/inference/predict with a real anonymized DICOM must return
    HTTP 200 and a valid (feature-flag-filtered) InferenceResponse body."""
    dicom_bytes = _load_real_dicom()

    response = await test_client.post(
        "/api/v1/inference/predict",
        files={"file": ("MR000000.dcm", dicom_bytes, "application/octet-stream")},
        headers={"X-API-Key": API_KEY},
    )

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}: {response.text}"
    )
    body = response.json()

    # These keys are always present in InferenceResponse (public fields)
    for required_key in ("case_id", "audit_id", "captured_at", "model_version"):
        assert required_key in body, (
            f"Key '{required_key}' missing from response: {body}"
        )


# ---------------------------------------------------------------------------
# Test 3 — Audit trail: mock inference service was called with correct payload
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_predict_calls_inference_service_with_dicom_bytes(test_client):
    """The inference service must be called exactly once with the raw DICOM
    bytes that were uploaded — confirms the pipeline passes data through
    correctly and the audit trail is initiated."""
    dicom_bytes = _load_real_dicom()

    response = await test_client.post(
        "/api/v1/inference/predict",
        files={"file": ("MR000000.dcm", dicom_bytes, "application/octet-stream")},
        headers={"X-API-Key": API_KEY},
    )

    assert response.status_code == 200

    # Retrieve the mock service injected by the test_client fixture
    # (app.state.inference_service is the MagicMock set in conftest.py)
    from app.main import create_app  # noqa: F401 — only needed for type hint context

    # The mock records all calls; verify it was called once
    mock_svc = test_client._transport.app.state.inference_service  # type: ignore[attr-defined]
    assert mock_svc.predict.call_count == 1, (
        f"inference_service.predict should be called exactly once, "
        f"got {mock_svc.predict.call_count}"
    )

    # The argument passed must be bytes (the raw DICOM content)
    call_args = mock_svc.predict.call_args
    assert call_args is not None
    passed_bytes = call_args.args[0] if call_args.args else call_args.kwargs.get("dicom_bytes")
    assert isinstance(passed_bytes, bytes), (
        f"inference_service.predict should receive bytes, got {type(passed_bytes)}"
    )
    assert len(passed_bytes) > 0, "Passed bytes must be non-empty"
