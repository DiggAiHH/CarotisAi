from __future__ import annotations

import asyncio
import importlib.util
import sys
from io import BytesIO
from pathlib import Path

import pydicom
import structlog

logger = structlog.get_logger()

from app.core.config import get_settings

# Dynamically import scripts/anonymize.py to reuse the PII tag list
_anon_script = Path(get_settings().project_root) / "scripts" / "anonymize.py"
_spec = importlib.util.spec_from_file_location("anonymize", _anon_script)
_anon_module = importlib.util.module_from_spec(_spec)
sys.modules["anonymize"] = _anon_module
_spec.loader.exec_module(_anon_module)  # type: ignore[union-attr]

DICOM_PII_TAGS_BASIC: tuple[tuple[int, int], ...] = _anon_module.DICOM_PII_TAGS_BASIC


class AnonymizationService:
    def __init__(self):
        self.logger = logger.bind(service="anonymization")

    async def ensure_anonymized(self, dicom_bytes: bytes) -> bytes:
        """Return anonymized DICOM bytes by removing all PII tags."""
        return await asyncio.to_thread(self._ensure_anonymized_sync, dicom_bytes)

    def _ensure_anonymized_sync(self, dicom_bytes: bytes) -> bytes:
        ds = pydicom.dcmread(BytesIO(dicom_bytes))
        removed = 0
        for tag in DICOM_PII_TAGS_BASIC:
            if tag in ds:
                del ds[tag]
                removed += 1
        self.logger.info("anonymized_dicom", tags_removed=removed)
        buffer = BytesIO()
        ds.save_as(buffer)
        return buffer.getvalue()

    def check_only(self, dicom_bytes: bytes) -> tuple[bool, list[str]]:
        """Return (is_anonymized, list_of_pii_tags_found)."""
        ds = pydicom.dcmread(BytesIO(dicom_bytes))
        found: list[str] = []
        for tag in DICOM_PII_TAGS_BASIC:
            if tag in ds:
                found.append(f"{tag[0]:04X},{tag[1]:04X}")
        is_anonymized = len(found) == 0
        if not is_anonymized:
            self.logger.warning("pii_detected", tags=found)
        return is_anonymized, found
