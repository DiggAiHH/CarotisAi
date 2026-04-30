# COPILOT_STATUS_REPORT.md — Carotis-AI Vollständiger Projekt-Status-Report
> Generiert: 2026-04-30 · Modell: GitHub Copilot (Claude Sonnet 4.6) · Modus: Plan/Analyse

---

## 1. REPO-ÜBERSICHT (Top-Level)

| Name | Typ | Zweck | Status | Letzte Änderung |
|------|-----|-------|--------|-----------------|
| `00_INDEX.md` | FILE | Projekt-Einstieg — Szenarien, How-To | COMPLETE | 2026-04-29 |
| `01_HARNESS.md` | FILE | Modell-Routing-Matrix, DoD-Format, Eskalation | COMPLETE | 2026-04-29 |
| `02_ROADMAP.md` | FILE | Phasen P0–P7 (24-Monats-Plan) | COMPLETE | 2026-04-29 |
| `03_PROMPT_TEMPLATES.md` | FILE | 9 Copy-Paste-Prompts für alle Use-Cases | COMPLETE | 2026-04-29 |
| `04_MASTER_PLAN.md` | FILE | Architektur-Diagramm + Stakeholder-Map + Risiken | COMPLETE | 2026-04-29 |
| `05_DECISION_TREE_HARVESTING.md` | FILE | JSON-Schema für ärztliche Entscheidungen | COMPLETE | 2026-04-29 |
| `06_ROHDE_MEETING_KIT.md` | FILE | Meeting-Vorbereitung für Prof. Rohde | COMPLETE | 2026-04-29 |
| `07_OFFICE_AGENT_PROMPTS.md` | FILE | Stride-Prompts A–H für Office-Doc-Updates | COMPLETE | 2026-04-30 |
| `08_RESEARCH_ATTENTION_2020-2026.md` | FILE | Literatur-Inventar (27+ Papers) | COMPLETE | 2026-04-29 |
| `09_COPILOT_PROMPT_SEQUENCE.md` | FILE | GitHub Copilot Prompt-Sequenz | COMPLETE | 2026-04-29 |
| `09b_KIMI_PROMPT_SEQUENCE.md` | FILE | Kimi Prompt-Sequenz mit K-01..K-46 | COMPLETE | 2026-04-30 |
| `09b_KIMI_PROMPT_SEQUENCE.md.bak` | FILE | Backup der Kimi-Sequenz | NEEDS_REVIEW | 2026-04-29 |
| `AGENTS.md` | FILE | Agent-Instructions (Pre-Flight, Hard Rules, Stack, ADRs) | COMPLETE | 2026-04-30 |
| `CLAUDE.md` | FILE | Working Memory v1.4 — People, Stack, Phase-Status | COMPLETE | 2026-04-30 |
| `CV_Laith_Alshdaifat.md` | FILE | Lou's CV als Markdown | COMPLETE | 2026-04-29 |
| `dashboard.html` | FILE | Offline-Kanban-Dashboard mit Session-Stats | COMPLETE | 2026-04-30 |
| `Carotis-AI Diagnostik-Suite.html` | FILE | Marketing-HTML-Seite (Rohde-Meeting) | COMPLETE | 2026-04-29 |
| `kimi_prompt_p0f_pivot_ready.md` | FILE | P0f Production-Demo-Pivot Plan W-01..W-12 | COMPLETE | 2026-04-30 |
| `Mail_Aroob_an_Rohde_DRAFT.txt` | FILE | Mail-Entwurf an Prof. Rohde (Plain-Text) | PARTIAL | 2026-04-29 |
| `MEMORY.md` | FILE | Index aller Langzeit-Memory-Dateien | COMPLETE | 2026-04-30 |
| `PROMPT_1_COPILOT_STATUS_REPORT.md` | FILE | Status-Report-Generator-Prompt | COMPLETE | 2026-04-30 |
| `PROMPT_2_COPILOT_EXECUTION_PLAN.md` | FILE | Execution-Plan-Prompt | COMPLETE | 2026-04-30 |
| `RUNBOOK_TODAY.md` | FILE | Tages-Runbook (Aufgaben-Liste) | PARTIAL | 2026-04-30 |
| `stride_execution_plan.md` | FILE | Stride-V2-Ausführungsplan | COMPLETE | 2026-04-29 |
| `stride_prompt_a_ready.md` .. `stride_prompt_h_ready.md` | FILE × 8 | Fertige Stride-Prompts A–H (Copy-Paste) | COMPLETE | 2026-04-30 |
| `tasks.jsonl` | FILE | Maschinenlesbare Task-Liste (38 Tasks: T-001..T-025 + K-01..K-34) | PARTIAL | 2026-04-30 |
| `Das Carotis-AI System … Plaque-Analyse.md` | FILE | Fachpaper-Entwurf | COMPLETE | 2026-04-29 |
| `Regulatorischer Rahmen … DSGVO.md` | FILE | Regulatorik-Übersicht EU AI Act, MDR, DSGVO | COMPLETE | 2026-04-29 |
| `code/` | DIR | Vollständiger Code-Stack (Backend, Frontend, ML, Hermes) | PARTIAL | 2026-04-30 |
| `data/` | DIR | Demo-Daten-Root (delegiert nach code/data/) | NEEDS_REVIEW | 2026-04-29 |
| `deploy/` | DIR | Production-Deployment-Config (Caddy, Docker, Fly.io) | COMPLETE | 2026-04-30 |
| `ethics/` | DIR | Ethikantrag, DPIA, Einwilligungserklärung | PARTIAL | 2026-04-29 |
| `memory/` | DIR | Run-Logs, Anomalien, Entscheidungen, Domänenwissen | COMPLETE | 2026-04-30 |
| `regulatory/` | DIR | ADRs, Risk-Register, AVV, Hardware-Spec | COMPLETE | 2026-04-30 |
| `schemas/` | DIR | JSON-Schema + Sample für Decision-Tree v0.3 | COMPLETE | 2026-04-30 |
| `scripts/` | DIR | Root-Level Skripte (anonymize, preflight, validate) | COMPLETE | 2026-04-30 |

---

## 2. BACKEND-STATUS (`code/backend/`)

### 2.1 Struktur-Tree

