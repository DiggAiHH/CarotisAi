from __future__ import annotations

import pytest
from httpx import AsyncClient

_VALID_PAYLOAD = {
    "case_id": "a" * 64,
    "captured_at": "2026-04-28T12:00:00Z",
    "physician_role_hash": "b" * 64,
    "ai_prediction": {
        "stenosis_pct_nascet": 50.0,
        "confidence": 0.9,
        "vulnerability_markers": {
            "intraplaque_hemorrhage": 0.5,
            "thin_fibrous_cap": 0.2,
            "lipid_rich_necrotic_core": 0.3,
            "systolic_motion_anomaly": 0.1,
        },
        "model_version": "v0.3.2",
        "model_sha": "abc123d",
    },
    "physician_decision": {
        "stenosis_pct_nascet": 50.0,
        "confirmed_markers": [],
        "rejected_markers": [],
        "added_markers": [],
    },
    "agreement_with_ai": {
        "verdict": "full_agreement",
        "delta_pct": 0.0,
        "delta_markers": [],
        "trust_score_for_this_case": 5,
    },
    "anonymisation": {
        "method": "DICOM_PS_3.15_basic",
        "salt_version": "v2026-04",
        "audit_id": "AT-001",
        "k_anonymity_min": 5,
    },
}


@pytest.mark.asyncio
async def test_capture_valid(test_client: AsyncClient):
    # Use a unique case_id to avoid UNIQUE constraint collisions across tests
    payload = {**_VALID_PAYLOAD, "case_id": "c" * 64}
    response = await test_client.post(
        "/api/v1/decision-tree/capture",
        json=payload,
        headers={"X-API-Key": "a" * 32},
    )
    assert response.status_code == 200
    data = response.json()
    assert "audit_id" in data
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_capture_missing_field(test_client: AsyncClient):
    payload = {**_VALID_PAYLOAD}
    del payload["agreement_with_ai"]
    response = await test_client.post(
        "/api/v1/decision-tree/capture",
        json=payload,
        headers={"X-API-Key": "a" * 32},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_capture_invalid_case_id(test_client: AsyncClient):
    payload = {**_VALID_PAYLOAD, "case_id": "short"}
    response = await test_client.post(
        "/api/v1/decision-tree/capture",
        json=payload,
        headers={"X-API-Key": "a" * 32},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_capture_invalid_verdict(test_client: AsyncClient):
    payload = {**_VALID_PAYLOAD}
    payload["agreement_with_ai"]["verdict"] = "invalid"
    response = await test_client.post(
        "/api/v1/decision-tree/capture",
        json=payload,
        headers={"X-API-Key": "a" * 32},
    )
    assert response.status_code == 422
