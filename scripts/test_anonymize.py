"""
Tests für scripts/anonymize.py — Carotis-AI Anonymisierungs-Pipeline.

Run mit:
    pytest scripts/test_anonymize.py -v

oder ohne pytest direkt:
    python scripts/anonymize.py --self-test
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from anonymize import (
    DICOM_PII_TAGS_BASIC,
    MIN_K_ANONYMITY,
    QUASI_IDENTIFIERS,
    AnonymisationConfig,
    BatchManifest,
    anonymize_file_skeleton,
    build_quasi_identifier_combo,
    check_k_anonymity,
    get_week_bucket,
    hash_with_salt,
    make_case_id,
    run_batch,
    write_manifest_json,
)


# ---- hash_with_salt ----

class TestHashWithSalt:
    def test_deterministic_for_same_inputs(self):
        assert hash_with_salt("study_uid_A", "salt_v1") == hash_with_salt("study_uid_A", "salt_v1")

    def test_changes_with_value(self):
        assert hash_with_salt("study_A", "salt_v1") != hash_with_salt("study_B", "salt_v1")

    def test_changes_with_salt(self):
        assert hash_with_salt("study_A", "salt_v1") != hash_with_salt("study_A", "salt_v2")

    def test_returns_64_char_hex(self):
        h = hash_with_salt("anything", "salt")
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)


# ---- make_case_id ----

class TestMakeCaseId:
    def test_stable_within_week(self):
        a = make_case_id("study_X", "salt_v1", "2026-W18")
        b = make_case_id("study_X", "salt_v1", "2026-W18")
        assert a == b

    def test_changes_between_weeks(self):
        a = make_case_id("study_X", "salt_v1", "2026-W18")
        b = make_case_id("study_X", "salt_v1", "2026-W19")
        assert a != b


# ---- get_week_bucket ----

class TestGetWeekBucket:
    def test_iso_format(self):
        bucket = get_week_bucket(datetime(2026, 4, 27, tzinfo=timezone.utc))
        assert bucket == "2026-W18"

    def test_year_boundary(self):
        # 2025-12-29 ist Mo der ISO-Woche 2026-W01
        bucket = get_week_bucket(datetime(2025, 12, 29, tzinfo=timezone.utc))
        assert bucket == "2026-W01"


# ---- k-anonymity ----

class TestKAnonymity:
    def test_below_threshold_rejects(self):
        counter: dict = {}
        qi = ("60-64", "M", "CT", "2026", "DE")
        counter[qi] = MIN_K_ANONYMITY - 1
        assert check_k_anonymity(qi, counter) < MIN_K_ANONYMITY

    def test_at_threshold_passes(self):
        counter: dict = {}
        qi = ("60-64", "M", "CT", "2026", "DE")
        counter[qi] = MIN_K_ANONYMITY
        assert check_k_anonymity(qi, counter) >= MIN_K_ANONYMITY

    def test_unknown_combo_returns_zero(self):
        counter: dict = {}
        assert check_k_anonymity(("unknown",), counter) == 0


# ---- quasi-identifier extraction ----

class TestBuildQI:
    def test_extracts_all_qi(self):
        meta = {
            "patient_age_bucket": "60-64",
            "patient_sex": "F",
            "modality": "CT",
            "study_year": "2026",
            "institution_country": "JO",
        }
        combo = build_quasi_identifier_combo(meta)
        assert combo == ("60-64", "F", "CT", "2026", "JO")

    def test_unknown_field_uses_placeholder(self):
        combo = build_quasi_identifier_combo({})
        assert all(c == "UNKNOWN" for c in combo)
        assert len(combo) == len(QUASI_IDENTIFIERS)


# ---- anonymize_file_skeleton ----

class TestAnonymizeFile:
    def test_writes_output_when_k_sufficient(self, tmp_path: Path):
        src = tmp_path / "input"
        src.mkdir()
        f = src / "sample.dcm"
        f.write_bytes(b"original")
        out = tmp_path / "output"

        config = AnonymisationConfig(salt="test_salt", min_k=1)  # k=1 → immer ok
        counter: dict = {}
        result = anonymize_file_skeleton(f, out, config, counter)

        assert result.status == "ok"
        assert result.case_id != ""
        assert result.pii_tags_removed == len(DICOM_PII_TAGS_BASIC)
        assert result.anonymized_path is not None
        assert Path(result.anonymized_path).exists()

    def test_rejects_when_k_too_low(self, tmp_path: Path):
        src = tmp_path / "input"
        src.mkdir()
        f = src / "sample.dcm"
        f.write_bytes(b"original")
        out = tmp_path / "output"

        config = AnonymisationConfig(salt="test", min_k=10)
        counter: dict = {}
        result = anonymize_file_skeleton(f, out, config, counter)

        assert result.status == "rejected_low_k"
        assert result.anonymized_path is None
        assert not out.exists() or not list(out.iterdir())

    def test_check_only_doesnt_write(self, tmp_path: Path):
        src = tmp_path / "input"
        src.mkdir()
        f = src / "sample.dcm"
        f.write_bytes(b"original")
        out = tmp_path / "output"

        config = AnonymisationConfig(salt="test", min_k=1, check_only=True)
        counter: dict = {}
        result = anonymize_file_skeleton(f, out, config, counter)

        assert result.status == "skipped_check_only"
        assert result.anonymized_path is None


# ---- run_batch ----

class TestRunBatch:
    def test_empty_dir_returns_empty_manifest(self, tmp_path: Path):
        src = tmp_path / "in"
        src.mkdir()
        out = tmp_path / "out"
        config = AnonymisationConfig(salt="t", min_k=1)
        manifest = run_batch(src, out, config)
        assert manifest.results == []

    def test_processes_all_dcm_files(self, tmp_path: Path):
        src = tmp_path / "in"
        src.mkdir()
        for i in range(3):
            (src / f"file_{i}.dcm").write_bytes(b"x")
        out = tmp_path / "out"
        config = AnonymisationConfig(salt="t", min_k=1)
        manifest = run_batch(src, out, config)
        assert len(manifest.results) == 3
        assert all(r.status == "ok" for r in manifest.results)

    def test_manifest_has_unique_case_ids(self, tmp_path: Path):
        src = tmp_path / "in"
        src.mkdir()
        for i in range(5):
            (src / f"f_{i}.dcm").write_bytes(b"x")
        out = tmp_path / "out"
        config = AnonymisationConfig(salt="t", min_k=1)
        manifest = run_batch(src, out, config)
        case_ids = [r.case_id for r in manifest.results if r.case_id]
        assert len(case_ids) == len(set(case_ids)), "case_ids müssen einzigartig sein"


# ---- write_manifest_json ----

class TestWriteManifest:
    def test_round_trip(self, tmp_path: Path):
        src = tmp_path / "in"
        src.mkdir()
        (src / "f.dcm").write_bytes(b"x")
        out = tmp_path / "out"
        config = AnonymisationConfig(salt="t", min_k=1)
        manifest = run_batch(src, out, config)

        manifest_path = out / "test.manifest.json"
        write_manifest_json(manifest, manifest_path)

        assert manifest_path.exists()
        loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert loaded["batch_id"] == manifest.batch_id
        assert len(loaded["results"]) == 1
        assert loaded["config"]["min_k"] == 1


# ---- DICOM PII Tags Sanity ----

class TestDicomPIITags:
    def test_includes_patient_name(self):
        # Patient's Name = (0x0010, 0x0010) MUSS auf der Liste stehen
        assert (0x0010, 0x0010) in DICOM_PII_TAGS_BASIC

    def test_includes_patient_id(self):
        assert (0x0010, 0x0020) in DICOM_PII_TAGS_BASIC

    def test_includes_institution_name(self):
        assert (0x0008, 0x0080) in DICOM_PII_TAGS_BASIC

    def test_no_duplicates(self):
        assert len(DICOM_PII_TAGS_BASIC) == len(set(DICOM_PII_TAGS_BASIC))


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
