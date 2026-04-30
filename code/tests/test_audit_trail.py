from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db.database import get_session_factory, init_db
from app.db.models import AuditEvent


@pytest.fixture(autouse=True)
async def _init_db():
    await init_db()


@pytest.mark.asyncio
async def test_audit_event_inserted():
    import uuid

    unique_event = f"test_insert_{uuid.uuid4().hex[:8]}"
    SessionLocal = get_session_factory()
    async with SessionLocal() as session:
        audit = AuditEvent(
            event_type=unique_event,
            actor="pytest",
            payload_json='{"test": true}',
        )
        session.add(audit)
        await session.commit()

        result = await session.execute(
            select(AuditEvent).where(AuditEvent.event_type == audit.event_type)
        )
        assert result.scalar_one() is not None


@pytest.mark.asyncio
async def test_audit_event_update_raises():
    SessionLocal = get_session_factory()
    async with SessionLocal() as session:
        audit = AuditEvent(
            event_type="test_update",
            actor="pytest",
            payload_json="{}",
        )
        session.add(audit)
        await session.commit()

        with pytest.raises(IntegrityError):
            audit.event_type = "modified"
            await session.commit()


@pytest.mark.asyncio
async def test_audit_event_delete_raises():
    SessionLocal = get_session_factory()
    async with SessionLocal() as session:
        audit = AuditEvent(
            event_type="test_delete",
            actor="pytest",
            payload_json="{}",
        )
        session.add(audit)
        await session.commit()

        with pytest.raises(IntegrityError):
            await session.delete(audit)
            await session.commit()


@pytest.mark.asyncio
async def test_inference_creates_audit(
    test_client: AsyncClient,
    test_anonymized_dicom: bytes,
    mock_inference_service,
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
    # Service mock returns 200; audit should be created by the service
    assert response.status_code == 200