```
backend/
├── main.py                          # Dev-Entrypoint: uvicorn.run("main:app", reload=True) [8 lines]
├── requirements.txt                 # 18 Produktion + Dev-Deps
├── Dockerfile                       # python:3.11-slim, Non-Root carotis
├── .env.example                     # Vorlage für Umgebungsvariablen
├── alembic/                         # DB-Migration (vorhanden)
└── app/
    ├── main.py                      # create_app() Factory — Docker + Tests [~170 lines]
    ├── __init__.py
    ├── api/
    │   ├── dependencies.py          # verify_api_key, verify_admin_key
    │   ├── __init__.py
    │   └── routes/
    │       ├── health.py            # GET /health/, /ready, /live
    │       ├── inference.py         # POST /api/v1/inference/predict
    │       ├── decision_tree.py     # POST/GET /api/v1/decision-tree/*
    │       ├── audit.py             # GET /api/v1/audit/*
    │       ├── demo.py              # GET/POST /api/v1/demo/*
    │       └── __init__.py
    ├── core/
    │   ├── config.py                # pydantic-settings, 30 Felder, API-Key ≥32 chars Validator
    │   ├── security.py              # X-API-Key Header-Auth + verify_demo_token
    │   ├── logging.py               # structlog JSON/Console + get_logger()
    │   ├── exceptions.py            # AnonymizationError, ModelNotLoadedError, SchemaValidationError
    │   ├── error_handlers.py        # Globale Exception-Handler-Registrierung
    │   └── __init__.py
    ├── db/
    │   ├── database.py              # SQLAlchemy 2.0 async + get_engine() @lru_cache + append-only AuditEvent-Listener
    │   ├── models.py                # Inference, DecisionTree, AuditEvent, DemoToken
    │   └── __init__.py
    ├── schemas/
    │   ├── inference.py             # PredictionResponse, HealthResponse, DecisionTreeRequest
    │   ├── decision_tree.py         # DecisionTreeCreate, DecisionTreeResponse
    │   ├── audit.py                 # AuditPage, AuditEventEntry, DisagreementSummary
    │   └── __init__.py
    └── services/
        ├── anonymization_service.py         # SHA-256-Hash-Anonymisierung
        ├── audit_service.py                 # Append-only Audit-Trail + PII-Strip
        ├── confidence_calibration_service.py # Platt/Isotonic Calibration
        ├── decision_tree_service.py         # Capture + PII-Check + Disagreement-Detection
        ├── dicom_service.py                 # DICOM-Parsing + 33 PII-Tags Entfernung
        ├── gradcam.py                       # Grad-CAM-Heatmap-Generierung
        ├── inference_service.py             # ONNX-Runtime-Inferenz + Grad-CAM + Kalibrierung
        ├── pii_detection_service.py         # Regex + SpaCy DE-NER Ensemble
        ├── transformers_pii_layer.py        # OpenMed-ClinicalLongformer Layer (optional)
        ├── xai_service.py                   # XAI-Postprocessing
        └── __init__.py
```

### 2.2 Status-Karten

```yaml
file: app/core/config.py
purpose: pydantic-settings, 30 Felder, API-Key ≥32-Zeichen-Validator, SQLite-Enforcement
status: COMPLETE
lines: ~85
todo_count: 0
test_coverage: YES  # test_config.py

file: app/core/security.py
purpose: X-API-Key Header-Auth (APIKeyHeader), verify_demo_token mit Quota-Prüfung
status: COMPLETE
lines: ~75
todo_count: 0
test_coverage: YES  # test_security_hardening.py, test_demo_token.py

file: app/db/models.py
purpose: SQLAlchemy 2.0 Mapped-Klassen — Inference, DecisionTree, AuditEvent, DemoToken
status: COMPLETE
lines: ~150
issues:
  - DecisionTree.case_id hat unique=True → nur ein DT pro Case-ID möglich (gewollt)
todo_count: 0
test_coverage: YES  # test_audit_trail.py, test_decision_tree_validation.py

file: app/db/database.py
purpose: Lazy async engine via @lru_cache, append-only AuditEvent-Listener, init_db()
status: COMPLETE
lines: ~70
todo_count: 0
test_coverage: YES  # test_audit_trail.py, test_smoke.py

file: app/services/inference_service.py
purpose: ONNX-Runtime-Inferenz, DICOM-Anonymisierung, Grad-CAM, Calibration, Audit-Event
status: COMPLETE
lines: ~120
issues:
  - fallback_demo=True Modus liefert Zufalls-Daten (korrekt für Demo-Betrieb)
todo_count: 0
test_coverage: YES  # test_inference_full.py

file: app/services/decision_tree_service.py
purpose: Capture mit PII-Check, Disagreement-Erkennung, Memory-Dump nach memory/decisions/
status: COMPLETE
lines: ~200
issues:
  - Memory-Dump schreibt JSON nach memory/decisions/ — in Docker-Container als Volume gemounted
todo_count: 0
test_coverage: YES  # test_decision_tree_validation.py, test_decision_tree_override.py

file: app/services/audit_service.py
purpose: Append-only Audit-Trail, PII-Strip aus Payloads (10 bekannte PII-Keys)
status: COMPLETE
lines: ~120
todo_count: 0
test_coverage: YES  # test_audit_service.py, test_audit_trail.py

file: app/services/pii_detection_service.py
purpose: Regex + SpaCy DE-NER Ensemble, lazy-load, PIISpan DataClass
status: COMPLETE
lines: ~150
todo_count: 0
test_coverage: YES  # test_pii_detection.py (16 Tests)

file: app/services/confidence_calibration_service.py
purpose: Platt/Isotonic Calibration + TrustScoreService (Composite-Metrik)
status: COMPLETE
lines: ~100
todo_count: 0
test_coverage: YES  # test_confidence_calibration.py (12 Tests)

file: app/services/transformers_pii_layer.py
purpose: Optional OpenMed-ClinicalLongformer für deutsche klinische NER, lazy-load
status: COMPLETE
lines: ~120
issues:
  - Benötigt transformers + torch → separates Download-Skript (scripts/download_pii_model.py)
  - Deaktiviert via config: transformers_pii_enabled=false (Default)
todo_count: 0
test_coverage: YES  # test_transformers_pii_layer.py (17 Tests)

file: app/api/routes/demo.py
purpose: Demo-Token-Validierung, /whoami, /log-walkthrough-step (Walkthrough-Tracking)
status: COMPLETE
lines: ~75
todo_count: 0
test_coverage: YES  # test_demo_token.py

file: app/main.py
purpose: create_app() Factory mit CORS, Limiter, Exception-Handlers, Router-Registration
status: COMPLETE
lines: ~175
todo_count: 0
test_coverage: YES  # test_smoke.py
```

