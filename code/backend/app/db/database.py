from __future__ import annotations

from collections.abc import AsyncIterator
from functools import lru_cache

from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings
from app.db.models import AuditEvent, Base


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    """Lazy engine creation. Tests can clear lru_cache + monkeypatch Settings."""
    settings = get_settings()
    return create_async_engine(
        settings.database_url,
        echo=settings.debug,
        future=True,
        pool_pre_ping=True,
    )


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(get_engine(), expire_on_commit=False)


async def init_db() -> None:
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncIterator[AsyncSession]:
    SessionLocal = get_session_factory()
    async with SessionLocal() as session:
        yield session


async def reset_db() -> None:
    """Test helper: drop_all + create_all."""
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


def _raise_append_only(mapper, connection, target):
    raise IntegrityError(
        statement="AuditEvent is append-only",
        params=None,
        orig=RuntimeError("append-only"),
    )


event.listen(AuditEvent, "before_update", _raise_append_only)
event.listen(AuditEvent, "before_delete", _raise_append_only)
