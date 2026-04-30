"""Pydantic schemas for decision-tree capture.

Mirrors the JSON schema in 05_DECISION_TREE_HARVESTING.md §3.
Mandatory fields are the minimum the 5-second fast form requires.
All others are optional — the 30-sec form fills them.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator

AgreementVerdict = Literal[
    "full_agreement",
    "partial_agreement",
    "disagreement",
    "physician_override",
]

ConfidenceLevel = Literal["low", "medium", "high", "very_high"]

OverrideReason = Literal[
    "patient_specific",
    "clinical_judgment",
    "insufficient_evidence",
    "alert_fatigue",
    "other",
]

StenosisVerdict = Literal["normal", "mild", "moderate", "severe", "critical"]


class DisagreementCreate(BaseModel):
    """Structured capture of physician-AI disagreement (CDSiC taxonomy)."""

    ai_verdict: StenosisVerdict = Field(
        description="AI assessment that the physician is overriding"
    )
    physician_verdict: StenosisVerdict = Field(
        description="Physician's differing assessment"
    )
    override_reason: OverrideReason = Field(
        description="Standardised override reason per CDSiC taxonomy"
    )
    override_free_text: str | None = Field(
        default=None,
        max_length=500,
        description="Optional free-text override justification. PII-filtered before storage.",
    )

    @model_validator(mode="after")
    def _verdicts_must_differ(self) -> "DisagreementCreate":
        if self.ai_verdict == self.physician_verdict:
            raise ValueError(
                "ai_verdict and physician_verdict must differ for a disagreement record"
            )
        return self


class DecisionTreeCreate(BaseModel):
    # --- Mandatory (5-sec form) ---
    case_hash: str = Field(description="SHA-256 from inference response")
    physician_role_hash: str = Field(
        description="Anonymised physician identifier (sha256(role + project_salt))"
    )
    stenosis_pct_nascet: float = Field(ge=0.0, le=100.0)
    agreement_verdict: AgreementVerdict

    # --- Optional (30-sec form) ---
    confidence_self_reported: ConfidenceLevel | None = None
    delta_pct: float | None = Field(
        default=None,
        description="Physician estimate minus AI estimate (negative = AI was too high)",
    )
    confirmed_markers: list[str] = Field(default_factory=list)
    rejected_markers: list[str] = Field(default_factory=list)
    added_markers: list[str] = Field(default_factory=list)

    # --- Reasoning (most valuable — optional) ---
    deciding_feature: str | None = None
    ruled_out: list[str] = Field(default_factory=list)
    ruled_out_reason: str | None = None
    would_consult: str | None = None
    would_re_image_if: str | None = None
    free_text_notes: str | None = Field(
        default=None,
        max_length=2000,
        description="Optionale freie Notiz. Wird PII-gefiltert vor Speicherung.",
    )

    # --- Trust signal ---
    trust_score_for_this_case: int | None = Field(
        default=None, ge=1, le=5, description="1=AI completely wrong, 5=AI nailed it"
    )

    # --- Disagreement / Override (CDSiC taxonomy, optional) ---
    disagreement: DisagreementCreate | None = None


class DecisionTreeResponse(BaseModel):
    id: int
    case_hash: str
    captured_at: datetime
    agreement_verdict: AgreementVerdict
    delta_pct: float | None