### 2.3 API-Endpunkte-Inventory

```
GET    /health/                        → health.py         → PUBLIC
GET    /health/ready                   → health.py         → PUBLIC
GET    /health/live                    → health.py         → PUBLIC
GET    /metrics                        → Prometheus        → PUBLIC (instrumentator auto-exposed)

POST   /api/v1/inference/predict       → inference.py      → AUTH(X-API-Key) + RATE-LIMIT(30/min)
POST   /api/v1/decision-tree/capture   → decision_tree.py  → AUTH(X-API-Key)
POST   /api/v1/decision-tree/check-text→ decision_tree.py  → AUTH(X-API-Key)
GET    /api/v1/decision-tree/recent    → decision_tree.py  → AUTH(X-API-Key)
GET    /api/v1/audit/trail             → audit.py          → AUTH(X-API-Key) + AUTH(X-Admin-Key) + RATE-LIMIT(30/min)
GET    /api/v1/audit/anomalies         → audit.py          → AUTH(X-API-Key) + AUTH(X-Admin-Key) + RATE-LIMIT(10/min)
GET    /api/v1/demo/whoami             → demo.py           → AUTH(X-Demo-Token)
POST   /api/v1/demo/log-walkthrough-step → demo.py         → AUTH(X-Demo-Token)
```

**Fehlende Endpunkte aus der Spec:**
- `GET /api/v1/schemas/decision_tree.schema.json` — Schema-Endpoint nicht implementiert (kein Blocker)
- `POST /api/v1/demo/tokens` — Token-Management-Endpoint für Admin (nicht implementiert, Tokens werden über scripts/generate_rohde_token.py angelegt)
- `GET /api/v1/inference/history` — Verlauf der Inferenzen (nicht implementiert)

### 2.4 Datenbank-Schema

```yaml
Table: inferences
  id: String(36) PRIMARY KEY default=uuid4
  case_id: String(64) INDEX NOT NULL
  captured_at: DateTime(tz) DEFAULT utcnow NOT NULL
  ai_prediction_json: Text NOT NULL
  model_version: String(32) NOT NULL
  model_sha: String(64) NOT NULL
  audit_id: String(36) NOT NULL

Table: decision_trees
  id: String(36) PRIMARY KEY default=uuid4
  case_id: String(64) UNIQUE INDEX NOT NULL  # ⚠️ unique → nur 1 DT pro Case
  captured_at: DateTime(tz) DEFAULT utcnow NOT NULL
  physician_role_hash: String(64) NOT NULL
  data_json: Text NOT NULL  # @validates gegen JSON-Schema v0.3
  agreement_verdict: SQLEnum(AgreementVerdict) NOT NULL  # full_agreement/partial/disagreement

Table: audit_events
  id: String(36) PRIMARY KEY default=uuid4
  timestamp: DateTime(tz) DEFAULT utcnow NOT NULL
  event_type: String(64) NOT NULL
  actor: String(128) NOT NULL
  payload_json: Text NOT NULL
  # APPEND-ONLY: before_update/before_delete → IntegrityError("append-only")

Table: demo_tokens
  token_hash: String(64) PRIMARY KEY  # SHA-256 des rohen Tokens
  label: String(128) NOT NULL
  expires_at: DateTime(tz) NOT NULL
  requests_used: Integer DEFAULT 0 NOT NULL
  max_requests: Integer DEFAULT 100 NOT NULL
  rohde_tag: Boolean DEFAULT False NOT NULL  # Prof. Rohde Demo-Token Markierung
```

**Fehlende Tabellen:** Keine kritischen Lücken.

### 2.5 Offene TODOs im Backend-Code

**Ergebnis: 0 TODO/FIXME/XXX/HACK in allen Backend-Quelldateien.**
(Treffer nur in `.venv/` Third-Party-Paketen — ignoriert.)

### 2.6 Test-Status Backend

- Test-Dateien in `code/tests/`: **17 Dateien** (excl. conftest.py)
- Letzte bekannte Runs: 101/101 pytest grün (Stand K-43..K-46 vom 2026-04-30)

| Test-Datei | Testet | Abdeckung |
|-----------|--------|-----------|
| test_smoke.py | Grundsätzlicher App-Start, Endpoints | Backend-Routes |
| test_audit_service.py | AuditService, PII-Strip, append-only | audit_service.py |
| test_audit_trail.py | AuditEvent append-only DB-Constraint | db/models.py |
| test_anonymization_bridge.py | DICOM-Anonymisierung, PII-Tag-Entfernung | dicom_service.py |
| test_config.py | Pydantic-Settings Validierung | config.py |
| test_confidence_calibration.py | 12 Tests: Platt/Isotonic/TrustScore | confidence_calibration_service.py |
| test_decision_tree_override.py | 6 Tests: CDSiC Override-Reasons | decision_tree_service.py |
| test_decision_tree_validation.py | Schema-Validierung, PII-Check | decision_tree_service.py |
| test_demo_token.py | DemoToken Quota, Expiry, SHA-256 | security.py, demo.py |
| test_gradcam.py | 5 Tests: SegHiResCAM, GradCAM | ml/xai/gradcam.py |
| test_inference_full.py | Vollständiger Inferenz-Flow mit Mock-ONNX | inference_service.py |
| test_ml_pipeline.py | ML-Import-Smoke: MFSD-UNet, Losses | ml/models, ml/training |
| test_model_signing.py | Sign + Verify Bundle-Integrität | scripts/sign_model.py |
| test_pii_detection.py | 16 Tests: Regex, SpaCy-Ensemble | pii_detection_service.py |
| test_security_hardening.py | API-Key, Rate-Limit, Auth-Reject | api/routes, security.py |
| test_transformers_pii_layer.py | 17 Tests: TransformersPIILayer | transformers_pii_layer.py |

**Module ohne Tests:**
- `app/services/xai_service.py` — kein dediziertes Test-File
- `app/services/gradcam.py` — gedeckt indirekt über test_gradcam.py
- `app/core/error_handlers.py` — kein dediziertes Test-File
- `scripts/generate_rohde_token.py`, `scripts/aggregate_free_text.py` — nur Smoke-Tests

