"""initial

Revision ID: 0001
Revises:
Create Date: 2026-04-29

Dies wurde via `alembic revision --autogenerate -m "initial"` erstellt.
Hier nur als Vorlage / Stub.
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "inferences",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("case_id", sa.String(64), nullable=False, index=True),
        sa.Column(
            "captured_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column("ai_prediction_json", sa.Text, nullable=False),
        sa.Column("model_version", sa.String(32), nullable=False),
        sa.Column("model_sha", sa.String(64), nullable=False),
        sa.Column("audit_id", sa.String(36), nullable=False),
    )

    op.create_table(
        "decision_trees",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "case_id",
            sa.String(64),
            nullable=False,
            unique=True,
            index=True,
        ),
        sa.Column(
            "captured_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "physician_role_hash", sa.String(64), nullable=False
        ),
        sa.Column("data_json", sa.Text, nullable=False),
        sa.Column(
            "agreement_verdict",
            sa.Enum(
                "full_agreement",
                "partial_agreement",
                "disagreement",
                name="agreementverdict",
            ),
            nullable=False,
        ),
    )

    op.create_table(
        "audit_events",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column("event_type", sa.String(64), nullable=False),
        sa.Column("actor", sa.String(128), nullable=False),
        sa.Column("payload_json", sa.Text, nullable=False),
    )


def downgrade():
    op.drop_table("audit_events")
    op.drop_table("decision_trees")
    op.drop_table("inferences")
