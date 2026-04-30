from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import verify_api_key
from app.db.database import get_db, get_session_factory
from app.db.models import DecisionTree
from app.schemas.inference import DecisionTreeRequest
from app.services.decision_tree_service import DecisionTreeService
from app.services.pii_detection_service import PIIDetectionService, get_pii_service

router = APIRouter(
    prefix="/decision-tree",
    tags=["decision-tree"],
    dependencies=[Depends(verify_api_key)],
)


@router.post("/capture")
async def capture(
    request: DecisionTreeRequest,
    pii_service: PIIDetectionService = Depends(get_pii_service),
):
    service = DecisionTreeService(
        db_session_factory=get_session_factory(), pii_service=pii_service
    )
    audit_id = await service.capture(
        case_id=request.case_id,
        physician_role_hash=request.physician_role_hash,
        payload=request.model_dump(mode="json"),
    )
    return {"audit_id": audit_id, "status": "ok"}


@router.post("/check-text")
async def check_text(
    payload: dict,
    pii_service: PIIDetectionService = Depends(get_pii_service),
):
    text = payload.get("text", "")
    if not isinstance(text, str):
        raise HTTPException(status_code=422, detail="text must be string")
    if len(text) > 2000:
        raise HTTPException(status_code=422, detail="text exceeds 2000 chars")
    spans = pii_service.detect(text)
    return {
        "is_clean": len(spans) == 0,
        "pii_spans": [
            {"start": s.start, "end": s.end, "label": s.label} for s in spans
        ],
    }


@router.get("/recent")
async def recent(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(DecisionTree)
        .order_by(DecisionTree.captured_at.desc())
        .offset(offset)
        .limit(limit)
    )
    items = result.scalars().all()
    return {
        "items": [
            {
                "id": item.id,
                "case_id": item.case_id,
                "captured_at": item.captured_at,
                "agreement_verdict": item.agreement_verdict.value,
            }
            for item in items
        ],
        "limit": limit,
        "offset": offset,
    }
