from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Query, Request
import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import verify_admin_key, verify_api_key
from app.db.database import get_db, get_session_factory
from app.db.models import AuditEvent
from app.services.decision_tree_service import DecisionTreeService
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(
    prefix="/audit",
    tags=["audit"],
    dependencies=[Depends(verify_api_key), Depends(verify_admin_key)],
)


@router.get("/trail")
@limiter.limit("30/minute")
async def trail(
    request: Request,
    event_type: str | None = None,
    since: datetime | None = None,
    until: datetime | None = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    query = select(AuditEvent).order_by(AuditEvent.timestamp.desc())
    if event_type:
        query = query.where(AuditEvent.event_type == event_type)
    if since:
        query = query.where(AuditEvent.timestamp >= since)
    if until:
        query = query.where(AuditEvent.timestamp <= until)

    result = await db.execute(query.offset(offset).limit(limit))
    items = result.scalars().all()
    return {
        "items": [
            {
                "id": item.id,
                "timestamp": item.timestamp,
                "event_type": item.event_type,
                "actor": item.actor,
            }
            for item in items
        ],
        "limit": limit,
        "offset": offset,
    }


@router.get("/events")
@limiter.limit("30/minute")
async def events(
    request: Request,
    type: str | None = None,  # noqa: A002 - public query parameter name
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    query = select(AuditEvent).order_by(AuditEvent.timestamp.desc())
    if type:
        query = query.where(AuditEvent.event_type == type)

    result = await db.execute(query.offset(offset).limit(limit))
    items = result.scalars().all()
    return {
        "items": [
            {
                "id": item.id,
                "timestamp": item.timestamp,
                "event_type": item.event_type,
                "actor": item.actor,
                "payload_redacted": json.loads(item.payload_json),
            }
            for item in items
        ],
        "limit": limit,
        "offset": offset,
    }


@router.get("/anomalies")
@limiter.limit("10/minute")
async def anomalies(request: Request):
    service = DecisionTreeService(db_session_factory=get_session_factory())
    disagreements = await service.detect_disagreements(window_days=7)
    return {
        "window_days": 7,
        "count": len(disagreements),
        "items": [
            {
                "case_id": d.case_id,
                "captured_at": d.captured_at,
                "agreement_verdict": d.agreement_verdict.value,
            }
            for d in disagreements
        ],
    }
