"""Feature flags for the research-prototype purpose limitation.

The active purpose limitation requires the public UI to avoid quantitative
stenosis values and plaque vulnerability scores by default. The backend may
still keep those values internally for research audit records.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class FeatureFlags(BaseSettings):
    """Feature flags loaded from ``FEATURE_*`` environment variables.

    The values are cached for the process lifetime so a session cannot silently
    switch between feature-flag states without a restart.
    """

    model_config = SettingsConfigDict(
        env_prefix="FEATURE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    cds_module_enabled: bool = Field(
        default=False,
        description=(
            "Enable the clinical decision support module. When false, the API "
            "does not expose quantitative stenosis values or plaque "
            "vulnerability scores to the public UI."
        ),
    )
    stenosis_quantification_exposed: bool = Field(
        default=False,
        description="Expose stenosis_pct_nascet in public inference responses.",
    )
    vulnerability_markers_in_ui: bool = Field(
        default=False,
        description="Expose vulnerability_markers in public inference responses.",
    )
    heatmap_overlay_enabled: bool = Field(
        default=True,
        description="Expose the research attention heatmap overlay.",
    )
    workflow_capture_enabled: bool = Field(
        default=True,
        description="Enable workflow and decision-tree capture.",
    )
    zweckbestimmung_version: str = Field(
        default="zweckbestimmung_2026-05-06",
        description="Version string of the active purpose limitation.",
    )

    def public_inference_keys(self) -> set[str]:
        """Return the public inference response fields allowed for the UI."""
        keys: set[str] = {
            "case_id",
            "audit_id",
            "captured_at",
            "model_version",
            "model_sha",
            "confidence_bucket",
            "trust_score",
            "calibrated",
        }
        if self.heatmap_overlay_enabled:
            keys.add("heatmap_b64")
        if self.workflow_capture_enabled:
            keys.add("workflow_summary")
        if self.cds_module_enabled or self.stenosis_quantification_exposed:
            keys.add("stenosis_pct_nascet")
        if self.cds_module_enabled or self.vulnerability_markers_in_ui:
            keys.add("vulnerability_markers")
        return keys

    def is_research_prototype_mode(self) -> bool:
        """Return true when all CDS exposure flags are disabled."""
        return (
            not self.cds_module_enabled
            and not self.stenosis_quantification_exposed
            and not self.vulnerability_markers_in_ui
        )


@lru_cache(maxsize=1)
def get_feature_flags() -> FeatureFlags:
    """Load feature flags once per process."""
    return FeatureFlags()
