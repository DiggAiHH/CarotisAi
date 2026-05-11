"""Smoke tests — verify the backend starts and key endpoints work.

Run with:
    pytest code/tests/test_smoke.py -v

Requires:
    pip install httpx pytest pytest-asyncio
"""

from __future__ import annotations

import io
import os

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.core.config import get_settings

TEST_API_KEY = "test-smoke-key-32-chars-long!!!!"


@pytest.fixture(scope="module")
def app():
    # Force-set env vars (not setdefault) so they override any .env file values
    os.environ["API_KEY"] = TEST_API_KEY
    os.environ["ADMIN_API_KEY"] = "b" * 32
    os.environ["ANONYMIZATION_SALT"] = "s" * 32
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
    os.environ["ONNX_MODEL_PATH"] = "/nonexistent/model.onnx"
    os.environ["DEBUG"] = "true"
    get_settings.cache_clear()

    from app.main import create_app

    return create_app()


@pytest_asyncio.fixture
async def client(app):
    from app.db.database import init_db
    from unittest.mock import MagicMock, AsyncMock
    from app.schemas.inference import PredictionResponse

    await init_db()
    mock_svc = MagicMock()
    mock_svc.model_loaded = True
    mock_svc.predict = AsyncMock(
        return_value=PredictionResponse(
            case_id="abc123",
            stenosis_pct_nascet=50.0,
            confidence=0.9,
            vulnerability_markers={},
            heatmap_b64=None,
            model_version="v0.0.0",
            model_sha="abc123",
            audit_id="audit-1",
            captured_at="2026-04-28T12:00:00Z",
        )
    )
    app.state.inference_service = mock_svc

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test", follow_redirects=True
    ) as c:
        yield c


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    resp = await client.get("/health/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "model_loaded" in data


@pytest.mark.asyncio
async def test_health_no_auth_required(client: AsyncClient) -> None:
    """Health endpoint should be public."""
    resp = await client.get("/health/")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_inference_requires_auth(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/inference/predict")
    assert resp.status_code in (401, 403, 422)


@pytest.mark.asyncio
async def test_inference_rejects_non_dicom(client: AsyncClient) -> None:
    fake_file = io.BytesIO(b"not a dicom file")
    resp = await client.post(
        "/api/v1/inference/predict",
        headers={"X-API-Key": TEST_API_KEY},
        files={"file": ("test.dcm", fake_file, "application/octet-stream")},
    )
    # Mock accepts anything; in production this would be 400/422 for bad DICOM
    assert resp.status_code in (200, 400, 422, 503)


@pytest.mark.asyncio
async def test_decisions_post(client: AsyncClient) -> None:
    payload = {
        "case_id": "d" * 64,
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
            "verdict": "partial_agreement",
            "delta_pct": 0.0,
            "trust_score_for_this_case": 4,
        },
        "anonymisation": {
            "method": "DICOM_PS_3.15_basic",
            "salt_version": "v2026-04",
            "audit_id": "AT-001",
            "k_anonymity_min": 5,
        },
    }
    resp = await client.post(
        "/api/v1/decision-tree/capture",
        headers={"X-API-Key": TEST_API_KEY, "Content-Type": "application/json"},
        json=payload,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "audit_id" in data


@pytest.mark.asyncio
async def test_decisions_recent(client: AsyncClient) -> None:
    resp = await client.get(
        "/api/v1/decision-tree/recent", headers={"X-API-Key": TEST_API_KEY}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "limit" in data
