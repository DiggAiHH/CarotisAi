from __future__ import annotations

import hmac
from datetime import datetime, timezone
from hashlib import sha256

from fastapi import Depends, Header, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings

_API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=True)


_ADMIN_KEY_HEADER = APIKeyHeader(name="X-Admin-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(_API_KEY_HEADER)) -> str:
    """Validate X-API-Key header against configured secret.

    Returns the validated key so routes can log the caller identity
    without exposing the full key.
    """
    settings = get_settings()
    if not hmac.compare_digest(api_key, settings.api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key


def hash_demo_token(token: str) -> str:
    """Hash a raw demo token before comparing it with the DB whitelist."""
    return sha256(token.encode("utf-8")).hexdigest()


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _as_aware_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


async def verify_admin_key(
    admin_key: str | None = Security(_ADMIN_KEY_HEADER),
) -> str:
    """Validate X-Admin-Key header for protected endpoints like /metrics."""
    settings = get_settings()
    if admin_key is None or not hmac.compare_digest(admin_key, settings.admin_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing admin key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return admin_key


async def _get_db():
    from app.db.database import get_db

    async for session in get_db():
        yield session


async def verify_demo_token(
    x_demo_token: str = Header(..., alias="X-Demo-Token"),
    db: AsyncSession = Depends(_get_db),
) -> "DemoToken":  # noqa: F821
    """Validate a demo token against the SQLite whitelist and consume quota."""
    from app.db.models import DemoToken

    settings = get_settings()
    token_hash = hash_demo_token(x_demo_token)
    if settings.master_demo_token_hash and hmac.compare_digest(
        token_hash,
        settings.master_demo_token_hash,
    ):
        return DemoToken(
            token_hash=token_hash,
            label="master-admin-demo",
            expires_at=datetime.max.replace(tzinfo=timezone.utc),
            requests_used=0,
            max_requests=2_147_483_647,
            rohde_tag=False,
            physician_role_hash="master-admin-demo",
        )

    result = await db.execute(
        select(DemoToken).where(DemoToken.token_hash == token_hash)
    )
    token = result.scalar_one_or_none()
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing demo token",
        )
    if _as_aware_utc(token.expires_at) <= _utc_now():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Demo token expired",
        )
    if token.requests_used >= token.max_requests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Demo token quota exceeded",
        )

    token.requests_used += 1
    await db.commit()
    await db.refresh(token)
    return token
