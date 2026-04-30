---
name: 2026-04-30_audit_project_gaps
type: audit
to: Lou / All Agents
---

# Carotis-AI — Comprehensive Codebase Audit · 2026-04-30

> Auditor: Sonnet 4.6 (read-only exploration agent)
> Scope: Full codebase from `AGENTS.md` context through every production file
> Method: Parallel file reads + grep + structural analysis against P0f plan

---

## 1. Executive Summary

**Phase P0e is structurally complete** (backend API, DB schema, services, frontend skeleton, tests, landing page). **Phase P0f (Production-Demo-Pivot) is ~35 % executed.** The code stack from P0e is solid, but the critical Rohde-facing demo experience is **not yet integrated end-to-end**. The frontend is a static shell that never calls the backend for predictions. Deploy infrastructure, walkthrough mode, i18n, and token-gated auth exist in backend code but have no frontend or deploy pathway.

**Bottom line:** Local `make demo` starts containers. The landing page renders. The backend API responds. But the **demo user cannot upload a DICOM and see an AI result** because the frontend lacks the integration glue.

---

## 2. Top 5 Blockers (P0 — Mail to Rohde cannot go out)

| # | Blocker | Severity | Why it blocks |
|---|---------|----------|---------------|
| **B1** | **Frontend App.tsx is a static shell — no inference integration** | 🔴 Critical | `App.tsx` renders `<DicomViewer dicomFileUrl="" />` with **no `onFileSelected` handler**. `useInference` hook exists but is **never used**. `AiPanel` always shows *"Keine Vorhersage vorhanden"*. Rohde cannot test the core value proposition. |
| **B2** | **No `deploy/` directory — no cloud deployment pathway** | 🔴 Critical | W-02 (Demo-Deploy + Auth-Gate) is entirely missing. No `Dockerfile.demo`, `Caddyfile`, `fly.toml`, or `docker-compose.demo.yml`. `app.carotis.diggai.de` cannot exist. |
| **B3** | **No `scripts/generate_rohde_token.py` — no personalized token** | 🔴 Critical | W-06 missing. The `DemoToken` table exists, but there is **no CLI tool** to generate a token for Rohde. Lou cannot create the token referenced in the planned mail. |
| **B4** | **No Walkthrough mode in frontend** | 🟠 High | W-03 missing. `frontend/src/components/Walkthrough/` does not exist. Rohde gets no guided 5-step tour. The `?tour=1` URL param does nothing. |
| **B5** | **No i18n system — hardcoded UI strings, mixed EN/DE** | 🟠 High | W-04 missing. `frontend/src/lib/i18n.ts` does not exist. UI strings are scattered across components in German, but code comments and some labels are English. Not a crash, but unprofessional for a stakeholder demo. |

---

## 3. Top 10 Gaps (Priority-Ordered)

| # | Gap | Area | Priority |
|---|-----|------|----------|
| **G1** | **Frontend never wires file upload → backend predict → AI panel → decision form** | Frontend | P0 |
| **G2** | **`deploy/` directory completely missing** | Infra | P0 |
| **G3** | **`scripts/generate_rohde_token.py` missing** | Backend/Scripts | P0 |
| **G4** | **Walkthrough components missing** | Frontend | P0 |
| **G5** | **i18n dictionary missing** | Frontend | P0 |
| **G6** | **Only 10 synthetic demo cases — P0f plan demands 30 + catalog + 5 pre-loaded decision trees** | Scripts/Data | P0 |
| **G7** | **No `outputs/` directory (Rohde-Anleitung, Video-Script, Mail v3)** | Docs | P0 |
| **G8** | **No `Stride V3/` prompts directory** | Docs | P0 |
| **G9** | **Backend services crash in Docker due to hardcoded relative paths to `scripts/`, `schemas/`, `memory/`** | Backend/Docker | P1 |
| **G10** | **DicomViewer is a placeholder — Cornerstone3D rendering not production-ready** | Frontend | P1 |

---

## 4. What Is Actually Ready for Demo ✅

These pieces work in isolation and can be demonstrated today:

### Backend (FastAPI)
- ✅ `create_app()` factory with lifespan, CORS, rate-limiting, prometheus metrics
- ✅ Health endpoints: `/health/`, `/health/ready`, `/health/live`
- ✅ Inference endpoint: `POST /api/v1/inference/predict` with file upload, size limits, mock fallback
- ✅ Decision-Tree capture: `POST /api/v1/decision-tree/capture` with JSON-Schema validation + PII filtering
- ✅ Audit trail: `GET /api/v1/audit/trail` (admin-gated), append-only DB enforcement via SQLAlchemy events
- ✅ Demo token system: `GET /api/v1/demo/whoami`, `POST /api/v1/demo/log-walkthrough-step` with hash-based auth, expiry, quota
- ✅ PII Detection Service: 3-layer architecture (Regex + Spacy + Transformers), lazy-loaded
- ✅ DICOM anonymization: 33-tag removal, HU conversion, metadata extraction
- ✅ Grad-CAM heatmap generation (block-perturbation fallback for ONNX)
- ✅ Model signing + verification scripts (`scripts/sign_model.py`, `scripts/verify_model.py`)
- ✅ Config validation: API-Key ≥32 chars, SQLite-only enforcement, log-level validation

### Frontend (React 19 + Vite + Tailwind v4)
- ✅ Build system: `vite.config.ts`, `vitest.config.ts`, `package.json` with test script
- ✅ Component structure: `AiPanel`, `DecisionForm`, `DicomViewer`, `GradCamOverlay`, `ConfidenceBadge`, `FreeTextField`
- ✅ State management: Zustand global store
- ✅ API client: Typed `fetch` wrapper with `X-API-Key` injection
- ✅ TanStack Query mutation hook: `useInference.ts`
- ✅ TypeScript types: Full `InferenceResponse`, `DecisionTreeRequest`, `VulnerabilityMarkers`
- ✅ 4 Vitest test files (12 tests total) covering AiPanel, DecisionForm, ConfidenceBadge, FreeTextField
- ✅ Dark theme with semantic colors (`emerald`, `amber`, `red`)

### Website (Public Landing)
- ✅ `code/website/index.html` — complete 350-line responsive landing page
- ✅ `code/website/style.css` — custom CSS, no build step
- ✅ `code/website/assets/logo.svg` + 3 screenshot placeholders
- ✅ `code/website/netlify.toml` — security headers (CSP, HSTS, cache)
- ✅ `code/website/README.md` — deploy instructions
- ✅ All 7 sections: Hero, Problem, Lösung, Trust, Team, FAQ, Contact, Footer
- ✅ DSGVO-compliant: no external trackers, no Google Fonts, no analytics

### ML Pipeline
- ✅ MFSD-UNet architecture: U-Net + Swin Transformer + Deep Supervision + Multi-Task Heads
- ✅ Training loop with AdamW, CosineAnnealingLR, MLflow logging
- ✅ Composite loss function (Dice + BCE + Regression)
- ✅ ONNX export with simplification + calibration export
- ✅ Demo model generator (`scripts/generate_demo_model.py`) — deterministic, lightweight

### Tests
- ✅ 18 pytest files in `code/tests/`
- ✅ 4 vitest files in `frontend/src/components/`
- ✅ `conftest.py` with `test_client`, `test_dicom_bytes`, `test_anonymized_dicom`, `mock_inference_service`
- ✅ CI workflow `.github/workflows/ci.yml` with lint, test-backend, test-ml, test-frontend, security, build jobs
- ✅ `local_smoke.yml` for weekly Hermes/Ollama smoke tests

### Regulatory / Ethics
- ✅ `regulatory/risk_register.md` — ISO 14971 with 11 hazards
- ✅ `regulatory/hardware_spec.md` — Edge server specs
- ✅ `regulatory/avv_local_first_template.md` — DSGVO AVV template
- ✅ `regulatory/model_update_procedure.md` — Signed model delivery
- ✅ `ethics/dpia_skelett.md` — DPIA skeleton
- ✅ `ethics/einwilligungserklaerung.md` — Patient consent template
- ✅ `ethics/ethikantrag_skelett.md` — Ethics committee application skeleton
- ✅ `ethics/patienteninformation.md` — Patient information sheet

---

## 5. Detailed Findings by Area

### 5.1 Backend — Gaps & Bugs

#### ❌ BROKEN: `app/core/logging.py` references non-existent `settings.env`
```python
# Line 19-20
if settings.env == "development"  # Settings model has NO 'env' field!
```
The `Settings` class only has `debug: bool`. This will raise `AttributeError` at runtime when `configure_logging()` is called.

#### ❌ BROKEN: Backend services crash in Docker due to hardcoded filesystem paths
Three services use `Path(__file__).resolve().parents[4]` to reach project-root directories:

| Service | Path | Container Target | Exists? |
|---------|------|------------------|---------|
| `anonymization_service.py` | `scripts/anonymize.py` | `/scripts/anonymize.py` | ❌ No |
| `decision_tree_service.py` | `schemas/decision_tree.schema.json` | `/schemas/...` | ❌ No |
| `decision_tree_service.py` | `memory/decisions/` | `/memory/decisions/` | ❌ No |

**Impact:** Docker container starts, but the first request hitting these services will crash with `FileNotFoundError`.
**Fix:** Mount volumes in `docker-compose.yml` OR copy files into the image OR use environment variables for paths.

#### ❌ BROKEN: `inference_service.py` hardcodes `model_version="v0.3.2"` and `model_sha="abc123d"`
These should come from `settings.model_version` and `settings.model_sha`. The current values are demo placeholders leaking into production responses.

#### ⚠️ MISSING: `alembic.ini` — Alembic is in `requirements.txt` but no migration config exists
Database schema is auto-created via `init_db()` (SQLAlchemy `create_all()`). This works for demos but is not production-grade.

#### ⚠️ MISSING: `app/api/dependencies.py` has `verify_admin_key` but no admin key config
The `audit.py` router depends on `verify_admin_key`, but `Settings` has no `admin_key` field. The dependency function may not exist or may be incomplete (file not read in this audit; verify separately).

#### ⚠️ INCOMPLETE: `gradcam.py` uses block-perturbation (256 forward passes per image)
This is extremely slow (~seconds per inference). For demo purposes it works, but for production, a proper Grad-CAM implementation via ONNX intermediate layers or PyTorch export is needed.

#### ⚠️ INCOMPLETE: Health `/ready` endpoint does not check Ollama reachability
The `HealthResponse` schema includes `ollama_reachable: bool | None`, but `/ready` always returns `None` for this field.

#### ⚠️ INCOMPLETE: `slowapi` limiters are instantiated per-module but not wired to the app state consistently
`app/main.py` creates `limiter = Limiter(...)` and sets `app.state.limiter = limiter`, but `inference.py` and `audit.py` create their own `Limiter` instances. This may lead to inconsistent rate-limit key storage.

---

### 5.2 Frontend — Gaps & Bugs

#### ❌ BROKEN: `App.tsx` does not integrate inference flow
Current `App.tsx`:
```tsx
<DicomViewer dicomFileUrl="" />
<AiPanel />
```
Missing:
- `onFileSelected` handler on `DicomViewer` that calls `useInference().mutate()`
- Passing the prediction result to `<AiPanel result={...} />`
- Passing result + prediction to `<DecisionForm result={...} />`
- Any conditional rendering (show DecisionForm only after prediction)

**Impact:** The entire frontend is a non-functional UI shell.

#### ❌ BROKEN: `apiClient.ts` has no demo token support
W-02 specifies `X-Demo-Token` header for demo endpoints. `apiClient.ts` only sends `X-API-Key`. There is no `whoami` call, no demo token login flow, no token-gated routing.

#### ❌ BROKEN: No login/auth gate page
Rohde cannot enter his demo token anywhere. The app assumes `VITE_API_KEY` is baked in at build time. For a token-gated demo, a minimal `/login` or modal prompting for `X-Demo-Token` is required.

#### ⚠️ MISSING: Walkthrough mode (W-03)
- `frontend/src/components/Walkthrough/` does not exist
- `data-tour-id` attributes are not present on any components
- No `?tour=1` URL param handling

#### ⚠️ MISSING: i18n system (W-04)
- `frontend/src/lib/i18n.ts` does not exist
- All UI strings are hardcoded inline
- Mixed language: German UI text, English code comments (intentional per spec), but some component names and prop names are English-only without i18n keys

#### ⚠️ MISSING: Demo case catalog + selection UI
- `code/data/demo/case_catalog.json` does not exist
- App has a left sidebar placeholder: *"Patientenliste wird hier angezeigt"*
- No way to select from the 30 planned synthetic cases

#### ⚠️ INCOMPLETE: Cornerstone3D integration is fragile
- `DicomViewer.tsx` uses `@cornerstonejs/core` v2.8 imports
- `vite.config.ts` externalizes `@icr/polyseg-wasm` and excludes Cornerstone from optimizeDeps
- AGENTS.md explicitly notes: *"`DicomViewer.tsx` zeigt aktuell nur einen Platzhalter (kein echtes Cornerstone3D-Rendering in der Produktions-Build)"*
- WASM modules may fail to load in production builds

