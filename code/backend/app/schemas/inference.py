from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class VulnerabilityMarkers(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intraplaque_hemorrhage: float = Field(ge=0, le=1)
    thin_fibrous_cap: float = Field(ge=0, le=1)
    lipid_rich_necrotic_core: float = Field(ge=0, le=1)
    systolic_motion_anomaly: float = Field(ge=0, le=1)


class AiPrediction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stenosis_pct_nascet: float = Field(default=..., ge=0, le=100)
    confidence: float = Field(ge=0, le=1)
    vulnerability_markers: VulnerabilityMarkers
    model_version: str = Field(pattern=r"^v\d+\.\d+\.\d+$")
    model_sha: str = Field(pattern=r"^[a-f0-9]{7,64}$")


class PhysicianDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stenosis_pct_nascet: float = Field(default=..., ge=0, le=100)
    confidence_self_reported: Literal["low", "medium", "high", "very_high"] | None = (
        None
    )
    confirmed_markers: list[str] = []
    rejected_markers: list[str] = []
    added_markers: list[str] = []


class Reasoning(BaseModel):
    model_config = ConfigDict(extra="forbid")

    deciding_feature: str | None = None
    ruled_out: list[str] = []
    ruled_out_reason: str | None = None
    would_consult: str | None = None
    would_re_image_if: str | None = None
    free_text_notes: str | None = Field(
        default=None,
        max_length=2000,
        description="Optional free-text note. PII-filtered before storage.",
    )


class Disagreement(BaseModel):
    """Structured physician-AI disagreement capture (CDSiC taxonomy)."""

    model_config = ConfigDict(extra="forbid")

    ai_verdict: Literal["normal", "mild", "moderate", "severe", "critical"]
    physician_verdict: Literal["normal", "mild", "moderate", "severe", "critical"]
    override_reason: Literal[
        "patient_specific",
        "clinical_judgment",
        "insufficient_evidence",
        "alert_fatigue",
        "other",
    ]
    override_free_text: str | None = Field(
        default=None,
        max_length=500,
        description="Optional override justification. PII-filtered before storage.",
    )

    @model_validator(mode="after")
    def _verdicts_must_differ(self) -> "Disagreement":
        if self.ai_verdict == self.physician_verdict:
            raise ValueError(
                "ai_verdict and physician_verdict must differ for a disagreement record"
            )
        return self


class AgreementWithAi(BaseModel):
    model_config = ConfigDict(extra="forbid")

    verdict: Literal[
        "full_agreement", "partial_agreement", "disagreement", "physician_override"
    ]
    delta_pct: float
    delta_markers: list[str] = []
    trust_score_for_this_case: int = Field(ge=1, le=5)


class Anonymisation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    method: Literal["DICOM_PS_3.15_basic", "DICOM_PS_3.15_research", "custom_v1"]
    salt_version: str = Field(pattern=r"^v\d{4}-\d{2}$")
    audit_id: str
    k_anonymity_min: int = Field(ge=5)


class DecisionTreeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str = Field(pattern=r"^[a-f0-9]{64}$")
    captured_at: datetime
    physician_role_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    ai_prediction: AiPrediction
    physician_decision: PhysicianDecision
    reasoning: Reasoning | None = None
    agreement_with_ai: AgreementWithAi
    anonymisation: Anonymisation
    disagreement: Disagreement | None = None


class InternalInferenceRecord(BaseModel):
    """Backend-internal inference record for audit and research analysis.

    RESEARCH USE — never returned to UI when feature_flags.cds_module_enabled
    is False.
    """

    case_id: str
    stenosis_pct_nascet: float = Field(ge=0, le=100)
    confidence: float
    confidence_bucket: str = "medium"  # low, medium, high
    trust_score: float | None = None
    calibrated: bool = False
    vulnerability_markers: dict[str, float]
    heatmap_b64: str | None = None
    model_version: str
    model_sha: str
    audit_id: str
    captured_at: datetime


class InferenceResponse(BaseModel):
    """Public inference response returned to the UI in research mode."""

    case_id: str
    audit_id: str
    captured_at: datetime
    model_version: str
    model_sha: str
    heatmap_b64: str | None = None
    confidence_bucket: str = "medium"
    trust_score: float | None = None
    calibrated: bool = False


# Backward-compatible name used by existing service tests and mocks.
PredictionResponse = InternalInferenceRecord


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool | None = None
    db_ok: bool | None = None
    ollama_reachable: bool | None = None
    research_prototype_mode: bool | None = None
    zweckbestimmung_version: str | None = None
    cds_module_enabled: bool | None = None
    timestamp: datetime