---

## 3. FRONTEND-STATUS (`code/frontend/`)

### 3.1 Struktur-Tree

```
src/
├── components/
│   ├── AiPanel/
│   │   ├── AiPanel.tsx              # Stenose %, Konfidenz, Vulnerability, Trust Score
│   │   └── AiPanel.test.tsx         # 3 Tests
│   ├── AuthGate/
│   │   ├── AuthGate.tsx             # Demo-Token Login-Gate
│   │   ├── useDemoToken.ts          # localStorage Token-Persistenz
│   │   └── index.ts
│   ├── ConfidenceBadge.tsx          # 3 Komponenten: Badge, Bar, LowConfidenceWarning
│   ├── ConfidenceBadge.test.tsx     # 3 Tests
│   ├── DecisionForm/
│   │   ├── DecisionForm.tsx         # 30s-Arzt-Entscheidung: Verdict, Stenose, Trust 1-5, Override
│   │   └── DecisionForm.test.tsx    # 2 Tests
│   ├── DicomViewer/
│   │   ├── DicomViewer.tsx          # Cornerstone3D canvas, Drag-Drop, Heatmap-Toggle
│   │   ├── HeatmapOverlay.tsx       # Canvas-basiertes Heatmap (2D-Array/base64)
│   │   └── index.ts
│   ├── FreeTextField.tsx            # Textarea mit PII-Erkennung + localStorage Draft
│   ├── FreeTextField.test.tsx       # 3 Tests
│   ├── GradCamOverlay/
│   │   └── GradCamOverlay.tsx       # <img>-basiertes base64-Overlay
│   └── Walkthrough/
│       ├── Walkthrough.tsx          # 5-Schritt Spotlight-Tour
│       ├── WalkthroughStep.tsx      # Schritt-Karte mit dynamischer Positionierung
│       └── index.ts
├── hooks/
│   └── useInference.ts              # TanStack useMutation → POST /api/v1/inference/predict
├── lib/
│   ├── apiClient.ts                 # Typed fetch-Wrapper, X-API-Key + X-Demo-Token Header
│   ├── cornerstoneSetup.ts          # Cornerstone3D-Init + Tool-Gruppe
│   └── i18n.ts                      # Deutsch Key-Value Dictionary
├── types/
│   └── index.ts                     # API + UI-State Typen
├── App.tsx                          # 3-Spalten-Layout: Header + Sidebar + DicomViewer + AiPanel
├── main.tsx                         # React + TanStack QueryClientProvider Root
├── store.ts                         # Zustand Global-Store (4 Felder)
├── index.css
├── vite-env.d.ts
└── services/
    # (leeres Verzeichnis — Legacy, kann entfernt werden)
```

### 3.2 Komponenten-Status

| Datei | Status | Props | API | data-walkthrough | Tests |
|-------|--------|-------|-----|------------------|-------|
| AiPanel.tsx | COMPLETE | YES | NO | NO | YES (3) |
| AuthGate.tsx | COMPLETE | YES | YES (`/api/v1/demo/whoami`) | NO | NO |
| ConfidenceBadge.tsx | COMPLETE | YES (3) | NO | NO | YES (3) |
| DecisionForm.tsx | COMPLETE | YES | YES (`/api/v1/decision-tree/capture`) | NO | YES (2) |
| DicomViewer.tsx | COMPLETE | YES | NO (File-API lokal) | YES | NO |
| HeatmapOverlay.tsx | COMPLETE | YES | NO | NO | NO |
| FreeTextField.tsx | COMPLETE | YES | YES (`/api/v1/decision-tree/check-text`) | NO | YES (3) |
| GradCamOverlay.tsx | COMPLETE | YES | NO | NO | NO |
| Walkthrough.tsx | COMPLETE | YES | NO | NO (setzt attrs) | NO |
| WalkthroughStep.tsx | COMPLETE | YES | NO | NO | NO |

### 3.3 State-Management-Map

**Zustand Store (`store.ts`) — 4 Felder:**

| Feld | Typ | Wer schreibt | Persistent |
|------|-----|-------------|-----------|
| `selectedCaseId` | `string \| null` | `setSelectedCaseId()` in App.tsx | NEIN |
| `currentPrediction` | `InferenceResponse \| null` | `setCurrentPrediction()` nach Inferenz-Erfolg | NEIN |
| `decisionTreeDraft` | `Record<string,unknown> \| null` | `setDecisionTreeDraft()` — **AKTUELL UNGENUTZT** | NEIN |
| `walkthroughSeen` | `boolean` | `setWalkthroughSeen()` in Walkthrough.tsx | JA → `localStorage.carotis:walkthroughSeen` |

**TanStack React Query:**

| Hook | Endpoint | Typ |
|------|----------|-----|
| `useInference()` | `POST /api/v1/inference/predict` | `useMutation<InferenceResponse, Error, File>` |
| Inline in DecisionForm.tsx | `POST /api/v1/decision-tree/capture` | `useMutation` |
| Debounced in FreeTextField.tsx | `POST /api/v1/decision-tree/check-text` | Direct call (kein Hook) |

**localStorage-Keys:**
- `carotis:walkthroughSeen` — Walkthrough-Status
- `carotis:demoToken` — Demo-Token (persistent bis Expiry)
- `dt:free_text_draft` — FreeTextField Auto-Save Draft

### 3.4 API-Client-Status

**Methoden in `apiClient.ts`:**
- `getHealth()` — `GET /health/` PUBLIC
- `predict(file: File)` — `POST /api/v1/inference/predict` AUTH
- `captureDecisionTree(payload)` — `POST /api/v1/decision-tree/capture` AUTH
- `checkText(text: string)` — `POST /api/v1/decision-tree/check-text` AUTH

**Auth:** `X-API-Key` aus `VITE_API_KEY` + `X-Demo-Token` aus localStorage
**Error-Handling:** 401 → Redirect Login, 429 → Alert, 503 → Alert, sonst throw

**Fehlende Methoden:**
- `logWalkthroughStep()` — `POST /api/v1/demo/log-walkthrough-step` (nicht im apiClient, Walkthrough sendet nicht)
- `getRecentDecisions()` — `GET /api/v1/decision-tree/recent` (kein Frontend-UI)
- `getAuditTrail()` — `GET /api/v1/audit/trail` (nur Admin, kein Frontend)

