# Carotis-AI — Agent Instructions

> Jede KI liest diese Datei **vor** jeder Arbeit. Für tiefen Kontext folge den Links — kopiere Inhalte hierher nicht.

---

## Projekt-Übersicht

**Carotis-AI** ist ein lokales, erklärbares KI-System zur Quantifizierung der Carotis-Stenose und Plaque-Vulnerability aus CTA-Bildern. Promotionsprojekt am Klinikum Dortmund unter Leitung von Lou (Laith Alshdaifat) und Dr. med. Aroob Alrawashdeh.

**Kernunterschiede gegenüber anderen Lösungen:**
- Local-First Edge AI (kein Cloud-Export von Patientendaten)
- Grad-CAM + SHAP für Erklärbarkeit (XAI)
- Decision-Tree-Harvesting (ärztliche Begründungen werden erfasst und gelernt)
- Daily-Learning-Loop für kontinuierliche Verbesserung

**Aktuelle Phase:** P0 (Rohde-Meeting-Vorbereitung + Floy-Recherche). Alle Phasen P1–P7 sind blockiert bis Prof. Rohde sein Go gegeben hat.

---

## Pre-Flight (PFLICHT — jede Session)

1. [`ULTRAPLAN.md`](ULTRAPLAN.md) lesen — Agent Pre-Flight Protocol v3 (Tool-Matrix, Anti-Patterns, E2E-Wissen, Skills-Inventar)
2. [`CLAUDE.md`](CLAUDE.md) lesen — Working Memory, People, Stack, Phase-Status
3. [`MEMORY.md`](MEMORY.md) lesen — Index aller Langzeit-Memories
4. Letzte 3 Run-Logs überfliegen: `memory/runs/` (neueste zuerst)
4. Prüfen: wurde diese Aufgabe schon versucht? → `grep -r "<keyword>" memory/runs/`
5. Bekannte Anomalien prüfen: `memory/anomalies/` (leer bis P5) **und** Abschnitt [Bekannte Anomalien und technische Schulden](#bekannte-anomalien-und-technische-schulden) in dieser Datei
6. Task-Status in [`tasks.jsonl`](tasks.jsonl) auf `"in_progress"` setzen

---

## Hard Rules (niemals verletzen)

| Regel | Detail |
|------|--------|
| ❌ Keine Patientendaten in die Cloud | Keine externe API, kein E-Mail-Versand, kein Cloud-Storage |
| ❌ Keine direkten Office-Doc-Edits | Modelle generieren nur Stride-Prompts → Lou führt sie in der UI aus |
| ❌ Keine Code-Änderungen ohne Pre-Flight | Siehe Schritte 1–5 oben |
| ❌ Kein Session-Ende ohne Run-Log | Schreibe `memory/runs/<YYYY-MM-DD>_<sessionID>.md` |
| ❌ Kein Modell-Training auf nicht-anonymisierten Daten | DICOM PS 3.15 De-Identification Profile ist Pflicht |
| ❌ Keine Cloud-Inferenz für Patientenbilder | ONNX Runtime läuft ausschließlich lokal |

---

## Model Routing

Vollständige Matrix in [`01_HARNESS.md`](01_HARNESS.md). Kurzreferenz:

| Aufgabe | Modell |
|------|-------|
| Architektur-Entscheidungen, ADRs, regulatorische Texte, Stakeholder-Kommunikation | **Opus 4.7** |
| Code-Implementierung, Bug-Debug, Office-Drafts, Test-Suites | **Sonnet 4.6** |
| Atomare Edits, i18n, Datei-Umbenennungen, Verify/Build, MEMORY.md-Updates | **Haiku 4.5** |
| Medizinische/regulatorische Entscheidungen (DSGVO, MDR, Ethik) | **Opus 4.7 only** |

Regel: Wenn Pseudo-Code mit exakter Datei+Zeile existiert → Haiku. Wenn Denken/Trade-offs nötig → Sonnet/Opus.

---

## Sprachregelung

- **Arbeitssprache:** Deutsch (Antworten, Dokumentation, Kommentare in Markdown)
- **Code + Commits:** Englisch only

---

## Tech Stack

Die folgenden Versionen sind die **tatsächlich eingesetzten** (Stand Code-Exploration 2026-04-30), nicht aspirational:

| Schicht | Technologie |
|-------|-----------|
| Frontend | React 19.0.0 + Vite 5.4.2 + TypeScript 5.5.3 + Tailwind CSS 4.0.0 |
| DICOM-Viewer | Cornerstone.js 2.8 (`@cornerstonejs/core`, `@cornerstonejs/dicom-image-loader`, `@cornerstonejs/tools`) |
| Backend (Edge) | Python 3.11 + FastAPI 0.115.5 + Uvicorn 0.32.1 |
| Datenbank | SQLite via SQLAlchemy 2.0.36 + aiosqlite 0.20.0 (async) + Alembic 1.14.0 |
| ML-Training | PyTorch 2.5.1 + torchvision 0.20.1 + MONAI 1.4.0 + timm 1.0.12 |
| Modell-Architektur | MFSD-UNet (U-Net + Swin Transformer + Deep Supervision) |
| Inference Runtime | ONNX Runtime ≥1.24.0 (CPU-only lokal) |
| XAI | grad-cam 1.5.5 + SHAP 0.47.0 |
| Lokale KI | Ollama (`ollama/ollama:latest`) + Hermes Agent (Port 8200) |
| Anonymisierung | pydicom 3.0.1 — DICOM PS 3.15 Basic Application Level Confidentiality Profile |
| Integration | HL7/FHIR → Klinikum-PVS (geplant) |
| Demo-Hosting | Fly.io (`carotis.diggai.de`) + Hetzner (`api.carotis.diggai.de`) — **niemals echte Patientendaten** |

**Wichtige Abhängigkeiten (Backend):**
- `pydantic==2.10.3` / `pydantic-settings==2.6.1`
- `slowapi==0.1.9` (Rate Limiting)
- `structlog==24.4.0` (Logging)
- `python-jose[cryptography]==3.3.0` (JWT — zukünftig)
- `prometheus-fastapi-instrumentator==7.0.0` (Metriken)
- `spacy>=3.7,<4.0` (PII Detection, lazy-loaded)
- `scikit-learn` (optional — Confidence Calibration, lazy-loaded)

**Frontend-Abhängigkeiten:**
- `@tanstack/react-query==5.56.2`
- `zustand==5.0.0`
- `dicomweb-client==0.10.4`
- `use-debounce==10.1.1`
- `@icr/polyseg-wasm==0.4.0`

---

## Projektstruktur

```
code/
├── backend/              # FastAPI Edge-Server
│   ├── app/
│   │   ├── api/
│   │   │   ├── router.py          # Orphaned — wird in app/main.py NICHT verwendet
│   │   │   ├── dependencies.py    # verify_api_key, verify_admin_key
│   │   │   └── routes/
│   │   │       ├── health.py      # GET /health/, /health/ready, /health/live
│   │   │       ├── inference.py   # POST /api/v1/inference/predict (rate-limited)
│   │   │       ├── decision_tree.py # POST /api/v1/decision-tree/capture, GET /api/v1/decision-tree/recent
│   │   │       └── audit.py       # GET /api/v1/audit/trail, GET /api/v1/audit/anomalies
│   │   ├── core/
│   │   │   ├── config.py          # pydantic-settings, validiert API-Key ≥32 Zeichen, SQLite-Enforcement
│   │   │   ├── logging.py         # structlog JSON/Console + _strip_pii Processor
│   │   │   ├── security.py        # X-API-Key Header-Auth via fastapi.Security
│   │   │   ├── exceptions.py      # Custom exceptions (AnonymizationError, ModelNotLoadedError, ...)
│   │   │   └── error_handlers.py  # Globale Exception-Handler-Registrierung
│   │   ├── db/
│   │   │   ├── database.py        # SQLAlchemy 2.0 async engine + init_db() + reset_db() + append-only AuditEvent-Listener
│   │   │   └── models.py          # Base, Inference, DecisionTree, AuditEvent
│   │   ├── schemas/               # Pydantic v2 Request/Response-Schemas
│   │   │   ├── inference.py       # PredictionResponse, HealthResponse, DecisionTreeRequest, ...
│   │   │   ├── decision_tree.py   # DecisionTreeCreate, DecisionTreeResponse
│   │   │   └── audit.py           # AuditPage, AuditTrailEntry, DisagreementSummary
│   │   └── services/              # Business-Logik
│   │       ├── dicom_service.py           # DICOM-Parsing + Anonymisierung (33 PII-Tags)
│   │       ├── anonymization_service.py   # Hash-basierte Anonymisierung
│   │       ├── inference_service.py       # ONNX-Runtime-Inferenz + Grad-CAM
│   │       ├── confidence_calibration_service.py  # Kalibrierung der Modell-Konfidenz
│   │       ├── xai_service.py             # XAI-Postprocessing
│   │       ├── gradcam.py                 # Grad-CAM-Heatmap-Generierung
│   │       ├── audit_service.py           # Audit-Trail-Schreiben (⚠️ Import-Bug: referenziert InferenceLog/DecisionTreeLog, Model heißt Inference/DecisionTree)
│   │       ├── decision_tree_service.py   # Decision-Tree-Capture + Disagreement-Detection
│   │       ├── pii_detection_service.py   # SpaCy-basierte PII-Erkennung
│   │       └── transformers_pii_layer.py  # Transformer-basierte PII-Erkennung (optional)
│   ├── main.py             # Dev-Entrypoint: uvicorn.run("main:app", reload=True)
│   ├── app/main.py         # create_app() Factory — für Docker & Tests
│   ├── requirements.txt
│   ├── Dockerfile          # python:3.11-slim, Non-Root-User carotis
│   └── .env.example
├── frontend/             # React 19 SPA
│   ├── src/
│   │   ├── components/
│   │   │   ├── AIPanel.tsx                  # Rechts-Panel mit AI-Ergebnissen
│   │   │   ├── AiPanel/AiPanel.tsx          # (Duplikat/Alt — prüfen welches aktiv)
│   │   │   ├── ConfidenceBadge.tsx
│   │   │   ├── DecisionForm/DecisionForm.tsx
│   │   │   ├── DicomViewer/                 # DICOM-Viewer mit Cornerstone3D
│   │   │   │   ├── DicomViewer.tsx
│   │   │   │   ├── HeatmapOverlay.tsx
│   │   │   │   ├── index.ts
│   │   │   │   └── test_DicomViewer.tsx     # Einzige Frontend-Testdatei
│   │   │   ├── FreeTextField.tsx
│   │   │   └── GradCamOverlay/GradCamOverlay.tsx
│   │   ├── hooks/
│   │   │   └── useInference.ts    # TanStack Query Mutation
│   │   ├── lib/
│   │   │   ├── apiClient.ts       # Typed fetch-Wrapper mit X-API-Key
│   │   │   └── cornerstoneSetup.ts # Cornerstone3D-Initialisierung
│   │   ├── services/
│   │   │   └── api.ts             # (Legacy/Alt — apiClient.ts ist aktiv)
│   │   ├── types/
│   │   │   ├── index.ts
│   │   │   └── api.ts
│   │   ├── store.ts               # Zustand-Global-Store
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   └── index.css
│   ├── package.json        # KEIN "test"-Script vorhanden!
│   ├── vite.config.ts      # Port 3000, Proxy /api → backend:8000, WASM-Support
│   ├── tsconfig.json       # Strict, @/* → src/*, noUnusedLocals, noUnusedParameters
│   ├── eslint.config.js    # ESLint 9 Flat Config (@eslint/js, typescript-eslint, react-hooks, react-refresh)
│   ├── Dockerfile          # Multi-Stage: node:22-alpine → nginx:1.27-alpine
│   └── nginx.conf
├── ml/                   # Trainings- und Export-Pipeline
│   ├── models/
│   │   └── mfsd_unet.py         # MFSD-UNet Architektur
│   ├── training/
│   │   ├── train.py             # Train-Loop (AdamW, CosineAnnealingLR, MLflow)
│   │   ├── dataset.py           # MONAI Dataset / DataLoader
│   │   └── losses.py            # CombinedLoss (Deep Supervision + Regression + Klassifikation)
│   ├── data/
│   │   ├── dataset.py
│   │   └── transforms.py
│   ├── inference/
│   │   └── onnx_export.py       # PyTorch → ONNX (Opset 17, onnxsim)
│   ├── xai/
│   │   └── gradcam.py
│   ├── export_onnx.py           # (Legacy/Alt — ml/inference/onnx_export.py ist aktiv)
│   └── requirements.txt
├── hermes/               # Lokaler KI-Agent (Ollama-Wrapper)
│   ├── config.toml       # Ollama-URL, Modell (mistral:7b), Port 8200
│   ├── Dockerfile
│   ├── settings/
│   │   └── knowledge_harness.json
│   └── skills/           # Markdown-Skills (anonymize-batch, capture-decision-tree, nightly-retrain, ...)
├── tests/                # pytest-Suite (Code-Ebene, NICHT backend/tests/)
│   ├── conftest.py       # test_client, test_dicom_bytes, test_anonymized_dicom, mock_inference_service
│   ├── test_smoke.py
│   ├── test_anonymization_bridge.py
│   ├── test_audit_trail.py
│   ├── test_config.py
│   ├── test_confidence_calibration.py
│   ├── test_decision_tree_override.py
│   ├── test_decision_tree_validation.py
│   ├── test_gradcam.py
│   ├── test_inference_full.py
│   ├── test_ml_pipeline.py
│   ├── test_model_signing.py
│   ├── test_pii_detection.py
│   └── test_transformers_pii_layer.py
├── scripts/
│   ├── generate_demo_model.py
│   ├── generate_demo_data.py
│   ├── aggregate_free_text.py
│   ├── sign_model.py
│   ├── verify_model.py
│   ├── anonymize.py
│   ├── demo.sh / demo.ps1
│   ├── install_local_stack.sh / install_local_stack.ps1
│   └── ...
├── data/
│   ├── models/           # ONNX-Artefakte (read-only im Container)
│   ├── db/               # SQLite-Datenbank (persistent)
│   └── dicom_temp/       # Ephemeres DICOM-Verarbeitungsverzeichnis
├── docker-compose.yml    # 4 Services: backend, frontend, ollama, hermes
├── Makefile
├── pytest.ini            # asyncio_mode = auto, testpaths = tests backend/tests ml
└── .github/workflows/
    ├── ci.yml
    └── local_smoke.yml
```

---

## Build- und Test-Kommandos

### Mit Docker (empfohlen)

```bash
cd code
cp backend/.env.example backend/.env  # API_KEY anpassen (min. 32 Zeichen!)
docker compose up --build

# Backend:   http://localhost:8000
# Frontend:  http://localhost:3000
# API-Docs:  http://localhost:8000/docs  (nur dev-Modus)
```

### Ohne Docker — Backend

```bash
cd code/backend
python -m venv .venv && .venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env  # API_KEY anpassen
# Dev-Modus mit Hot-Reload:
python main.py
# Oder Factory-Modus (für Docker-kompatible Tests):
# uvicorn app.main:create_app --factory --reload --host 0.0.0.0 --port 8000
```

### Ohne Docker — Frontend

```bash
cd code/frontend
npm install
# .env.local anlegen:
echo "VITE_API_URL=http://localhost:8000" > .env.local
echo "VITE_API_KEY=<dein-api-key>" >> .env.local
npm run dev        # Dev-Server auf Port 3000
npm run build      # Produktions-Build → dist/
npm run lint       # ESLint
npm run typecheck  # tsc --noEmit
# "npm test" laeuft Vitest + jsdom + @testing-library
```

### ML-Pipeline

```bash
cd code
# Training (benötigt GPU-VM oder lokale GPU)
python -m ml.training.train --data-root /path/to/data --epochs 100 --checkpoint-dir /path/to/checkpoints

# ONNX-Export nach Training
python -m ml.inference.onnx_export --checkpoint /path/to/checkpoints/best.pt --output data/models/mfsd_unet.onnx

# Demo-Modell erzeugen (keine GPU nötig)
python scripts/generate_demo_model.py --output data/models/mfsd_unet.onnx
```

### Tests

```bash
cd code
$env:PYTHONPATH="backend"
$env:DEBUG="true"

# Smoke-Tests (kein Docker nötig)
.\.venv313\Scripts\python.exe -m pytest tests\test_smoke.py -v

# E2E-Stresstest
.\.venv313\Scripts\python.exe -m pytest tests\test_rohde_walkthrough_e2e.py -v

# Alle Tests mit Coverage (Schwelle: 75 %)
.\.venv313\Scripts\python.exe -m pytest tests\ -v --cov=backend\app --cov-report=xml --cov-fail-under=75 -p no:warnings

# ML-Module importieren testen
cd ml
..\.venv313\Scripts\python.exe -c "from models.mfsd_unet import MFSDUNet; print('OK')"
```

### Makefile-Targets

| Target | Befehl | Beschreibung |
|--------|--------|-------------|
| `make init` | `mkdir -p data/…` + `.env` kopieren | Datenverzeichnisse anlegen |
| `make demo-model` | `python scripts/generate_demo_model.py` | Demo-ONNX erzeugen |
| `make demo` | `init` + `demo-model` + `docker compose up` + Health-Wait | Kompletter One-Shot-Demo |
| `make up` | `docker compose up --build -d` | Alle Container starten |
| `make down` | `docker compose down` | Alle Container stoppen |
| `make logs` | `docker compose logs -f` | Logs tailen |
| `make test` | `PYTHONPATH=backend pytest tests/ -v` | Alle Tests (mit Auto-Install-Fallback) |
| `make clean` | `docker compose down --rmi local --volumes` | Alles entfernen |

---

## Code-Style-Richtlinien

### Python
- **Formatter:** `black` (CI prüft `black --check backend/app ml`)
- **Linter:** `ruff` (CI prüft `ruff check backend/app ml`)
- **Security:** `bandit -r backend/app -ll`
- **Konfiguration:** Es gibt **keine** `pyproject.toml`, `.ruff.toml` oder `setup.cfg` — alle Python-Tools laufen mit Default-Einstellungen
- **Typ-Hinweise:** `from __future__ import annotations` in jeder Datei; moderne Union-Syntax `str | None`; `Annotated` für FastAPI-Dependencies; vollständige Type-Hints auf allen öffentlichen APIs
- **Dokumentation:** Docstrings in englischer Sprache, Google-Style oder einfache Triple-Quotes; häufig mit Security-Kontext (z.B. "No patient data is persisted here")
- **Imports:** Standardbibliothek → Drittanbieter → Interne Module; ausschließlich absolute Imports mit `app.`-Präfix (z.B. `from app.core.config import get_settings`); keine relativen Imports
- **Datenklassen:** `dataclasses` für interne Service-Strukturen (z.B. `DicomMetadata`); `pydantic.BaseModel` für API-Schemas mit `ConfigDict(extra="forbid", from_attributes=True)`
- **Logging:** `structlog` ausschließlich (kein `print`); JSON in Produktion, ConsoleRenderer in Dev; Custom `_strip_pii`-Processor entfernt 6 bekannte PII-Keys aus Log-Events; Style: `logger.info("event_name", key=value)`
- **Naming:** `snake_case.py` für Dateien, `PascalCase` für Klassen, `snake_case` für Funktionen/Variablen, `UPPER_SNAKE_CASE` für Konstanten

### TypeScript / React
- **Linter:** ESLint 9 mit Flat Config (`eslint.config.js`): `@eslint/js`, `typescript-eslint`, `eslint-plugin-react-hooks`, `eslint-plugin-react-refresh`
- **Typ-Check:** `tsc --noEmit` (strict mode aktiv); `noUnusedLocals`, `noUnusedParameters`, `noFallthroughCasesInSwitch` enforced
- **Styling:** Tailwind CSS v4 mit Utility-Klassen; **keine** eigenen CSS-Dateien außer `index.css`; Dark Theme mit `slate-950` / `slate-100`; semantische Farbcodierung (`emerald`=niedrig, `amber`=mittel, `red`=hoch)
- **State:** Zustand global via Zustand (`store.ts`); Server-State via TanStack React Query (`useInference.ts`)
- **Pfad-Alias:** `@/*` mapped auf `src/*`
- **Komponenten:** Funktionskomponenten only; Props als `interface Props` direkt über der Komponente; Named Exports: `export function ComponentName({ ... }: Props)`; PascalCase-Verzeichnis mit gleichnamiger Datei: `AiPanel/AiPanel.tsx`
- **API-Client:** Dünner typed `fetch`-Wrapper in `lib/apiClient.ts`; injiziert immer `X-API-Key`; Base-URL via `import.meta.env.VITE_API_URL`; API-Prefix `/api/v1`; keine Roh-Fehler-Logs (PII-Vorsicht)
- **Naming:** `PascalCase.tsx` für Komponenten, `camelCase.ts` für Utilities/Hooks; Types/Interfaces `PascalCase`
- **UI-Text:** Deutsch; Code: Englisch

### Allgemein
- **Commits:** Englisch, imperative Form (`Add feature`, nicht `Added feature`)
- **Dateinamen:** `snake_case.py`, `PascalCase.tsx`, `kebab-case.yml`
- **Umgebungsvariablen:** Nie hardcoden; Backend via `pydantic-settings` (`get_settings` mit `@lru_cache`); Frontend via `import.meta.env`
- **API-Keys:** Mindestens 32 Zeichen (256-Bit-Entropie); im Backend via Pydantic-Validator in `app/core/config.py` geprüft

---

## Teststrategie

### Test-Pyramide
- **Unit / Schema:** `test_decision_tree_validation.py`, `test_config.py` — reine Pydantic-/Schema-Validierung, kein App-Kontext nötig
- **Integration:** `test_smoke.py`, `test_inference_full.py`, `test_anonymization_bridge.py`, `test_audit_trail.py`, `test_gradcam.py`, `test_pii_detection.py`, `test_transformers_pii_layer.py` — FastAPI via `httpx.AsyncClient` + `ASGITransport`, in-memory SQLite
- **Smoke-Tests:** Container bauen, Health-Check, kritische Pfade ohne externe Abhängigkeiten
- **ML-Tests:** `test_ml_pipeline.py`, `test_export_onnx.py`, `ml/models/test_mfsd_unet.py`, `ml/training/test_losses.py`, `ml/training/test_train.py`, `ml/data/test_dataset.py` — Import-Smoke und Modul-Logik
- **Utilities:** `test_model_signing.py`, `test_confidence_calibration.py`, `test_decision_tree_override.py` — Hilfs-Skript- und Service-Tests

### Test-Fixtures (`tests/conftest.py`)
- `test_client` (fixture) — Vollständiger `httpx.AsyncClient` mit initialisierter In-Memory-DB und Mock-Inference-Service; API-Key auf 32× `"a"` gesetzt
- `test_dicom_bytes` (fixture) — Minimal valide DICOM-Bytes (pydicom generiert, mit PII-Tags `PatientName`, `PatientID` zum Testen der Anonymisierung)
- `test_anonymized_dicom` (fixture) — DICOM-Bytes ohne PII-Tags
- `mock_inference_service` (fixture) — `MagicMock` mit deterministischem `PredictionResponse`

### Wichtige Test-Patterns
- **Async-first:** Alle Backend-Tests nutzen `pytest-asyncio` mit `asyncio_mode = auto` (konfiguriert in `pytest.ini`)
- **Auth-Testing:** Unauthentifizierte Requests explizit auf 401/403 geprüft
- **PII-Verifikation:** Anonymisierungstests prüfen Entfernung von `PatientName`, `PatientBirthDate`, `StudyDate`; Erhalt von `Modality`, `PixelData`, `Rows`, `Columns`
- **Determinismus:** Hash-Tests verifizieren stabile SHA-256-Ausgaben
- **Append-only Audit:** SQLAlchemy `before_update` / `before_delete` Event-Listener auf `AuditEvent` werfen `IntegrityError("append-only")` — explizit getestet
- **Boundary-Testing:** Parametrisierte Tests für Grenzwerte (Stenose 0.0–100.0; Trust-Score 1–5)

### Coverage
- **Schwelle: 75 %** (`--cov-fail-under=75`)
- Coverage-Report als XML-Artifact in CI

### CI-Pipeline (`.github/workflows/ci.yml`)
Getriggert auf: `push` zu `main`, `dev`; `pull_request` zu `main`

| Job | Tools |
|-----|-------|
| `lint` | `ruff check backend/app ml` + `black --check backend/app ml` + Frontend `npm run lint` + `npm run typecheck` |
| `test-backend` | `pytest` mit 75 %-Coverage-Gate + codecov-upload. Env: DEBUG=true, API_KEY, ADMIN_API_KEY, ANONYMIZATION_SALT |
| `test-ml` | `pytest ml/` mit 60 %-Coverage-Gate |
| `test-frontend` | `npm ci` → `npm run typecheck` → `npm run lint` → `npm test -- --run` (Vitest + jsdom + @testing-library, 12 Tests) |
| `security` | `bandit -r backend/app -ll` + Cloud-API-Verbot-Scan + `npm audit --audit-level=moderate` |
| `build` | `docker compose build` + Health-Check + `docker compose down` |

**Zusätzlicher Workflow:** `local_smoke.yml` — wöchentlich (Montags 05:00 UTC) Hermes-Agent Smoke-Test gegen Ollama-Container.

---

## Sicherheitsrichtlinien

### Local-First-Prinzip
- Patientendaten verlassen **niemals** den lokalen Rechner/Edge-Server
- Keine Cloud-Inferenz, kein Upload zu externen APIs
- SQLite ist die **einzige** erlaubte Datenbank: `DATABASE_URL`-Validator in `app/core/config.py` lehnt Nicht-SQLite-URLs explizit mit DSGVO/Local-First-Fehlermeldung ab
- DICOM-Dateien werden **in-memory** anonymisiert bevor Verarbeitung

### Anonymisierung (DICOM PS 3.15)
- `DicomService.parse_and_anonymise()` entfernt 33 PII-Tags (PatientName, PatientID, StudyDate, etc.)
- Roh-DICOM-Bytes verlassen die Parsing-Funktion nicht
- Audit-Trail speichert nur SHA-256-Hashes und numerische Werte

### API-Sicherheit
- `X-API-Key` Header-Auth für alle sensiblen Endpunkte via `fastapi.Security(APIKeyHeader)` in `app/core/security.py`
- `X-Admin-Key` für Audit-Endpunkte (`/audit/trail`, `/audit/anomalies`)
- Rate-Limiting via `slowapi` (`get_remote_address`):
  - `/api/v1/inference/predict`: 30/Minute
  - `/api/v1/decision-tree/*`: 60/Minute
- CORS via `cors_origins` (comma-separated String, validiert in Config)
- `allow_credentials=False`; erlaubte Methoden: `GET`, `POST`; erlaubte Header: `X-API-Key`, `X-Admin-Key`, `Content-Type`

### Datenbank-Sicherheit
- `AuditEvent`-Tabelle ist append-only (SQLAlchemy-Event-Listener blockieren UPDATE/DELETE mit `IntegrityError("append-only")`)
- Keine PII in SQLite — nur Hashes, numerische Werte, JSON-Payloads
- Retention: 25 Jahre (konfigurierbar via `audit_retention_years`)

### Container-Sicherheit
- Backend läuft als Non-Root-User (`carotis`)
- Frontend: nginx als unprivileged user
- Model-Verzeichnis im Container read-only (`:ro`)

### Logging-Sicherheit
- Custom `structlog`-Processor `_strip_pii` entfernt 6 bekannte PII-Keys aus jedem Log-Event
- Es werden niemals Roh-DICOM-Daten oder Patienten-IDs geloggt

### Modell-Integrität
- ONNX-Modelle werden optional via SHA-256 geprüft (`model_sha` in Config)
- Modell-Signing-Pipeline implementiert in `scripts/sign_model.py` + `scripts/verify_model.py`
  - Signatur-Hierarchie: cosign → GPG → SHA-256+Timestamp (Fallback)
  - Output: `.tar.gz` Bundle mit `model.onnx`, `meta.json`, `signature.json`
  - Verify prüft Bundle-Integrität, SHA-256-Match, Signatur und optionales Alter

---

## Bekannte Anomalien und technische Schulden

> Stand: 2026-04-30. Alle kritischen/hohen Punkte aus der vorherigen Session sind behoben. Verbleibende Punkte sind optional oder erfordern P1+ Kontext.

### ✅ Behoben in dieser Session (2026-04-30)

| Anomalie | Status | Fix |
|----------|--------|-----|
| Import-Mismatch in `audit_service.py` | ✅ FIXED | Kompletter Rewrite auf aktuelle Modelle (AuditEvent, DecisionTree, Inference) + PII-Strip |
| Orphaned `api/router.py` | ✅ FIXED | Datei entfernt (war Dead-Code) |
| `pytest.ini` referenziert nicht-existentes `backend/tests/` | ✅ FIXED | `backend/tests` aus `testpaths` entfernt |
| Fehlende Frontend-Tests | ✅ FIXED | Vitest + jsdom + @testing-library; 12 Tests; `npm test -- --run` gruen (kann bei jsdom/WASM haengen — Timeout 120s) |
| Doppelte/veraltete Frontend-Komponenten | ✅ FIXED | Alte `AIPanel.tsx`, `services/api.ts`, `types/api.ts` entfernt; einheitlicher Stack |
| ML-Modul `export_onnx.py` dupliziert | ✅ FIXED | Alte `ml/export_onnx.py` entfernt; `ml/inference/onnx_export.py` Bugfix (pretrained_swin entfernt); Tests + Skills aktualisiert |
| FastAPI/Starlette Versionskonflikt | ✅ FIXED | FastAPI 0.115.5 → 0.136.1 (Starlette 1.0.0 kompatibel) |
| sklearn Import-Reihenfolge vertauscht | ✅ FIXED | `_import_sklearn()` gab `(Isotonic, Logistic)` statt `(Logistic, Isotonic)` zurück |
| pytest DeprecationWarning als Fehler | ✅ FIXED | `ignore::DeprecationWarning:fastapi` in `pytest.ini` hinzugefügt |
| Fragile `parents[4]` Pfade | ✅ FIXED | `get_settings().project_root` in models.py, decision_tree_service.py, anonymization_service.py |
| DicomViewer Memory Leak | ✅ FIXED | `URL.revokeObjectURL()` + `crypto.randomUUID()` statt `Math.random()` |
| Dependencies.py Auth-Duplikat | ✅ FIXED | Re-export aus `security.py`, konsistente Signaturen |
| CSP `connect-src` hardcoded | ✅ FIXED | Config `csp_connect_src` in middleware.py |
| MCP-Trio B1-B5 Erweiterungen | ✅ DONE | Browser-MCP, Combined-MCP, Graphify Tags, Auto-Start, CI-Integration |

### 🟢 Niedrig: Keine Python-Tool-Konfigurationsdateien

- Es existieren keine `pyproject.toml`, `.ruff.toml` oder `.prettierrc`.
- `black`, `ruff`, `bandit` laufen mit Default-Konfiguration.
- **Hinweis:** `eslint.config.js` existiert für das Frontend (ESLint 9 Flat Config).

**Aktion (optional, P1-Readiness):** `pyproject.toml` mit `[tool.black]` und `[tool.ruff]` anlegen.

### 🟢 Niedrig: MCP-Server Setup

- Browser-MCP (`browser_mcp.py`) erfordert Playwright: `pip install playwright>=1.40 && playwright install chromium`
- Combined-MCP (`combined_mcp.py`) als Ressourcen-sparende Alternative zu 4 separaten Prozessen
- `run_loop.py pre` startet Hermes/Ollama automatisch wenn `CAROTIS_AUTO_START=1`
- CI-Job `test-mcp` in `.github/workflows/ci.yml` — läuft mit `--ignore-warn`

### 🟡 Mittel: Cornerstone3D Rendering-Pipeline

- `src/components/DicomViewer/DicomViewer.tsx` zeigt aktuell nur einen Platzhalter (kein echtes Cornerstone3D-Rendering in der Produktions-Build).
- WASM-Module sind externalized (erwartete Vite-Warnung); Chunk-Size > 500 kB.

**Aktion (P3):** Cornerstone3D-Initialisierung (WASM-Loader, Rendering-Pipeline) implementieren und E2E-Test mit echtem DICOM.


---

## Datei-Index (Root-Level)

| Datei | Zweck |
|------|-------|
| [`00_INDEX.md`](00_INDEX.md) | Projekt-Einstieg — Szenarien und How-To |
| [`01_HARNESS.md`](01_HARNESS.md) | Modell-Routing-Matrix, DoD-Format, Eskalation |
| [`02_ROADMAP.md`](02_ROADMAP.md) | Phasen P0–P7 (24-Monats-Plan) |
| [`03_PROMPT_TEMPLATES.md`](03_PROMPT_TEMPLATES.md) | 9 Copy-Paste-Prompts für alle Use-Cases |
| [`04_MASTER_PLAN.md`](04_MASTER_PLAN.md) | Architektur-Diagramm + Stakeholder-Map + Risiken |
| [`05_DECISION_TREE_HARVESTING.md`](05_DECISION_TREE_HARVESTING.md) | JSON-Schema für ärztliche Entscheidungen |
| [`06_ROHDE_MEETING_KIT.md`](06_ROHDE_MEETING_KIT.md) | Meeting-Vorbereitung für Prof. Rohde |
| [`07_OFFICE_AGENT_PROMPTS.md`](07_OFFICE_AGENT_PROMPTS.md) | Stride-Prompts A–H für Office-Doc-Updates |
| [`08_RESEARCH_ATTENTION_2020-2026.md`](08_RESEARCH_ATTENTION_2020-2026.md) | Literatur-Inventar (27+ Papers) |
| [`09_COPILOT_PROMPT_SEQUENCE.md`](09_COPILOT_PROMPT_SEQUENCE.md) | GitHub Copilot Prompt-Sequenz |
| [`09b_KIMI_PROMPT_SEQUENCE.md`](09b_KIMI_PROMPT_SEQUENCE.md) | Kimi Prompt-Sequenz |
| [`tasks.jsonl`](tasks.jsonl) | Maschinenlesbare P0-Task-Liste (T-001 bis T-024) |
| [`CLAUDE.md`](CLAUDE.md) | Working Memory, People, Stack, Phase-Status |
| [`MEMORY.md`](MEMORY.md) | Index aller Langzeit-Memory-Dateien |
| [`memory/`](memory/) | Run-Logs, Entscheidungen, Anomalien, Domänenwissen |
| [`ethics/`](ethics/) | Ethikantrag-Skelett, Einwilligungserklärung, DPIA-Skelett |
| [`regulatory/`](regulatory/) | ADRs, Risk-Register |
| [`schemas/`](schemas/) | JSON-Schema + Sample für Decision-Tree |

---

## Run-Log-Format (am Session-Ende schreiben)

```markdown
---
name: <YYYY-MM-DD>_<model>_<kurzes-thema>
type: run
---
## Goal
## Done
## Surprised by
## Avoided
## Next
## Memory updates
```

Speicherort: `memory/runs/<YYYY-MM-DD>_<sessionID>.md`  
Zeiger-Zeile in [`MEMORY.md`](MEMORY.md) ergänzen.

---

*Letztes Update: 2026-04-30 v3 · AGENTS.md: 10/10 Anomalien FIXED (audit_service, orphaned router, pytest.ini, Frontend-Tests, Frontend-Cleanup, export_onnx, FastAPI/Starlette, sklearn, parents[4], DicomViewer, dependencies.py, CSP). Test-Baseline: 105 passed/0 failed/11 skipped + Frontend 12 passed. MCP-Trio B1-B5 DONE. Deploy-Blocker: FLY_API_TOKEN, SSH Hetzner, INWX DNS. ULTRAPLAN.md v4 ist Master-Referenz fuer Tools + MCP-Server.*
