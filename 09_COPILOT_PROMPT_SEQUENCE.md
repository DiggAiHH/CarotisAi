# 09_COPILOT_PROMPT_SEQUENCE — VS Code Copilot Chat Prompts

> **Zweck:** Lou kopiert die Prompts unten **eins nach dem anderen** (oder parallel, wo markiert) in Copilot Chat in VS Code. Jeder Prompt ist self-contained — kein Kontext-Vorwissen nötig. Modell-Empfehlung pro Prompt steht im Header.
>
> **Quota-Strategie:** Sonnet 4.6 ist Default für Engineering-Arbeit. Codex GPT-5.3 für Python-schwere ML-Pipelines. GPT-4.1 für mechanische Edits (billig). Bei jedem Prompt steht, was zu wählen ist.
>
> **Theoretische Basis:** Jake van Clief — *Interpretable Context Methodology / Model Workspace Protocol* (arXiv 2603.16021). Numbered Folders = Stages, Markdown = Prompts, Scripts = mechanische Arbeit. Filesystem ersetzt Framework-Orchestrierung.
>
> **Local-AI-Stack:** Ollama (`localhost:11434`) als Inference-Endpoint + Hermes Agent (Nous Research) als Self-Improving-Layer + caveman/caveman-compress für Token-Budget. Diese Konfiguration ist **wiederverwendbar** für jedes lokal gehostete OSS-Projekt — die Struktur in `code/` bleibt identisch, nur das Modell hinter `localhost:11434` wechselt.

---

## Setup vor dem ersten Prompt (5 Min)

1. VS Code öffnen.
2. Workspace: `C:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI\code`
3. **Reference-Files in Copilot Chat als Kontext anhängen** (per `@workspace` oder Drag-Drop in den Chat):
   - `../CLAUDE.md`
   - `../MEMORY.md`
   - `../05_DECISION_TREE_HARVESTING.md`
   - `../schemas/decision_tree.schema.json`
   - `../regulatory/risk_register.md`
   - `../regulatory/adr/ADR-0001-local-first.md`
   - `../regulatory/adr/ADR-0002-decision-tree-harvesting.md`
4. Bei jedem Prompt: zuerst Modell oben rechts im Copilot-Chat wechseln, **dann** Prompt einfügen.

---

## Reihenfolge auf einen Blick

```
                                                         legend: [S]=sequential blockt unten · [P]=parallel safe
┌──────────────────────────────────────────────────────────────────────────────────┐
│  STAGE A — Onboarding (BLOCKS everything)                                        │
│  [S] P-01 → .github/copilot-instructions.md     · Sonnet 4.6                     │
└──────────────────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────────────────┐
│  STAGE B — Code-Memory (alle parallel)                                           │
│  [P] P-02 → code/CLAUDE.md                       · Sonnet 4.6                    │
│  [P] P-03 → code/HARNESS.md                      · Sonnet 4.6                    │
│  [P] P-04 → code/AGENTS.md (Hermes-Spec)         · Sonnet 4.6                    │
│  [P] P-05 → code/MEMORY.md (Index)               · GPT-4.1                       │
└──────────────────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────────────────┐
│  STAGE C — Infrastructure (alle parallel)                                        │
│  [P] P-06 → code/docker-compose.yml + Ollama      · Sonnet 4.6                   │
│  [P] P-07 → code/backend/.env.example             · GPT-4.1                      │
│  [P] P-08 → code/scripts/install_local_stack.sh   · Sonnet 4.6                   │
│  [P] P-09 → code/scripts/install_local_stack.ps1  · GPT-4.1 (port von P-08)      │
└──────────────────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────────────────┐
│  STAGE D — Backend (sequenziell innerhalb, parallel zu E + F)                    │
│  [S] P-10 → code/backend/app/core/config.py       · Codex 5.3                    │
│  [S] P-11 → code/backend/app/db/                  · Codex 5.3                    │
│  [S] P-12 → code/backend/app/services/            · Codex 5.3                    │
│  [S] P-13 → code/backend/app/api/                 · Codex 5.3                    │
│  [S] P-14 → code/backend/app/main.py (factory)    · Sonnet 4.6                   │
└──────────────────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────────────────┐
│  STAGE E — Frontend (parallel zu D + F)                                          │
│  [P] P-15 → code/frontend/src/main.tsx + App      · Sonnet 4.6                   │
│  [P] P-16 → code/frontend/src/components/Viewer   · Sonnet 4.6                   │
│  [P] P-17 → code/frontend/src/components/AIPanel  · Sonnet 4.6                   │
│  [P] P-18 → code/frontend/src/components/DTForm   · Sonnet 4.6                   │
└──────────────────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────────────────┐
│  STAGE F — ML Pipeline (parallel zu D + E)                                       │
│  [P] P-19 → code/ml/data/dataset.py               · Codex 5.3                    │
│  [P] P-20 → code/ml/models/mfsd_unet.py           · Codex 5.3                    │
│  [P] P-21 → code/ml/training/losses.py            · Codex 5.3                    │
│  [P] P-22 → code/ml/training/train.py             · Codex 5.3                    │
│  [P] P-23 → code/ml/export_onnx.py                · Codex 5.3                    │
└──────────────────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────────────────┐
│  STAGE G — Tests + CI (sequentiell nach D/E/F)                                   │
│  [S] P-24 → code/tests/ erweitern                 · Sonnet 4.6                   │
│  [P] P-25 → code/.github/workflows/ci.yml         · Sonnet 4.6                   │
│  [P] P-26 → code/.github/workflows/local_smoke.yml · GPT-4.1                     │
└──────────────────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────────────────┐
│  STAGE H — Hermes Integration + Demo                                             │
│  [P] P-27 → code/hermes/config.toml               · Sonnet 4.6                   │
│  [P] P-28 → code/hermes/skills/ (3 Skills)        · Sonnet 4.6                   │
│  [S] P-29 → code/scripts/demo.sh erweitern        · Sonnet 4.6                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

**Parallelisierungs-Strategie für deine 2 Tage:**
- **Tag 1 vormittags:** Stage A (eine Tab) → dann Stage B + C in 4–5 parallelen Tabs
- **Tag 1 nachmittags:** Stage D + E + F in 3 parallelen Tabs (verschiedene Sub-Verzeichnisse → kein Merge-Konflikt)
- **Tag 2 vormittags:** Stage G + H
- **Tag 2 nachmittags:** Smoke-Test mit `bash scripts/demo.sh` + `bash scripts/preflight.sh`

---

## STAGE A — Onboarding

### P-01 · `.github/copilot-instructions.md` · Sonnet 4.6 · [BLOCKS ALL]

**Was es tut:** GitHub Copilot lädt diese Datei bei jedem Chat-Aufruf in `code/` automatisch als System-Kontext. Ohne sie sind alle weiteren Prompts kontext-blind. **Erst diese Datei, dann alles andere.**

```
Erstelle die Datei .github/copilot-instructions.md im aktuellen Workspace 
(code/-Verzeichnis von Carotis-AI).

Diese Datei wird von GitHub Copilot bei jedem Chat-Request automatisch geladen 
und definiert das Projekt-Verständnis für jede künftige Code-Generierung.

INHALT:

# Carotis-AI — Copilot Project Instructions

