from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.core.config import Settings, get_settings


class TestSettings:
    def test_happy_path(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "a" * 32)
        monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
        monkeypatch.setenv("LOG_LEVEL", "INFO")
        monkeypatch.setenv("MIN_K_ANONYMITY", "5")
        s = Settings()
        assert s.api_key == "a" * 32
        assert s.database_url.startswith("sqlite")
        assert s.min_k_anonymity == 5

    def test_api_key_too_short(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "short")
        monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
        with pytest.raises(ValidationError) as exc_info:
            Settings()
        assert "api_key" in str(exc_info.value).lower()

    def test_min_k_below_5(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "a" * 32)
        monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
        monkeypatch.setenv("MIN_K_ANONYMITY", "3")
        with pytest.raises(ValidationError) as exc_info:
            Settings()
        assert "min_k_anonymity" in str(exc_info.value).lower()

    def test_log_level_invalid(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "a" * 32)
        monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
        monkeypatch.setenv("LOG_LEVEL", "VERBOSE")
        with pytest.raises(ValidationError) as exc_info:
            Settings()
        assert "log_level" in str(exc_info.value).lower()

    def test_get_settings_cached(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "a" * 32)
        monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
        get_settings.cache_clear()
        s1 = get_settings()
        s2 = get_settings()
        assert s1 is s2
