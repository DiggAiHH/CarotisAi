from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from enum import Enum as PyEnum
from pathlib import Path

from jsonschema import ValidationError as JsonSchemaValidationError
from jsonschema import validate
from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


# Lazy-load decision tree schema to avoid import-time settings resolution
_DECISION_TREE_SCHEMA: dict | None = None


def _get_decision_tree_schema() -> dict:
    global _DECISION_TREE_SCHEMA
    if _DECISION_TREE_SCHEMA is None:
        _schema_root = Path(get_settings().project_root)
        _schema_path = _schema_root / "schemas" / "decision_tree.schema.json"
        _DECISION_TREE_SCHEMA = json.loads(_schema_path.read_text(encoding="utf-8"))
    return _DECISION_TREE_SCHEMA


class AgreementVerdict(PyEnum):
    FULL_AGREEMENT = "full_agreement"
    PARTIAL_AGREEMENT = "partial_agreement"
    DISAGREEMENT = "disagreement"


class Inference(Base):
    __tablename__ = "inferences"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    case_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    ai_prediction_json: Mapped[str] = mapped_column(Text, nullable=False)
    model_version: Mapped[str] = mapped_column(String(32), nullable=False)
    model_sha: Mapped[str] = mapped_column(String(64), nullable=False)
    audit_id: Mapped[str] = mapped_column(String(36), nullable=False)


class DecisionTree(Base):
    __tablename__ = "decision_trees"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    case_id: Mapped[str] = mapped_column(
        String(64), unique=True, index=True, nullable=False
    )
    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    physician_role_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    data_json: Mapped[str] = mapped_column(Text, nullable=False)
    agreement_verdict: Mapped[AgreementVerdict] = mapped_column(
        SQLEnum(AgreementVerdict, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
    )

    @validates("data_json")
    def validate_data_json(self, key: str, value: str) -> str:
        try:
            data = json.loads(value)
            validate(instance=data, schema=_get_decision_tree_schema())
        except (json.JSONDecodeError, JsonSchemaValidationError) as exc:
            raise ValueError(
                f"data_json must conform to decision_tree.schema.json: {exc}"
            ) from exc
        return value


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    actor: Mapped[str] = mapped_column(String(128), nullable=False)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)


class DemoToken(Base):
    __tablename__ = "demo_tokens"

    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    label: Mapped[str] = mapped_column(String(128), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    requests_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_requests: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    rohde_tag: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    physician_role_hash: Mapped[str] = mapped_column(
        String(64), default="demo-physician", nullable=False
    )
