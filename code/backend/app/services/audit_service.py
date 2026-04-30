"""Audit service — append-only audit trail and read-only aggregation.

Never stores PII. Only hashes, timestamps, model versions, and numeric results.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from sqlalchemy import func, select

from app.core.logging import get_logger
from app.db.database import get_session_factory
from app.db.models import AuditEvent, DecisionTree
from app.schemas.audit import AuditEventEntry, AuditPage, DisagreementSummary

logger = get_logger(__name__)

# Known PII keys to strip from any JSON payload before persisting
_PII_KEYS = {
    "patient_name",
    "patient_id",
    "patient_birth_date",
    "study_date",
    "accession_number",
    "referring_physician_name",
    "performing_physician_name",
    "operator_name",
    "institution_name",
    "institution_address",
}


def _strip_pii_from_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a deep copy with known PII keys redacted."""
    if not isinstance(payload, dict):
        return payload
    result: dict[str, Any] = {}
    for key, value in payload.items():
        lower_key = key.lower()
        if lower_key in _PII_KEYS:
            result[key] = "<REDACTED>"
        elif isinstance(value, dict):
            result[key] = _strip_pii_from_payload(value)
        elif isinstance(value, list):
            result[key] = [
                _strip_pii_from_payload(v) if isinstance(v, dict) else v for v in value
            ]
        else:
            result[key] = value
    return result


class AuditService:
    def __init__(self) -> None:
        self._factory = get_session_factory()

    async def log_event(
        self,
        *,
        event_type: str,
        actor: str,
        payload: dict[str, Any],
    ) -> None:
        """Write an append-only audit event with PII stripped."""
        safe_payload = _strip_pii_from_payload(payload)
        async with self._factory() as session:
            entry = AuditEvent(
                event_type=event_type,
                actor=actor,
                payload_json=json.dumps(safe_payload, default=str),
            )
            session.add(entry)
            await session.commit()

    async def get_trail(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
        since: datetime | None = None,
        event_type: str | None = None,
    ) -> AuditPage:
        """Return paginated audit events."""
        async with self._factory() as session:
            base_q = select(AuditEvent).order_by(AuditEvent.timestamp.desc())
            if since is not None:
                base_q = base_q.where(AuditEvent.timestamp >= since)
            if event_type is not None:
                base_q = base_q.where(AuditEvent.event_type == event_type)

            total = await session.scalar(
                select(func.count()).select_from(base_q.subquery())
            )
            rows = (
                (await session.execute(base_q.offset(offset).limit(limit)))
                .scalars()
                .all()
            )

        items = [
            AuditEventEntry(
                id=r.id,
                timestamp=r.timestamp,
                event_type=r.event_type,
                actor=r.actor,
                payload_summary=r.payload_json[:200],
            )
            for r in rows
        ]
        return AuditPage(total=total or 0, limit=limit, offset=offset, items=items)

    async def get_disagreements(
        self, *, since: datetime, limit: int = 100
    ) -> list[DisagreementSummary]:
        """Return cases where the physician disagreed within a time window."""
        async with self._factory() as session:
            q = (
                select(DecisionTree)
                .where(
                    DecisionTree.captured_at >= since,
                    DecisionTree.agreement_verdict.in_(
                        ["disagreement", "physician_override"]
                    ),
                )
                .order_by(DecisionTree.captured_at.desc())
                .limit(limit)
            )
            rows = (await session.execute(q)).scalars().all()

        result = []
        for row in rows:
            try:
                data = json.loads(row.data_json)
                delta = data.get("agreement_with_ai", {}).get("delta_pct", 0.0)
                physician_pct = data.get("physician_decision", {}).get(
                    "stenosis_pct_nascet", 0.0
                )
                trust = data.get("agreement_with_ai", {}).get(
                    "trust_score_for_this_case"
                )
            except (json.JSONDecodeError, AttributeError):
                delta = 0.0
                physician_pct = 0.0
                trust = None

            result.append(
                DisagreementSummary(
                    case_id=row.case_id[:16],
                    captured_at=row.captured_at,
                    ai_stenosis_pct=round(physician_pct - delta, 1),
                    physician_stenosis_pct=round(physician_pct, 1),
                    delta_pct=delta,
                    agreement_verdict=row.agreement_verdict.value,
                    trust_score=trust,
                )
            )
        return result

    async def decision_stats(self) -> dict[str, Any]:
        """Aggregate stats for the daily learning loop dashboard."""
        async with self._factory() as session:
            total = await session.scalar(select(func.count()).select_from(DecisionTree))
            agreements = await session.scalar(
                select(func.count())
                .select_from(DecisionTree)
                .where(DecisionTree.agreement_verdict == "full_agreement")
            )
            rows = (await session.execute(select(DecisionTree))).scalars().all()

        trust_scores: list[int] = []
        deltas: list[float] = []
        for row in rows:
            try:
                data = json.loads(row.data_json)
                trust = data.get("agreement_with_ai", {}).get(
                    "trust_score_for_this_case"
                )
                delta = data.get("agreement_with_ai", {}).get("delta_pct")
                if trust is not None:
                    trust_scores.append(trust)
                if delta is not None:
                    deltas.append(delta)
            except (json.JSONDecodeError, AttributeError):
                continue

        total = total or 0
        return {
            "total_decisions": total,
            "full_agreement_rate": round(agreements / total, 3) if total else 0.0,
            "avg_trust_score": (
                round(sum(trust_scores) / len(trust_scores), 2)
                if trust_scores
                else None
            ),
            "avg_delta_pct": round(sum(deltas) / len(deltas), 2) if deltas else None,
        }