### 3.5 Routing / Navigation

- **Kein React Router** — Single-Page, kein URL-Routing. **Beabsichtigt** (Demo-Simplicity)
- **AuthGate** ist in `App.tsx` als Wrapper gerendert: `<AuthGate><MainLayout /></AuthGate>`
- **Flow:** Token-Eingabe → `POST /api/v1/demo/whoami` Validierung → Main-App

### 3.6 Offene TODOs im Frontend

**Ergebnis: 0 TODO/FIXME/XXX/HACK in allen .ts/.tsx Dateien.**

### 3.7 Test-Status Frontend

| Datei | Tests | Framework | Status |
|-------|-------|-----------|--------|
| AiPanel.test.tsx | 3 | Vitest + jsdom + @testing-library | ✅ grün |
| DecisionForm.test.tsx | 2 | Vitest | ✅ grün |
| ConfidenceBadge.test.tsx | 3 | Vitest | ✅ grün |
| FreeTextField.test.tsx | 3 | Vitest | ✅ grün |
| **Gesamt** | **11** | | ✅ alle grün |

**Ohne Tests:** DicomViewer, HeatmapOverlay, GradCamOverlay, Walkthrough, AuthGate (alle UI-/WASM-intensiv)

---

## 4. ML-PIPELINE-STATUS (`code/ml/`)

### 4.1 Struktur-Tree

```
ml/
├── models/
│   ├── mfsd_unet.py             # MFSD-UNet Architektur (U-Net + Swin Transformer + Deep Supervision)
│   └── test_mfsd_unet.py        # Import-Smoke + Forward-Pass-Shape
├── training/
│   ├── train.py                 # Train-Loop (AdamW, CosineAnnealingLR, MLflow)
│   ├── losses.py                # CombinedLoss (Deep Supervision + Regression + Klassifikation)
│   ├── dataset.py               # MONAI Dataset / DataLoader
│   ├── test_train.py            # Training Smoke-Test
│   └── test_losses.py           # Loss-Funktion Unit-Tests
├── data/
│   ├── dataset.py               # DataLoader-Wrapper
│   └── transforms.py            # MONAI Augmentations
├── inference/
│   └── onnx_export.py           # PyTorch → ONNX (Opset 17, onnxsim)
├── xai/
│   ├── gradcam.py               # SegHiResCAM + GradCAM Implementierung
│   └── evaluate_cam_methods.py  # Vergleichs-Evaluierung CAM-Methoden
├── test_export_onnx.py          # ONNX-Export Roundtrip-Test
├── requirements.txt             # PyTorch 2.5.1, MONAI 1.4.0, timm 1.0.12, ...
└── __init__.py
```

### 4.2 Modelle

| Modul | Status | Implementiert |
|-------|--------|--------------|
| `models/mfsd_unet.py` | COMPLETE | U-Net + Swin Transformer + Deep Supervision Forward-Pass |
| `models/heads.py` | **MISSING** | Multi-Task-Head für deciding_feature (T-021 pending P3) |

### 4.3 Training

| Datei | Status | Lauffähig |
|-------|--------|-----------|
| `training/train.py` | COMPLETE | Ja (benötigt GPU/CUDA für volles Training) |
| `training/losses.py` | COMPLETE | CombinedLoss differenzierbar |
| `training/dataset.py` | COMPLETE | MONAI DataLoader |
| `data/transforms.py` | COMPLETE | MONAI Augmentations |

**Fehlend:** `reasoning_alignment` Loss-Komponente (T-019 pending P3), Reasoning-Alignment-Loss = cosine_similarity(GradCAM, annotated_mask)

### 4.4 ONNX-Export

- `inference/onnx_export.py` — **COMPLETE**. Opset 17, onnxsim. Demo-Modell via `scripts/generate_demo_model.py`.
- `test_export_onnx.py` — Roundtrip-Test: Diff < 1e-4

### 4.5 Offene TODOs (ML)

- `models/heads.py` nicht vorhanden (T-021)
- `scripts/hp_search.py` nicht vorhanden (T-022)
- Reasoning-Alignment-Loss in `losses.py` noch nicht integriert (T-019)
- **0 TODO-Kommentare** in vorhandenen ML-Dateien

---

## 5. INFRASTRUKTUR-STATUS

### 5.1 Docker

**`code/docker-compose.yml` (Dev/Default):**
```yaml
Services:
  ollama:   image: ollama/ollama:latest        PORT: 11434  HEALTHCHECK: curl localhost:11434/api/tags
  hermes:   build: ./hermes                    PORT: 8200   HEALTHCHECK: curl localhost:8200/health
  backend:  build: ./backend                   PORT: 8000   HEALTHCHECK: curl localhost:8000/health  ✅
  frontend: build: ./frontend                  PORT: 3000   KEINE HEALTHCHECK
```

**`code/deploy/docker-compose.demo.yml` (Production):**
```yaml
Services:
  backend:  build: ../backend      ✅
  frontend: nginx:1.27-alpine      ✅ (benötigt prebuild: npm run build → dist/)
  caddy:    caddy:2.8-alpine       ✅ TLS-Termination
  (ollama + hermes optional, nicht included)

✅ BUG-001 FIXED (2026-04-30): backend healthcheck → "/health/" (war "/api/v1/health/")
```

**Dockerfiles:**
- `backend/Dockerfile` — python:3.11-slim, Non-Root carotis ✅
- `frontend/Dockerfile` — Multi-Stage: node:22-alpine → nginx:1.27-alpine ✅
- `hermes/Dockerfile` — vorhanden ✅

### 5.2 CI/CD

**`.github/workflows/ci.yml`:**

| Job | Trigger | Status |
|-----|---------|--------|
| `lint` | push main/dev, PR main | ruff + black + eslint + typecheck |
| `test-backend` | push main/dev, PR main | pytest 75%-Gate + codecov |
| `test-ml` | push main/dev, PR main | pytest 60%-Gate |
| `test-frontend` | push main/dev, PR main | npm typecheck + lint + test |
| `security` | push main/dev, PR main | bandit + npm audit |
| `build` | push main/dev, PR main | docker compose build + Health-Check |

