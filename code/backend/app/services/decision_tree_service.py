from __future__ import annotations

import asyncio
import json
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

import structlog
from jsonschema import ValidationError as JsonSchemaValidationError
from jsonschema import validate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.models import AuditEvent, DecisionTree
from app.services.pii_detection_service import PIIDetectionService

logger = structlog.get_logger()

# Load decision tree schema once
_SCHEMA_PATH = (
    Path(__file__).resolve().parents[4] / "schemas" / "decision_tree.schema.json"
)
_DECISION_TREE_SCHEMA = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))

# Local memory dump directory
_MEMORY_DIR = Path(__file__).resolve().parents[4] / "memory" / "decisions"


def _pii_check_text(
    pii_service: PIIDetectionService | None,
    text: str | None,
    field_name: str,
) -> list[dict[str, Any]] | None:
    """Return spans if PII detected, else None."""
    if pii_service is None or not text:
        return None
    spans = pii_service.detect(text)
    if spans:
        return [{"start": s.start, "end": s.end, "label": s.label} for s in spans]
    return None


class DecisionTreeService:
    def __init__(
        self,
        db_session_factory: async_sessionmaker,
        pii_service: PIIDetectionService | None = None,
    ):
        self.logger = logger.bind(service="decision_tree")
        self.db_session_factory = db_session_factory
        self.pii_service = pii_service

    async def capture(
        self,
        case_id: str,
        physician_role_hash: str,
        payload: dict[str, Any],
    ) -> str:
        log = self.logger.bind(case_id=case_id)
        log.info("capture_started")

        # 1. JSON Schema validation
        try:
            validate(instance=payload, schema=_DECISION_TREE_SCHEMA)
        except JsonSchemaValidationError as exc:
            log.error("schema_validation_failed", error=str(exc))
            raise ValueError(f"Decision tree payload invalid: {exc}") from exc

        # 2. PII-Check on free_text_notes (B-14: backend autoritativ)
        if self.pii_service is not None:
            free_text = (payload.get("reasoning", {}) or {}).get("free_text_notes")
            pii_spans = _pii_check_text(self.pii_service, free_text, "free_text_notes")
            if pii_spans:
                await self._write_pii_reject_audit(
                    case_id, physician_role_hash, "free_text_notes", pii_spans
                )
                log.warning(
                    "pii_detected_in_free_text",
                    span_count=len(pii_spans),
                    labels=sorted(set(s["label"] for s in pii_spans)),
                )
                raise ValueError(
                    f"PII detected in free_text_notes: {len(pii_spans)} "
                    f"span(s) of types {sorted(set(s['label'] for s in pii_spans))}. "
                    f"Bitte umformulieren."
                )

            # 2b. PII-Check on override_free_text (B-14)
            override_text = (payload.get("disagreement") or {}).get(
                "override_free_text"
            )
            override_pii_spans = _pii_check_text(
                self.pii_service, override_text, "override_free_text"
            )
            if override_pii_spans:
                await self._write_pii_reject_audit(
                    case_id,
                    physician_role_hash,
                    "override_free_text",
                    override_pii_spans,
                )
                log.warning(
                    "pii_detected_in_override_text",
                    span_count=len(override_pii_spans),
                    labels=sorted(set(s["label"] for s in override_pii_spans)),
                )
                raise ValueError(
                    f"PII detected in override_free_text: {len(override_pii_spans)} "
                    f"span(s) of types {sorted(set(s['label'] for s in override_pii_spans))}. "
                    f"Bitte umformulieren."
                )

        # 3. Persist to DB
        async with self.db_session_factory() as session:
            dt = DecisionTree(
                case_id=case_id,
                physician_role_hash=physician_role_hash,
                data_json=json.dumps(payload),
                agreement_verdict=payload["agreement_with_ai"]["verdict"],
            )
            session.add(dt)
            await session.commit()

        # 4. Write to local memory directory
        _MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        date_prefix = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        mem_path = _MEMORY_DIR / f"{date_prefix}_{case_id[:8]}.json"
        await asyncio.to_thread(
            mem_path.write_text,
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        # 5. Audit event (override-specific if applicable)
        audit_id = str(uuid.uuid4())
        disagreement = payload.get("disagreement")
        if disagreement:
            event_type = "decision_tree_override"
            audit_payload = {
                "case_id": case_id,
                "audit_id": audit_id,
                "override_reason": disagreement.get("override_reason"),
                "ai_verdict": disagreement.get("ai_verdict"),
                "physician_verdict": disagreement.get("physician_verdict"),
            }
        else:
            event_type = "decision_tree_captured"
            audit_payload = {"case_id": case_id, "audit_id": audit_id}

        async with self.db_session_factory() as session:
            audit = AuditEvent(
                event_type=event_type,
                actor=physician_role_hash,
                payload_json=json.dumps(audit_payload),
            )
            session.add(audit)
            await session.commit()

        log.info("capture_completed", audit_id=audit_id, event_type=event_type)
        return audit_id

    async def _write_pii_reject_audit(
        self,
        case_id: str,
        physician_role_hash: str,
        field: str,
        spans: list[dict[str, Any]],
    ) -> None:
        """Write audit event for PII rejection WITHOUT content (B-15)."""
        async with self.db_session_factory() as session:
            audit = AuditEvent(
                event_type="decision_tree_pii_reject",
                actor=physician_role_hash,
                payload_json=json.dumps(
                    {
                        "case_id_short": case_id[:16],
                        "field": field,
                        "pii_span_count": len(spans),
                        "pii_labels": sorted(set(s["label"] for s in spans)),
                    }
                ),
            )
            session.add(audit)
            await session.commit()

    async def list_for_review(self, since: datetime) -> list[DecisionTree]:
        async with self.db_session_factory() as session:
            result = await session.execute(
                select(DecisionTree).where(DecisionTree.captured_at >= since)
            )
            return list(result.scalars().all())

    async def detect_disagreements(self, window_days: int = 7) -> list[DecisionTree]:
        since = datetime.now(timezone.utc) - timedelta(days=window_days)
        async with self.db_session_factory() as session:
            result = await session.execute(
                select(DecisionTree).where(
                    DecisionTree.captured_at >= since,
                    DecisionTree.agreement_verdict == "disagreement",
                )
            )
            return list(result.scalars().all())
