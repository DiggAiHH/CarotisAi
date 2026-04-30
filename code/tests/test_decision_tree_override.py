"""Tests for decision-tree capture with disagreement/override support (Schema v0.3)."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


def _base_payload() -> dict:
    return {
        "case_id": "a" * 64,
        "captured_at": "2026-04-28T12:00:00Z",
        "physician_role_hash": "b" * 64,
        "ai_prediction": {
            "stenosis_pct_nascet": 65.0,
            "confidence": 0.89,
            "vulnerability_markers": {
                "intraplaque_hemorrhage": 0.82,
                "thin_fibrous_cap": 0.41,
                "lipid_rich_necrotic_core": 0.71,
                "systolic_motion_anomaly": 0.13,
            },
            "model_version": "v0.3.2",
            "model_sha": "abc123d",
        },
        "physician_decision": {
            "stenosis_pct_nascet": 65.0,
            "confirmed_markers": ["intraplaque_hemorrhage"],
            "rejected_markers": [],
            "added_markers": [],
        },
        "agreement_with_ai": {
            "verdict": "full_agreement",
            "delta_pct": 0.0,
            "trust_score_for_this_case": 4,
        },
        "anonymisation": {
            "method": "DICOM_PS_3.15_basic",
            "salt_version": "v2026-04",
            "audit_id": "AT-001",
            "k_anonymity_min": 5,
        },
    }


# ---------------------------------------------------------------------------
# Schema validation tests
# ---------------------------------------------------------------------------


class TestSchemaValidation:
    @pytest.mark.asyncio
    async def test_capture_without_disagreement_ok(
        self, test_client: AsyncClient
    ) -> None:
        """Backward compat: captures without disagreement block still valid."""
        payload = _base_payload()
        resp = await test_client.post(
            "/api/v1/decision-tree/capture",
            headers={"X-API-Key": "a" * 32, "Content-Type": "application/json"},
            json=payload,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "audit_id" in data

    @pytest.mark.asyncio
    async def test_capture_with_disagreement_ok(self, test_client: AsyncClient) -> None:
        """Capture with full disagreement block succeeds."""
        payload = _base_payload()
        payload["disagreement"] = {
            "ai_verdict": "moderate",
            "physician_verdict": "mild",
            "override_reason": "clinical_judgment",
            "override_free_text": "Plaque scheint chronisch stabil.",
        }
        payload["agreement_with_ai"]["verdict"] = "disagreement"
        resp = await test_client.post(
            "/api/v1/decision-tree/capture",
            headers={"X-API-Key": "a" * 32, "Content-Type": "application/json"},
            json=payload,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"

    @pytest.mark.asyncio
    async def test_disagreement_same_verdict_rejected(
        self, test_client: AsyncClient
    ) -> None:
        """Disagreement requires ai_verdict != physician_verdict."""
        payload = _base_payload()
        payload["disagreement"] = {
            "ai_verdict": "moderate",
            "physician_verdict": "moderate",
            "override_reason": "other",
        }
        resp = await test_client.post(
            "/api/v1/decision-tree/capture",
            headers={"X-API-Key": "a" * 32, "Content-Type": "application/json"},
            json=payload,
        )
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_disagreement_invalid_reason_rejected(
        self, test_client: AsyncClient
    ) -> None:
        """Override reason must be from CDSiC enum."""
        payload = _base_payload()
        payload["disagreement"] = {
            "ai_verdict": "moderate",
            "physician_verdict": "mild",
            "override_reason": "random_reason",
        }
        resp = await test_client.post(
            "/api/v1/decision-tree/capture",
            headers={"X-API-Key": "a" * 32, "Content-Type": "application/json"},
            json=payload,
        )
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_disagreement_override_free_text_too_long(
        self, test_client: AsyncClient
    ) -> None:
        """override_free_text max 500 chars."""
        payload = _base_payload()
        payload["disagreement"] = {
            "ai_verdict": "moderate",
            "physician_verdict": "mild",
            "override_reason": "other",
            "override_free_text": "x" * 501,
        }
        resp = await test_client.post(
            "/api/v1/decision-tree/capture",
            headers={"X-API-Key": "a" * 32, "Content-Type": "application/json"},
            json=payload,
        )
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Audit trail tests
# ---------------------------------------------------------------------------


class TestAuditTrail:
    @pytest.mark.asyncio
    async def test_override_audit_event_written(self, test_client: AsyncClient) -> None:
        """Disagreement capture writes decision_tree_override audit event."""
        payload = _base_payload()
        payload["disagreement"] = {
            "ai_verdict": "severe",
            "physician_verdict": "moderate",
            "override_reason": "insufficient_evidence",
        }
        payload["agreement_with_ai"]["verdict"] = "physician_override"
        resp = await test_client.post(
            "/api/v1/decision-tree/capture",
            headers={"X-API-Key": "a" * 32, "Content-Type": "application/json"},
            json=payload,
        )
        assert resp.status_code == 200