**`.github/workflows/local_smoke.yml`:** Wöchentlich Montags 05:00 UTC — Hermes-Agent Smoke-Test

### 5.3 Hermes / Local AI

**`hermes/config.toml`:** Ollama-URL=http://ollama:11434, Modell=nous-hermes-3-llama-3.1, Port=8200

**Skills in `hermes/skills/` (9 Markdown-Dateien):**

| Skill | Zweck |
|-------|-------|
| `aggregate-free-text.md` | Nightly Free-Text Cluster-Aggregation |
| `anonymize-batch.md` | DICOM-Batch-Anonymisierung |
| `browser-harness.md` | Browser-Automatisierung für Demo |
| `capture-decision-tree.md` | Decision-Tree Capture-Workflow |
| `clinical-research-harness.md` | Klinische Forschungs-Automatisierung |
| `decision-pattern-miner.md` | Pattern-Mining aus Decision-Trees |
| `doctor-knowledge-capture.md` | Wissenserfassung von Ärzten |
| `nightly-retrain.md` | Nightly-Learning-Loop |
| `trust-calibration-monitor.md` | Trust-Score-Monitoring |

---

## 6. DOKUMENTATIONS-STATUS

### 6.1 Root-Level MD-Dateien

| Datei | Letztes Update | Status |
|-------|----------------|--------|
| AGENTS.md | 2026-04-30 | COMPLETE |
| CLAUDE.md | 2026-04-30 v1.4 | COMPLETE |
| MEMORY.md | 2026-04-30 | COMPLETE |
| RUNBOOK_TODAY.md | 2026-04-30 | PARTIAL (tagesaktuell) |
| 00_INDEX.md | 2026-04-29 | COMPLETE |
| 01_HARNESS.md | 2026-04-29 | COMPLETE |
| 02_ROADMAP.md | 2026-04-29 | COMPLETE |
| 03_PROMPT_TEMPLATES.md | 2026-04-29 | COMPLETE |
| 04_MASTER_PLAN.md | 2026-04-29 | COMPLETE |
| 05_DECISION_TREE_HARVESTING.md | 2026-04-29 | COMPLETE |
| 06_ROHDE_MEETING_KIT.md | 2026-04-29 | COMPLETE |
| 07_OFFICE_AGENT_PROMPTS.md | 2026-04-30 | COMPLETE |
| 08_RESEARCH_ATTENTION_2020-2026.md | 2026-04-29 | COMPLETE |
| tasks.jsonl | 2026-04-30 | PARTIAL (W-01..W-12 fehlen) |

### 6.2 ADRs (`regulatory/adr/`)

| Datei | Titel | Status |
|-------|-------|--------|
| `ADR-0001-local-first.md` | Local-First: keine Cloud-Inferenz, SQLite-only | COMPLETE |
| `ADR-0002-decision-tree-harvesting.md` | Decision-Tree-Harvesting Schema | COMPLETE |
| `ADR-0003-api-versioning-router-prefix.md` | /api/v1 Prefix-Strategie | COMPLETE |
| `ADR-0004-lazy-db-engine-init.md` | @lru_cache Engine, kein Modul-Import-Side-Effect | COMPLETE |
| `004_transformers_pii_layer.md` | Transformers-PII-Layer (Naming-Inkonsistenz!) | COMPLETE |
| `005_hirescam_xai.md` | HiResCAM statt GradCAM (Naming-Inkonsistenz!) | COMPLETE |
| `006_confidence_calibration.md` | Confidence Calibration Service | COMPLETE |
| `ADR-0007-reasoning-alignment-loss.md` | Reasoning-Alignment-Loss (T-019) | COMPLETE |
| `ADR_TEMPLATE.md` | Template | COMPLETE |

⚠️ **Naming-Inkonsistenz:** ADR-0001..0004, ADR-0007 nutzen `ADR-XXXX-name.md`, während 004, 005, 006 `NNN_name.md` nutzen.

⚠️ **Fehlend:** `ADR-0005-demo-token-auth.md`, `ADR-0006-trust-score-composite.md` — Naming-Kollisionen deuten auf eine Umbenennungsphase hin.

### 6.3 Memory-Struktur

- `memory/runs/`: **55+ Logs** (2026-04-27 bis 2026-04-30), letzter: `2026-04-30_plan_next_phase.md`
- `memory/anomalies/`: 2 Dateien — `2026-04-29_kimi_e2e_13_bugs.md` + README
- `memory/decisions/`: 6 JSON-Dateien (Entscheidungs-Snapshots von 2026-04-29..30)

---

## 7. OFFENE PUNKTE & TECHNISCHE SCHULDEN (Priorisiert)

### 7.1 🔴 KRITISCH (Blockiert Demo / Funktionalität)

```yaml
BUG-001:
  title: "deploy/docker-compose.demo.yml healthcheck nutzt falschen Pfad"
  status: ✅ FIXED (2026-04-30)
  detail: >
    backend healthcheck war "http://localhost:8000/api/v1/health/" — FALSCH.
    Health-Router hat kein /api/v1 Prefix. Korrigiert auf "http://localhost:8000/health/"
  file: code/deploy/docker-compose.demo.yml

BUG-002:
  title: "Website verweist auf https://app.carotis.diggai.de — Domain wahrscheinlich nicht live"
  detail: >
    code/website/index.html und code/website/netlify.toml referenzieren https://app.carotis.diggai.de.
    Kein Beweis dass diese Domain aktiv deployed ist. Wird Besuchern einen 404 zeigen.
  file: code/website/index.html, code/website/netlify.toml
  impact: Wenn die Website auf Netlify liegt, kommen Demo-Klicks ins Leere
  fix: Deployment verifizieren oder URL anpassen
```

### 7.2 🟡 HOCH (Blockiert P0f / Rohde-Meeting)

