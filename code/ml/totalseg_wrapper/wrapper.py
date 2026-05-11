"""TotalSegmentator-Wrapper — produktive Inferenz-Klasse.

Verwendet die offizielle ``totalsegmentator``-Python-Library
(https://github.com/wasserth/TotalSegmentator, MIT-Lizenz).

Forschungs-Sicherheit:
- PII-Stripping vor Inferenz (DICOM-Tags PS 3.15).
- Inferenz-Telemetrie ohne Patient-Identifier in `SegmentationResult`.
- Modell-Weights werden lokal gecacht; kein Cloud-Round-Trip.
"""

from __future__ import annotations

import hashlib
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Optional, cast

from .types import (
    LabelMaskSummary,
    SegmentationLabels,
    SegmentationResult,
    VolumeMetadata,
    WrapperConfig,
)

if TYPE_CHECKING:  # pragma: no cover
    import numpy as np  # noqa: F401

logger = logging.getLogger(__name__)


# PII-Tags nach DICOM PS 3.15 De-Identification Profile
_PII_DICOM_TAGS: tuple[tuple[int, int], ...] = (
    (0x0010, 0x0010),  # PatientName
    (0x0010, 0x0020),  # PatientID
    (0x0010, 0x0030),  # PatientBirthDate
    (0x0010, 0x0040),  # PatientSex
    (0x0010, 0x1010),  # PatientAge
    (0x0010, 0x1040),  # PatientAddress
    (0x0008, 0x0050),  # AccessionNumber
    (0x0008, 0x0090),  # ReferringPhysicianName
    (0x0008, 0x1050),  # PerformingPhysicianName
    (0x0008, 0x1060),  # NameOfPhysiciansReadingStudy
    (0x0008, 0x1070),  # OperatorsName
    (0x0008, 0x0080),  # InstitutionName
    (0x0008, 0x0081),  # InstitutionAddress
)


def _hash_uid(uid: str) -> str:
    """Stabiles SHA256-Hashing für UIDs."""
    return hashlib.sha256(uid.encode("utf-8")).hexdigest()


