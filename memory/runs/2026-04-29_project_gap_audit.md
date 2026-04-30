---
name: 2026-04-29_gap_audit
author: Kimi Code CLI (Auditor)
type: audit
---

# Carotis-AI — Comprehensive Gap Analysis

**Date:** 2026-04-29
**Scope:** Backend, Frontend, ML Pipeline, DevOps, Security, Documentation, Compliance
**Method:** Static source-code analysis of 47+ files

---

## Executive Summary

The Carotis-AI project has a solid architectural skeleton but suffers from **critical runtime-breaking inconsistencies** between backend routes, frontend API clients, and data models. Several services are defined but never wired into the application. The ML pipeline has a fatal ONNX export bug. Docker Compose has port mismatches. Most critically: the audit service references non-existent database models, which will cause the backend to crash on startup if any audit endpoint is exercised beyond the basic smoke tests.

---

## Gap Table

| # | Area | Gap | Severity | Fix Effort | Priority |
|---|------|-----|----------|-----------|----------|
| 1 | **Backend** | `audit_service.py` imports `DecisionTreeLog` and `InferenceLog` from `app.db.models`, but `models.py` defines `DecisionTree` and `Inference`. **Runtime crash** on any audit service call. | **Critical** | 1–2 h | P0 |
| 2 | **Backend** | `audit_service.py` references agreement verdict `"physician_override"` which does not exist in the `AgreementVerdict` enum (`models.py`). | **Critical** | 30 min | P0 |
| 3 | **Backend** | Inference endpoint is `/api/v1/inference/predict`, but AGENTS.md documents `/inference/analyze`. Frontend `api.ts` calls `/inference/analyze`. **Three different paths exist.** | **Critical** | 1–2 h | P0 |
| 4 | **Backend** | `verify_admin_key` dependency checks `settings.admin_api_key`, but `Settings` class in `config.py` has **no such field**. All audit endpoints (`/trail`, `/anomalies`) return **403** unconditionally. | **Critical** | 30 min | P0 |
| 5 | **Backend** | `inference_service.py` raises generic `ValueError` when PII is detected in DICOM; should raise `AnonymizationError` (registered handler in `main.py` exists but is never triggered). | **High** | 30 min | P1 |
| 6 | **Backend** | `inference_service.py` hardcodes `model_version="v0.3.2"` and `model_sha="abc123d"` instead of reading from `Settings`. | **High** | 30 min | P1 |
| 7 | **Backend** | `dicom_service.py` (with HU conversion, windowing, CV2 resize) is fully implemented but **never used** by `inference_service.py`, which does its own inferior preprocessing (PIL resize, no HU, no windowing). | **High** | 2–4 h | P1 |
| 8 | **Backend** | `xai_service.py` (`XAIService` class with proper overlay blending) is implemented but **never instantiated**; `inference_service.py` calls raw `generate_gradcam_heatmap()` directly. | **High** | 1–2 h | P1 |
| 9 | **Backend** | Rate limiting is only applied to `/inference/predict` (30/min). `/decision-tree/capture`, `/audit/trail`, `/audit/anomalies`, `/decision-tree/recent` have **no rate limits**. | **High** | 1–2 h | P1 |
| 10 | **Backend** | `DecisionTreeService.capture()` writes raw PII-containing payload to local filesystem (`memory/decisions/`) **before** PII check. If PII is detected, the file is already persisted. | **High** | 1–2 h | P1 |
| 11 | **Backend** | `audit_service.py` is fully implemented but **never registered** in any API route. Audit endpoints use `DecisionTreeService` instead. | **High** | 2–4 h | P1 |
| 12 | **Frontend** | Two competing API clients exist: `services/api.ts` (uses `/inference/analyze`) and `lib/apiClient.ts` (uses `/api/v1/inference/predict`). Different endpoints, different types. | **Critical** | 2–4 h | P0 |
| 13 | **Frontend** | Two competing `AIPanel` components: `components/AIPanel.tsx` (full-featured with DecisionTreeForm) and `components/AiPanel/AiPanel.tsx` (simpler). `App.tsx` imports the simpler one, hiding the decision-tree capture flow. | **High** | 2–4 h | P1 |
| 14 | **Frontend** | `App.tsx` has no file upload→backend inference integration. The DICOM viewer renders locally, but there is no "Analyze" button that sends the file to `/inference/predict`. | **High** | 4–8 h | P1 |
| 15 | **Frontend** | No routing library (react-router). Missing pages: Login/Auth, Settings, Case History, Admin Dashboard. Single-page app is hardcoded to one layout only. | **High** | 8–16 h | P2 |
| 16 | **Frontend** | `package.json` has **no `"test"` script**. CI (`ci.yml`) references `npm test -- --run` which will fail. Vitest is not installed. | **High** | 2–4 h | P1 |
| 17 | **Frontend** | `types/api.ts` and `types/index.ts` have divergent interfaces (e.g. `AgreementVerdict` omits `"physician_override"` in `api.ts`; `PhysicianDecision.confidence_self_reported` type differs). | **Medium** | 1–2 h | P2 |
| 18 | **ML** | `onnx_export.py` calls `MFSDUNet(pretrained_swin=False)`, but `MFSDUNet.__init__` has **no `pretrained_swin` parameter**. **Export crashes** with `TypeError`. | **Critical** | 30 min | P0 |
| 19 | **ML** | `ml/export_onnx.py` duplicates `ml/inference/onnx_export.py`. Two export scripts with different output names. | **Medium** | 1 h | P2 |
| 20 | **ML** | `ml/training/dataset.py` imports `nibabel` inside `__getitem__` (runtime import on every sample), causing severe I/O overhead. | **Medium** | 30 min | P2 |
| 21 | **ML** | No training config YAML template exists in the repo. `train.py` requires `--config <yaml>` but no example is provided. | **Medium** | 1–2 h | P2 |
| 22 | **ML** | `ml/data/dataset.py` (MONAI-based) and `ml/training/dataset.py` (torch.utils.data.Dataset) are two different dataset implementations with incompatible interfaces. | **Medium** | 2–4 h | P2 |
| 23 | **DevOps** | `docker-compose.yml` exposes frontend on port `3000`, but the Dockerfile builds nginx on port `80`. Port mapping `3000:80` is missing; container will be unreachable. | **Critical** | 30 min | P0 |
| 24 | **DevOps** | `docker-compose.yml` mounts `../scripts/anonymize.py` into the backend container, but `anonymization_service.py` resolves the script via `Path(__file__).resolve().parents[4]`, which breaks inside the container filesystem layout. | **High** | 1–2 h | P1 |
| 25 | **DevOps** | No healthcheck defined for `hermes` and `frontend` services in docker-compose. | **Medium** | 1 h | P2 |
| 26 | **DevOps** | `nginx.conf` proxies `/api/` to `backend:8000`, but inside the Docker network the backend service name is `backend` (correct). However, no `X-Forwarded-Proto` or HTTPS redirect config exists. | **Medium** | 1–2 h | P2 |
| 27 | **Security** | No API key rotation mechanism. Single static key in `.env` with no expiry, no multi-key support, no key derivation. | **High** | 4–8 h | P1 |
| 28 | **Security** | DICOM file size limit is missing. `UploadFile` reads entire file into memory with `await file.read()`. Large DICOMs (3D CTA = 500 MB+) will OOM. | **High** | 1–2 h | P1 |
| 29 | **Security** | No content-type validation on DICOM upload. Client can send any file type. | **Medium** | 30 min | P2 |
| 30 | **Security** | `CORS_ORIGINS` is a raw comma-separated string split at runtime with no URL validation. Malformed origins could break CORS parsing. | **Low** | 30 min | P3 |
| 31 | **Security** | `AnonymizationService` in backend uses `DICOM_PII_TAGS_BASIC` from `scripts/anonymize.py`, but `dicom_service.py` defines its own `_PII_TAGS` frozenset. The two lists are **different** (33 vs 30 tags, different formats). | **High** | 1–2 h | P1 |
| 32 | **Compliance** | `DecisionTreeService.capture()` writes to `memory/decisions/` on disk, but there is no retention policy, encryption-at-rest, or access control on this directory. | **High** | 2–4 h | P1 |
| 33 | **Compliance** | `AuditEvent` table is append-only (tested), but `Inference` and `DecisionTree` tables allow UPDATE/DELETE with no SQLAlchemy event listeners. | **Medium** | 1–2 h | P2 |
| 34 | **Compliance** | `test_anonymization_bridge.py` asserts `response.status_code == 200` for a DICOM with PII, because the test uses a mock inference service. **The real anonymization rejection path is not tested end-to-end.** | **High** | 2–4 h | P1 |
| 35 | **Documentation** | No `README.md` in `code/` root. No API usage guide. No deployment runbook for production (TLS, backup, monitoring). | **Medium** | 4–8 h | P2 |
| 36 | **Documentation** | `ml/training/` has no README explaining config YAML schema, expected data directory layout, or how to run on GPU vs CPU. | **Low** | 1–2 h | P3 |
| 37 | **Tests** | `test_audit_trail.py` tests append-only immutability, but `test_inference_creates_audit` only asserts `status_code == 200`; it does **not** verify an `AuditEvent` row was actually inserted. | **Medium** | 1–2 h | P2 |
| 38 | **Tests** | No frontend tests exist (`.test.tsx`, `.spec.ts`). `test_DicomViewer.tsx` is empty/placeholder. | **High** | 8–16 h | P2 |
| 39 | **Tests** | `test_smoke.py` has a comment: "Mock accepts anything; in production this would be 400/422 for bad DICOM". The bad-DICOM path is **not tested**. | **Medium** | 1–2 h | P2 |
| 40 | **Backend** | `app/core/logging.py` references `settings.env`, but `Settings` has no `env` field. This will raise `AttributeError` when `configure_logging()` is called. | **Critical** | 30 min | P0 |
| 41 | **Backend** | `pytest.ini` references `backend/tests` and `ml` in `testpaths`, but `backend/tests/` directory does **not exist** (tests are in `code/tests/`). This causes pytest collection warnings. | **Medium** | 30 min | P2 |
| 42 | **Backend** | `pydicom.dcmread` in `inference_service.py` is called without `force=True`, so malformed DICOM headers will raise exceptions that are not caught and transformed into HTTP 422. | **Medium** | 1 h | P2 |
| 43 | **Frontend** | `cornerstoneSetup.ts` configures `maxWebWorkers: 1` which will bottleneck large DICOM loading. No error handling if WASM initialization fails. | **Low** | 1–2 h | P3 |
| 44 | **Frontend** | `HeatmapOverlay.tsx` expects `heatmap: number[][]` but the backend returns `heatmap_b64: string`. Type mismatch between frontend and backend. | **Medium** | 1 h | P2 |
| 45 | **Frontend** | `AIPanel.tsx` (the full one) hardcodes `physician_role_hash: "placeholder-hash"` in the decision tree payload. This will fail backend validation (`pattern=r"^[a-f0-9]{64}$"`). | **High** | 1–2 h | P1 |
| 46 | **ML** | `MFSDUNet` outputs `deciding_feature` logits (12 classes), but no label map / class names are defined anywhere in the repo. The feature head is untrainable without a label mapping. | **Medium** | 2–4 h | P2 |
| 47 | **ML** | `CarotisCompositeLoss` uses `nn.CrossEntropyLoss` for `deciding_feature`, but the model output is raw logits and the target in `_prepare_batch` is `deciding_feature_label`. No verification that label indices are in `[0, 11]`. | **Medium** | 1–2 h | P2 |
| 48 | **DevOps** | `docker-compose.yml` `hermes` service has no `healthcheck`, so `depends_on` with `condition: service_healthy` for backend is irrelevant (backend depends on ollama, not hermes). But hermes could fail silently. | **Low** | 30 min | P3 |
| 49 | **DevOps** | Backend Dockerfile runs `uvicorn` with `--workers 2`, but `InferenceService` loads an ONNX model at startup. With 2 workers, the model is loaded **twice** into memory (no shared memory). | **Medium** | 2–4 h | P2 |
| 50 | **Security** | `anonymization_service.py` dynamically executes `scripts/anonymize.py` via `exec_module`. If that script is tampered with, arbitrary code runs in the backend context. | **High** | 2–4 h | P1 |

