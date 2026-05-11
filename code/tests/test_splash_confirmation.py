from __future__ import annotations

import pytest
from httpx import AsyncClient


API_KEY = "a" * 32
ADMIN_KEY = "b" * 32


@pytest.mark.asyncio
async def test_splash_confirmation_creates_audit_event(test_client: AsyncClient) -> None:
    payload = {
        "session_id": "session-2026-05-11",
        "role_hash": "role-hash-session-001",
        "confirmed_at": "2026-05-11T19:45:00Z",
        "version": "zweckbestimmung_2026-05-06",
    }

    response = await test_client.post(
        "/api/v1/audit/splash-confirmation",
        headers={"X-API-Key": API_KEY},
        json=payload,
    )

    assert response.status_code == 200
    assert response.json()["server_mode"] == "research_prototype"

    events = await test_client.get(
        "/api/v1/audit/events",
        params={"type": "splash_confirmation"},
        headers={"X-API-Key": API_KEY, "X-Admin-Key": ADMIN_KEY},
    )

    assert events.status_code == 200
    items = events.json()["items"]
    assert len(items) == 1
    event = items[0]
    assert event["event_type"] == "splash_confirmation"
    assert event["payload_redacted"]["version"] == "zweckbestimmung_2026-05-06"
    assert event["payload_redacted"]["session_id"] == payload["session_id"]
    assert event["payload_redacted"]["role_hash"] == payload["role_hash"]
    assert event["payload_redacted"]["confirmed_at"].startswith("2026-05-11")


@pytest.mark.asyncio
async def test_splash_confirmation_rejects_missing_fields(
    test_client: AsyncClient,
) -> None:
    response = await test_client.post(
        "/api/v1/audit/splash-confirmation",
        headers={"X-API-Key": API_KEY},
        json={
            "session_id": "session-2026-05-11",
            "confirmed_at": "2026-05-11T19:45:00Z",
            "version": "zweckbestimmung_2026-05-06",
        },
    )

    assert response.status_code == 422
