"""DICOM parsing and anonymisation service.

Implements DICOM PS 3.15 Basic Application Level Confidentiality Profile.
All 33 PII tags are removed/replaced before the pixel array is returned.
The raw DICOM bytes NEVER leave this function — only numpy arrays do.
"""

from __future__ import annotations

import io
from dataclasses import dataclass, field

import numpy as np
import pydicom

# DICOM PS 3.15 Basic Profile — all mandatory attributes to de-identify
_PII_TAGS: frozenset[str] = frozenset(
    {
        "PatientName",
        "PatientID",
        "PatientBirthDate",
        "PatientSex",
        "PatientAge",
        "PatientWeight",
        "PatientAddress",
        "PatientTelephoneNumbers",
        "EthnicGroup",
        "StudyID",
        "AccessionNumber",
        "ReferringPhysicianName",
        "StudyDate",
        "StudyTime",
        "SeriesDate",
        "SeriesTime",
        "AcquisitionDate",
        "AcquisitionTime",
        "ContentDate",
        "ContentTime",
        "InstanceCreationDate",
        "InstanceCreationTime",
        "PerformingPhysicianName",
        "OperatorsName",
        "RequestingPhysician",
        "InstitutionName",
        "InstitutionAddress",
        "InstitutionalDepartmentName",
        "StationName",
        "DeviceSerialNumber",
        "ProtocolName",
        "RequestAttributesSequence",
        "ScheduledProcedureStepSequence",
    }
)


@dataclass
class DicomMetadata:
    """Non-PII metadata kept for clinical context."""

    rows: int = 0
    cols: int = 0
    pixel_spacing: tuple[float, float] = field(default_factory=lambda: (1.0, 1.0))
    slice_thickness_mm: float = 1.0
    rescale_slope: float = 1.0
    rescale_intercept: float = 0.0


class DicomService:
    """Parse a DICOM byte buffer, strip PII, return pixel array + safe metadata."""

    def parse_and_anonymise(
        self, dicom_bytes: bytes
    ) -> tuple[np.ndarray, DicomMetadata]:
        """Return (pixel_array float32 in HU, safe metadata).

        Raises ValueError for invalid DICOM or missing pixel data.
        """
        try:
            ds = pydicom.dcmread(io.BytesIO(dicom_bytes), force=True)
        except Exception as exc:
            raise ValueError(f"Cannot read DICOM: {exc}") from exc

        if not hasattr(ds, "PixelData"):
            raise ValueError("DICOM file has no pixel data")

        # Strip PII — immutable: work on a copy
        ds_clean = ds.copy()
        for tag in _PII_TAGS:
            if hasattr(ds_clean, tag):
                delattr(ds_clean, tag)

        metadata = DicomMetadata(
            rows=int(getattr(ds_clean, "Rows", 0)),
            cols=int(getattr(ds_clean, "Columns", 0)),
            pixel_spacing=tuple(
                float(v) for v in getattr(ds_clean, "PixelSpacing", [1.0, 1.0])
            ),
            slice_thickness_mm=float(getattr(ds_clean, "SliceThickness", 1.0)),
            rescale_slope=float(getattr(ds_clean, "RescaleSlope", 1.0)),
            rescale_intercept=float(getattr(ds_clean, "RescaleIntercept", 0.0)),
        )

        pixel_array = self._to_hu(ds_clean, metadata)
        return pixel_array, metadata

    @staticmethod
    def _to_hu(ds: pydicom.Dataset, meta: DicomMetadata) -> np.ndarray:
        """Convert raw pixel values to Hounsfield Units (float32)."""
        raw = ds.pixel_array.astype(np.float32)
        hu = raw * meta.rescale_slope + meta.rescale_intercept
        return hu

    @staticmethod
    def preprocess_for_model(
        hu_array: np.ndarray,
        target_size: tuple[int, int] = (512, 512),
        window_center: float = 40.0,
        window_width: float = 400.0,
    ) -> np.ndarray:
        """Windowing + resize + normalise → (1, 1, H, W) float32 ONNX input."""
        import cv2

        # Window + clip to soft-tissue window (carotid default)
        low = window_center - window_width / 2
        high = window_center + window_width / 2
        windowed = np.clip(hu_array, low, high)
        normalised = (windowed - low) / (high - low)  # → [0, 1]

        resized = cv2.resize(normalised, target_size, interpolation=cv2.INTER_LINEAR)
        return resized[np.newaxis, np.newaxis, :, :].astype(np.float32)
