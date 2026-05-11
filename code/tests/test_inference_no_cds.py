from __future__ import annotations

import io

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_default_inference_response_does_not_expose_cds_fields(
    test_client: AsyncClient,
) -> None:
    response = await test_client.post(
        "/api/v1/inference/predict",
        headers={"X-API-Key": "a" * 32},
        files={"file": ("test.dcm", io.BytesIO(b"mock dicom"), "application/dicom")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "stenosis_pct_nascet" not in payload
    assert "vulnerability_markers" not in payload
    assert "confidence" not in payload
    assert payload["case_id"] == "abc123"
    assert "heatmap_b64" in payload