## Project
Local-First, DSGVO-konformes Clinical Decision Support System für die 
Carotis-Stenose-Quantifizierung aus CTA-Bildern. Promotionsprojekt am 
Klinikum Dortmund (Aroob Alrawashdeh, Betreuer Prof. Dr. Stefan Rohde). 
Innovation: Decision-Tree-Harvesting — Modell lernt die ärztliche Begründung, 
nicht nur das Bild. Spec: ../05_DECISION_TREE_HARVESTING.md

## Stack
- Backend: Python 3.11 + FastAPI + Pydantic v2 + SQLAlchemy async + ONNX 
  Runtime + structlog + Prometheus
- Frontend: React 19 + Vite + TypeScript + Tailwind v4 + Cornerstone.js 
  DICOM viewer + Zustand + TanStack Query
- ML: PyTorch 2.5 + MONAI + timm (Swin Transformer) + grad-cam + MLflow + 
  ONNX export
- Local AI: Ollama (localhost:11434) + Hermes Agent (Nous Research) + 
  caveman compression
- Infrastructure: Docker Compose, kein Cloud-Provider für Patientendaten

## Hard Rules (NICHT verhandelbar)
1. Local-First: KEIN Cloud-API-Call für Patientendaten. Ausnahme nur bei 
   bereits anonymisierten aggregierten Modell-Updates. Siehe 
   ../regulatory/adr/ADR-0001-local-first.md
2. Anonymisierung: jeder Patientendaten-Pfad nutzt scripts/anonymize.py 
   (DICOM PS 3.15 + k-Anonymity ≥ 5). Niemals direkter Zugriff auf 
   PII-Felder.
3. Audit-Trail: jede AI-Inferenz und jede Arzt-Entscheidung wird mit 
   timestamp + model_version + model_sha geloggt.
4. Schema-First: alle Daten-Strukturen werden in JSON Schema 2020-12 
   definiert (siehe schemas/decision_tree.schema.json) BEVOR der Code 
   geschrieben wird.
5. Tests: jede Funktion in app/services/ und ml/ braucht mind. 1 pytest. 
   Funktionen mit Patientendaten-Pfad: 100% Coverage.
6. UI-Sprache: Deutsch (Klinikum-Setting). Code-Kommentare + Commit-
   Messages: Englisch.

## Conventions
- Imports: Python — absolute imports vom Package-Root (`from app.services 
  import ...`); TypeScript — `@/...` Alias auf src/
- Type-Hints: Python `from __future__ import annotations` immer. Pydantic 
  v2 BaseModel statt @dataclass für API-Schemas.
- Error-Handling: nie bare `except:`. Strukturierte Errors via 
  custom Exception-Klassen in app/core/exceptions.py.
- Logging: structlog mit `bind()` für Request-Context. Niemals `print()`. 
  Niemals PII in Logs.
- Tests: pytest + pytest-asyncio + httpx AsyncClient. Fixtures in 
  conftest.py.

## Architecture Decisions (lies BEVOR du Architektur änderst)
- ADR-0001 Local-First: ../regulatory/adr/ADR-0001-local-first.md
- ADR-0002 Decision-Tree-Harvesting: ../regulatory/adr/ADR-0002-decision-tree-harvesting.md

## Risk Register
Bevor du etwas an Anonymisierung, Audit-Trail oder Daily-Learning-Loop 
änderst: ../regulatory/risk_register.md lesen. Hazards H-001, H-002, 
H-003, H-006 sind compliance-kritisch.

## Engineering Harness
Übergeordneter Workspace: ../ (das Projekt-Root). 
- ../CLAUDE.md = working memory aller Modelle
- ../MEMORY.md = Index aller Memorys
- ../memory/runs/ = Run-Logs (jede Session schreibt einen)
- ../memory/anomalies/ = bekannte Stolpersteine — vor Code-Änderung lesen

Methodologie: Jake van Clief — Interpretable Context Methodology (MWP). 
Filesystem-Struktur ist die Agent-Architektur. Wenn unklar wo etwas 
hingehört: Numbered-Folder-Convention beachten und in ../00_INDEX.md 
nachschauen.

## When in Doubt
- Architektur-Frage → ADR schreiben unter ../regulatory/adr/
- Patientendaten-Pfad → STOP, an Lou eskalieren
- Schema-Änderung → schemas/ Schema zuerst aktualisieren, dann Code
- Memory-Konflikt → ../memory/anomalies/ lesen
- Modell-Wahl im Routing → ../01_HARNESS.md Routing-Matrix

REGELN für die Generierung dieser Datei:
- Genau diesen Text mit den korrekten relativen Pfaden
- Markdown-Format
- Headings auf Englisch (Industry-Standard für Copilot-Instructions)
- Keine Auslassungen
```

**Verify:**
```bash
cat .github/copilot-instructions.md | head -20
```

**DoD:** Datei existiert, mind. 100 Zeilen, alle relativen Pfade gelesen-OK.

---

## STAGE B — Code-Memory (alle parallel)

### P-02 · `code/CLAUDE.md` · Sonnet 4.6 · [PARALLEL mit P-03/04/05]

```
Erstelle code/CLAUDE.md — die working memory für jede Code-Session in 
diesem Verzeichnis. Bezieht sich auf das übergeordnete ../CLAUDE.md 
(Master) aber fokussiert auf Code-spezifische Regeln.

Struktur:
1. Header mit Verweis auf ../CLAUDE.md (Master) und ../00_INDEX.md (Tour)
2. AI Mode — Engineering Harness (übernehmen aus ../CLAUDE.md, leicht 
   gekürzt)
3. Sub-Project: code/ ist das Implementierungs-Verzeichnis innerhalb des 
   Carotis-AI-Workspaces.
4. Stack (kurz): backend/ (FastAPI + ONNX), frontend/ (React 19 + 
   Cornerstone), ml/ (PyTorch + MONAI), hermes/ (Nous Research Agent + 
   Ollama), scripts/ (Bootstrap + Demo + Anonymisierung)
5. Critical Path: data anonymisiert → ML trainiert → ONNX exportiert → 
   Backend lädt ONNX → Frontend ruft Backend → Decision-Tree wird 
   captured → Daily-Loop trainiert nach
6. Pre-Flight für Code-Sessions:
   ```bash
   ../scripts/preflight.sh
   git status
   pytest -q                 # Smoke
   ```
7. Verbote:
   - Keine Cloud-API-Calls auf Patientendaten
   - Keine print() statt structlog
   - Keine bare except
   - Kein Schema-Bypass (jedes Daten-Objekt validiert sich gegen 
     schemas/)
   - Kein direkter Edit von Office-Files (siehe 
     ../memory/domain/fb_office_docs.md)
8. Last-Update Footer.

Halte die Datei < 200 Zeilen. Kürzer ist besser. Sonnet 4.6 spricht 
flüssiges Caveman — drop fluff, technical exact, code unchanged.
```

**Verify:** `wc -l code/CLAUDE.md` < 200.

---

### P-03 · `code/HARNESS.md` · Sonnet 4.6 · [PARALLEL]

```
Erstelle code/HARNESS.md — der Local-AI-Harness für Code-Generation 
INNERHALB von code/. Spezialisiert auf den Hermes+Ollama+Caveman-Stack, 
nicht auf Anthropic Claude.

Struktur:

## Goldene Regel
Wir nutzen drei Modelle, nicht eins:
1. **Cloud-Claude** (Opus / Sonnet via Anthropic API): für Architektur 
   + Code-Review (begrenzte Kontingente)
