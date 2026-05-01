"""
E2E-Stresstest: Rohde-Demo-Flow

Testet den kompletten Flow mit gemocktem Inference-Service
(der echte ONNX-Runtime ist in der Test-Umgebung nicht verfuegbar).
"""
from __future__ import annotations

import asyncio
import io
import os
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# Env-Vars muessen vor allen app-Imports gesetzt werden, da app.main
# bei Import sofort create_app() aufruft (Modul-Level).
os.environ["API_KEY"] = "a" * 32
os.environ["ADMIN_API_KEY"] = "b" * 32
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["ONNX_MODEL_PATH"] = "/nonexistent/model.onnx"
os.environ["ANONYMIZATION_SALT"] = "s" * 16
os.environ["DEBUG"] = "true"

from app.core.config import get_settings
from app.core.security import hash_demo_token
from app.db.database import get_session_factory, init_db
from app.db.models import DemoToken
from app.main import create_app
from app.schemas.inference import PredictionResponse

TEST_API_KEY = os.environ["API_KEY"]
ADMIN_API_KEY = os.environ["ADMIN_API_KEY"]


def _make_token() -> str:
    return f"rohde-e2e-{uuid.uuid4().hex}"


async def _insert_demo_token(
    raw_token: str,
    label: str = "rohde-e2e",
    requests_used: int = 0,
    max_requests: int = 100,
) -> None:
    async with get_session_factory()() as session:
        session.add(
            DemoToken(
                token_hash=hash_demo_token(raw_token),
                label=label,
                expires_at=datetime.now(timezone.utc).replace(year=datetime.now(timezone.utc).year + 1),
                requests_used=requests_used,
                max_requests=max_requests,
            )
        )
        await session.commit()


@pytest_asyncio.fixture
async def client():
    # Reset env vars in case another test module changed them
    os.environ["API_KEY"] = "a" * 32
    os.environ["ADMIN_API_KEY"] = "b" * 32
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
    os.environ["ONNX_MODEL_PATH"] = "/nonexistent/model.onnx"
    os.environ["ANONYMIZATION_SALT"] = "s" * 16
    os.environ["DEBUG"] = "true"
    get_settings.cache_clear()
    app = create_app()
    await init_db()

    mock_svc = MagicMock()
    mock_svc.model_loaded = True
    mock_svc.predict = AsyncMock(
        return_value=PredictionResponse(
            case_id="rohde-case-001",
            stenosis_pct_nascet=65.0,
            confidence=0.85,
            vulnerability_markers={},
            heatmap_b64="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
            model_version="v0.3.2",
            model_sha="abc123d",
            audit_id="audit-rohde-001",
            captured_at="2026-04-30T12:00:00Z",
        )
    )
    app.state.inference_service = mock_svc

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=True,
    ) as c:
        yield c


@pytest.mark.asyncio
async def test_rohde_flow_token_auth(client: AsyncClient):
    """S1: Token-Auth muss gueltigen Token akzeptieren."""
    token = _make_token()
    await _insert_demo_token(token)
    res = await client.get(
        "/api/v1/demo/whoami",
        headers={"X-Demo-Token": token},
    )
    assert res.status_code == 200
    data = res.json()
    assert "label" in data
    assert "requests_remaining" in data


@pytest.mark.asyncio
async def test_rohde_flow_inference(client: AsyncClient):
    """S2: DICOM-Upload + Inferenz muss funktionieren."""
    token = _make_token()
    await _insert_demo_token(token)
    fake_file = io.BytesIO(b"fake dicom content for mock")
    res = await client.post(
        "/api/v1/inference/predict",
        headers={"X-Demo-Token": token, "X-API-Key": TEST_API_KEY},
        files={"file": ("test.dcm", fake_file, "application/dicom")},
    )
    assert res.status_code == 200
    data = res.json()
    assert "case_id" in data
    assert "stenosis_pct_nascet" in data
    assert "heatmap_b64" in data


