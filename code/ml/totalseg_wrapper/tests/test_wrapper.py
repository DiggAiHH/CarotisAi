"""Tests für TotalSegmentator-Wrapper.

Schwere ML-Dependencies werden gemockt — diese Tests verifizieren die
Wrapper-Logik (PII-Validation, Audit-Payload, Type-Konversion), nicht die
TotalSegmentator-Inferenz selbst.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ml.totalseg_wrapper.types import (
    LabelMaskSummary,
    SegmentationLabels,
    SegmentationResult,
    VolumeMetadata,
    WrapperConfig,
)
from ml.totalseg_wrapper.wrapper import TotalSegmentatorWrapper


@pytest.fixture()
def fake_metadata() -> VolumeMetadata:
    return VolumeMetadata(
        volume_shape=(256, 256, 200),
        voxel_spacing_mm=(0.7, 0.7, 1.0),
        modality="CT",
        study_uid_hash="abc123",
        series_uid_hash="def456",
    )


@pytest.fixture()
def fake_summary() -> LabelMaskSummary:
    return LabelMaskSummary(
        label=SegmentationLabels.ICA_LEFT,
        voxel_count=4815,
        volume_mm3=2360.7,
        bounding_box_min=(120, 80, 30),
        bounding_box_max=(150, 110, 80),
    )


class TestPiiValidation:
    def test_rejects_patient_prefix(self):
        wrapper = TotalSegmentatorWrapper()
        with pytest.raises(ValueError, match="Verdacht auf Patient-Identifier"):
            wrapper._validate_case_id("patient-12345")

    def test_rejects_patid_prefix(self):
        wrapper = TotalSegmentatorWrapper()
        with pytest.raises(ValueError, match="Verdacht auf Patient-Identifier"):
            wrapper._validate_case_id("patid-99")

    def test_rejects_pat_underscore(self):
        wrapper = TotalSegmentatorWrapper()
        with pytest.raises(ValueError, match="Verdacht auf Patient-Identifier"):
            wrapper._validate_case_id("pat_alice_smith")

    def test_rejects_empty(self):
        wrapper = TotalSegmentatorWrapper()
        with pytest.raises(ValueError):
            wrapper._validate_case_id("")
        with pytest.raises(ValueError):
            wrapper._validate_case_id("   ")

    def test_rejects_long(self):
        wrapper = TotalSegmentatorWrapper()
        with pytest.raises(ValueError):
            wrapper._validate_case_id("x" * 100)

    def test_accepts_research_id(self):
        wrapper = TotalSegmentatorWrapper()
        wrapper._validate_case_id("research-case-001")  # should not raise
        wrapper._validate_case_id("imagecas-train-0042")
        wrapper._validate_case_id("klinikum-do-retro-2024-q1-001")


class TestAuditPayload:
    def test_payload_has_no_pii(self, fake_metadata, fake_summary):
        result = SegmentationResult(
            case_id="research-case-001",
            captured_at=datetime(2026, 5, 10, 12, 0, tzinfo=timezone.utc),
            inference_seconds=3.421,
            model_version="2.4.0",
            model_sha256="deadbeef" * 8,
            config_used=WrapperConfig(),
            metadata=fake_metadata,
            label_summaries=(fake_summary,),
        )
        payload = result.to_audit_payload()
        payload_json = json.dumps(payload).lower()
        for forbidden in ("patient", "alice", "mueller", "1990-01-01", "patid"):
            assert forbidden not in payload_json, f"PII-Leak: '{forbidden}'"

    def test_payload_contains_expected_keys(self, fake_metadata, fake_summary):
        result = SegmentationResult(
            case_id="research-case-001",
            captured_at=datetime(2026, 5, 10, 12, 0, tzinfo=timezone.utc),
            inference_seconds=3.421,
            model_version="2.4.0",
            model_sha256="deadbeef" * 8,
            config_used=WrapperConfig(),
            metadata=fake_metadata,
            label_summaries=(fake_summary,),
        )
        payload = result.to_audit_payload()
        assert payload["case_id"] == "research-case-001"
        assert payload["inference_seconds"] == 3.421
        assert payload["model_version"] == "2.4.0"
        assert payload["task"] == "headneck_bones_vessels"
        assert payload["volume_shape"] == [256, 256, 200]
        assert len(payload["label_summaries"]) == 1
        assert payload["label_summaries"][0]["label"] == "internal_carotid_artery_left"
        assert payload["label_summaries"][0]["voxel_count"] == 4815

    def test_payload_is_json_serializable(self, fake_metadata, fake_summary):
        result = SegmentationResult(
            case_id="research-case-001",
            captured_at=datetime.now(timezone.utc),
            inference_seconds=3.421,
            model_version="2.4.0",
            model_sha256="deadbeef" * 8,
            config_used=WrapperConfig(),
            metadata=fake_metadata,
            label_summaries=(fake_summary,),
        )
        # Should not raise
        json.dumps(result.to_audit_payload())


class TestConfigDefaults:
    def test_default_config_is_research_safe(self):
        config = WrapperConfig()
        assert config.task == "headneck_bones_vessels"
        assert config.resolution_mm == 1.5
        assert config.strict_strip_pii is True
        assert SegmentationLabels.ICA_LEFT in config.labels_of_interest
        assert SegmentationLabels.ICA_RIGHT in config.labels_of_interest

    def test_config_is_frozen(self):
        config = WrapperConfig()
        with pytest.raises((AttributeError, TypeError)):
            config.task = "anything"  # type: ignore[misc]


class TestSegmentationFlow:
    def test_segment_raises_on_missing_input(self, tmp_path):
        wrapper = TotalSegmentatorWrapper()
        with pytest.raises(FileNotFoundError):
            wrapper.segment(
                input_path=tmp_path / "nonexistent.nii.gz",
                case_id="research-case-001",
                output_dir=tmp_path / "out",
            )

    @patch("ml.totalseg_wrapper.wrapper.TotalSegmentatorWrapper._lazy_imports")
    def test_segment_orchestrates_call(self, mock_lazy, tmp_path):
        """End-to-end-Smoke mit gemockten ML-Deps."""
        # Setup fake input
        input_file = tmp_path / "case.nii.gz"
        input_file.write_bytes(b"fake-nifti")
        output_dir = tmp_path / "out"

        # Mock the lazy-imported libs
        fake_ts = MagicMock()
        fake_nib = MagicMock()
        fake_np = MagicMock()

        # nib.load returns an image with shape + zooms
        fake_img = MagicMock()
        fake_img.shape = (256, 256, 200)
        fake_img.header.get_zooms.return_value = (0.7, 0.7, 1.0)
        fake_nib.load.return_value = fake_img

        mock_lazy.return_value = (fake_ts, fake_nib, fake_np)

        wrapper = TotalSegmentatorWrapper()
        result = wrapper.segment(
            input_path=input_file,
            case_id="research-case-001",
            output_dir=output_dir,
        )

        # TotalSegmentator wurde aufgerufen
        fake_ts.assert_called_once()
        call_kwargs = fake_ts.call_args.kwargs
        assert call_kwargs["task"] == "headneck_bones_vessels"
        assert "internal_carotid_artery_left" in call_kwargs["roi_subset"]
        assert "internal_carotid_artery_right" in call_kwargs["roi_subset"]
        assert call_kwargs["quiet"] is True

        # Result ist PII-frei und enthält erwartete Felder
        assert result.case_id == "research-case-001"
        assert result.inference_seconds >= 0
        assert result.config_used.task == "headneck_bones_vessels"


class TestLabels:
    def test_labels_enum_values(self):
        assert SegmentationLabels.ICA_LEFT.value == "internal_carotid_artery_left"
        assert SegmentationLabels.ICA_RIGHT.value == "internal_carotid_artery_right"

    def test_labels_enum_is_string_compatible(self):
        # Should work with totalsegmentator roi_subset (expects list of strings)
        labels = [SegmentationLabels.ICA_LEFT.value, SegmentationLabels.ICA_RIGHT.value]
        assert all(isinstance(label, str) for label in labels)
