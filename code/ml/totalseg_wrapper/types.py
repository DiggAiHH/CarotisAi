"""Typed dataclasses für TotalSegmentator-Wrapper-I/O.

PII-frei per Konstruktion: enthält keine Patient-Identifier.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class SegmentationLabels(str, Enum):
    """TotalSegmentator ``headneck_bones_vessels``-Task-Labels.

    Nur die für Carotis-AI relevanten Labels — vollständige Liste siehe
    https://github.com/wasserth/TotalSegmentator#class-details
    """

    ICA_LEFT = "internal_carotid_artery_left"
    ICA_RIGHT = "internal_carotid_artery_right"
    COMMON_CAROTID_LEFT = "common_carotid_artery_left"
    COMMON_CAROTID_RIGHT = "common_carotid_artery_right"
    VERTEBRAL_ARTERY_LEFT = "vertebral_artery_left"
    VERTEBRAL_ARTERY_RIGHT = "vertebral_artery_right"
    BACKGROUND = "background"


@dataclass(frozen=True, slots=True)
class WrapperConfig:
    """Konfiguration des Wrappers.

    Defaults sind Forschungsprototyp-konform.
    """

    task: str = "headneck_bones_vessels"
    resolution_mm: float = 1.5
    """Voxel-Resampling-Auflösung. 1.5 mm ist TotalSegmentator-Default."""

    device: str = "auto"
    """``"auto"``, ``"cuda"``, ``"cuda:0"``, ``"cpu"``."""

    output_format: str = "nifti"
    """``"nifti"`` oder ``"numpy"``."""

    labels_of_interest: tuple[SegmentationLabels, ...] = (
        SegmentationLabels.ICA_LEFT,
        SegmentationLabels.ICA_RIGHT,
    )
    """Auf welche Labels die Ausgabe gefiltert wird."""

    strict_strip_pii: bool = True
    """Wenn True, werden PII-DICOM-Tags vor Inferenz aus dem Header entfernt."""

    cache_dir: Path | None = None
    """Cache-Verzeichnis für TotalSegmentator-Weights. None = TS-Default."""


@dataclass(frozen=True, slots=True)
class VolumeMetadata:
    """Forschungs-Metadaten zum Input-Volume. KEIN PII."""

    volume_shape: tuple[int, int, int]
    voxel_spacing_mm: tuple[float, float, float]
    """Original-Spacing aus dem Header."""
    modality: str
    """z.B. ``"CT"``."""
    study_uid_hash: str | None = None
    """SHA256 der StudyInstanceUID (Re-Identifikation für interne Audit-Zwecke ok)."""
    series_uid_hash: str | None = None


@dataclass(frozen=True, slots=True)
class LabelMaskSummary:
    """Quantitative Summary einer einzelnen Label-Maske (forschungs-neutral)."""

    label: SegmentationLabels
    voxel_count: int
    volume_mm3: float
    bounding_box_min: tuple[int, int, int]
    bounding_box_max: tuple[int, int, int]


@dataclass(frozen=True, slots=True)
class SegmentationResult:
    """Output einer Inferenz-Runde. PII-frei."""

    case_id: str
    """Forscher-vergebene Fall-ID. NIEMALS DICOM PatientID o.ä."""

    captured_at: datetime
    inference_seconds: float
    model_version: str
    model_sha256: str
    config_used: WrapperConfig
    metadata: VolumeMetadata
    label_summaries: tuple[LabelMaskSummary, ...]

    mask_path: Path | None = None
    """Pfad zur gespeicherten NIfTI-Maske (lokal, nicht in Cloud)."""

    mask_numpy_shape: tuple[int, int, int] | None = None
    warnings: tuple[str, ...] = field(default_factory=tuple)

    def to_audit_payload(self) -> dict[str, Any]:
        """Audit-Log-Eintrag, garantiert PII-frei.

        Wird vom Backend ``audit_service.log_event`` konsumiert.
        """
        return {
            "case_id": self.case_id,
            "captured_at": self.captured_at.isoformat(),
            "inference_seconds": round(self.inference_seconds, 3),
            "model_version": self.model_version,
            "model_sha256": self.model_sha256,
            "task": self.config_used.task,
            "resolution_mm": self.config_used.resolution_mm,
            "volume_shape": list(self.metadata.volume_shape),
            "voxel_spacing_mm": [round(s, 4) for s in self.metadata.voxel_spacing_mm],
            "label_summaries": [
                {
                    "label": ls.label.value,
                    "voxel_count": ls.voxel_count,
                    "volume_mm3": round(ls.volume_mm3, 2),
                }
                for ls in self.label_summaries
            ],
            "warnings": list(self.warnings),
        }