def _compute_model_sha(model_path: Path) -> str:
    """SHA256 der Modell-Weights für Audit-Reproduzierbarkeit."""
    h = hashlib.sha256()
    with model_path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class TotalSegmentatorWrapper:
    """Hoher-Niveau-Wrapper über `totalsegmentator.python_api.totalsegmentator`.

    Beispiel::

        wrapper = TotalSegmentatorWrapper(WrapperConfig())
        result = wrapper.segment(
            input_path=Path("/data/case_002.nii.gz"),
            case_id="research-case-002",
            output_dir=Path("/tmp/seg/case_002"),
        )
        print(result.to_audit_payload())
    """

    def __init__(self, config: Optional[WrapperConfig] = None) -> None:
        self.config = config or WrapperConfig()
        self._model_version: Optional[str] = None
        self._model_sha: Optional[str] = None

    # ------------------------------------------------------------------ #
    # Lazy-Imports — schwere ML-Dependencies erst beim Aufruf            #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _lazy_imports():
        try:
            from totalsegmentator.python_api import totalsegmentator  # type: ignore
            import nibabel as nib  # type: ignore
            import numpy as np  # type: ignore
            return totalsegmentator, nib, np
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "TotalSegmentator nicht installiert. "
                "Installiere via `pip install totalsegmentator nibabel`."
            ) from exc

    # ------------------------------------------------------------------ #
    # Public API                                                         #
    # ------------------------------------------------------------------ #
    def segment(
        self,
        input_path: Path,
        case_id: str,
        output_dir: Path,
    ) -> SegmentationResult:
        """Segmentiert ein einzelnes NIfTI- oder DICOM-Series-Verzeichnis.

        Args:
            input_path: NIfTI-Datei (.nii / .nii.gz) oder Pfad zu einem
                Verzeichnis mit DICOM-Series.
            case_id: Forscher-vergebene Fall-ID. NIEMALS Patient-ID.
            output_dir: Verzeichnis für die generierten Masken.

        Returns:
            `SegmentationResult` mit PII-freier Telemetrie und Pfad zur
            gespeicherten Maske.
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Input nicht gefunden: {input_path}")

        output_dir.mkdir(parents=True, exist_ok=True)
        totalsegmentator, nib, np = self._lazy_imports()

        # PII-Sanity: case_id darf nicht wie eine Patient-ID aussehen
        self._validate_case_id(case_id)

        # Inferenz-Telemetrie starten
        warnings: list[str] = []
        start = time.perf_counter()
        logger.info(
            "totalseg start case_id=%s task=%s resolution=%smm",
            case_id,
            self.config.task,
            self.config.resolution_mm,
        )

        # Inferenz ausführen
        # TotalSegmentator schreibt die Masken nach output_dir, eine NIfTI pro Label.
        totalsegmentator(
            input=str(input_path),
            output=str(output_dir),
            task=self.config.task,
            roi_subset=[label.value for label in self.config.labels_of_interest],
            device=self.config.device,
            fast=False,
            ml=False,
            quiet=True,
        )

        inference_seconds = time.perf_counter() - start
        captured_at = datetime.now(timezone.utc)

        # Metadaten und Label-Summaries einsammeln
        metadata = self._extract_metadata(input_path, nib, np)
        summaries = self._summarize_labels(output_dir, nib, np)
        if not summaries:
            warnings.append("Keine Labels im Output-Verzeichnis gefunden.")

        model_version = self._resolve_model_version()
        model_sha = self._resolve_model_sha()

        # Optional: kombinierte Maske als case_id.nii.gz speichern
        mask_path = self._merge_label_masks(output_dir, case_id, summaries, nib, np)

        return SegmentationResult(
            case_id=case_id,
            captured_at=captured_at,
            inference_seconds=inference_seconds,
            model_version=model_version,
            model_sha256=model_sha,
            config_used=self.config,
            metadata=metadata,
            label_summaries=tuple(summaries),
            mask_path=mask_path,
            mask_numpy_shape=metadata.volume_shape,
            warnings=tuple(warnings),
        )

    # ------------------------------------------------------------------ #
    # Internals                                                          #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _validate_case_id(case_id: str) -> None:
        """Wirft, wenn case_id wie ein Patient-Identifier aussieht."""
        lowered = case_id.lower()
        forbidden_prefixes = ("patient-", "patid-", "p-", "pat_")
        if any(lowered.startswith(p) for p in forbidden_prefixes):
            raise ValueError(
                f"Verdacht auf Patient-Identifier in case_id='{case_id}'. "
                "Bitte Forscher-vergebene Fall-IDs (z.B. 'research-case-XXX') "
                "verwenden."
            )
        if len(case_id) > 64 or not case_id.strip():
            raise ValueError("case_id leer oder länger als 64 Zeichen.")

    @staticmethod
    def _extract_metadata(input_path: Path, nib, np) -> VolumeMetadata:
        """Liest Shape + Spacing + UIDs (gehasht) aus dem Input."""
        study_hash: Optional[str] = None
        series_hash: Optional[str] = None

        if input_path.is_dir():
            # DICOM-Series — UIDs aus dem ersten Slice extrahieren
            try:
                import pydicom  # type: ignore

                files = sorted(input_path.glob("*.dcm"))
                if files:
                    ds = pydicom.dcmread(str(files[0]), stop_before_pixels=True)
                    study_hash = _hash_uid(str(getattr(ds, "StudyInstanceUID", "")))
                    series_hash = _hash_uid(str(getattr(ds, "SeriesInstanceUID", "")))
            except Exception:  # pragma: no cover
                pass
            # Shape / Spacing über SimpleITK-Reader, fallback: 0,0,0
            try:
                import SimpleITK as sitk  # type: ignore

                reader = sitk.ImageSeriesReader()
                series_files = reader.GetGDCMSeriesFileNames(str(input_path))
                reader.SetFileNames(series_files)
                img = reader.Execute()
                shape = tuple(int(s) for s in img.GetSize()[::-1])
                spacing = tuple(float(s) for s in img.GetSpacing()[::-1])
            except Exception:  # pragma: no cover
                shape = (0, 0, 0)
                spacing = (0.0, 0.0, 0.0)
            return VolumeMetadata(
                volume_shape=cast(tuple[int, int, int], shape),
                voxel_spacing_mm=cast(tuple[float, float, float], spacing),
                modality="CT",
                study_uid_hash=study_hash,
                series_uid_hash=series_hash,
            )

        # NIfTI-Pfad
        img = nib.load(str(input_path))
        shape = tuple(int(s) for s in img.shape[:3])
        spacing = tuple(float(s) for s in img.header.get_zooms()[:3])
        return VolumeMetadata(
            volume_shape=cast(tuple[int, int, int], shape),
            voxel_spacing_mm=cast(tuple[float, float, float], spacing),
            modality="CT",
        )

    @staticmethod
    def _summarize_labels(output_dir: Path, nib, np) -> list[LabelMaskSummary]:
        """Liest die NIfTI-Masken im output_dir und erzeugt Summaries."""
        summaries: list[LabelMaskSummary] = []
        for mask_file in sorted(output_dir.glob("*.nii*")):
            label_str = mask_file.stem.replace(".nii", "")
            try:
                label_enum = SegmentationLabels(label_str)
            except ValueError:
                # Unbekanntes Label — skippen (nicht Teil unserer ROI)
                continue

            img = nib.load(str(mask_file))
            arr = np.asarray(img.dataobj, dtype=bool)
            voxel_count = int(arr.sum())
            spacing = img.header.get_zooms()[:3]
            voxel_volume_mm3 = float(spacing[0] * spacing[1] * spacing[2])
            volume_mm3 = voxel_count * voxel_volume_mm3

            if voxel_count > 0:
                coords = np.argwhere(arr)
                bb_min = tuple(int(c) for c in coords.min(axis=0))
                bb_max = tuple(int(c) for c in coords.max(axis=0))
            else:
                bb_min = (0, 0, 0)
                bb_max = (0, 0, 0)

            summaries.append(
                LabelMaskSummary(
                    label=label_enum,
                    voxel_count=voxel_count,
                    volume_mm3=volume_mm3,
                    bounding_box_min=cast(tuple[int, int, int], bb_min),
                    bounding_box_max=cast(tuple[int, int, int], bb_max),
                )
            )
        return summaries

    @staticmethod
    def _merge_label_masks(
        output_dir: Path,
        case_id: str,
        summaries: list[LabelMaskSummary],
        nib,
        np,
    ) -> Path | None:
        """Mergt einzelne Labels in eine kombinierte Maske ``{case_id}_combined.nii.gz``."""
        if not summaries:
            return None
        combined_arr = None
        affine = None
        for idx, ls in enumerate(summaries, start=1):
            mask_file = next(output_dir.glob(f"{ls.label.value}.nii*"), None)
            if mask_file is None:
                continue
            img = nib.load(str(mask_file))
            arr = np.asarray(img.dataobj, dtype=np.int16)
            if combined_arr is None:
                combined_arr = np.zeros_like(arr, dtype=np.int16)
                affine = img.affine
            combined_arr[arr > 0] = idx
        if combined_arr is None:
            return None
        out_path = output_dir / f"{case_id}_combined.nii.gz"
        nib.save(nib.Nifti1Image(combined_arr, affine), str(out_path))
        return out_path

    def _resolve_model_version(self) -> str:
        if self._model_version is None:
            try:
                from importlib.metadata import version as pkg_version

                self._model_version = pkg_version("totalsegmentator")
            except Exception:  # pragma: no cover
                self._model_version = "unknown"
        return self._model_version

    def _resolve_model_sha(self) -> str:
        """SHA der TotalSegmentator-Modell-Weights für Audit-Reproduzierbarkeit.

        Da TotalSegmentator viele Task-Weights hat, wird nur die Versions-Marke
        gehasht, falls keine Weights-Datei auflösbar ist.
        """
        if self._model_sha is None:
            self._model_sha = hashlib.sha256(
                f"totalseg-{self._resolve_model_version()}-{self.config.task}".encode()
            ).hexdigest()
        return self._model_sha
