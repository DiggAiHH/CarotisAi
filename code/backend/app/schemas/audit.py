"""Pydantic schemas for audit trail endpoints."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class AuditEventEntry(BaseModel):
    id: str
    timestamp: datetime
    event_type: str
    actor: str
    payload_summary: str = Field(description="First 200 chars of redacted payload")


class AuditPage(BaseModel):
    total: int = Field(description="Total matching rows (for pagination)")
    limit: int
    offset: int
    items: list[AuditEventEntry]


class DisagreementSummary(BaseModel):
    case_id: str = Field(description="First 16 chars only — sufficient for logging")
    captured_at: datetime
    ai_stenosis_pct: float
    physician_stenosis_pct: float
    delta_pct: float
    agreement_verdict: str
    trust_score: int | None = None
