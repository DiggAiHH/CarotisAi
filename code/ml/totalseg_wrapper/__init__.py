"""TotalSegmentator-Wrapper — ICA-Segmentierung über öffentliche Pre-trained-Weights.

Quelle: Wasserthal et al., TotalSegmentator (MIT-Lizenz),
        https://github.com/wasserth/TotalSegmentator
Aufgabe: ``headneck_bones_vessels`` — segmentiert u.a.
         ``internal_carotid_artery_left`` und ``internal_carotid_artery_right``.

Forschungsprototyp-Konformität (zweckbestimmung_2026-05-06):
- Keine Stenose-Quantifizierung, kein Plaque-Score in Outputs.
- Reine Segmentations-Masken + Forschungs-Metadaten (Inference-Zeit,
  Modell-Version, SHA256 der Weights).
- PII-frei: Outputs enthalten nie Patient-IDs, Namen, Geburtsdaten.
"""

from .types import (
    SegmentationResult,
    SegmentationLabels,
    WrapperConfig,
)
from .wrapper import TotalSegmentatorWrapper

__all__ = [
    "SegmentationResult",
    "SegmentationLabels",
    "WrapperConfig",
    "TotalSegmentatorWrapper",
]