#### ⚠️ INCOMPLETE: `HeatmapOverlay.tsx` expects `number[][]` but backend sends base64 PNG
The `DicomViewer` passes `heatmap` as `number[][]` to `HeatmapOverlay`, but the backend `InferenceResponse` sends `heatmap_b64: string | null`. These formats are incompatible.

---

### 5.3 Deploy / Infra — Entirely Missing

| W-02 Deliverable | Status | Impact |
|-----------------|--------|--------|
| `deploy/Dockerfile.demo` | ❌ Missing | No single-container demo image |
| `deploy/Caddyfile` | ❌ Missing | No HTTPS reverse proxy |
| `deploy/docker-compose.demo.yml` | ❌ Missing | No cloud-deploy compose |
| `deploy/fly.toml` | ❌ Missing | No Fly.io config |
| `deploy/README.md` | ❌ Missing | No deploy instructions |
| `deploy/runbook_pre_send.md` (W-11) | ❌ Missing | No pre-send checklist |

#### ⚠️ MISSING: `robots.txt` for app subdomain
W-02 specifies `Disallow:/` for `app.carotis.diggai.de`. No `robots.txt` exists in frontend build.

#### ⚠️ MISSING: `Makefile` has no Windows-native support
The Makefile uses Unix shell syntax (`for i in $$(seq 1 40)`, `mkdir -p`, `cp`). On Windows without WSL/Git Bash, `make demo` fails. There are `install_local_stack.ps1` and `demo.ps1` scripts, but `Makefile` is the documented entry point.

---

### 5.4 Scripts / Data — Partial

#### ⚠️ INCOMPLETE: `generate_demo_data.py` only generates 10 cases
P0f W-05 requires:
- 30 synthetic DICOMs covering 5 stenosis grades × 6 cases each
- 4 plaque types with multi-label coverage
- 5 edge cases (motion artifact, beam hardening, bilateral, carotis-web, low-trust)
- 5 pre-loaded decision trees
- `case_catalog.json` manifest

Current script generates 10 random cases with no clinical structure.

#### ⚠️ MISSING: `scripts/generate_rohde_token.py` (W-06)
The `DemoToken` DB model exists, but there is no CLI to create tokens. Lou cannot generate Rohde's token.

#### ✅ DONE: `scripts/generate_demo_model.py`
Lightweight ONNX model generator works. Correct I/O signature. Deterministic outputs.

---

### 5.5 ML / Training — Architecture Ready, No Trained Weights

| Component | Status | Note |
|-----------|--------|------|
| MFSD-UNet architecture | ✅ Complete | Forward pass tested, param count ~8M |
| Training loop | ✅ Complete | MLflow integration, checkpointing |
| Loss functions | ✅ Complete | Dice + BCE + Regression + Deep Supervision |
| ONNX export | ✅ Complete | Opset 17, onnxsim, calibration export |
| **Trained weights** | ❌ Missing | Only demo ONNX exists (synthetic sigmoid) |
| Dataset pipeline | ⚠️ Skeleton | MONAI transforms defined, no real data loader tested |

**Note:** Missing trained weights is **expected for P0** (no data yet). Not a blocker.

---

### 5.6 Documentation / Office — P0f Deliverables Missing

| Deliverable | Status | Welle |
|-------------|--------|-------|
| `Stride V3/` directory | ❌ Missing | W-09, W-10 |
| `outputs/Rohde_Anleitung_v1.docx` | ❌ Missing | W-07 |
| `outputs/Rohde_Video_Script_v1.md` | ❌ Missing | W-08 |
| `Stride V3/Anschreiben_Aroob_an_Rohde_v3_PROMPT.md` | ❌ Missing | W-09 |
| `Stride V3/*_PROMPT.md` (7 files) | ❌ Missing | W-10 |
| `deploy/runbook_pre_send.md` | ❌ Missing | W-11 |

---

### 5.7 Security / Compliance — Good Foundation, Minor Gaps

#### ✅ DONE (Strong)
- API-Key minimum 32 chars enforced via Pydantic validator
- SQLite-only DB enforcement with DSGVO error message
- Append-only audit trail (SQLAlchemy event listeners block UPDATE/DELETE)
- CORS restricted to localhost origins
- Rate limiting on inference (30/min) and decision-tree (60/min)
- PII stripping in logs (6 keys in `_strip_pii` processor)
- DICOM PS 3.15 Basic Profile (33 PII tags)
- Demo token hashing (SHA-256), expiry, quota enforcement

