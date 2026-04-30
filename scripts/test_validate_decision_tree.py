"""pytest tests for decision tree schema validation."""
from __future__ import annotations

import json

import pytest
from jsonschema import Draft202012Validator


def load_schema():
    from pathlib import Path
    schema_path = Path(__file__).resolve().parent.parent / "schemas" / "decision_tree.schema.json"
    return json.loads(schema_path.read_text(encoding="utf-8"))


@pytest.fixture
def validator():
    schema = load_schema()
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _make_tree(**overrides):
    """Return a minimal valid decision tree with overrides applied."""
    base = {
        "case_id": "a" * 64,
        "captured_at": "2026-08-15T14:23:00Z",
        "physician_role_hash": "b" * 64,
        "ai_prediction": {
            "stenosis_pct_nascet": 50.0,
            "confidence": 0.9,
            "vulnerability_markers": {
                "intraplaque_hemorrhage": 0.5,
                "thin_fibrous_cap": 0.2,
                "lipid_rich_necrotic_core": 0.3,
                "systolic_motion_anomaly": 0.1,
            },
            "model_version": "v0.1.0",
            "model_sha": "abc123d",
        },
        "physician_decision": {
            "stenosis_pct_nascet": 55.0,
            "confirmed_markers": [],
            "rejected_markers": [],
            "added_markers": [],
        },
        "agreement_with_ai": {
            "verdict": "full_agreement",
            "delta_pct": 5.0,
            "trust_score_for_this_case": 4,
        },
        "anonymisation": {
            "method": "DICOM_PS_3.15_basic",
            "salt_version": "v2026-04",
            "audit_id": "AT-001",
            "k_anonymity_min": 5,
        },
    }
    base.update(overrides)
    return base


class TestFreeTextNotes:
    def test_free_text_notes_valid(self, validator):
        tree = _make_tree(reasoning={"free_text_notes": "Plaque unklar, Verlaufskontrolle empfohlen."})
        errors = list(validator.iter_errors(tree))
        assert errors == []

    def test_free_text_notes_too_long(self, validator):
        tree = _make_tree(reasoning={"free_text_notes": "x" * 2001})
        errors = list(validator.iter_errors(tree))
        assert any("2000" in e.message for e in errors)

    def test_free_text_notes_null(self, validator):
        tree = _make_tree(reasoning={"free_text_notes": None})
        errors = list(validator.iter_errors(tree))
        assert errors == []

    def test_free_text_notes_empty_string(self, validator):
        tree = _make_tree(reasoning={"free_text_notes": ""})
        errors = list(validator.iter_errors(tree))
        assert errors == []

    def test_reasoning_null(self, validator):
        tree = _make_tree(reasoning=None)
        errors = list(validator.iter_errors(tree))
        assert errors == []

    def test_sample_file_still_valid(self, validator):
        from pathlib import Path
        sample_path = Path(__file__).resolve().parent.parent / "schemas" / "decision_tree.sample.json"
        data = json.loads(sample_path.read_text(encoding="utf-8"))
        data.pop("_comment", None)
        errors = list(validator.iter_errors(data))
        assert errors == []
