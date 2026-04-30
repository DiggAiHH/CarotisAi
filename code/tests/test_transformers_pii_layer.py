"""Tests for TransformersPIILayer and refactored PIIDetectionService.

Skips gracefully if torch/transformers are not installed.
"""

from __future__ import annotations

import pytest

from app.services.pii_detection_service import (
    Ensemble,
    PIISpan,
    RegexLayer,
    get_pii_service,
)

# ---------------------------------------------------------------------------
# Transformers layer availability check
# ---------------------------------------------------------------------------

try:
    import torch  # noqa: F401
    import transformers  # noqa: F401

    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False


# ---------------------------------------------------------------------------
# RegexLayer tests (isolated)
# ---------------------------------------------------------------------------


class TestRegexLayer:
    def test_detects_phone(self):
        spans = RegexLayer.detect("Rufen Sie 01234-567890 an.")
        assert any(s.label == "PHONE" for s in spans)

    def test_detects_email(self):
        spans = RegexLayer.detect("Mail: max.mustermann@klinikum.de")
        assert any(s.label == "EMAIL" for s in spans)

    def test_detects_german_name_with_title(self):
        spans = RegexLayer.detect("Dr. Schmidt untersucht den Patienten.")
        assert any(s.label == "PERSON" for s in spans)

    def test_empty_string(self):
        assert RegexLayer.detect("") == []


# ---------------------------------------------------------------------------
# Ensemble tests
# ---------------------------------------------------------------------------


class TestEnsemble:
    def test_prefers_longer_span(self):
        spans = [
            PIISpan(0, 10, "PERSON", "Dr. Schmidt"),
            PIISpan(0, 3, "PERSON", "Dr."),  # shorter, contained
        ]
        merged = Ensemble.merge(spans)
        assert len(merged) == 1
        assert merged[0].end == 10

    def test_non_overlapping_spans_preserved(self):
        spans = [
            PIISpan(0, 5, "PHONE", "01234"),
            PIISpan(10, 20, "EMAIL", "a@b.de"),
        ]
        merged = Ensemble.merge(spans)
        assert len(merged) == 2


# ---------------------------------------------------------------------------
# PIIDetectionService integration tests
# ---------------------------------------------------------------------------


class TestPIIDetectionService:
    def test_detect_combines_layers(self):
        svc = get_pii_service()
        spans = svc.detect("Dr. Mueller, Tel: 01234-567890")
        labels = {s.label for s in spans}
        assert "PERSON" in labels
        assert "PHONE" in labels

    def test_is_clean_true(self):
        svc = get_pii_service()
        assert svc.is_clean("Keine PII hier, nur medizinischer Text.")

    def test_is_clean_false(self):
        svc = get_pii_service()
        assert not svc.is_clean("Dr. Mueller untersucht.")

    def test_redact_replaces_spans(self):
        svc = get_pii_service()
        text = svc.redact("Mail: max@klinikum.de")
        assert "[REDACTED-EMAIL]" in text
        assert "max@klinikum.de" not in text


# ---------------------------------------------------------------------------
# TransformersPIILayer tests (skip if deps missing)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not TRANSFORMERS_AVAILABLE, reason="torch/transformers not installed"
)
class TestTransformersPIILayer:
    def test_layer_initialization(self):
        from app.services.transformers_pii_layer import TransformersPIILayer

        layer = TransformersPIILayer()
        assert (
            layer.model_id
            == "OpenMed/OpenMed-PII-German-ClinicalLongformer-Base-149M-v1"
        )
        assert layer.threshold == 0.85

    def test_label_mapping_basic(self):
        from app.services.transformers_pii_layer import _map_label

        assert _map_label("B-FIRSTNAME") == "PERSON"
        assert _map_label("I-PHONE") == "PHONE"
        assert _map_label("B-EMAIL") == "EMAIL"
        assert _map_label("B-SSN") == "ID"
        assert _map_label("O") is None
        assert _map_label("B-UNKNOWN") is None

    def test_label_mapping_extended(self):
        from app.services.transformers_pii_layer import _map_label

        assert _map_label("B-DATE", extended=True) == "DATE"
        assert _map_label("B-STREET", extended=True) == "ADDRESS"
        assert _map_label("B-DATE", extended=False) is None

    def test_detect_empty_string(self):
        from app.services.transformers_pii_layer import TransformersPIILayer

        layer = TransformersPIILayer()
        assert layer.detect("") == []

    def test_detect_empty_returns_list(self):
        from app.services.transformers_pii_layer import TransformersPIILayer

        layer = TransformersPIILayer()
        # Empty string should return [] immediately without loading model
        result = layer.detect("")
        assert isinstance(result, list)
        assert result == []


# ---------------------------------------------------------------------------
# Config integration tests
# ---------------------------------------------------------------------------


class TestConfigIntegration:
    def test_transformers_pii_defaults(self):
        from app.core.config import Settings

        s = Settings(
            api_key="x" * 32,
        )
        assert s.transformers_pii_enabled is False
        assert s.transformers_pii_threshold == 0.85
        assert (
            s.transformers_pii_model
            == "OpenMed/OpenMed-PII-German-ClinicalLongformer-Base-149M-v1"
        )

    def test_threshold_validation(self):
        from app.core.config import Settings

        with pytest.raises(ValueError):
            Settings(api_key="x" * 32, transformers_pii_threshold=1.5)

        with pytest.raises(ValueError):
            Settings(api_key="x" * 32, transformers_pii_threshold=-0.1)
