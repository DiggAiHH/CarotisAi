from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.inference import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=HealthResponse, summary="Basic health check")
async def health_check():
    """Always returns 200 if the process is alive."""
    return HealthResponse(
        status="ok",
        model_loaded=None,
        db_ok=None,
        ollama_reachable=None,
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/ready", response_model=HealthResponse, summary="Readiness probe")
async def health_ready(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Returns 200 only if DB and model are ready."""
    try:
        await db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    inference_service = getattr(request.app.state, "inference_service", None)
    model_loaded = inference_service.model_loaded if inference_service else False

    status = "ok" if (db_ok and model_loaded) else "degraded"

    return HealthResponse(
        status=status,
        model_loaded=model_loaded,
        db_ok=db_ok,
        ollama_reachable=None,
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/live", response_model=HealthResponse, summary="Liveness probe")
async def health_live():
    """Always returns 200 if the process is running."""
    return HealthResponse(
        status="ok",
        model_loaded=None,
        db_ok=None,
        ollama_reachable=None,
        timestamp=datetime.now(timezone.utc),
    )