---

## Top 10 Most Critical Gaps (Fix Immediately)

### 1. CRITICAL: Audit Service References Non-Existent Models
- **File:** `code/backend/app/services/audit_service.py:15`
- **Impact:** Backend crashes with `ImportError` if any code path touches `AuditService`.
- **Fix:** Rename imports to `DecisionTree` and `Inference`, or rename models to `DecisionTreeLog` / `InferenceLog` consistently across the codebase.

### 2. CRITICAL: Admin Key Missing from Config
- **File:** `code/backend/app/core/config.py`, `code/backend/app/api/dependencies.py:16`
- **Impact:** Every audit endpoint returns 403. Audit trail is inaccessible.
- **Fix:** Add `admin_api_key: str | None = None` to `Settings` with minimum length validator.

### 3. CRITICAL: API Path Chaos (Three Versions of Same Endpoint)
- **Files:** `code/backend/app/api/routes/inference.py`, `code/frontend/src/services/api.ts`, `code/frontend/src/lib/apiClient.ts`, `code/backend/app/main.py:97`
- **Impact:** Frontend cannot communicate with backend reliably. `/inference/analyze` (frontend) ≠ `/api/v1/inference/predict` (backend).
- **Fix:** Unify to one path. Update `AGENTS.md`, all frontend clients, and all tests. Recommend `/api/v1/inference/analyze`.

