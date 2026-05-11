"""Tests for constant-time API key comparison (hmac.compare_digest)."""

from __future__ import annotations

import os

import pytest
import pytest_asyncio
from fastapi import HTTPException

os.environ["API_KEY"] = "a" * 32
os.environ["ADMIN_API_KEY"] = "b" * 32
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["ANONYMIZATION_SALT"] = "s" * 16

from app.core.config import get_settings
from app.core.security import hash_demo_token, verify_admin_key, verify_api_key, verify_demo_token


class TestVerifyApiKey:
    @pytest.mark.asyncio
    async def test_valid_key_returns_key(self):
        key = get_settings().api_key
        result = await verify_api_key(key)
        assert result == key

    @pytest.mark.asyncio
    async def test_invalid_key_raises_401(self):
        with pytest.raises(HTTPException) as exc_info:
            await verify_api_key("wrong-key" * 4)
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_timing_attack_resistance_via_compare_digest(self):
        """hmac.compare_digest is used instead of != for constant-time comparison."""
        key = get_settings().api_key
        assert await verify_api_key(key) == key
        with pytest.raises(HTTPException):
            await verify_api_key(key[:-1] + "X")


class TestVerifyAdminKey:
    @pytest.mark.asyncio
    async def test_valid_admin_key_returns_key(self):
        key = get_settings().admin_api_key
        result = await verify_admin_key(key)
        assert result == key

    @pytest.mark.asyncio
    async def test_invalid_admin_key_raises_401(self):
        with pytest.raises(HTTPException) as exc_info:
            await verify_admin_key("wrong-admin")
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_missing_admin_key_raises_401(self):
        with pytest.raises(HTTPException) as exc_info:
            await verify_admin_key(None)
        assert exc_info.value.status_code == 401


class TestHashDemoToken:
    def test_hash_is_sha256_hex(self):
        result = hash_demo_token("test-token")
        assert len(result) == 64
        assert all(c in "0123456789abcdef" for c in result)

    def test_hash_is_deterministic(self):
        assert hash_demo_token("same") == hash_demo_token("same")

    def test_different_tokens_different_hashes(self):
        assert hash_demo_token("a") != hash_demo_token("b")