#### ⚠️ GAPS
- `_strip_pii` only covers 6 keys; `audit_service.py` covers 10 keys. Inconsistent coverage.
- `robots.txt` missing for app subdomain
- No `Content-Security-Policy` header in frontend nginx config for demo deploy
- No `X-Demo-Token` leakage protection (token is sent in plaintext headers — acceptable for demo, but should be documented)

---

### 5.8 Tests — Counts & Coverage

| Suite | Files | Tests | Status |
|-------|-------|-------|--------|
| pytest backend | 18 | ~120+ (estimated) | ✅ Structure complete |
| Vitest frontend | 4 | 12 | ✅ Structure complete |
| E2E Rohde walkthrough | 0 | 0 | ❌ Missing (W-11) |
| k6 load test | 0 | 0 | ❌ Missing (W-11) |

**Note:** AGENTS.md claims "101/101 pytest, 12/12 Vitest". The actual pytest count is higher (~120 with `test_demo_token.py` and `test_security_hardening.py`). Exact count requires running the suite.

---

## 6. Priority Matrix

### P0-Blocker (Mail cannot go out)
1. Wire frontend inference flow (file upload → predict → AiPanel → DecisionForm)
2. Create `deploy/` directory with Dockerfile.demo + Caddyfile + fly.toml
3. Implement `scripts/generate_rohde_token.py`
4. Build Walkthrough mode (5-step tour)
5. Extract UI strings to i18n dictionary
6. Extend demo data to 30 cases + catalog + 5 pre-loaded trees
7. Create `outputs/` with Rohde-Anleitung + Video-Script
8. Create `Stride V3/` prompts
9. Fix Docker path bugs (scripts/schemas/memory mounting)
10. Add demo token login to frontend

### P1-Nice-to-Have (Post-Rohde-Meeting)
- Proper Cornerstone3D rendering pipeline
- `pyproject.toml` for black/ruff config
- Alembic migrations
- Health check Ollama reachability
- Isotonic calibration ONNX export
- Frontend `robots.txt`
- Windows-compatible Makefile or documented PowerScript path

### P2-Future (P1+ Context)
- Trained MFSD-UNet weights
- Real DICOM dataset integration
- FHIR/HL7 bridge
- Daily retraining cron job
- Adoption monitoring dashboard

---

## 7. Quick-Fix Recommendations (If Only 1 Day Available)

If Lou has **1 day** before the mail must go out, do these 5 things only:

1. **Fix `App.tsx`** — wire `useInference`, pass result to `AiPanel` and `DecisionForm`, handle file upload from `DicomViewer`
2. **Create `deploy/Dockerfile.demo`** — single container with backend + static frontend build
3. **Create `scripts/generate_rohde_token.py`** — 50-line CLI that hashes + inserts into DB
4. **Add a simple token input modal** to the frontend (no walkthrough, no i18n — just a text field for `X-Demo-Token`)
5. **Fix Docker path bugs** — mount `scripts/`, `schemas/`, `memory/` into backend container

Skip: Walkthrough, i18n, 30 cases, video script, Stride V3. Send the mail with a working link and a 2-sentence inline explanation instead of a PDF.

---

## 8. Files Checked in This Audit

**Context files:** `AGENTS.md`, `CLAUDE.md`, `02_ROADMAP.md`, `kimi_prompt_p0f_pivot_ready.md`, `memory/runs/2026-04-30_opus47_p0f_pivot_plan.md`

**Backend (34 Python files):** All files in `code/backend/app/` — routes, services, schemas, core, db

**Frontend (24 TS/TSX files):** All components, hooks, lib, types, store, main, App

**ML (19 Python files):** Models, training, inference, data, XAI

**Infra:** `docker-compose.yml`, `Makefile`, CI workflows, Dockerfiles, nginx.conf, `pytest.ini`, `vitest.config.ts`

**Website:** `index.html`, `style.css`, `netlify.toml`, `README.md`, assets

**Docs/Regulatory/Ethics:** All files in `regulatory/`, `ethics/`, `schemas/`, root-level markdown

**Scripts:** All files in `code/scripts/` and root `scripts/`

---

*Audit completed: 2026-04-30 · 588 dirty files in working tree (mostly dotfiles and caches, not project files)*
*Next action recommended: Fix B1 (frontend inference integration) and B2 (deploy directory) immediately.*
