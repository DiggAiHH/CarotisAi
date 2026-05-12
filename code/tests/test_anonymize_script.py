from __future__ import annotations

import csv
import os
from pathlib import Path

import pydicom
import pytest

# Ensure env vars are set before any app import
os.environ.setdefault("API_KEY", "a" * 32)
os.environ.setdefault("ADMIN_API_KEY", "b" * 32)
os.environ.setdefault("ANONYMIZATION_SALT", "s" * 32)

from scripts.anonymize import main


REAL_MRI_DIR = Path(__file__).resolve().parents[1] / "tests" / "test_data" / "real_mri"


def _write_minimal_dicom(path: Path, *, patient_name: str | None = None, patient_id: str | None = None) -> None:
    """Write a minimal but valid DICOM file with File Meta Information and preamble."""
    ds = pydicom.Dataset()
    ds.Rows = 64
    ds.Columns = 64
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.PixelRepresentation = 0
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelData = b"\x00" * (64 * 64 * 2)

    if patient_name is not None:
        ds.PatientName = patient_name
    if patient_id is not None:
        ds.PatientID = patient_id

    file_meta = pydicom.dataset.FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = pydicom.uid.SecondaryCaptureImageStorage
    file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

    fds = pydicom.dataset.FileDataset(
        path,
        ds,
        file_meta=file_meta,
        preamble=b"\x00" * 128,
    )
    pydicom.dcmwrite(path, fds)


class TestDryRun:
    def test_dry_run_detects_pii_without_writing(self, tmp_path: Path) -> None:
        source = tmp_path / "pii.dcm"
        _write_minimal_dicom(source, patient_name="Test Patient", patient_id="12345")

        exit_code = main(["--input", str(source), "--dry-run"])
        assert exit_code == 0

        # No output directory should be created
        assert not (tmp_path / "output").exists()

    def test_dry_run_on_clean_files_reports_skipped(self) -> None:
        assert REAL_MRI_DIR.exists(), "real_mri test data missing"
        exit_code = main(["--input", str(REAL_MRI_DIR), "--dry-run"])
        assert exit_code == 0


class TestBatchProcessing:
    def test_batch_skips_already_clean_files(self, tmp_path: Path) -> None:
        assert REAL_MRI_DIR.exists(), "real_mri test data missing"
        output_dir = tmp_path / "out"
        manifest = tmp_path / "manifest.csv"

        exit_code = main([
            "--input", str(REAL_MRI_DIR),
            "--output", str(output_dir),
            "--manifest", str(manifest),
        ])
        assert exit_code == 0

        # All 5 files should be copied as "skipped"
        assert output_dir.exists()
        dcm_files = sorted(output_dir.glob("*.dcm"))
        assert len(dcm_files) == 5

        # Manifest should show all skipped
        rows = list(csv.DictReader(manifest.read_text(encoding="utf-8").splitlines()))
        assert len(rows) == 5
        for row in rows:
            assert row["status"] == "skipped"
            assert row["tags_removed"] == "0"
            assert row["output_path"] != ""


class TestManifest:
    def test_manifest_csv_format(self, tmp_path: Path) -> None:
        clean_path = tmp_path / "clean.dcm"
        _write_minimal_dicom(clean_path)

        pii_path = tmp_path / "pii.dcm"
        _write_minimal_dicom(pii_path, patient_name="Patient A", patient_id="99999")

        output_dir = tmp_path / "out"
        manifest = tmp_path / "manifest.csv"

        exit_code = main([
            "--input", str(tmp_path),
            "--output", str(output_dir),
            "--manifest", str(manifest),
        ])
        assert exit_code == 0

        rows = list(csv.DictReader(manifest.read_text(encoding="utf-8").splitlines()))
        assert len(rows) == 2

        statuses = {r["status"] for r in rows}
        assert "skipped" in statuses
        assert "ok" in statuses

        # Verify columns exist
        for row in rows:
            assert "original_hash" in row
            assert "output_path" in row
            assert "tags_removed" in row
            assert "status" in row
            assert len(row["original_hash"]) == 64  # SHA-256 hex


class TestExitCodes:
    def test_exit_code_2_when_input_does_not_exist(self) -> None:
        exit_code = main(["--input", "/nonexistent/path/foobar", "--dry-run"])
        assert exit_code == 2

    def test_exit_code_2_when_no_dicom_files(self, tmp_path: Path) -> None:
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        exit_code = main(["--input", str(empty_dir), "--dry-run"])
        assert exit_code == 2

    def test_output_same_as_input_raises(self, tmp_path: Path) -> None:
        source = tmp_path / "file.dcm"
        source.write_bytes(b"dummy")
        with pytest.raises(ValueError, match="output path must differ from input path"):
            main(["--input", str(source), "--output", str(source)])
