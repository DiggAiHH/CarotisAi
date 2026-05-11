"""Splash confirmation audit endpoint for the research prototype.

Source: memory/domain/zweckbestimmung_master_2026-05-06.md section E
Audit anchor: memory/runs/2026-05-10_disclaimer_audit.md findings G1 and G4

Behavior:
- POST /api/v1/audit/splash-confirmation
- Payload: {session_id, role_hash, confirmed_at, version}
- Stores an AuditEvent of type ``splash_confirmation``
- No PII in payload; schema rejects unknown fields
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator

from app.api.dependencies import verify_api_key
from app.core.feature_flags import get_feature_flags
from app.core.logging import get_logger
from app.services.audit_service import AuditService

logger = get_logger(__name__)

router = APIRouter(
    prefix="/audit",
    tags=["audit"],
    dependencies=[Depends(verify_api_key)],
)

_KNOWN_VERSIONS: set[str] = {
    "zweckbestimmung_2026-05-06",
}


class SplashConfirmationRequest(BaseModel):
    """Payload emitted by the frontend ResearchSplashGate.

    Must never contain PII. Schema validation rejects unknown fields.
    """

    session_id: str = Field(min_length=8, max_length=128)
    role_hash: str = Field(min_length=8, max_length=128)
    confirmed_at: datetime
    version: str = Field(min_length=8, max_length=64)

    model_config = {"extra": "forbid"}

    @field_validator("version")
    @classmethod
    def known_version(cls, v: str) -> str:
        if v not in _KNOWN_VERSIONS:
            raise ValueError(
                f"Unknown purpose-limitation version: {v}. "
                f"Allowed: {sorted(_KNOWN_VERSIONS)}",
            )
        return v


class SplashConfirmationResponse(BaseModel):
    audit_id: str
    server_mode: str = Field(
        description="'research_prototype' if all CDS flags are false, otherwise 'mixed'",
    )


def _get_audit_service() -> AuditService:
    return AuditService()


@router.post(
    "/splash-confirmation",
    response_model=SplashConfirmationResponse,
    status_code=status.HTTP_200_OK,
)
async def post_splash_confirmation(
    payload: SplashConfirmationRequest,
    audit: Annotated[AuditService, Depends(_get_audit_service)],
) -> SplashConfirmationResponse:
    """Write the splash-gate research confirmation to the audit trail.

    The server mode is included so later reviews can prove which feature-flag
    state was active when the user confirmed the purpose limitation.
    """
    feature_flags = get_feature_flags()
    server_mode = (
        "research_prototype" if feature_flags.is_research_prototype_mode() else "mixed"
    )

    event_payload = {
        "version": payload.version,
        "session_id": payload.session_id,
        "role_hash": payload.role_hash,
        "confirmed_at": payload.confirmed_at.isoformat(),
        "server_mode": server_mode,
        "server_flags_version": feature_flags.zweckbestimmung_version,
    }

    try:
        audit_id = await audit.log_event(
            event_type="splash_confirmation",
            actor="research_splash_gate",
            payload=event_payload,
        )
    except Exception as exc:
        logger.exception("splash_confirmation_audit_failed", error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Audit log error; confirmation was not persisted.",
        ) from exc

    logger.info(
        "splash_confirmation_logged",
        audit_id=audit_id,
        version=payload.version,
        server_mode=server_mode,
    )

    return SplashConfirmationResponse(
        audit_id=str(audit_id),
        server_mode=server_mode,
    )