```yaml
ISSUE-001:
  title: "W-01..W-12 P0f-Tasks nicht in tasks.jsonl erfasst"
  detail: >
    kimi_prompt_p0f_pivot_ready.md und CLAUDE.md referenzieren W-01..W-12 (Production-Demo-Pivot),
    aber diese Tasks existieren NICHT in tasks.jsonl. Tracking-Lücke.
  fix: W-Tasks in tasks.jsonl hinzufügen

ISSUE-002:
  title: "Stride-Prompts D, E, F, G, B, A (T-004 bis T-010) noch pending"
  detail: >
    T-004 (Tech_Description), T-005 (Value_Proposition), T-006 (Präsentation),
    T-007 (Anschreiben), T-008 (Mail-Text), T-009 (Review), T-010 (Mail rausschicken)
    alle auf Status "pending". Mail an Rohde noch nicht verschickt.
  impact: Rohde-Meeting nicht terminiert → P1 blockiert

ISSUE-003:
  title: "Demo-Token für Prof. Rohde noch nicht generiert"
  detail: >
    scripts/generate_rohde_token.py existiert (K-43), aber es gibt keine Dokumentation
    ob ein Token tatsächlich generiert und in der DB gespeichert wurde.
  fix: python scripts/generate_rohde_token.py ausführen + Token sicher an Aroob übermitteln

ISSUE-004:
  title: "frontend/src/services/ Verzeichnis leer (Legacy)"
  detail: Leeres Verzeichnis, sollte entfernt werden um Verwirrung zu vermeiden.
  severity: Niedrig, aber Ordnung
```

### 7.3 🟢 MITTEL (P1-Readiness)

```yaml
ISSUE-005:
  title: "Zustand.decisionTreeDraft Feld ungenutzt"
  detail: >
    store.ts definiert decisionTreeDraft: Record<string,unknown>|null und setDecisionTreeDraft(),
    aber keine Komponente liest oder schreibt dieses Feld.
  fix: Feld entfernen oder für zukünftigen DecisionForm-Draft nutzen

ISSUE-006:
  title: "app/services/xai_service.py ohne dedizierte Tests"
  detail: xai_service.py existiert aber test_xai_service.py fehlt.
  fix: Mindest-Tests für XAI-Postprocessing hinzufügen

ISSUE-007:
  title: "ADR-Naming inkonsistent (ADR-XXXX vs NNN_name)"
  detail: >
    ADR-0001..0004 und 0007 nutzen das richtige Format. 004_transformers, 005_hirescam,
    006_confidence nutzen altes Format. Umbenennung empfohlen.
  fix: mv 004_transformers_pii_layer.md ADR-0004b-transformers-pii-layer.md (etc.)
```

### 7.4 🔵 NIEDRIG (Nice-to-have)

```yaml
ISSUE-008:
  title: "GradCamOverlay vs HeatmapOverlay — zwei unterschiedliche Overlay-Implementierungen"
  detail: >
    GradCamOverlay.tsx: <img>-basiert für base64-PNG.
    HeatmapOverlay.tsx: Canvas-basiert für 2D-Array + Jet-Colormap.
    Beide existieren parallel, kein einheitliches Pattern.
  fix: Long-term: eine Implementierung (Canvas bevorzugt), oder dokumentiere Use-Cases klar

ISSUE-009:
  title: "Keine E2E-Tests (Playwright/Cypress)"
  detail: Kritische User-Flows (DICOM hochladen → Inferenz → Decision Form → Submit) haben keine E2E-Tests.

ISSUE-010:
  title: "Keine pyproject.toml für Python-Tool-Config"
  detail: black/ruff laufen mit Defaults. pyproject.toml mit [tool.black]/[tool.ruff] empfohlen für P1.

ISSUE-011:
  title: "Frontend Walkthrough sendet nicht an /api/v1/demo/log-walkthrough-step"
  detail: >
    Das Backend hat POST /api/v1/demo/log-walkthrough-step implementiert, aber
    Walkthrough.tsx sendet keine Events. Walkthrough-Tracking für Rohde-Demo nicht aktiv.
```

---

## 8. NÄCHSTE SCHRITTE (Empfohlene Reihenfolge)

```yaml
- id: NEXT-001
  title: "BUG-001 fixen: docker-compose.demo.yml healthcheck"
  priority: CRITICAL
  status: ✅ DONE (2026-04-30)
  files_touched: [code/deploy/docker-compose.demo.yml]

- id: NEXT-002
  title: "W-01..W-12 in tasks.jsonl erfassen"
  priority: HIGH
  blocked_by: []
  blocks: []
  estimated_effort: S
  files_to_touch: [tasks.jsonl]
  acceptance_criteria:
    - W-01..W-12 als JSONL-Einträge vorhanden mit status, blocked_by, dod

- id: NEXT-003
  title: "T-004..T-008: Stride-Prompts D,E,F,G,B,A ausführen (Office-Docs finalisieren)"
  priority: HIGH
  blocked_by: []
  blocks: [NEXT-004]
  estimated_effort: M
  files_to_touch: [Stride V2/ Office-Dokumente]
  acceptance_criteria:
    - Tech_Description_Klinikum_v2.docx, Value_Proposition_Klinikum_v2.docx vorhanden
    - Carotis_Ai_Rohde_v2.pptx ≥14 Folien
    - Mail_Aroob_an_Rohde_v2.docx finalisiert

- id: NEXT-004
  title: "T-009 + T-010: Aroob Review + Mail an Rohde rausschicken"
  priority: HIGH
  blocked_by: [NEXT-003]
  blocks: [NEXT-007]
  estimated_effort: S
  acceptance_criteria:
    - Mail versendet + Datum/Uhrzeit dokumentiert
    - memory/runs/<datum>_mail_an_rohde.md angelegt

- id: NEXT-005
  title: "Demo-Token für Rohde generieren + verifizieren"
  priority: HIGH
  blocked_by: [NEXT-001]
  blocks: [NEXT-006]
  estimated_effort: XS
  acceptance_criteria:
    - python scripts/generate_rohde_token.py → Token mit rohde_tag=True in DB
    - GET /api/v1/demo/whoami mit Token → 200

- id: NEXT-006
  title: "Production-Demo deployen (Caddy + TLS + Domain)"
  priority: HIGH
  blocked_by: [NEXT-001, NEXT-005]
  blocks: [NEXT-007]
  estimated_effort: M
  files_to_touch: [code/deploy/Caddyfile, code/deploy/docker-compose.demo.yml]
  acceptance_criteria:
    - https://app.carotis.diggai.de erreichbar (oder alternativer Domain)
    - GET /health/ → 200
    - AuthGate mit Rohde-Token → Main-App

- id: NEXT-007
  title: "Walkthrough → log-walkthrough-step Tracking aktivieren"
  priority: MEDIUM
  blocked_by: [NEXT-006]
  blocks: []
  estimated_effort: S
  files_to_touch:
    - code/frontend/src/components/Walkthrough/Walkthrough.tsx
    - code/frontend/src/lib/apiClient.ts
  acceptance_criteria:
    - Walkthrough sendet step_id + event an /api/v1/demo/log-walkthrough-step
    - audit_events Tabelle enthält demo_walkthrough_step Einträge

- id: NEXT-008
  title: "Zustand.decisionTreeDraft entfernen oder nutzen"
  priority: MEDIUM
  blocked_by: []
  blocks: []
  estimated_effort: XS
  files_to_touch: [code/frontend/src/store.ts]
  acceptance_criteria:
    - Keine ungenutzten Felder im Store
    - npm run typecheck → 0 errors

- id: NEXT-009
  title: "frontend/src/services/ Verzeichnis entfernen"
  priority: LOW
  blocked_by: []
  blocks: []
  estimated_effort: XS
  files_to_touch: [code/frontend/src/services/]
  acceptance_criteria:
    - Leeres Verzeichnis gelöscht

- id: NEXT-010
  title: "E2E-Smoke-Test für Demo-Flow"
  priority: MEDIUM
  blocked_by: [NEXT-006, NEXT-007]
  blocks: []
  estimated_effort: M
  acceptance_criteria:
    - Demo-Flow (Upload → Inferenz → DecisionForm → Submit) automatisiert verifizierbar
```