### 4. CRITICAL: ONNX Export Runtime Crash
- **File:** `code/ml/inference/onnx_export.py:25`
- **Impact:** Cannot export trained models to ONNX. Pipeline is broken.
- **Fix:** Remove `pretrained_swin=False` argument from `MFSDUNet()` call.

### 5. CRITICAL: Docker Compose Port Mismatch (Frontend)
- **File:** `code/docker-compose.yml:62`, `code/frontend/Dockerfile:18`
- **Impact:** Frontend container is unreachable. Compose maps 3000, nginx listens on 80.
- **Fix:** Change compose to `3000:80` or switch Dockerfile to expose 3000 with a dev server (not recommended for prod).

### 6. CRITICAL: Logging Config References Missing Field
- **File:** `code/backend/app/core/logging.py:20`
- **Impact:** `configure_logging()` raises `AttributeError` on startup in any environment that calls it.
- **Fix:** Add `env: str = "development"` to `Settings`, or use `settings.debug` instead.

### 7. HIGH: PII Payload Persisted Before Validation
- **File:** `code/backend/app/services/decision_tree_service.py:127`
- **Impact:** If PII is detected in free text, the raw payload has already been written to `memory/decisions/`.
- **Fix:** Move PII check **before** filesystem write. Reorder steps 2 and 4 in `capture()`.

