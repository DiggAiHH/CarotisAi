"""Tests for PII Detection Service.

Covers regex + Spacy NER layers. Spacy model is optional — tests must pass
without it (regex-only fallback).
"""

from __future__ import annotations

import pytest

from app.services.pii_detection_service import PIIDetectionService


@pytest.fixture
def svc():
    return PIIDetectionService()


class TestRegexLayer:
    """Regex fallbacks work regardless of Spacy installation."""

    def test_detects_phone(self, svc):
        spans = svc.detect("Tel: 0231/12345-67")
        assert any(s.label == "PHONE" for s in spans)

    def test_detects_email(self, svc):
        spans = svc.detect("kontakt@klinikum-do.de")
        assert any(s.label == "EMAIL" for s in spans)

    def test_detects_id(self, svc):
        spans = svc.detect("Akte AB-12345")
        assert any(s.label == "ID" for s in spans)

    def test_detects_german_name_with_title(self, svc):
        spans = svc.detect("Mein Patient Herr Schmidt")
        assert any(s.label == "PERSON" for s in spans)

    def test_detects_frau_name(self, svc):
        spans = svc.detect("Frau Müller kommt morgen")
        assert any(s.label == "PERSON" for s in spans)

    def test_detects_dr_name(self, svc):
        spans = svc.detect("Dr. Weber hat gesagt")
        assert any(s.label == "PERSON" for s in spans)

    def test_clean_medical_text(self, svc):
        text = "Plaque echolucent dorsal, Stenosegrad 65 % nach NASCET."
        assert svc.is_clean(text)

    def test_empty_string(self, svc):
        assert svc.detect("") == []
        assert svc.is_clean("")

    def test_multiple_spans(self, svc):
        spans = svc.detect("Patient Herr Müller, Tel 0231/123-456, mueller@klinik.de")
        labels = {s.label for s in spans}
        assert "PERSON" in labels
        assert "PHONE" in labels
        assert "EMAIL" in labels


class TestRedact:
    def test_redact_replaces_spans(self, svc):
        text = "Herr Schmidt, Tel 0231/12345"
        redacted = svc.redact(text)
        assert "[REDACTED-PERSON]" in redacted
        assert "[REDACTED-PHONE]" in redacted
        assert "Herr Schmidt" not in redacted

    def test_redact_clean_text_unchanged(self, svc):
        text = "Stenosegrad 65 %, Plaque calcifiziert."
        assert svc.redact(text) == text


class TestCheckTextEndpoint:
    """Integration tests via FastAPI TestClient."""

    @pytest.fixture
    def client(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "a" * 32)
        monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
        monkeypatch.setenv("ONNX_MODEL_PATH", "/tmp/fake.onnx")
        monkeypatch.setenv("DEBUG", "true")
        from app.core.config import get_settings

        get_settings.cache_clear()
        from app.db.database import get_engine

        get_engine.cache_clear()
        from fastapi.testclient import TestClient
        from app.main import create_app

        app = create_app()
        return TestClient(app)

    def test_check_text_clean(self, client):
        r = client.post(
            "/api/v1/decision-tree/check-text",
            json={"text": "Stenosegrad 65 %, Plaque calcifiziert."},
            headers={"X-API-Key": "a" * 32},
        )
        assert r.status_code == 200
        assert r.json()["is_clean"] is True
        assert r.json()["pii_spans"] == []

    def test_check_text_with_pii(self, client):
        r = client.post(
            "/api/v1/decision-tree/check-text",
            json={"text": "Patient Herr Müller, Tel 0231/123-456"},
            headers={"X-API-Key": "a" * 32},
        )
        assert r.status_code == 200
        assert r.json()["is_clean"] is False
        spans = r.json()["pii_spans"]
        assert any(s["label"] == "PERSON" for s in spans)
        assert any(s["label"] == "PHONE" for s in spans)

    def test_check_text_empty(self, client):
        r = client.post(
            "/api/v1/decision-tree/check-text",
            json={"text": ""},
            headers={"X-API-Key": "a" * 32},
        )
        assert r.status_code == 200
        assert r.json()["is_clean"] is True

    def test_check_text_too_long(self, client):
        r = client.post(
            "/api/v1/decision-tree/check-text",
            json={"text": "x" * 2001},
            headers={"X-API-Key": "a" * 32},
        )
        assert r.status_code == 422

    def test_check_text_not_string(self, client):
        r = client.post(
            "/api/v1/decision-tree/check-text",
            json={"text": 123},
            headers={"X-API-Key": "a" * 32},
        )
        assert r.status_code == 422
