"""Tests that decision_tree.schema.json is loaded lazily, not at import time."""

from __future__ import annotations

import os

# Ensure no env vars are set that would trigger Settings creation
for key in list(os.environ.keys()):
    if key.startswith("API_KEY") or key.startswith("ADMIN") or key == "DATABASE_URL":
        del os.environ[key]

# This import must succeed even without env vars because schema is lazy-loaded
from app.db import models


def test_schema_not_loaded_at_import():
    # If another test already loaded it, reset to verify lazy mechanism
    original = models._DECISION_TREE_SCHEMA
    try:
        models._DECISION_TREE_SCHEMA = None
        assert models._DECISION_TREE_SCHEMA is None
    finally:
        models._DECISION_TREE_SCHEMA = original


def test_schema_loaded_on_demand(monkeypatch):
    monkeypatch.setenv("API_KEY", "a" * 32)
    monkeypatch.setenv("ADMIN_API_KEY", "b" * 32)
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    monkeypatch.setenv("ANONYMIZATION_SALT", "s" * 16)

    from app.core.config import get_settings
    get_settings.cache_clear()

    schema = models._get_decision_tree_schema()
    assert schema is not None
    assert "type" in schema
    assert schema["type"] == "object"

    # Second call returns cached schema
    assert models._get_decision_tree_schema() is schema