### 8. HIGH: No File Upload Integration in Frontend
- **File:** `code/frontend/src/App.tsx`, `code/frontend/src/components/DicomViewer/DicomViewer.tsx`
- **Impact:** User can load a DICOM into the viewer but cannot send it to the AI for analysis.
- **Fix:** Wire `onFileSelected` in `DicomViewer` to `useInference` mutation, then feed the result into `AIPanel`.

### 9. HIGH: Duplicate API Clients with Divergent Paths
- **Files:** `code/frontend/src/services/api.ts`, `code/frontend/src/lib/apiClient.ts`
- **Impact:** Maintenance nightmare. One client will drift and break.
- **Fix:** Delete one client. Consolidate all API calls into a single typed client.

### 10. HIGH: Arbitrary Code Execution Risk from Dynamic Import
- **File:** `code/backend/app/services/anonymization_service.py:15-19`
- **Impact:** `exec_module` on an external script. If `scripts/anonymize.py` is modified by an attacker, code runs in backend context.
- **Fix:** Inline the tag list into `anonymization_service.py` or read it as JSON/data, not Python code.

---

## Recommended Order of Fixing

### Week 1 — Unblock Runtime (P0)
1. Fix `audit_service.py` model imports (Gap #1).
2. Add `admin_api_key` to `Settings` (Gap #2).
3. Unify all API paths to `/api/v1/inference/analyze` (Gap #3).
4. Fix `onnx_export.py` constructor call (Gap #18).
5. Fix Docker Compose frontend port mapping (Gap #23).
6. Fix `logging.py` `settings.env` reference (Gap #40).

### Week 2 — Security & Data Integrity (P1)
7. Add rate limiting to all non-health endpoints (Gap #9).
8. Fix PII write-before-check in `DecisionTreeService` (Gap #7).
9. Replace dynamic `exec_module` with inline tag list (Gap #50).
10. Add file size limit and content-type validation (Gap #28).
11. Implement API key rotation mechanism or at least multi-key support (Gap #27).
12. Wire `DicomService` and `XAIService` into `InferenceService` (Gaps #7, #8).
13. Fix hardcoded model version/sha (Gap #6).
14. Fix `physician_role_hash` placeholder in frontend (Gap #45).

### Week 3 — Frontend Completeness (P1–P2)
15. Consolidate API clients into one (Gap #12).
16. Unify `AIPanel` components — use the full-featured one in `App.tsx` (Gap #13).
17. Implement upload→analyze→display flow in `App.tsx` (Gap #14).
18. Align `types/api.ts` with `types/index.ts` (Gap #17).
19. Fix `HeatmapOverlay` / `gradcam_b64` type mismatch (Gap #44).

### Week 4 — Testing & DevOps (P2)
20. Add `"test"` script to `package.json` and install Vitest (Gap #16).
21. Write at least one frontend component test for `DecisionForm`.
22. Fix `pytest.ini` testpaths (Gap #41).
23. Add healthchecks to hermes and frontend in compose (Gap #25).
24. Fix nginx proxy headers and add HTTPS redirect guidance (Gap #26).
25. Add backend Dockerfile comment about ONNX model double-loading with `--workers 2` (Gap #49).

### Week 5 — Documentation & ML Polish (P2–P3)
26. Write `code/README.md` with architecture overview and quickstart.
27. Add ML training config YAML template.
28. Document the 12 `deciding_feature` class labels.
29. Add `nibabel` import to module level in `dataset.py`.
30. Write deployment runbook (backup, TLS, monitoring).

---

## Files Requiring Immediate Attention

| File | Issue Count | Action |
|------|-------------|--------|
| `code/backend/app/services/audit_service.py` | 3 | Fix imports, fix enum string, wire into router |
| `code/backend/app/core/config.py` | 2 | Add `admin_api_key`, add `env` |
| `code/backend/app/services/inference_service.py` | 4 | Use config values, use DicomService/XAIService, raise AnonymizationError |
| `code/backend/app/services/decision_tree_service.py` | 1 | Reorder PII check before file write |
| `code/backend/app/api/routes/inference.py` | 1 | Rename `/predict` → `/analyze` |
| `code/backend/app/api/routes/audit.py` | 1 | Add rate limits |
| `code/frontend/src/App.tsx` | 2 | Wire upload→analyze, swap AIPanel |
| `code/frontend/src/services/api.ts` | 2 | Consolidate with apiClient.ts |
| `code/frontend/src/lib/apiClient.ts` | 2 | Consolidate with api.ts |
| `code/ml/inference/onnx_export.py` | 1 | Remove invalid constructor arg |
| `code/docker-compose.yml` | 2 | Fix frontend port, fix anonymize.py mount path |

---

## Positive Findings (Do Not Break)

- ✅ `AuditEvent` SQLAlchemy `before_update` / `before_delete` listeners correctly enforce append-only.
- ✅ `Settings.database_url` validator correctly rejects non-SQLite URLs.
- ✅ `Settings.api_key` enforces ≥32 characters.
- ✅ `DecisionTreeRequest` Pydantic schema has strict regex patterns for `case_id` and `physician_role_hash`.
- ✅ `anonymization_service.py` correctly checks DICOM for PII before inference.
- ✅ `docker-compose.yml` uses non-root user in backend Dockerfile.
- ✅ `DecisionTreeService` performs JSON Schema validation on payloads.
- ✅ CORS is strictly limited to configured origins.
- ✅ Prometheus metrics endpoint exposed at `/metrics`.
- ✅ `pytest.ini` properly configured for async tests.

---

## Appendix: Inconsistency Matrix

| Concept | Backend Route | Frontend (api.ts) | Frontend (apiClient.ts) | AGENTS.md Doc |
|---------|--------------|-------------------|------------------------|---------------|
| Inference | `/api/v1/inference/predict` | `/inference/analyze` | `/api/v1/inference/predict` | `/inference/analyze` |
| Decision Tree | `/api/v1/decision-tree/capture` | `/api/v1/decision-tree/capture` | `/api/v1/decision-tree/capture` | `/decisions` |
| Health | `/health/` | — | `/health` | `/health` |
| Audit Trail | `/api/v1/audit/trail` | — | — | `/audit/trail` |

**Conclusion:** The inference endpoint is the only one with a three-way mismatch. Fixing this is the highest-impact frontend-backend coordination task.
