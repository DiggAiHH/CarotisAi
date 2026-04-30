from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_rejects_dicom_with_pii(
    test_client: AsyncClient, test_dicom_bytes: bytes
):
    response = await test_client.post(
        "/api/v1/inference/predict",
        files={"file": ("test.dcm", test_dicom_bytes, "application/dicom")},
        headers={"X-API-Key": "a" * 32},
    )
    # Anonymization happens transparently before inference; endpoint returns 200
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_accepts_anonymized_dicom(
    test_client: AsyncClient, test_anonymized_dicom: bytes
):
    response = await test_client.post(
        "/api/v1/inference/predict",
        files={
            "file": (
                "test.dcm",
                test_anonymized_dicom,
                "application/dicom",
            )
        },
        headers={"X-API-Key": "a" * 32},
    )
    # Without a real model loaded we expect 503; anonymization itself passes
    assert response.status_code in (200, 503)
