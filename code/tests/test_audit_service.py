"""Tests for the hardened AuditService.

Covers: PII stripping, append-only enforcement, no raw PII in payload_json.
"""

from __future__ import annotations

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db.database import get_session_factory, init_db
from app.db.models import AuditEvent
from app.services.audit_service import AuditService, _strip_pii_from_payload


@pytest.fixture(autouse=True)
async def _init_db():
    await init_db()


class TestPIIStrip:
    def test_strip_redacts_known_keys(self):
        payload = {"patient_name": "Mueller", "result": 42}
        out = _strip_pii_from_payload(payload)
        assert out["patient_name"] == "<REDACTED>"
        assert out["result"] == 42

    def test_strip_nested(self):
        payload = {"outer": {"patient_id": "12345", "score": 0.9}}
        out = _strip_pii_from_payload(payload)
        assert out["outer"]["patient_id"] == "<REDACTED>"
        assert out["outer"]["score"] == 0.9

    def test_strip_list_of_dicts(self):
        payload = {"items": [{"patient_birth_date": "1990-01-01", "ok": True}]}
        out = _strip_pii_from_payload(payload)
        assert out["items"][0]["patient_birth_date"] == "<REDACTED>"
        assert out["items"][0]["ok"] is True


class TestLogEvent:
    @pytest.mark.asyncio
    async def test_log_event_persists(self):
        svc = AuditService()
        await svc.log_event(event_type="test_insert", actor="pytest", payload={"k": 1})

        SessionLocal = get_session_factory()
        async with SessionLocal() as session:
            result = await session.execute(
                select(AuditEvent).where(AuditEvent.event_type == "test_insert")
            )
            assert result.scalar_one() is not None

    @pytest.mark.asyncio
    async def test_log_event_strips_pii_before_persist(self):
        svc = AuditService()
        await svc.log_event(
            event_type="pii_test",
            actor="pytest",
            payload={"patient_name": "Mustermann", "value": 99},
        )

        SessionLocal = get_session_factory()
        async with SessionLocal() as session:
            result = await session.execute(
                select(AuditEvent).where(AuditEvent.event_type == "pii_test")
            )
            event = result.scalar_one()
            assert "Mustermann" not in event.payload_json
            assert "<REDACTED>" in event.payload_json
            assert "99" in event.payload_json


class TestAppendOnly:
    @pytest.mark.asyncio
    async def test_audit_event_update_raises(self):
        SessionLocal = get_session_factory()
        async with SessionLocal() as session:
            audit = AuditEvent(
                event_type="test_update", actor="pytest", payload_json="{}"
            )
            session.add(audit)
            await session.commit()

            with pytest.raises(IntegrityError):
                audit.event_type = "modified"
                await session.commit()

    @pytest.mark.asyncio
    async def test_audit_event_delete_raises(self):
        SessionLocal = get_session_factory()
        async with SessionLocal() as session:
            audit = AuditEvent(
                event_type="test_delete", actor="pytest", payload_json="{}"
            )
            session.add(audit)
            await session.commit()

            with pytest.raises(IntegrityError):
                await session.delete(audit)
                await session.commit()


class TestGetTrail:
    @pytest.mark.asyncio
    async def test_get_trail_paginates(self):
        svc = AuditService()
        for i in range(5):
            await svc.log_event(
                event_type="paginate_test", actor="pytest", payload={"idx": i}
            )

        page = await svc.get_trail(limit=3, offset=0)
        assert page.limit == 3
        assert len(page.items) == 3
        assert page.total >= 5

    @pytest.mark.asyncio
    async def test_get_trail_no_pii_in_summary(self):
        svc = AuditService()
        await svc.log_event(
            event_type="summary_test",
            actor="pytest",
            payload={"patient_name": "Secret", "visible": "yes"},
        )

        page = await svc.get_trail(event_type="summary_test")
        assert len(page.items) == 1
        assert "Secret" not in page.items[0].payload_summary
        assert "yes" in page.items[0].payload_summary


class TestDecisionStats:
    @pytest.mark.asyncio
    async def test_decision_stats_empty(self):
        svc = AuditService()
        stats = await svc.decision_stats()
        assert stats["total_decisions"] == 0
        assert stats["full_agreement_rate"] == 0.0