2. **Local-Hermes** (auf Ollama, llama-3.3-70b-instruct oder 
   nous-hermes-3-llama-3.1): für Tool-Use + Memory + Skills (unbegrenzt 
   lokal)
3. **Local-Caveman** (qwen2.5-coder:7b oder ähnlich): für Token-Compression 
   + Boilerplate-Code (sehr schnell, sehr klein)

## Routing-Matrix für code/
| Aufgabe | Modell | Endpoint |
|---|---|---|
| ADR / Architektur-Entscheidung | Cloud-Claude Opus | api.anthropic.com |
| Code-Review vor Merge | Cloud-Claude Sonnet | api.anthropic.com |
| Implementation einer Komponente nach Spec | Hermes via Ollama | localhost:11434 |
| Boilerplate (i18n, getter/setter, type defs) | Caveman via Ollama | localhost:11434 |
| Memory-Updates / Run-Logs | Hermes | localhost:11434 |
| Compression von Memory-Files (caveman-compress) | Caveman | localhost:11434 |
| GitHub Copilot Code-Completion | gpt-5 / sonnet-4.6 (im IDE) | github.com |

## Hermes Setup
1. Ollama installieren (siehe scripts/install_local_stack.sh)
2. Modelle ziehen: ollama pull nous-hermes-3-llama-3.1, ollama pull 
   qwen2.5-coder:7b
3. Hermes Agent: pip install hermes-agent (siehe hermes/config.toml)
4. Hermes startet auf localhost:8200 (Default), nutzt Ollama als 
   Backend

## Caveman Compression
Memory-Files können > 5k Token werden. Vor jeder Session:
```bash
hermes compress --input ../CLAUDE.md --output ../CLAUDE.compressed.md \
  --model qwen2.5-coder:7b --target-tokens 1500
```
Erspart 40-60% Input-Tokens bei minimalem Informationsverlust.

## Wann welches Modell — Decision Flow
[Mermaid-Diagramm einbauen]

## Workflow innerhalb von Code-Sessions
1. Pre-Flight (siehe code/CLAUDE.md)
2. Lese MEMORY.md + HARNESS.md
3. Wähle Modell nach Routing-Matrix
4. Wenn Cloud-Modell: Quota beachten (3% verbleibend für deinen Plan)
5. Wenn Local: starte Ollama vorher (`ollama serve` in Background)
6. Implementiere
7. Test
8. Run-Log in ../memory/runs/<datum>_<modell>_<thema>.md

## Wiederverwendbarkeit
Diese Struktur ist NICHT carotis-spezifisch. Für jedes andere lokal 
gehostete OSS-Projekt: kopiere code/HARNESS.md, code/AGENTS.md, 
code/hermes/, code/scripts/install_local_stack.* — der Rest ist 
Drop-in. Modelle hinter localhost:11434 austauschbar.

## Quellen
- Jake van Clief, Interpretable Context Methodology (arXiv 2603.16021)
- Hermes Agent: https://github.com/NousResearch/hermes-agent
- Ollama: https://ollama.com

REGEL: Halte die Datei < 250 Zeilen. Praktisch, nicht prosaisch.
```

---

### P-04 · `code/AGENTS.md` (Hermes-Spec) · Sonnet 4.6 · [PARALLEL]

```
Erstelle code/AGENTS.md — das ist die Spec für den Hermes-Agent + die 
Skills + die Tool-Permissions. Datei wird von Hermes beim Boot geladen 
(via hermes/config.toml).

Inhalt:

## Agent-Identität
- Name: carotis-helper
- Modell: nous-hermes-3-llama-3.1 (Default), Override via 
  HERMES_MODEL env var
- Endpoint: http://localhost:11434 (Ollama)
- Kontextfenster: 32k Token, comprimiert via caveman wenn > 24k

## Persistente Memory
Hermes liest beim Start:
- ../CLAUDE.md (Master Working Memory)
- ../MEMORY.md (Memory-Index)
- code/CLAUDE.md (Code-Specific)
- letzte 3 Files in ../memory/runs/

Schreibt nach jeder Session: ../memory/runs/<datum>_hermes_<thema>.md

## Skills (3 zentrale)

### Skill 1: anonymize-batch
Trigger: "Anonymisiere DICOM-Batch in <pfad>"
Aktion: Ruft scripts/anonymize.py mit den korrekten Argumenten + 
checked DSGVO-Compliance + schreibt Manifest.

### Skill 2: capture-decision-tree
Trigger: "Erfasse Arzt-Entscheidung für Fall <id>"
Aktion: Validiert gegen schemas/decision_tree.schema.json + schreibt 
in memory/decisions/

### Skill 3: nightly-retrain
Trigger: "Trainiere Modell mit neuen Decision-Trees"
Aktion: Liest memory/decisions/, validiert, ruft ml/training/train.py 
mit incremental=true, vergleicht Performance, pusht bei Verbesserung 
≥ 0.1 % via signiertem Bundle.

