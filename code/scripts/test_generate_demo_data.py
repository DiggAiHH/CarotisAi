"""Tests for generate_demo_data.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pydicom
import pytest

# project root = code/scripts/../../
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = PROJECT_ROOT / "schemas" / "decision_tree.schema.json"
ANON_SCRIPT = PROJECT_ROOT / "scripts" / "anonymize.py"
GEN_SCRIPT = PROJECT_ROOT / "code" / "scripts" / "generate_demo_data.py"
OUTPUT_DIR = PROJECT_ROOT / "data" / "demo"

DICOM_PII_TAGS = (
    (0x0010, 0x0010),  # PatientName
    (0x0010, 0x0020),  # PatientID
    (0x0010, 0x0030),  # BirthDate
    (0x0008, 0x0050),  # AccessionNumber
    (0x0008, 0x0090),  # ReferringPhysician
    (0x0008, 0x1050),  # PerformingPhysician
    (0x0008, 0x1070),  # OperatorsName
)


@pytest.fixture(scope="module")
def generated_data():
    """Run generator once per test module."""
    result = subprocess.run(
        [sys.executable, str(GEN_SCRIPT), "--count", "10"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Generator failed: {result.stderr}"
    return OUTPUT_DIR


class TestDicomGeneration:
    def test_ten_dicoms_created(self, generated_data: Path) -> None:
        dicoms = list((generated_data / "dicoms").glob("*.dcm"))
        assert len(dicoms) == 10

    def test_no_pii_in_dicoms(self, generated_data: Path) -> None:
        for dcm_path in (generated_data / "dicoms").glob("*.dcm"):
            ds = pydicom.dcmread(dcm_path)
            for tag in DICOM_PII_TAGS:
                elem = ds[tag] if tag in ds else None
                if elem is not None:
                    val = str(elem.value).strip()
                    assert (
                        val == "" or val == "None"
                    ), f"PII found in {dcm_path.name} at tag {tag}: {val!r}"

    def test_anonymize_check_passes(self, generated_data: Path) -> None:
        out_dir = generated_data / "anonymized"
        out_dir.mkdir(exist_ok=True)
        result = subprocess.run(
            [
                sys.executable,
                str(ANON_SCRIPT),
                "--check",
                "--input",
                str(generated_data / "dicoms"),
                "--output",
                str(out_dir),
                "--min-k",
                "1",
            ],
            capture_output=True,
            text=True,
        )
        assert (
            result.returncode == 0
        ), f"anonymize.py --check failed: {result.stdout}\n{result.stderr}"


class TestDecisionTreeGeneration:
    def test_ten_trees_created(self, generated_data: Path) -> None:
        trees = list((generated_data / "decision_trees").glob("*.json"))
        assert len(trees) == 10

    def test_all_trees_validate(self, generated_data: Path) -> None:
        from jsonschema import Draft202012Validator

        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)

        for tree_path in (generated_data / "decision_trees").glob("*.json"):
            data = json.loads(tree_path.read_text(encoding="utf-8"))
            errors = list(validator.iter_errors(data))
            assert (
                len(errors) == 0
            ), f"Validation failed for {tree_path.name}: " + "; ".join(
                e.message for e in errors
            )