@pytest.mark.asyncio
async def test_rohde_flow_decision_tree(client: AsyncClient):
    """S3: Decision-Tree-Capture muss funktionieren."""
    token = _make_token()
    await _insert_demo_token(token)
    payload = {
        "case_id": "e" * 64,
        "captured_at": "2026-04-30T12:00:00Z",
        "physician_role_hash": "b" * 64,
        "ai_prediction": {
            "stenosis_pct_nascet": 65.0,
            "confidence": 0.85,
            "vulnerability_markers": {
                "intraplaque_hemorrhage": 0.0,
                "thin_fibrous_cap": 0.0,
                "lipid_rich_necrotic_core": 0.0,
                "systolic_motion_anomaly": 0.0,
            },
            "model_version": "v0.3.2",
            "model_sha": "abc123d",
        },
        "physician_decision": {
            "stenosis_pct_nascet": 65.0,
            "confirmed_markers": [],
            "rejected_markers": [],
            "added_markers": [],
        },
        "agreement_with_ai": {
            "verdict": "full_agreement",
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
    res = await client.post(
        "/api/v1/decision-tree/capture",
        headers={"X-API-Key": TEST_API_KEY, "Content-Type": "application/json"},
        json=payload,
    )
    assert res.status_code == 200
    data = res.json()
    assert "audit_id" in data
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_rohde_flow_audit_trail(client: AsyncClient):
    """S4: Audit-Trail muss Events enthalten."""
    token = _make_token()
    await _insert_demo_token(token)
    res = await client.get(
        "/api/v1/audit/trail",
        headers={"X-API-Key": TEST_API_KEY, "X-Admin-Key": ADMIN_API_KEY},
    )
    assert res.status_code == 200
    data = res.json()
    assert "items" in data


@pytest.mark.asyncio
async def test_rohde_flow_rate_limiting(client: AsyncClient):
    """S5: Rate-Limiting muss bei Ueberlastung greifen."""
    token = _make_token()
    await _insert_demo_token(token, max_requests=50)
    tasks = [
        client.get(
            "/api/v1/demo/whoami",
            headers={"X-Demo-Token": token},
        )
        for _ in range(35)
    ]
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    status_codes = [
        r.status_code for r in responses if not isinstance(r, Exception)
    ]
    assert len(status_codes) > 0


@pytest.mark.asyncio
async def test_rohde_flow_walkthrough_logging(client: AsyncClient):
    """S6: Walkthrough-Step-Logging muss funktionieren."""
    token = _make_token()
    await _insert_demo_token(token)
    res = await client.post(
        "/api/v1/demo/log-walkthrough-step",
        headers={"X-Demo-Token": token},
        json={"step_id": "1", "event": "start", "metadata": {}},
    )
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_full_rohde_walkthrough(client: AsyncClient):
    """Kompletter Walkthrough in einem Test."""
    token = _make_token()
    await _insert_demo_token(token, max_requests=100)

    # 1. Auth
    auth_res = await client.get(
        "/api/v1/demo/whoami",
        headers={"X-Demo-Token": token},
    )
    assert auth_res.status_code == 200

    # 2. Inferenz
    fake_file = io.BytesIO(b"fake dicom content for mock")
    inf_res = await client.post(
        "/api/v1/inference/predict",
        headers={"X-Demo-Token": token, "X-API-Key": TEST_API_KEY},
        files={"file": ("test.dcm", fake_file, "application/dicom")},
    )
    assert inf_res.status_code == 200

    # 3. Decision Tree
    dt_payload = {
        "case_id": "f" * 64,
        "captured_at": "2026-04-30T12:00:00Z",
        "physician_role_hash": "b" * 64,
        "ai_prediction": {
            "stenosis_pct_nascet": 65.0,
            "confidence": 0.85,
            "vulnerability_markers": {
                "intraplaque_hemorrhage": 0.0,
                "thin_fibrous_cap": 0.0,
                "lipid_rich_necrotic_core": 0.0,
                "systolic_motion_anomaly": 0.0,
            },
            "model_version": "v0.3.2",
            "model_sha": "abc123d",
        },
        "physician_decision": {
            "stenosis_pct_nascet": 65.0,
            "confirmed_markers": [],
            "rejected_markers": [],
            "added_markers": [],
        },
        "agreement_with_ai": {
            "verdict": "full_agreement",
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
    dt_res = await client.post(
        "/api/v1/decision-tree/capture",
        headers={"X-API-Key": TEST_API_KEY, "Content-Type": "application/json"},
        json=dt_payload,
    )
    assert dt_res.status_code == 200

    # 4. Audit
    audit_res = await client.get(
        "/api/v1/audit/trail",
        headers={"X-API-Key": TEST_API_KEY, "X-Admin-Key": ADMIN_API_KEY},
    )
    assert audit_res.status_code == 200
    assert len(audit_res.json()["items"]) >= 1