## Tool-Permissions (allowlist)
- read: ../**, code/**, schemas/**
- write: memory/**, data/anonymized/**, models/**
- execute: scripts/anonymize.py, scripts/preflight.sh, ml/training/*
- DENIED: Cloud-API-Endpoints (Anthropic, OpenAI, etc.) für 
  Patientendaten. Cloud-LLMs nur für aggregierte Reports.

## Self-Improvement-Loop
Hermes lernt aus seinen eigenen Run-Logs. Wöchentlich:
- liest memory/runs/ der letzten 7 Tage
- identifiziert wiederholte Fehler
- generiert neue Skill oder Memory-Update
- speichert Vorschlag in memory/proposals/<datum>.md
- Lou approved oder rejected

## Konfiguration im Detail
Siehe hermes/config.toml.

REGELN: Datei < 200 Zeilen. Klar strukturiert. Hermes-Doku-Style 
(siehe hermes-agent.nousresearch.com/docs).
```

---

### P-05 · `code/MEMORY.md` (Index) · GPT-4.1 · [PARALLEL]

```
Erstelle code/MEMORY.md als Index aller code-spezifischen 
Memory-Files (nicht zu verwechseln mit ../MEMORY.md, das ist der 
Master).

Inhalt:

# code/MEMORY.md — Code-Subproject Memory Index

> Index aller code/-spezifischen Memorys. Master-Index ist ../MEMORY.md.

## Pointer auf Master-Files
- [../CLAUDE.md](../CLAUDE.md) — Master Working Memory
- [../MEMORY.md](../MEMORY.md) — Master Memory Index
- [../00_INDEX.md](../00_INDEX.md) — Tour

## Code-Memorys (in code/memory/)
_Werden bei jeder Code-Session gefüllt._

## Konventionen
- Code-spezifische Run-Logs: code/memory/runs/<datum>_<modell>_<thema>.md
- Code-spezifische Anomalien: code/memory/anomalies/<datum>_<bug>.md  
- Master-Memorys (Project, User, Refs) bleiben im Root unter ../memory/

## Wartung
- Bei jeder Code-Session: 1 Run-Log
- Bei Bug-Fix: 1 Anomaly-Eintrag
- Wöchentlich: Hermes wertet aus, schlägt vor

REGELN: Datei < 80 Zeilen. Reiner Index.
```

**Nach P-02 bis P-05 — Stage B done:** Du kannst jetzt mit Stage C parallel weiter.

---

## STAGE C — Infrastructure (alle parallel)

### P-06 · `code/docker-compose.yml` mit Ollama · Sonnet 4.6 · [PARALLEL]

```
Erstelle code/docker-compose.yml mit den folgenden Services:

services:
  ollama:
    - Image: ollama/ollama:latest
    - Volume: ollama-models:/root/.ollama (persistent für gepullte Modelle)
    - Port: 11434:11434
    - GPU: optional via deploy.resources.reservations.devices wenn nvidia
    - Environment: OLLAMA_HOST=0.0.0.0
    - Health-Check: curl localhost:11434/api/tags
  
  hermes:
    - Build: hermes/Dockerfile (siehe P-27)
    - depends_on: ollama (healthy)
    - Volume: ../memory:/app/memory:rw
    - Volume: ../schemas:/app/schemas:ro
    - Environment: HERMES_OLLAMA_URL=http://ollama:11434, HERMES_MODEL=nous-hermes-3-llama-3.1
    - Port: 8200:8200
  
  backend:
    - Build: backend/Dockerfile
    - depends_on: ollama (healthy)
    - Volume: ./data:/data:rw
    - Volume: ../scripts/anonymize.py:/app/scripts/anonymize.py:ro
    - Environment: aus backend/.env (siehe P-07)
    - Port: 8000:8000
    - Health-Check: curl localhost:8000/health
  
  frontend:
    - Build: frontend/Dockerfile
    - depends_on: backend
    - Port: 3000:3000
    - Environment: VITE_API_URL=http://backend:8000

volumes:
  ollama-models:

REGELN:
- Network: alle Services im internen Netz "carotis-net" (kein 
  externer Internet-Pfad für ollama/hermes/backend)
- Frontend hat externes Internet (für Cornerstone-CDN-Fallback) — 
  aber kein Patientendaten-Pfad
- Healthchecks sind Pflicht
- depends_on mit condition: service_healthy
```

---

### P-07 · `code/backend/.env.example` · GPT-4.1 · [PARALLEL]

```
Erstelle code/backend/.env.example mit allen Konfigurations-Variablen 
für die FastAPI-App. Mit Kommentaren pro Variable.

Variablen:
# --- API Auth ---
API_KEY=change-me-min-32-chars-via-doppler

# --- Database (Local SQLite, KEIN Cloud) ---
DATABASE_URL=sqlite+aiosqlite:///./data/carotis.db

# --- ONNX Model ---
ONNX_MODEL_PATH=/data/models/mfsd_unet.onnx
MODEL_VERSION=v0.3.2
MODEL_SHA=abc123d  # ergänzt durch CI

# --- Ollama / Hermes ---
OLLAMA_URL=http://ollama:11434
HERMES_URL=http://hermes:8200
DEFAULT_LOCAL_MODEL=nous-hermes-3-llama-3.1
COMPRESSION_MODEL=qwen2.5-coder:7b

# --- Anonymisierung ---
ANONYMIZATION_SALT=change-me-via-doppler-salt-rotation-quartal
ANONYMIZATION_SALT_VERSION=v2026-04
MIN_K_ANONYMITY=5

# --- Audit-Trail ---
AUDIT_DB_PATH=/data/audit.db
AUDIT_RETENTION_YEARS=25  # MDR-konform

# --- Logging ---
LOG_LEVEL=INFO
LOG_FORMAT=json  # structlog json output für Aggregation

# --- CORS ---
CORS_ORIGINS=http://localhost:3000,http://frontend:3000

# --- Feature Flags ---
ENABLE_DECISION_TREE_CAPTURE=true
ENABLE_DAILY_LEARNING_LOOP=false  # bis P5 deaktiviert
ENABLE_GRAD_CAM_OVERLAY=true

# --- Dev only ---
DEBUG=false
RELOAD=false

REGEL: NIEMALS echte Secrets in dieser Datei. Nur Platzhalter.
```

---

### P-08 · `code/scripts/install_local_stack.sh` · Sonnet 4.6 · [PARALLEL]

```
Erstelle code/scripts/install_local_stack.sh — installiert Ollama, 
zieht die Modelle, installiert Hermes Agent. Idempotent (kann 
mehrfach laufen).

Schritte:
1. Detect OS (linux/macos)
2. Ollama installieren falls nicht da: curl -fsSL https://ollama.com/install.sh | sh
3. Ollama-Service starten falls nicht läuft
4. Modelle pullen (ollama pull):
   - nous-hermes-3-llama-3.1 (Hermes-Agent-fähig)
   - qwen2.5-coder:7b (caveman-compression)
   - llava-llama3:8b (multimodal optional)
   Mit Skip-If-Already-Pulled-Logik.
5. Python venv erstellen falls nicht da
6. pip install hermes-agent (vom Nous-Research-Repo)
7. Hermes initialisieren mit der Config aus hermes/config.toml
8. Verify: curl localhost:11434/api/tags listet die Modelle, hermes ping 
   antwortet
9. Output: Setup-Summary

Style: bash strict mode (set -euo pipefail), Farb-Codes für 
banner/step/ok/fail (übernimm aus scripts/preflight.sh).

REGELN:
- Niemals sudo ohne explizite User-Bestätigung
- Wenn Ollama auf Port 11434 schon läuft (anderer Service): warne 
  und exit
- Logge alles in /tmp/install_local_stack.log
- 30-Min-Timeout für Modell-Pulls (Hermes-FAQ: lokal lange Prefill)
```

---

### P-09 · `code/scripts/install_local_stack.ps1` · GPT-4.1 · [PARALLEL]

```
Portiere code/scripts/install_local_stack.sh auf PowerShell. Ziel: 
identische Funktionalität auf Windows.

Spezifika:
- Ollama-Installer für Windows: https://ollama.com/download/OllamaSetup.exe 
  download + silent install
- Test-Path / Get-Service für Ollama-Service-Detection
- Set-ExecutionPolicy nicht ändern (sondern script signed oder mit 
  -ExecutionPolicy Bypass aufrufen)
- $ErrorActionPreference = "Stop"
- Farb-Codes via Write-Host -ForegroundColor

Zusätzlich: Hinweis im Header dass das Skript via:
   PowerShell -ExecutionPolicy Bypass -File scripts/install_local_stack.ps1
gestartet werden muss.
```

---

## STAGE D — Backend (sequenziell innerhalb)

### P-10 · `code/backend/app/core/config.py` · Codex 5.3 · [SEQUENTIAL within D]

```
Erstelle code/backend/app/core/config.py mit Pydantic-Settings v2 
basierend auf code/backend/.env.example.

Klasse Settings(BaseSettings):
- alle Variablen aus .env.example als typed fields
- Validators:
  - API_KEY: min_length=32
  - MIN_K_ANONYMITY: ge=5
  - LOG_LEVEL: in [DEBUG, INFO, WARNING, ERROR]
  - DATABASE_URL: must startwith "sqlite" (kein Cloud-DB-Connection-String)
- model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", 
  extra="ignore")
- get_settings() mit @lru_cache für FastAPI dependency injection

Plus: Pytest-Tests in code/backend/tests/test_config.py mit:
- Test happy path
- Test API_KEY too short → ValidationError
- Test min_k < 5 → ValidationError
- Test get_settings cached

REGEL: alle Defaults aus .env.example. Keine hardgecodeten Secrets.
```

---

### P-11 · `code/backend/app/db/` · Codex 5.3 · [SEQUENTIAL]

```
Erstelle code/backend/app/db/ mit folgenden Files:

database.py:
- Async SQLAlchemy engine + sessionmaker
- init_db() async function (für lifespan + tests)
- get_db() async generator für FastAPI dependency

models.py — SQLAlchemy ORM-Klassen:
- Inference (id, case_id, captured_at, ai_prediction_json, model_version, 
  model_sha, audit_id)
- DecisionTree (id, case_id, captured_at, physician_role_hash, 
  data_json (Validated gegen schemas/decision_tree.schema.json), 
  agreement_verdict)
- AuditEvent (id, timestamp, event_type, actor, payload_json) — append-only

Constraints:
- Alle ids: UUID4
- Alle timestamps: UTC
- case_id: indexed, unique pro DecisionTree
- AuditEvent: niemals UPDATE oder DELETE — erzwungen via SQLAlchemy event listener

Plus: alembic Migration für initial schema.

Tests in code/backend/tests/test_db.py:
- Test init_db erstellt alle Tabellen
- Test AuditEvent insert OK + UPDATE/DELETE → IntegrityError
- Test DecisionTree.data_json validiert gegen Schema beim Insert

REGEL: pure SQLite (aiosqlite). Kein Postgres. Kein Cloud-DB.
```

---

### P-12 · `code/backend/app/services/` · Codex 5.3 · [SEQUENTIAL]

```
Erstelle code/backend/app/services/ mit drei Service-Klassen:

inference_service.py:
- InferenceService Klasse
- __init__(model_path: str): lädt ONNX-Modell mit onnxruntime
- async predict(dicom_bytes: bytes) -> InferenceResult
  - DICOM dekodieren mit pydicom
  - Anonymisierungs-Check: prüft dass das DICOM bereits anonymisiert ist 
    (alle 33 PII-Tags absent), sonst ValueError
  - Preprocessing: 512x512 normalize
  - Inferenz
  - Postprocessing: Sigmoid → Stenosegrad %, Vulnerability-Vektor
  - Grad-CAM heatmap (via grad-cam Lib oder eigener Hook)
  - Audit-Event schreiben
  - Return InferenceResult Pydantic Model

anonymization_service.py:
- AnonymizationService Klasse
- async ensure_anonymized(dicom_bytes) — wrapper um scripts/anonymize.py
- check_only(dicom_bytes) -> bool — prüft ob anonymisiert ohne zu 
  schreiben

decision_tree_service.py:
- DecisionTreeService Klasse
- async capture(case_id, physician_role_hash, payload: dict) -> str
  - Validiert payload gegen schemas/decision_tree.schema.json (jsonschema)
  - Schreibt in DB
  - Schreibt zusätzlich in memory/decisions/<datum>_<hash>.json
  - Return audit_id
- async list_for_review(since: datetime) -> list[DecisionTree]
- async detect_disagreements(window_days: int) -> list — für wöchentliches 
  Anomaly-Triage

Tests:
- Mock ONNX-Modell für InferenceService
- Test anonymization_check rejects DICOM mit Patient Name
- Test decision_tree_service akzeptiert valide Payload, lehnt invalide ab

REGEL: jede Service-Methode ist async. structlog für jedes log. Keine 
prints.
```

---

### P-13 · `code/backend/app/api/` · Codex 5.3 · [SEQUENTIAL]

```
Erstelle code/backend/app/api/ mit folgenden Routern (FastAPI APIRouter):

routes/health.py:
- GET /health → {status, model_loaded, db_ok, timestamp}
- Public, kein Auth

routes/inference.py:
- POST /inference/predict
  - Multipart Upload eines DICOM-Files
  - Auth via API_KEY Header
  - Rate-Limit: 30 Requests/Minute pro API_KEY (slowapi)
  - Ruft inference_service.predict()
  - Return PredictionResponse Schema

routes/decision_tree.py:
- POST /decision-tree/capture
  - JSON-Body validiert gegen schemas/decision_tree.schema.json
  - Auth
  - Ruft decision_tree_service.capture()
  - Return {audit_id, status}
- GET /decision-tree/recent (für Admin / Aroob's Dashboard)

routes/audit.py:
- GET /audit/trail (admin-only, returns paginated AuditEvents)
- GET /audit/anomalies (returns disagreements der letzten 7 Tage)

Pydantic Response-Models in app/schemas/:
- PredictionResponse
- DecisionTreeResponse
- HealthResponse
- AuditTrailItem

Plus Exception-Handler für ValueError (anonymization fail), 
jsonschema.ValidationError, RateLimitExceeded.

Tests in tests/test_api.py:
- Test /health unauthenticated
- Test /inference/predict mit valid+invalid DICOM
- Test /decision-tree/capture mit valid+invalid payload
- Test /audit/trail mit + ohne admin

REGEL: API-Auth über X-API-Key Header (nicht Bearer-Token, kein OAuth — 
Local-First, kein User-Management nötig).
```

---

### P-14 · `code/backend/app/main.py` (Factory) · Sonnet 4.6 · [SEQUENTIAL]

```
Erstelle code/backend/app/main.py mit der create_app()-Factory:

def create_app() -> FastAPI:
  - lifespan context manager (startup: init_db, model load, lifespan ready 
    log; shutdown: cleanup)
  - FastAPI Instanz mit Title, Version, OpenAPI-URL nur im DEBUG-Mode
  - structlog Setup mit Request-ID-Middleware
  - SlowAPI Limiter
  - CORS Middleware (Origins aus Config)
  - Prometheus Instrumentator
  - Alle Router aus app/api/routes/ included
  - Custom Exception Handler
  - app.state.inference_service Setup

Top-level: app = create_app() für gunicorn / direkt-Aufruf.

Tests/test_main.py:
- Test startup creates DB tables
- Test inference_service in app.state
- Test middleware-Stack korrekt

REGEL: lifespan-Pattern statt @app.on_event (deprecated). 
structlog.contextvars für Request-Tracing.
```

---

## STAGE E — Frontend (parallel zu D + F)

### P-15 · `code/frontend/src/main.tsx` + `App.tsx` · Sonnet 4.6 · [PARALLEL]

```
Erstelle code/frontend/src/main.tsx + App.tsx als React 19 + Vite Setup.

main.tsx:
- ReactDOM.createRoot
- React.StrictMode
- QueryClientProvider mit React Query (TanStack)
- CSS-Imports (tailwind base)

App.tsx:
- Router-freie SPA für jetzt (eine Seite)
- Layout: Header (Klinikum-Dortmund-Branding) + 3-Spalten-Layout
  - Links: Patient-List (Mock-Daten zunächst)
  - Center: DicomViewer-Component (von P-16)
  - Rechts: AIPanel + DecisionTreeForm (von P-17, P-18)
- API-Health-Check im Header (zeigt Status-Punkt: green/yellow/red)
- Zustand-Store für selected_case_id

Plus: types/api.ts mit allen Pydantic-Response-Modellen aus dem Backend 
als TypeScript Interfaces.

Plus: lib/apiClient.ts mit axios oder fetch-wrapper, X-API-Key aus env.

Style: Tailwind v4. Dark mode Default (Medical-Imaging-Standard, 
Background near-black für DICOM viewer).

Tests: vitest + @testing-library/react smoke test für App rendert ohne 
Error.

REGEL: TypeScript strict. Pfade via @/ Alias.
```

---

### P-16 · `code/frontend/src/components/DicomViewer.tsx` · Sonnet 4.6 · [PARALLEL]

```
Erstelle code/frontend/src/components/DicomViewer.tsx — DICOM-Image-
Viewer mit Cornerstone.js v2.

Features:
- Lädt DICOM-File aus Backend via /inference/predict-Response
- Cornerstone-Tools: Pan, Zoom, Window/Level, Length-Measurement
- Heatmap-Overlay-Layer (Grad-CAM) toggleable mit Slider für Opacity 
  (0-100%)
- Window-Presets: Lung (-600/1500), Soft (40/400), Bone (300/1500)
- Region-Selection-Tool für Decision-Tree-Capture (Bounding-Box, gibt 
  Maske zurück)

Props:
- dicomFileUrl: string
- heatmap?: number[][] (optional, von AI-Response)
- onRegionSelected?: (mask: ImageData) => void

State (Zustand-Store): selectedTool, windowPreset, heatmapOpacity, 
selectedRegion

Tests: vitest mit Mock-DICOM (z.B. ein bytes-Array) — Component rendert, 
Tool-Wechsel funktioniert.

REGEL: kein Patientendaten-Logging im Frontend. Cornerstone-Errors 
abfangen und zur Audit-API senden.
```

---

### P-17 · `code/frontend/src/components/AIPanel.tsx` · Sonnet 4.6 · [PARALLEL]

```
Erstelle code/frontend/src/components/AIPanel.tsx — zeigt das AI-Ergebnis 
für den aktiven Fall.

Features:
- Stenosegrad % mit Konfidenz-Ring (CircularProgress, cyan auf dunklem 
  Background)
- Vulnerability-Marker: 4 Toggles (IPH, ThinCap, LRNC, Systolic Motion) 
  mit AI-Wahrscheinlichkeit + Manual-Override
- "Confirm AI" / "Adjust Measurement" / "Request Second Opinion" Buttons 
  (werden Decision-Tree-Form öffnen — siehe P-18)
- Audit-Trail-Mini (letzte 5 Inferenzen für diesen Fall)

Props:
- prediction: PredictionResponse (oder loading/error states)
- onConfirm: () => void
- onAdjust: () => void
- onSecondOpinion: () => void

Style: rechtes Panel, 360px breit, hellgrau (#F9FAFB) auf dunklem 
Background — siehe ../Carotis-AI Diagnostik-Suite.html als visueller 
Referenz.

Tests: vitest snapshot + interaction tests.

REGEL: alle Button-Klicks loggen in eine Audit-Queue (lokal, dann 
Batch an Backend).
```

---

### P-18 · `code/frontend/src/components/DecisionTreeForm.tsx` · Sonnet 4.6 · [PARALLEL]

```
Erstelle code/frontend/src/components/DecisionTreeForm.tsx — die 30-Sek-UI 
aus 05_DECISION_TREE_HARVESTING.md Sektion 4.

Features:
- 4 Felder: deciding_feature (Radio + Freitext), ruled_out (Multi-Select), 
  confidence_self_reported (3 Buttons high/med/low), agreement_with_ai 
  (Trust-Score 1-5)
- Default-Werte = AI-Vorschläge (User klickt nur bei Widerspruch)
- "SAVE" Button mit Counter (12 s sichtbar — psychologisch: zeigt dass 
  es schnell ist)
- "SKIP" Button — speichert state in localStorage für 24h Re-Prompt
- Pflicht-Modus-Flag aus Settings (ENABLE_DT_REQUIRED)

Submit: POST an /decision-tree/capture mit JSON validiert gegen 
schemas/decision_tree.schema.json (Schema kommt vom Backend via /schemas 
GET-Endpoint, oder wird zur Build-Zeit eingebaut).

Props:
- caseId: string
- aiPrediction: PredictionResponse
- onSubmit: (treeJson) => Promise
- onSkip: () => void

Tests: vitest — Schema-Validierung des Forms vor Submit, Skip-Logik, 
24h Re-Prompt.

REGEL: Form-State niemals an externe Services posten. Validation lokal 
im Browser.
```

---

## STAGE F — ML Pipeline (parallel zu D + E)

### P-19 · `code/ml/data/dataset.py` · Codex 5.3 · [PARALLEL]

```
Erstelle code/ml/data/dataset.py — PyTorch Dataset für anonymisierte 
Carotis-CTA-Bilder.

CarotisDataset(Dataset):
- __init__(root_dir, manifest_csv_path, transform=None, mode='train')
- Liest manifest.csv (von scripts/anonymize.py)
- Validiert beim Init: alle Files existieren, alle case_ids gehasht
- __getitem__: lädt DICOM, applied transform, gibt dict zurück:
  {image: Tensor[1,512,512], stenosis_pct, vulnerability_4d, 
   reasoning_region_mask (optional)}

Plus DataLoader-Factory:
- get_dataloader(dataset, batch_size, num_workers, shuffle)
- WeightedRandomSampler für Klassen-Imbalance (vulnerability ist rare)

MONAI-Augmentation-Pipeline:
- get_train_transforms() — Random Affine, Random Crop, Random Brightness
- get_val_transforms() — nur Normalize

Tests: synthetic Dataset mit 10 Mock-DICOM-Files, getitem return shape.

REGEL: niemals direkter PII-Zugriff. Manifest enthält nur case_ids 
+ Hash-Verify.
```

---

### P-20 · `code/ml/models/mfsd_unet.py` · Codex 5.3 · [PARALLEL]

```
Erstelle code/ml/models/mfsd_unet.py — die MFSD-UNet-Architektur 
(U-Net + Swin Transformer Bottleneck + Deep Supervision).

class MFSDUNet(nn.Module):
- Encoder: 4 Konv-Blöcke, downsamplng
- Bottleneck: Swin Transformer Block (timm.models.swin_transformer)
- Decoder: 4 Up-Konv-Blöcke mit Skip-Connections
- Heads:
  - Segmentation: 1-Channel Sigmoid (Vessel-Maske)
  - Stenosis-Regression: GlobalAvgPool → FC → 1 Output (NASCET %)
  - Vulnerability-Klassifikation: 4 Outputs mit Sigmoid
  - Deciding-Feature: 12-Klassen Softmax (für Reasoning-Loss in P-21)
- Deep Supervision: Side-Outputs aus 3 Decoder-Levels für Auxiliary 
  Loss

Forward returns: dict mit allen 4 Outputs + 3 Side-Outputs.

Plus: Grad-CAM-Hook-Setup (über register_forward_hook) für Heatmap-
Generierung.

Tests:
- Test forward mit input (1,1,512,512) gibt korrekte Output-Shapes
- Test parameter count plausibel (40-80M)

Quelle für Architektur: Xie et al. 2024 QIMS (zitiert in 
../08_RESEARCH_ATTENTION_2020-2026.md C1).

REGEL: PyTorch 2.5+, type hints, docstrings für jeden Layer.
```

---

### P-21 · `code/ml/training/losses.py` · Codex 5.3 · [PARALLEL]

```
Erstelle code/ml/training/losses.py mit der Composite-Loss aus 
ADR-0002.

class CarotisCompositeLoss(nn.Module):
- __init__(alpha=1.0, beta=0.5, gamma=0.3) — Gewichte konfigurierbar
- forward(predictions, targets):
  - dice = SoftDiceLoss(predictions['segmentation'], targets['mask'])
  - stenosis_mse = MSELoss(predictions['stenosis'], targets['stenosis_pct'])
  - vuln_bce = BCEWithLogitsLoss(predictions['vulnerability'], 
    targets['vulnerability_4d'])
  - reasoning_align = CosineSimLoss(grad_cam_of(predictions), 
    targets['reasoning_region_mask']) — aktiv NUR wenn target verfügbar
  - feature_ce = CrossEntropyLoss(predictions['deciding_feature'], 
    targets['deciding_feature_label'])
  - deep_super = sum of side-output BCE losses
  - total = alpha*dice + alpha*stenosis_mse + beta*vuln_bce + 
    gamma*reasoning_align + 0.2*feature_ce + 0.1*deep_super
  - return total, dict(per-component für logging)

Tests in test_losses.py:
- Test forward mit synthetischen Tensors gibt Skalar-Loss
- Test gamma=0 → reasoning_align nicht im Total
- Test target['reasoning_region_mask']=None → reasoning_align=0
- Test Loss-Werte für trivialen Fall (perfekte Vorhersage) → total≈0

Quelle: ADR-0002 + 05_DECISION_TREE_HARVESTING.md Sektion 6.

REGEL: differenzierbar überall, niemals .item() oder .detach() im 
forward (sonst kein Gradient).
```

---

### P-22 · `code/ml/training/train.py` · Codex 5.3 · [PARALLEL]

```
Erstelle code/ml/training/train.py — der Trainings-Script mit 
MLflow-Logging.

CLI-Argumente:
- --config (yaml file)
- --resume (checkpoint path, optional)
- --incremental (boolean — für Daily-Loop)
- --max-epochs
- --early-stopping-patience

Hauptschleife:
- Datasets laden (P-19)
- Modell instanziieren (P-20)
- Composite Loss (P-21)
- Optimizer: AdamW
- LR-Schedule: CosineAnnealingWarmRestarts
- MLflow run starten, log params + metrics
- Per epoch:
  - train: loss, dice, stenosis_mae, vuln_auc
  - val: alle metrics
  - log to MLflow
  - save checkpoint wenn val_dice verbessert
  - early stopping
- Bei --incremental: zusätzlich Replay-Buffer von alten Daten 
  einschalten (50% neu, 50% alt) gegen Catastrophic Forgetting

Auto-Rollback: nach Epoch wird val_composite mit base_model_composite 
verglichen — wenn val < base - 0.005: STOP + return code 1 (für 
Daily-Loop)

Tests: test_train.py mit synthetischen Mini-Datasets, 1 Epoch, prüft 
dass MLflow run erstellt wurde + checkpoint geschrieben.

REGEL: Reproducibility — Seed fixieren, deterministic CUDA, log alle 
Configs in MLflow.
```

---

### P-23 · `code/ml/export_onnx.py` · Codex 5.3 · [PARALLEL]

```
Erstelle code/ml/export_onnx.py — exportiert ein PyTorch-Checkpoint 
nach ONNX für die Backend-Inferenz.

CLI:
- --checkpoint <path>
- --output <path>
- --opset 18

Schritte:
1. Modell + Checkpoint laden
2. Modell in eval()
3. dummy_input = torch.randn(1, 1, 512, 512)
4. torch.onnx.export mit dynamic_axes für batch_size
5. Output-Names korrekt: "segmentation", "stenosis", "vulnerability", 
   "deciding_feature"
6. Verify: Re-load mit onnxruntime + Vergleich PyTorch-Output vs 
   ONNX-Output (max abs diff < 1e-5)
7. Onnx-Simplify-Pass mit onnxsim
8. Sign mit Sigstore (siehe scripts/sign_model.py — kommt in P3 / 
   T-016 aus tasks.jsonl)

Tests: roundtrip-test mit Mini-Modell.

REGEL: Verify ist Pflicht, nicht optional. Export ohne Verify 
schlägt mit Exit-Code 2.
```

---

## STAGE G — Tests + CI

### P-24 · `code/tests/` erweitern · Sonnet 4.6 · [SEQUENTIAL nach D/E/F]

```
Erweitere code/tests/ um eine vollständige Test-Suite. Bestehender 
test_smoke.py ist Basis.

Neue Files:
tests/test_anonymization_bridge.py:
- Test dass Backend keine PII-haltigen DICOMs annimmt
- Test scripts/anonymize.py wird korrekt aufgerufen

tests/test_decision_tree_validation.py:
- Test JSON-Schema-Validation am API-Endpoint
- Test invalid payloads werden abgelehnt

tests/test_audit_trail.py:
- Test AuditEvent ist append-only
- Test alle Inferenzen erzeugen Audit

tests/test_inference_full.py:
- Test mit echtem demo-ONNX-Modell (von scripts/generate_demo_model.py)
- End-to-end: DICOM upload → Prediction → DecisionTree → Audit

tests/conftest.py erweitern:
- Fixtures: test_db, test_app, test_client, test_dicom_bytes, 
  test_anonymized_dicom, mock_inference_service

tests/test_ml_pipeline.py:
- Test ml/training/train.py runs 1 epoch on synthetic data
- Test ml/export_onnx.py roundtrip

Coverage-Target: ≥ 80% für app/services und ml/training. 
≥ 90% für app/api/routes und scripts/anonymize.py (kritische Pfade).

REGEL: keine echten Patientendaten in Tests. Alle Test-DICOMs sind 
synthetisch generiert.
```

---

### P-25 · `code/.github/workflows/ci.yml` · Sonnet 4.6 · [PARALLEL]

```
Erstelle code/.github/workflows/ci.yml — GitHub Actions CI für jeden 
PR.

Jobs:
- lint:
  - Python: ruff + black
  - TypeScript: eslint + tsc --noEmit

- test-backend:
  - Python 3.11
  - cd backend && pip install -r requirements.txt
  - pytest tests/ -v --cov=app --cov-report=xml
  - upload coverage to Codecov

- test-ml:
  - Python 3.11 + GPU-skip-fallback
  - cd ml && pip install -r requirements.txt
  - pytest tests/test_ml_pipeline.py -v

- test-frontend:
  - Node 22
  - cd frontend && npm ci
  - npm run typecheck && npm run lint && npm run test

- security:
  - bandit (Python)
  - npm audit
  - check kein "openai" oder "anthropic" import in app/services/inference 
    (Local-First-Enforcement)

- build:
  - docker compose build (alle Services)
  - smoke-test: docker compose up -d, curl localhost:8000/health, 
    docker compose down

Trigger: pull_request, push to main.

REGEL: alle Jobs müssen grün sein für Merge. Keine "allow-failure".
```

---

### P-26 · `code/.github/workflows/local_smoke.yml` · GPT-4.1 · [PARALLEL]

```
Erstelle code/.github/workflows/local_smoke.yml — eigener Workflow, 
der den Hermes+Ollama-Stack im CI bootet.

Jobs:
- ollama-setup:
  - Pull ollama image
  - Start ollama container
  - Pull qwen2.5-coder:7b (das kleinste Modell — CI-tauglich)
  - Verify: curl localhost:11434/api/tags

- hermes-smoke:
  - depends_on: ollama-setup
  - Setup hermes mit minimal config
  - Test: hermes ping
  - Test: ein einfacher Prompt durch (zeit-limitiert auf 5 Min)

Trigger: workflow_dispatch (manuell) + scheduled wöchentlich.

REGEL: dieser Workflow ist optional (kein PR-Block). Nur als 
Health-Check unseres Local-Stacks gegen Ollama-Updates.
```

---

## STAGE H — Hermes Integration

### P-27 · `code/hermes/config.toml` · Sonnet 4.6 · [PARALLEL]

```
Erstelle code/hermes/config.toml — die Konfiguration für den 
Hermes-Agent.

Struktur (TOML):

[agent]
name = "carotis-helper"
description = "Self-improving agent für Carotis-AI Engineering und Operations"

[provider]
type = "ollama"
endpoint = "http://localhost:11434"
model = "nous-hermes-3-llama-3.1"
timeout_seconds = 1800  # 30 Min für lokale prefills

[memory]
type = "filesystem"
root = "../memory"
runs_dir = "../memory/runs"
domain_dir = "../memory/domain"
load_on_start = ["../CLAUDE.md", "../MEMORY.md", "../00_INDEX.md"]

[skills]
auto_load = true
skill_dir = "./skills"
allowed_executables = [
  "../scripts/anonymize.py",
  "../scripts/preflight.sh",
  "../scripts/validate_decision_tree.py"
]

[compression]
model = "qwen2.5-coder:7b"
target_tokens = 1500
trigger_at_tokens = 24000

[logging]
level = "INFO"
format = "json"
output = "/tmp/hermes-carotis.log"

[tool_permissions]
read = ["../**", "./**", "../schemas/**"]
write = ["../memory/**", "../data/anonymized/**"]
execute_allowlist = "skills"  # nur Skills aus skill_dir erlaubt
deny_endpoints = ["api.anthropic.com", "api.openai.com"]  # für 
                                                            # Patientendaten

REGEL: Compliance hart — kein Cloud-Endpoint für PII-Daten.
```

---

### P-28 · `code/hermes/skills/` (3 Skills) · Sonnet 4.6 · [PARALLEL]

```
Erstelle 3 Hermes-Skills in code/hermes/skills/. Format: 
skill-<name>.md mit Frontmatter (Hermes-Agent-Standard).

Skill 1: anonymize-batch.md
- Trigger phrases: "anonymisiere DICOM", "anonymize batch"
- Action: ruft scripts/anonymize.py auf, parsed Manifest, gibt 
  Zusammenfassung
- Required tools: bash
- Output: Markdown-Report mit ok/rejected/skipped

Skill 2: capture-decision-tree.md
- Trigger phrases: "erfasse Arzt-Entscheidung", "save decision"
- Action: nimmt JSON-Input, validiert gegen 
  schemas/decision_tree.schema.json (via scripts/validate_decision_tree.py), 
  schreibt in memory/decisions/, schreibt Audit-Event
- Required tools: filesystem, bash

Skill 3: nightly-retrain.md
- Trigger: "trainiere mit neuen Decision-Trees", oder Cron @ 22:15
- Action: liest memory/decisions/ since last_run, wenn ≥ 10 neue Trees: 
  ruft ml/training/train.py --incremental, vergleicht Performance, 
  pusht oder rolled-back
- Required tools: bash, filesystem

REGEL: jeder Skill ist als markdown self-contained dokumentiert. Hermes 
parsed das Frontmatter und führt die Action aus.

Quelle für Skill-Format: hermes-agent.nousresearch.com/docs/skills.
```

---

### P-29 · `code/scripts/demo.sh` erweitern · Sonnet 4.6 · [SEQUENTIAL]

```
Erweitere die bestehende code/scripts/demo.sh um den Hermes+Ollama-
Bootstrap.

Bestehende Schritte (1-4 wie sie sind) PLUS:

# ── Step 5: Local AI Stack ─────────────────────────────────────────
step "Bootstrapping Hermes + Ollama..."
if ! curl -sf localhost:11434/api/tags > /dev/null; then
  bash scripts/install_local_stack.sh
else
  ok "Ollama already running."
fi

# Verify Hermes
if curl -sf localhost:8200/ping > /dev/null; then
  ok "Hermes Agent running."
else
  step "Starting Hermes via docker-compose..."
  docker compose -f docker-compose.yml up -d hermes
  sleep 5
  curl -sf localhost:8200/ping || fail "Hermes did not start."
fi

# ── Step 6: Smoke Test ────────────────────────────────────────────
step "Running smoke test (anonymize sample DICOM)..."
docker compose run --rm backend python -m scripts.smoke_test
ok "All systems operational."

# Final banner
banner "Demo Stack Ready"
echo -e "  Backend:   http://localhost:8000"
echo -e "  Frontend:  http://localhost:3000"
echo -e "  Ollama:    http://localhost:11434"
echo -e "  Hermes:    http://localhost:8200"
echo -e "  Dashboard: ../dashboard.html (open in browser)"

REGEL: idempotent — alle Schritte können mehrfach laufen. Cleanup-
Pfad bei Fehler in jedem Step.
```

---

## Nach allen Prompts — Verifikations-Lauf

```bash
cd code
docker compose up -d
sleep 30
curl localhost:8000/health
curl localhost:11434/api/tags
curl localhost:8200/ping
pytest -v
cd .. && bash scripts/preflight.sh
```

Wenn alle 5 Calls grün: P0/P1/P2-Code-Fundament ist fertig. Du gehst dann zurück zum Stakeholder-Pfad (`RUNBOOK_TODAY.md`).

---

## Modell-Quota-Management

| Tag | Stage | Sonnet 4.6 Calls | Codex 5.3 Calls | GPT-4.1 Calls |
|---|---|---|---|---|
| Tag 1 vormittags | A + B + C | 5 | 0 | 4 |
| Tag 1 nachmittags | D + E + F | 9 | 9 | 0 |
| Tag 2 vormittags | G + H | 7 | 0 | 1 |
| **Total** | | **21** | **9** | **5** |

Mit Lou's €10/Monat Plan: typisch 100–200 Premium-Requests verfügbar. **Du verbrauchst < 30%.** Reserve für Bug-Fixing + Re-Runs.

---

## Memory-Pflicht nach jedem Prompt

Nach jedem Copilot-Prompt-Lauf einen 5-Zeilen-Eintrag in 
`../memory/runs/2026-04-28_copilot_<P-NN>.md`:

```markdown
# Session 2026-04-28 · Copilot Sonnet 4.6 · P-XX

**Goal:** <was sollte gebaut werden>
**Done:** <was wurde gebaut + File-Pfade>
**Surprised by:** <was ist anders als erwartet>
**Avoided:** <was war Halluzination, korrigiert>
**Next:** <P-NN+1 oder offene Bugs>
```

Ohne Memory-Updates verlierst du den Engineering-Harness-Vorteil.

---

## Sources

- [Jake van Clief — Interpretable Context Methodology (arXiv 2603.16021)](https://arxiv.org/abs/2603.16021)
- [Eduba.io](https://services.eduba.io/)
- [Stop Building AI Agents — YouTube](https://www.youtube.com/watch?v=MkN-ss2Nl10)
- [Hermes Agent (Nous Research)](https://github.com/nousresearch/hermes-agent)
- [Hermes-Agent Ollama Setup](https://hermes-agent.ai/blog/hermes-agent-ollama-setup)
- [Ollama Hermes Integration Docs](https://docs.ollama.com/integrations/hermes)
- [Composio Hermes Toolkit](https://composio.dev/toolkits/ollama/framework/hermes-agent)

---

**Version:** 1.0 · **Erstellt:** 2026-04-28 · Opus 4.7 (Cowork)