---

## 9. ARCHITEKTUR-LÜCKEN

Vergleich Code vs. Spec (04_MASTER_PLAN.md, 05_DECISION_TREE_HARVESTING.md, AGENTS.md):

| Feature | Spezifiziert | Implementiert | Delta |
|---------|-------------|---------------|-------|
| MFSD-UNet Forward-Pass | YES | YES | ✅ |
| ONNX-Runtime Inferenz | YES | YES | ✅ |
| Grad-CAM / HiResCAM | YES | YES | ✅ |
| Decision-Tree-Capture | YES | YES | ✅ |
| PII-Erkennung (Regex+SpaCy) | YES | YES | ✅ |
| Transformers-PII (OpenMed) | YES (optional) | YES | ✅ |
| Confidence Calibration | YES | YES | ✅ |
| Trust Score Composite | YES | YES | ✅ |
| Demo-Token-Auth | YES | YES | ✅ |
| Walkthrough (5 Schritte) | YES | YES (Frontend) | ⚠️ Tracking fehlt |
| Daily-Learning-Loop | YES | NEIN | 🔴 Deliberate (P4) |
| Reasoning-Alignment-Loss | YES (ADR-0007) | NEIN | 🟡 P3 pending |
| Multi-Task-Head (deciding_feature) | YES (T-021) | NEIN | 🟡 P3 pending |
| Heatmap-Annotation UI | YES (T-020) | NEIN | 🟡 P3 pending |
| HL7/FHIR-Integration | YES | NEIN | 🟢 P4 |
| Adoption-Monitor | YES (T-023) | NEIN | 🟢 P5 |
| DICOM PS 3.15 Anonymisierung | YES | YES | ✅ |
| Append-only Audit-Trail | YES | YES | ✅ |
| Modell-Signing (cosign/GPG) | YES | YES | ✅ |
| Demo-Token mit rohde_tag | YES | YES | ✅ |
| Website (Netlify Landing Page) | YES | YES (code/website/) | ⚠️ Domain-Status unklar |

---

## 10. TEST-GAP-ANALYSE

### Backend-Services ohne Tests

| Service | Abdeckung | Lücke |
|---------|-----------|-------|
| `xai_service.py` | KEINE | Dedizierte XAI-Postprocessing-Tests fehlen |
| `dicom_service.py` | PARTIAL | Nur Bridge-Test in test_anonymization_bridge.py |
| `error_handlers.py` | KEINE | Exception-Handler-Routing nicht explizit getestet |
| `gradcam.py` | YES (test_gradcam.py) | ✅ |
| `inference_service.py` | YES | ✅ |
| `decision_tree_service.py` | YES | ✅ |
| `audit_service.py` | YES | ✅ |
| `pii_detection_service.py` | YES | ✅ |
| `confidence_calibration_service.py` | YES | ✅ |
| `transformers_pii_layer.py` | YES | ✅ |

### API-Routes ohne Tests

| Route | Abdeckung | Lücke |
|-------|-----------|-------|
| `demo.py` | YES (test_demo_token.py) | ✅ |
| `audit.py` | YES (test_audit_service.py) | ✅ |
| `health.py` | PARTIAL (test_smoke.py) | `/health/ready` Degraded-Branch nicht explizit |
| `inference.py` | YES | ✅ |
| `decision_tree.py` | YES | ✅ |

### Frontend-Komponenten ohne Tests

| Komponente | Begründung |
|-----------|------------|
| DicomViewer.tsx | Cornerstone3D WASM — jsdom nicht kompatibel |
| HeatmapOverlay.tsx | Canvas-API fehlt in jsdom |
| GradCamOverlay.tsx | `<img>`-Rendering, niedrige Kritikalität |
| Walkthrough.tsx | DOM-Positioning-Logik, jsdom-limitiert |
| AuthGate.tsx | Fetch-Mock nötig, fehlt |

### ML-Module ohne Tests

| Modul | Lücke |
|-------|-------|
| `ml/data/transforms.py` | MONAI Transforms ohne Tests |
| `ml/xai/evaluate_cam_methods.py` | Evaluierungs-Skript ohne Tests |
| `models/heads.py` | Existiert noch nicht |

### Utilities / Scripts ohne Tests

| Script | Lücke |
|--------|-------|
| `scripts/generate_rohde_token.py` | Kein Test |
| `scripts/aggregate_free_text.py` | Kein Test |
| `scripts/hermes_healthcheck.py` | Kein Test |
| `scripts/verify_demo_e2e.sh` / `.ps1` | Shell-Test, nicht in pytest |

---

*Report erstellt von GitHub Copilot (Claude Sonnet 4.6) · Plan-Modus · 2026-04-30*
*Basierend auf: code/backend/, code/frontend/, code/ml/, code/tests/, code/hermes/, code/.github/workflows/, deploy/, regulatory/, memory/, tasks.jsonl*
*BUG-001 Status: ✅ FIXED in dieser Session*
