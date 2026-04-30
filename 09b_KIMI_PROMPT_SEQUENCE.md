# 09b_KIMI_PROMPT_SEQUENCE — Kimi K2.6 (Moonshot AI) Prompts

> **Wofür?** Du bist auf Kimi K2.6 statt GitHub Copilot Chat. Vorteile: riesiger Kontext (256k Token), keine wöchentliche Quota wie bei Copilot. Nachteile: kein `@workspace`, kein File-System, keine Verify-Commands automatisch — du machst das manuell.
>
> **Strategie:** Wir bündeln Files pro Stage in **einen** Prompt, weil Kimi's Kontext das aushält. Das spart 50 % Round-Trips gegenüber Copilot. Du kopierst Kimi's Output-Block in VS Code, prüfst visuell, fertig.
>
> **Lesson Learned aus P-01 (Copilot):** Line-Count-DoDs sind Müll — Copilot hat 76 statt 100 Zeilen geliefert, Inhalt war komplett. Hier verwenden wir **funktionale Checks** statt Zeilen-Zählen.

---

## Wie du Kimi bedienst

1. Öffne Kimi (`https://kimi.moonshot.cn/` oder `https://www.kimi.com/`)
2. Neue Konversation
3. **Schritt 0 — Session-Setup** (siehe unten): Den Kontext-Block einmal pasten. Kimi „lädt" das Projekt damit in seinen Kontext. Antwort von Kimi: „Verstanden, ich kenne jetzt Carotis-AI und arbeite im Engineering-Harness-Stil."
4. Dann **K-01 bis K-16** sequenziell pasten. Pro Prompt: Kimi gibt dir Markdown/Code, du speicherst die Files manuell.
5. **Visual Review** in VS Code nach jeder Antwort. Kein Stride-Tooling, keine Auto-Diffs.
6. Run-Log nach jedem Prompt: 5 Zeilen in `memory/runs/2026-04-28_kimi_K-NN.md`

---

## SCHRITT 0 — Session-Setup (paste ONCE am Anfang)

````
Du bist ab jetzt Engineering-Partner für das Projekt **Carotis-AI** — ein 
lokales, erklaerbares KI-System fuer die Carotis-Stenose-Diagnostik aus 
CTA-Bildern. Promotionsprojekt am Klinikum Dortmund (Aroob Alrawashdeh, 
Betreuer Prof. Dr. Stefan Rohde).

KERN-ARCHITEKTUR
- Backend: Python 3.11 + FastAPI + Pydantic v2 + SQLAlchemy async + ONNX 
  Runtime + structlog + Prometheus
- Frontend: React 19 + Vite + TypeScript + Tailwind v4 + Cornerstone.js 
  v2 (DICOM viewer) + Zustand + TanStack Query
- ML: PyTorch 2.5 + MONAI 1.4 + timm (Swin Transformer) + grad-cam + 
  MLflow + ONNX export
- Local AI: Ollama (localhost:11434) + Hermes Agent (Nous Research) + 
  caveman compression (qwen2.5-coder:7b)
- Keine Cloud-Provider fuer Patientendaten

THEORETISCHE BASIS
Jake van Clief — Interpretable Context Methodology / Model Workspace 
Protocol (arXiv 2603.16021). Numbered Folders = Stages. Markdown = 
Prompts. Scripts = mechanische Arbeit. Filesystem ersetzt Framework-
Orchestrierung.

INNOVATION
"Decision-Tree-Harvesting" — nach jeder Befundung erfasst eine 30-Sek-UI 
strukturiert die aerztliche Begruendung (deciding_feature, ruled_out, 
confidence, agreement_with_ai). Diese Decision-Trees werden anonymisiert 
und als zusaetzliche Loss-Komponente (Reasoning-Alignment-Loss) ins 
Modell eingespeist. Daily-Learning-Loop trainiert naechtlich, 
Auto-Rollback bei Performance-Verlust.

HARD RULES (NICHT verhandelbar)
1. Local-First: KEIN Cloud-API-Call fuer Patientendaten. Kein OpenAI/
   Anthropic/Google Endpoint im inference path. Anonymisierte aggregierte 
   Modell-Updates via signiertes Bundle ist OK.
2. Anonymisierung: Pflicht via DICOM PS 3.15 Basic Profile + k-Anonymity 
   ≥ 5. Bestehendes Skript: scripts/anonymize.py mit 24/24 pytest gruen.
3. Audit-Trail: jede AI-Inferenz und jede Arzt-Entscheidung mit 
   timestamp + model_version + model_sha geloggt. Append-only 
   AuditEvent-Tabelle.
4. Schema-First: schemas/decision_tree.schema.json (JSON Schema 2020-12) 
   ist Single-Source-of-Truth. Code muss dagegen validieren.
5. Tests: jede Service-Methode hat mind. 1 pytest. Kritische Pfade 
   (Anonymisierung, Inferenz, Audit) 100 % Coverage.
6. UI-Sprache: Deutsch. Code-Kommentare + Commits: Englisch.

STACK-CONVENTIONS
- Imports: Python absolute (from app.services import ...), TypeScript 
  @/-Alias auf src/.
- Type-Hints: from __future__ import annotations immer. Pydantic v2 
  BaseModel statt @dataclass fuer API-Schemas.
- Error-Handling: nie bare except. Custom Exceptions in 
  app/core/exceptions.py.
- Logging: structlog mit bind() fuer Request-Context. Niemals print(). 
  Niemals PII in Logs.
- Encoding: UTF-8 ohne BOM fuer alle Files. Windows-User: VS Code 
  reads UTF-8 nativ, PowerShell-Console-Codepage cp1252 ist nur 
  Console-Garbling, File ist OK.

MULTI-MODEL-ROUTING (wer macht was)
- Cloud-Claude Opus → Architektur, ADR, Stakeholder-Mails
- Cloud-Claude Sonnet → Code-Review, schwere Refactors
- GitHub Copilot Sonnet 4.6 / Codex 5.3 → Code-Implementation
- Kimi K2.6 (DU JETZT) → Bulk-Generation, lange Files, Boilerplate
- Hermes via Ollama → Tool-Use, Memory, Skills (lokal nach Setup)
- Caveman via Ollama → Compression, Boilerplate (lokal)

VERZEICHNIS-STRUKTUR (Workspace-Root: Carotis AI/)
- 00_INDEX.md  ← Tour
- 01_HARNESS.md  ← Modell-Routing, DoD, Memory-Hierarchie
- 02_ROADMAP.md  ← Phasen P0–P7 (24 Monate)
- 03_PROMPT_TEMPLATES.md  ← 9 Templates
- 04_MASTER_PLAN.md  ← v1.0
- 05_DECISION_TREE_HARVESTING.md  ← die Innovation
- 06_ROHDE_MEETING_KIT.md  ← Stakeholder-Prep
- 07_OFFICE_AGENT_PROMPTS.md  ← 8 Stride-Prompts (.docx Updates)
- 08_RESEARCH_ATTENTION_2020-2026.md  ← 27+ Papers
- 09_COPILOT_PROMPT_SEQUENCE.md  ← Copilot-Variante (29 Prompts)
- 09b_KIMI_PROMPT_SEQUENCE.md  ← DU LIEST DAS GERADE
- CLAUDE.md, MEMORY.md  ← Working Memory + Index
- code/  ← Implementations-Verzeichnis (du erweiterst es jetzt)
  - .github/copilot-instructions.md  ← schon erstellt (P-01)
  - backend/  ← FastAPI app
  - frontend/  ← React 19 + Cornerstone
  - ml/  ← PyTorch training pipeline
  - hermes/  ← Hermes Agent config (zu erstellen)
  - scripts/  ← demo.sh, install_local_stack.sh, etc.
  - tests/  ← pytest suite
  - schemas/  ← JSON schemas (Symlink auf ../schemas/)
- regulatory/  ← ADR-0001 Local-First, ADR-0002 Decision-Tree, 
  risk_register.md
- ethics/  ← Ethikantrag, Patienteninfo, Einwilligung, DPIA
- memory/  ← runs/, decisions/, anomalies/, domain/
- schemas/  ← decision_tree.schema.json + sample
- scripts/  ← anonymize.py (24/24 tests gruen), preflight.sh, 
  validate_decision_tree.py

DEINE ROLLE
Wenn ich dir gleich Prompts K-01 bis K-16 sende, erzeugst du EXAKT die 
geforderten Files. Output: ein Codeblock pro File mit Pfad-Header. 
Beispiel:

  // FILE: code/CLAUDE.md
  ```markdown
  # CLAUDE.md fuer code/
  ...
  ```

Keine Praeambeln, keine Erklaerungen vor/nach dem Code. Direkt der 
Codeblock. Mehrere Files pro Antwort sind OK wenn der Prompt das 
verlangt.

VERBOTE
- Keine Cloud-API-Calls auf Patientendaten in generiertem Code
- Kein print() statt structlog
- Kein bare except
- Kein Schema-Bypass
- Keine Halluzination von API-Endpoints (wenn unklar: an Lou eskalieren, 
  nicht raten)

ANTWORTE JETZT NUR MIT: "Verstanden. Ich kenne Carotis-AI, halte mich 
an die Hard Rules und liefere Files im FILE-Header-Codeblock-Format. 
Bereit fuer K-01."
````

**Verify Setup OK:** Kimi antwortet kurz mit „Verstanden ...". Wenn er anfängt zu philosophieren oder Klarstellungen will → Setup nochmal pasten.

**Token-Hinweis:** Dieser Setup-Block ist ~700 Worte / ~1500 Tokens. Bei Kimi's 256k-Kontext: vernachlässigbar.

---

## REIHENFOLGE

```
SCHRITT 0 (einmal)  →  Session-Setup [BLOCKS ALL]
                                ↓
K-01  →  copilot-instructions.md (already done in P-01, hier als Refresh)
                                ↓
K-02  →  Stage B bundled: code/CLAUDE.md + code/HARNESS.md + 
         code/AGENTS.md + code/MEMORY.md  (4 Files in 1 Prompt)
                                ↓
K-03  →  Stage C bundled: docker-compose.yml + .env.example + 
         install_local_stack.sh + install_local_stack.ps1
                                ↓
        ┌────────────┬────────────┬────────────┐
        ↓            ↓            ↓            ↓
K-04   K-05   K-06   K-07   K-08      ← Backend (5 separate, sequential)
        config db  services api   main
                ↓ (parallel zu K-04..K-08)
K-09  →  Frontend bundled: main + App + 3 Components (5 Files in 1)
                ↓ (parallel)
K-10..K-14   ← ML Pipeline (5 separate)
        dataset model losses train export
                                ↓
K-15  →  Tests + CI bundled (test_anonymization + test_decision + 
         test_audit + test_inference + ci.yml + local_smoke.yml)
                                ↓
K-16  →  Hermes bundled: config.toml + 3 skills + demo.sh extension
                                ↓
                        Smoke-Test (manuell)
```

**Insgesamt: 16 Prompts statt 29 (Copilot-Variante).** Kimi's Kontext frisst die Bündelung problemlos.

---

## K-01 · `code/.github/copilot-instructions.md` (Refresh)

> **Hinweis:** Du hast die Datei schon mit Copilot gebaut (P-01, 76 Zeilen). Wenn du den Inhalt verifiziert hast und er passt, **überspringe diesen Prompt**. Ansonsten: Kimi neu generieren lassen, weil Kimi's Output deterministischer aus dem Setup-Kontext wirkt.

```
Erzeuge die Datei code/.github/copilot-instructions.md mit den Hard 
Rules, Conventions, ADRs-Referenz und When-in-Doubt-Sektion aus dem 
Session-Setup. Englische Headings, Markdown.

Output: ein Codeblock mit FILE-Header.

Funktionale Checks (Lou prueft):
- Datei existiert
- Sektionen "Project", "Stack", "Hard Rules", "Conventions", 
  "ADRs", "Risk Register", "Engineering Harness", "When in Doubt" 
  vorhanden
- Alle relativen Pfade aufloesbar (../05_DECISION_TREE_HARVESTING.md, 
  ../regulatory/adr/ADR-0001-local-first.md, ../regulatory/adr/
  ADR-0002-decision-tree-harvesting.md, ../regulatory/risk_register.md, 
  ../CLAUDE.md, ../MEMORY.md, ../00_INDEX.md, ../01_HARNESS.md)
- Encoding UTF-8 ohne BOM
- KEINE Line-Count-Anforderung — Inhalt zaehlt
```

---

## K-02 · Stage B bundled — Code-Memory (4 Files in 1 Prompt)

```
Erzeuge in EINER Antwort vier Files. Jeder File-Block beginnt mit 
einem FILE-Header. Reihenfolge: CLAUDE.md, HARNESS.md, AGENTS.md, 
MEMORY.md.

FILE 1: code/CLAUDE.md
- Working Memory fuer Code-Sessions in diesem Verzeichnis
- Verweist auf ../CLAUDE.md (Master) und ../00_INDEX.md (Tour)
- Sub-Project-Definition: code/ ist das Implementierungs-Verzeichnis
- Kurzer Stack-Block (von Setup uebernehmen)
- Critical Path: data anonymisiert → ML trainiert → ONNX exportiert 
  → Backend laedt ONNX → Frontend ruft Backend → Decision-Tree 
  captured → Daily-Loop trainiert nach
- Pre-Flight fuer Code-Sessions: ../scripts/preflight.sh; git status; 
  pytest -q
- Verbote-Liste (verkuerzt aus Setup)
- Footer: Last-Update 2026-04-28
- Halte unter ~150 Zeilen; Caveman-Stil OK

FILE 2: code/HARNESS.md
- Local-AI-Harness fuer Code-Generation INNERHALB von code/
- Goldene Regel: 3 Modelle (Cloud-Claude, Hermes via Ollama, Caveman 
  via Ollama) plus GitHub Copilot
- Routing-Matrix-Tabelle (Aufgabe → Modell → Endpoint)
- Hermes Setup: Ollama installieren, Modelle pullen 
  (nous-hermes-3-llama-3.1, qwen2.5-coder:7b), Hermes Agent installieren
- Caveman-Compression: Beispiel-Befehl `hermes compress --input 
  ../CLAUDE.md --output ../CLAUDE.compressed.md --model 
  qwen2.5-coder:7b --target-tokens 1500`
- Workflow innerhalb von Code-Sessions (8 Schritte)
- Wiederverwendbarkeits-Sektion: code/HARNESS.md, code/AGENTS.md, 
  code/hermes/, code/scripts/install_local_stack.* sind Drop-in fuer 
  jedes andere lokale OSS-Projekt
- Quellen: Jake van Clief arXiv 2603.16021, Hermes Agent 
  github.com/NousResearch/hermes-agent, Ollama ollama.com

FILE 3: code/AGENTS.md
- Hermes-Agent-Spec
- Sektionen: Agent-Identitaet (name=carotis-helper, model=
  nous-hermes-3-llama-3.1, endpoint=localhost:11434, context=32k 
  comprimiert via caveman bei >24k)
- Persistente Memory: liest beim Start ../CLAUDE.md, ../MEMORY.md, 
  code/CLAUDE.md, letzte 3 in ../memory/runs/
- 3 Skills: anonymize-batch, capture-decision-tree, nightly-retrain 
  (jeweils 1 Absatz Beschreibung)
- Tool-Permissions Allowlist (read=../**, code/**, schemas/**; 
  write=memory/**, data/anonymized/**, models/**; 
  execute=scripts/anonymize.py, scripts/preflight.sh, 
  scripts/validate_decision_tree.py)
- DENIED Endpoints: api.anthropic.com, api.openai.com fuer 
  Patientendaten-Pfade
- Self-Improvement-Loop: Hermes liest woechentlich memory/runs/ und 
  schlaegt neue Skills oder Memory-Updates in memory/proposals/ vor

FILE 4: code/MEMORY.md
- Index aller code-spezifischen Memory-Files
- Pointer auf Master-Files (../CLAUDE.md, ../MEMORY.md, ../00_INDEX.md)
- Code-Memorys-Sektion (anfangs leer, "wird bei Code-Sessions 
  gefuellt")
- Konventionen: code/memory/runs/<datum>_<modell>_<thema>.md, 
  code/memory/anomalies/<datum>_<bug>.md
- Wartung: 1 Run-Log pro Code-Session, 1 Anomaly-Eintrag pro Bug-Fix
- Halte unter 80 Zeilen

Funktionale Checks:
- 4 Codebloecke mit FILE-Headern in der richtigen Reihenfolge
- Jede Datei UTF-8 ohne BOM
- Pfade aufloesbar
- KEINE Line-Counts gepruieft, nur Inhalt
```

---

## K-03 · Stage C bundled — Infrastructure (4 Files in 1 Prompt)

```
Erzeuge in EINER Antwort vier Infrastruktur-Files.

FILE 1: code/docker-compose.yml
Services: ollama, hermes, backend, frontend (siehe Reihenfolge unten 
mit depends_on und healthchecks).

services:
  ollama:
    image: ollama/ollama:latest
    volumes: [ollama-models:/root/.ollama]
    ports: ["11434:11434"]
    environment: [OLLAMA_HOST=0.0.0.0]
    healthcheck:
      test: ["CMD-SHELL", "curl -fs localhost:11434/api/tags || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
  hermes:
    build: { context: ./hermes }
    depends_on: { ollama: { condition: service_healthy } }
    volumes:
      - ../memory:/app/memory:rw
      - ../schemas:/app/schemas:ro
    environment:
      - HERMES_OLLAMA_URL=http://ollama:11434
      - HERMES_MODEL=nous-hermes-3-llama-3.1
    ports: ["8200:8200"]
  backend:
    build: { context: ./backend }
    depends_on: { ollama: { condition: service_healthy } }
    volumes:
      - ./data:/data:rw
      - ../scripts/anonymize.py:/app/scripts/anonymize.py:ro
    env_file: ./backend/.env
    ports: ["8000:8000"]
    healthcheck:
      test: ["CMD-SHELL", "curl -fs localhost:8000/health || exit 1"]
  frontend:
    build: { context: ./frontend }
    depends_on: { backend: { condition: service_healthy } }
    ports: ["3000:3000"]
    environment: [VITE_API_URL=http://backend:8000]

volumes: { ollama-models: }

networks (default): name=carotis-net, internal=false (frontend braucht 
externes CDN; backend/ollama/hermes laufen nur intern via service-name)

FILE 2: code/backend/.env.example
Variablen mit Kommentaren pro Zeile:
- API_KEY (placeholder, mind. 32 chars, via Doppler in Prod)
- DATABASE_URL=sqlite+aiosqlite:///./data/carotis.db
- ONNX_MODEL_PATH=/data/models/mfsd_unet.onnx
- MODEL_VERSION=v0.3.2
- MODEL_SHA=abc123d
- OLLAMA_URL=http://ollama:11434
- HERMES_URL=http://hermes:8200
- DEFAULT_LOCAL_MODEL=nous-hermes-3-llama-3.1
- COMPRESSION_MODEL=qwen2.5-coder:7b
- ANONYMIZATION_SALT=change-me-quartal
- ANONYMIZATION_SALT_VERSION=v2026-04
- MIN_K_ANONYMITY=5
- AUDIT_DB_PATH=/data/audit.db
- AUDIT_RETENTION_YEARS=25
- LOG_LEVEL=INFO
- LOG_FORMAT=json
- CORS_ORIGINS=http://localhost:3000,http://frontend:3000
- ENABLE_DECISION_TREE_CAPTURE=true
- ENABLE_DAILY_LEARNING_LOOP=false
- ENABLE_GRAD_CAM_OVERLAY=true
- DEBUG=false
- RELOAD=false
NIEMALS echte Secrets, nur Platzhalter.

FILE 3: code/scripts/install_local_stack.sh
Bash strict mode (set -euo pipefail), Farb-Codes (banner/step/ok/fail), 
idempotent.
1. Detect OS (uname -s; linux oder darwin), exit bei Windows mit 
   Hinweis auf install_local_stack.ps1
2. Ollama installieren falls nicht da: 
   curl -fsSL https://ollama.com/install.sh | sh
3. Ollama-Service starten: 
   pgrep -f "ollama serve" > /dev/null || nohup ollama serve > 
   /tmp/ollama.log 2>&1 & ; sleep 3
4. Modelle pullen mit Skip-If-Already-Pulled-Logik 
   (ollama list | grep -q <name> || ollama pull <name>):
   - nous-hermes-3-llama-3.1
   - qwen2.5-coder:7b
   - llava-llama3:8b (optional, hint im Output)
5. Python venv .venv erstellen falls nicht da
6. pip install hermes-agent (Hinweis: pypi-Name pruefen, ggf. 
   git+https://github.com/NousResearch/hermes-agent.git)
7. Verify: curl -fs localhost:11434/api/tags listet die Modelle
8. Output: Setup-Summary mit naechsten Schritten
Logge alles in /tmp/install_local_stack.log
Bei Port-Konflikt 11434: warnen + exit
30-Min-Timeout fuer Modell-Pulls

FILE 4: code/scripts/install_local_stack.ps1
Identische Logik auf PowerShell:
- $ErrorActionPreference = "Stop"
- Detect Windows, sonst Hinweis auf .sh-Variante
- Ollama-Installer download: 
  Invoke-WebRequest https://ollama.com/download/OllamaSetup.exe -OutFile $env:TEMP\OllamaSetup.exe
  Start-Process -Wait $env:TEMP\OllamaSetup.exe /S
- Test-Path "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
- Get-Process -Name ollama -ErrorAction SilentlyContinue oder Start
- Get-NetTCPConnection -LocalPort 11434 fuer Konflikt-Check
- Modell-Pull-Logik analog
- Farb-Codes via Write-Host -ForegroundColor
- Hinweis im Header dass Skript via 
  PowerShell -ExecutionPolicy Bypass -File aufgerufen werden muss

Output: 4 FILE-Header-Codebloecke, deutsche Kommentare in den Skripten 
sind OK, Code-Symbole englisch.
```

---

## K-04 · `code/backend/app/core/config.py` + `tests/test_config.py`

```
Erzeuge code/backend/app/core/config.py mit pydantic-settings v2 und 
parallel den Test code/backend/tests/test_config.py.

config.py:
- BaseSettings-Subclass `Settings` mit allen Variablen aus 
  backend/.env.example als typed fields (str, int, bool)
- Validators:
  - api_key: min_length=32
  - min_k_anonymity: ge=5
  - log_level: in {DEBUG, INFO, WARNING, ERROR}
  - database_url: must startwith "sqlite"
- model_config = SettingsConfigDict(env_file=".env", 
  env_file_encoding="utf-8", extra="ignore", case_sensitive=False)
- get_settings() mit @lru_cache fuer FastAPI dependency injection

test_config.py:
- pytest happy-path: alle env vars gesetzt, Settings() returns ohne 
  Fehler
- test_api_key_too_short → ValidationError
- test_min_k_below_5 → ValidationError
- test_log_level_invalid → ValidationError
- test_get_settings_cached: zweimaliger Aufruf gibt gleiches Objekt
- Verwende monkeypatch.setenv fuer env vars

Output: 2 FILE-Header-Codebloecke.

Funktionale Checks (Lou):
- pip install pydantic-settings; pytest tests/test_config.py
- Erwartung: alle Tests gruen
```

---

## K-05 · `code/backend/app/db/` (database.py, models.py, alembic init)

```
Erzeuge in EINER Antwort drei Files fuer das DB-Layer.

FILE 1: code/backend/app/db/database.py
- Async SQLAlchemy 2.0 Engine + sessionmaker (asyncpg/aiosqlite agnostic)
- engine = create_async_engine(settings.database_url, echo=False, 
  future=True)
- AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
- async def init_db() fuer lifespan: erstellt alle Tabellen aus 
  Base.metadata
- async def get_db() -> AsyncIterator[AsyncSession] fuer FastAPI 
  Dependency
- SQLAlchemy event listener auf AuditEvent-Tabelle: 
  before_update + before_delete → raise IntegrityError 
  ("AuditEvent is append-only")

FILE 2: code/backend/app/db/models.py
- Base = declarative_base() oder DeclarativeBase (SQLAlchemy 2.0)
- class Inference: id (UUID4 default), case_id (str, indexed), 
  captured_at (datetime UTC default now), ai_prediction_json (JSON 
  text), model_version (str), model_sha (str), audit_id (str)
- class DecisionTree: id, case_id (unique, indexed), captured_at, 
  physician_role_hash (str, 64 chars), data_json (validated against 
  schemas/decision_tree.schema.json beim insert via SQLAlchemy 
  validates-decorator), agreement_verdict (Enum: full_agreement, 
  partial_agreement, disagreement)
- class AuditEvent: id, timestamp, event_type (str), actor (str), 
  payload_json (text)
- Alle UUIDs mit default uuid.uuid4
- Alle datetimes UTC default datetime.now(timezone.utc)
- Imports: from __future__ import annotations

FILE 3: code/backend/alembic/versions/0001_initial.py
- Auto-generated Alembic migration fuer die 3 Tabellen
- Stub mit upgrade()/downgrade()
- Verweis im Header dass dies via `alembic revision --autogenerate -m 
  initial` erstellt wird, hier nur als Vorlage

Output: 3 FILE-Header-Codebloecke.

Funktionale Checks (Lou):
- pytest tests/test_db.py (kommt in K-15)
- Erwartung: AuditEvent.update() raises, DecisionTree mit invalid 
  data_json raises, init_db() laeuft ohne Error
```

---

## K-06 · `code/backend/app/services/` (3 Service-Klassen + Schemas)

```
Erzeuge in EINER Antwort die Service-Klassen und Pydantic-Schemas.

FILE 1: code/backend/app/schemas/inference.py
- PredictionResponse(BaseModel): case_id, stenosis_pct_nascet, 
  confidence, vulnerability_markers (dict), heatmap_b64 (optional 
  base64 PNG), model_version, model_sha, audit_id, captured_at
- DecisionTreeRequest(BaseModel): full schema aus 
  ../schemas/decision_tree.schema.json mit korrekten Pydantic-Types
- HealthResponse(BaseModel): status, model_loaded, db_ok, 
  ollama_reachable (optional), timestamp

FILE 2: code/backend/app/services/inference_service.py
- class InferenceService
- __init__(model_path: str, fallback_demo: bool = False): laedt 
  ONNX-Modell mit onnxruntime.InferenceSession; bei fallback_demo: 
  laedt scripts/generate_demo_model.py-Output
- async predict(dicom_bytes: bytes) -> PredictionResponse:
  1. DICOM dekodieren mit pydicom (BytesIO)
  2. Anonymisierungs-Check via 
     anonymization_service.check_only(dicom_bytes); raise 
     ValueError("Non-anonymized DICOM rejected") wenn PII gefunden
  3. Preprocessing: Resize 512x512, Normalize zu [0,1]
  4. Inference (ONNX run mit input_name aus model.get_inputs())
  5. Postprocessing:
     - segmentation: Sigmoid → Vessel-Maske
     - stenosis: float clamp 0-100
     - vulnerability: Sigmoid → 4d-Vektor
  6. Grad-CAM-Heatmap (gradcam-Lib oder eigene Hook-Implementation 
     in services/gradcam.py — separater Helper)
  7. Audit-Event in DB schreiben (model_version, model_sha, case_id_hash)
  8. Return PredictionResponse
- structlog.get_logger() im Module

FILE 3: code/backend/app/services/anonymization_service.py
- class AnonymizationService
- async ensure_anonymized(dicom_bytes: bytes) -> bytes: 
  ruft scripts.anonymize über subprocess oder import-mit-PYTHONPATH; 
  return anonymisierte Bytes
- def check_only(dicom_bytes: bytes) -> tuple[bool, list[str]]: 
  returns (is_anonymized, list_of_pii_tags_found); nutzt die DICOM 
  PS 3.15 Tags-Liste aus scripts/anonymize.py (importiere als 
  DICOM_PII_TAGS_BASIC)

FILE 4: code/backend/app/services/decision_tree_service.py
- class DecisionTreeService
- __init__(db_session_factory)
- async capture(case_id, physician_role_hash, payload: dict) -> str:
  1. jsonschema.validate gegen schemas/decision_tree.schema.json 
     (Schema cached)
  2. DecisionTree-Record schreiben (DB)
  3. Zusaetzlich nach memory/decisions/<datum>_<case_id_short>.json 
     schreiben
  4. AuditEvent erzeugen
  5. Return audit_id
- async list_for_review(since: datetime) -> list[DecisionTree]
- async detect_disagreements(window_days: int = 7) -> list

FILE 5: code/backend/app/services/gradcam.py (Helper)
- def generate_gradcam_heatmap(model_session, input_array, 
  target_class) -> np.ndarray
- Nutzt opencv-python-headless fuer Resize + Colormap-Anwendung
- Output: 512x512 Heatmap als np.uint8

Output: 5 FILE-Header-Codebloecke. Alle async wo I/O involviert. 
structlog.bind() fuer request_id Context. Niemals print().

Funktionale Checks (Lou):
- pytest tests/test_services.py (kommt in K-15)
- Erwartung: Mock-DICOM mit PII rejected, Mock-anonymized accepted, 
  Decision-Tree-Validation funktioniert
```

---

## K-07 · `code/backend/app/api/routes/` (4 Router)

```
Erzeuge die 4 FastAPI-Router.

FILE 1: code/backend/app/api/routes/health.py
- router = APIRouter(prefix="/health", tags=["health"])
- GET / → HealthResponse mit status, model_loaded (app.state.
  inference_service.model_loaded), db_ok (Test-Query SELECT 1), 
  timestamp
- Public, kein Auth-Dependency

FILE 2: code/backend/app/api/routes/inference.py
- router = APIRouter(prefix="/inference", tags=["inference"], 
  dependencies=[Depends(verify_api_key)])
- POST /predict (multipart upload):
  - file: UploadFile = File(...)
  - rate-limited via slowapi @limiter.limit("30/minute")
  - read bytes, ruft inference_service.predict
  - return PredictionResponse

FILE 3: code/backend/app/api/routes/decision_tree.py
- router = APIRouter(prefix="/decision-tree", tags=["decision-tree"], 
  dependencies=[Depends(verify_api_key)])
- POST /capture:
  - body: DecisionTreeRequest
  - ruft decision_tree_service.capture
  - return {audit_id: str, status: "ok"}
- GET /recent (Query: limit=20, offset=0): paginated DecisionTree-Liste

FILE 4: code/backend/app/api/routes/audit.py
- router mit Admin-only Dependency (Header X-Admin-Key zusaetzlich zu 
  X-API-Key oder leichteres Variant: Settings.ADMIN_API_KEY)
- GET /trail: paginated AuditEvent-Liste, filterbar nach event_type + 
  date range
- GET /anomalies: returns disagreements (DecisionTreeService.
  detect_disagreements(7))

PLUS: code/backend/app/api/dependencies.py
- async def verify_api_key(x_api_key: str = Header(...)): 
  if x_api_key != settings.api_key: raise HTTPException(401)
- async def verify_admin_key(x_admin_key: str = Header(...)): analog

PLUS: code/backend/app/core/exceptions.py
- class AnonymizationError(Exception): pass
- class SchemaValidationError(Exception): pass
- class ModelNotLoadedError(Exception): pass

PLUS: Exception-Handler in app/main.py (verweis nur, code in K-08)

Output: 4 Router-Files + dependencies.py + exceptions.py = 6 
FILE-Header-Codebloecke.

Funktionale Checks (Lou):
- pytest tests/test_api.py (in K-15)
- Erwartung: 401 ohne API-Key, 422 bei invalid payload, 200 bei 
  validem Path
```

---

## K-08 · `code/backend/app/main.py` (Factory) + lifespan

```
Erzeuge die FastAPI-App-Factory.

FILE 1: code/backend/app/main.py

from __future__ import annotations
import structlog
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.config import get_settings
from app.core.exceptions import AnonymizationError, SchemaValidationError, ModelNotLoadedError
from app.db.database import init_db
from app.services.inference_service import InferenceService
from app.api.routes import health, inference, decision_tree, audit

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
)
log = structlog.get_logger()
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    log.info("startup_begin", env=settings.log_level)
    await init_db()
    app.state.inference_service = InferenceService(model_path=settings.onnx_model_path)
    log.info("startup_done", model=settings.model_version)
    yield
    log.info("shutdown")


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Carotis-AI Edge Backend",
        version=settings.model_version,
        docs_url="/docs" if settings.debug else None,
        redoc_url=None,
        openapi_url="/openapi.json" if settings.debug else None,
        lifespan=lifespan,
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins.split(","),
        allow_methods=["GET", "POST"],
        allow_headers=["X-API-Key", "X-Admin-Key", "Content-Type"],
    )
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")

    @app.exception_handler(AnonymizationError)
    async def anon_handler(request: Request, exc: AnonymizationError):
        return {"detail": str(exc)}, 422

    @app.exception_handler(SchemaValidationError)
    async def schema_handler(request: Request, exc: SchemaValidationError):
        return {"detail": str(exc)}, 422

    @app.exception_handler(ModelNotLoadedError)
    async def model_handler(request: Request, exc: ModelNotLoadedError):
        return {"detail": "Model not loaded"}, 503

    app.include_router(health.router)
    app.include_router(inference.router)
    app.include_router(decision_tree.router)
    app.include_router(audit.router)
    return app


app = create_app()

FILE 2: code/backend/main.py (entry point — schon vorhanden in Lou's 
code/, NICHT ueberschreiben — nur verifizieren und melden ob 
Anpassung noetig ist)

Output: 1 FILE-Header-Codeblock fuer app/main.py. Wenn backend/main.py 
schon existiert: nur Hinweis "OK, kompatibel" ausgeben, nicht neu 
generieren.

Funktionale Checks (Lou):
- uvicorn app.main:app --reload --port 8000 startet ohne Error
- curl localhost:8000/health antwortet 200 mit JSON
```

---

## K-09 · Stage E bundled — Frontend (5 Files in 1 Prompt)

```
Erzeuge in EINER Antwort 5 Frontend-Files. Annahme: Lou's 
code/frontend/ hat bereits package.json (mit Cornerstone v2, React 19, 
Tailwind v4) und index.html. Wir bauen src/.

FILE 1: code/frontend/src/main.tsx
- ReactDOM.createRoot mit React.StrictMode
- QueryClientProvider mit React-Query (TanStack)
- Tailwind base CSS import
- Render <App />

FILE 2: code/frontend/src/App.tsx
- Layout: 3 Spalten (links 280px Patient-List, center flex DICOM-
  Viewer, rechts 360px AI-Panel + DT-Form)
- Header mit Klinikum-Dortmund-Branding + API-Health-Status-Punkt
- Zustand-Store fuer selected_case_id (siehe FILE 3)
- Dark-Mode Default (DICOM-Standard, near-black BG fuer Viewer)

FILE 3: code/frontend/src/store.ts
- Zustand-Store mit:
  - selectedCaseId: string | null
  - setSelectedCaseId(id)
  - currentPrediction: PredictionResponse | null
  - setCurrentPrediction(p)
  - decisionTreeDraft (fuer skip-and-resume)

FILE 4: code/frontend/src/components/DicomViewer.tsx
Cornerstone-Viewer:
- Props: dicomFileUrl, heatmap?: number[][], 
  onRegionSelected?: (mask: ImageData) => void
- Cornerstone-Tools: Pan, Zoom, WindowLevel, Length, Brush (fuer 
  region-select)
- Heatmap-Overlay-Layer toggleable mit Opacity-Slider 0-100%
- Window-Presets: Lung (-600/1500), Soft (40/400), Bone (300/1500)
- useEffect cleanup fuer Cornerstone-Tool-Group

FILE 5: code/frontend/src/components/AIPanel.tsx + DecisionTreeForm.tsx
(in einem File-Header zusammen — beide Components, beide exported)
- AIPanel: Props prediction, onConfirm, onAdjust, onSecondOpinion
  - CircularProgress fuer Konfidenz (cyan auf dark)
  - 4 Vulnerability-Toggles mit AI-Wahrscheinlichkeit + Manual-Override
  - 3 Action-Buttons (oeffnen DT-Form)
- DecisionTreeForm: Props caseId, aiPrediction, onSubmit, onSkip
  - 4 Felder: deciding_feature (Radio), ruled_out (Multi-Select), 
    confidence (3 Buttons), trust_score (1-5 Slider)
  - Default-Werte = AI-Vorschlaege
  - 12-Sek-Counter ueber dem SAVE-Button
  - SKIP speichert state in localStorage fuer 24h Re-Prompt
  - Submit: validiert lokal (jsonschema-js gegen 
    schemas/decision_tree.schema.json), POST /decision-tree/capture

FILE 6: code/frontend/src/lib/apiClient.ts
- axios oder fetch wrapper
- X-API-Key Header aus VITE_API_KEY
- Base URL aus VITE_API_URL
- Functions: getHealth(), predict(file), captureDecisionTree(payload)
- Error-Handling: 401 → redirect login (placeholder), 429 → toast 
  rate-limit, 503 → toast model-not-loaded

PLUS: code/frontend/src/types/api.ts mit allen Interfaces 
(PredictionResponse, DecisionTreeRequest, HealthResponse) — TypeScript 
mirrors der Pydantic-Models aus K-06.

Output: 7 FILE-Header-Codebloecke. TypeScript strict, @/-Alias auf 
src/.

Funktionale Checks (Lou):
- npm run typecheck (tsc --noEmit) gruen
- npm run dev → http://localhost:3000 zeigt 3-Spalten-Layout
- Health-Status-Punkt im Header gruen wenn Backend laeuft
```

---

## K-10 · `code/ml/data/dataset.py` + `transforms.py`

```
Erzeuge das ML-Data-Modul.

FILE 1: code/ml/data/dataset.py
- class CarotisDataset(torch.utils.data.Dataset)
- __init__(root_dir: Path, manifest_csv: Path, transform=None, 
  mode: Literal["train","val","test"]="train")
- Liest manifest.csv (von scripts/anonymize.py)
- Validiert beim Init: alle Files existieren, alle case_ids 
  64-char-hex
- __getitem__: laedt DICOM (pydicom), applied transform, gibt zurueck:
  {
    "image": Tensor[1,512,512] float,
    "stenosis": float,
    "vulnerability": Tensor[4],  # IPH, ThinCap, LRNC, SystolicMotion
    "deciding_feature_label": int (0-11, 12 classes),
    "reasoning_region_mask": Tensor[1,512,512] | None
  }
- get_dataloader(dataset, batch_size, num_workers, shuffle): 
  WeightedRandomSampler fuer vulnerability-imbalance bei mode=train

FILE 2: code/ml/data/transforms.py
- get_train_transforms(): MONAI Compose mit 
  - LoadImaged, EnsureChannelFirstd, ScaleIntensityRanged 
    (a_min=-100, a_max=600 fuer CTA), 
  - Resized (spatial_size=(512,512)),
  - RandAffined (rotation_range=0.1, scale_range=0.05, prob=0.5),
  - RandFlipd (axis=0/1, prob=0.3),
  - RandGaussianNoised (prob=0.2)
- get_val_transforms(): nur LoadImaged + EnsureChannelFirstd + 
  ScaleIntensityRanged + Resized

FILE 3: code/ml/data/test_dataset.py
- pytest mit synthetic mini dataset (10 mock DICOMs in tmp_path)
- Test getitem returns correct shapes
- Test mode='train' uses train transforms
- Test missing manifest entries raise

Output: 3 FILE-Header-Codebloecke. PyTorch 2.5+, MONAI 1.4+.

Funktionale Checks: pytest ml/data/test_dataset.py
```

---

## K-11 · `code/ml/models/mfsd_unet.py`

```
Erzeuge die MFSD-UNet-Architektur (U-Net + Swin Transformer Bottleneck 
+ Deep Supervision + 4 Heads). Quelle: Xie et al. 2024 QIMS, zitiert 
in ../08_RESEARCH_ATTENTION_2020-2026.md C1.

FILE 1: code/ml/models/mfsd_unet.py

from __future__ import annotations
import torch
import torch.nn as nn
from timm.models.swin_transformer import SwinTransformerBlock


class ConvBlock(nn.Module):
    """Doppel-Conv mit BatchNorm + ReLU."""
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1, bias=False),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1, bias=False),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.block(x)


class MFSDUNet(nn.Module):
    """
    Multi-Scale Feature with Swin Deep-Supervision UNet.

    Inputs:  (B, 1, 512, 512)
    Outputs: dict with
        - segmentation: (B, 1, 512, 512) Vessel-Maske, Sigmoid
        - stenosis:     (B, 1) NASCET % regression
        - vulnerability:(B, 4) IPH / ThinCap / LRNC / SystolicMotion
        - deciding_feature: (B, 12) Klassifikations-Logits
        - side_outputs: list of 3 (B,1,H,W) fuer Deep-Supervision
    """

    def __init__(self, in_channels: int = 1, base_filters: int = 32,
                 num_features_classes: int = 12):
        super().__init__()

        # Encoder: 4 Stufen
        self.enc1 = ConvBlock(in_channels, base_filters)            # 512x512
        self.enc2 = ConvBlock(base_filters, base_filters*2)         # 256x256
        self.enc3 = ConvBlock(base_filters*2, base_filters*4)       # 128x128
        self.enc4 = ConvBlock(base_filters*4, base_filters*8)       # 64x64
        self.pool = nn.MaxPool2d(2)

        # Bottleneck: Swin-Transformer-Block
        # Hier: vereinfachte Variante mit timm SwinTransformerBlock
        self.swin = SwinTransformerBlock(
            dim=base_filters*8,
            num_heads=8,
            window_size=8,  # 64 / 8 = 8
            shift_size=0,
        )
        self.bn_proj = nn.Conv2d(base_filters*8, base_filters*16, 1)

        # Decoder
        self.up3 = nn.ConvTranspose2d(base_filters*16, base_filters*8, 2, stride=2)
        self.dec3 = ConvBlock(base_filters*16, base_filters*8)
        self.up2 = nn.ConvTranspose2d(base_filters*8, base_filters*4, 2, stride=2)
        self.dec2 = ConvBlock(base_filters*8, base_filters*4)
        self.up1 = nn.ConvTranspose2d(base_filters*4, base_filters*2, 2, stride=2)
        self.dec1 = ConvBlock(base_filters*4, base_filters*2)
        self.up0 = nn.ConvTranspose2d(base_filters*2, base_filters, 2, stride=2)
        self.dec0 = ConvBlock(base_filters*2, base_filters)

        # Heads
        self.seg_head = nn.Conv2d(base_filters, 1, 1)
        self.gap = nn.AdaptiveAvgPool2d(1)
        self.stenosis_head = nn.Sequential(
            nn.Linear(base_filters*16, 64), nn.ReLU(),
            nn.Linear(64, 1),
        )
        self.vuln_head = nn.Sequential(
            nn.Linear(base_filters*16, 64), nn.ReLU(),
            nn.Linear(64, 4),  # 4 Marker, BCEWithLogits in Loss
        )
        self.feat_head = nn.Sequential(
            nn.Linear(base_filters*16, 64), nn.ReLU(),
            nn.Linear(64, num_features_classes),
        )

        # Deep-Supervision Side-Outputs
        self.side3 = nn.Conv2d(base_filters*8, 1, 1)
        self.side2 = nn.Conv2d(base_filters*4, 1, 1)
        self.side1 = nn.Conv2d(base_filters*2, 1, 1)

    def forward(self, x):
        # Encoder
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))
        e4 = self.enc4(self.pool(e3))

        # Bottleneck
        b = self.pool(e4)  # (B, 256, 32, 32) bei base_filters=32
        # Swin braucht (B, H*W, C); rearrange + back
        B, C, H, W = b.shape
        b_flat = b.flatten(2).transpose(1, 2)  # (B, H*W, C)
        b_swin = self.swin(b_flat)
        b = b_swin.transpose(1, 2).reshape(B, C, H, W)
        b = self.bn_proj(b)

        # Decoder
        d3 = self.dec3(torch.cat([self.up3(b), e4], dim=1))
        d2 = self.dec2(torch.cat([self.up2(d3), e3], dim=1))
        d1 = self.dec1(torch.cat([self.up1(d2), e2], dim=1))
        d0 = self.dec0(torch.cat([self.up0(d1), e1], dim=1))

        # Heads
        seg = self.seg_head(d0)  # (B, 1, 512, 512)
        gap = self.gap(b).flatten(1)  # (B, 256*16)  # bottleneck feature
        # Achtung: nach bn_proj ist Channels base_filters*16, fix gap-input

        return {
            "segmentation": seg,
            "stenosis": self.stenosis_head(gap),
            "vulnerability": self.vuln_head(gap),
            "deciding_feature": self.feat_head(gap),
            "side_outputs": [
                nn.functional.interpolate(self.side3(d3), size=512, mode="bilinear", align_corners=False),
                nn.functional.interpolate(self.side2(d2), size=512, mode="bilinear", align_corners=False),
                nn.functional.interpolate(self.side1(d1), size=512, mode="bilinear", align_corners=False),
            ],
        }


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


if __name__ == "__main__":
    m = MFSDUNet()
    print(f"Params: {count_parameters(m):,}")
    x = torch.randn(2, 1, 512, 512)
    out = m(x)
    for k, v in out.items():
        if isinstance(v, list):
            print(f"{k}: list of {len(v)} tensors, shape {v[0].shape}")
        else:
            print(f"{k}: {v.shape}")

FILE 2: code/ml/models/test_mfsd_unet.py
- pytest mit input (1,1,512,512) → korrekte Output-Shapes
- Param-Count im Bereich 10M-80M
- Backward-Pass funktioniert (Gradient flowt)

Output: 2 FILE-Header-Codebloecke.

Funktionale Checks: python ml/models/mfsd_unet.py (laeuft als script, 
gibt Param-Count); pytest ml/models/test_mfsd_unet.py
```

---

## K-12 · `code/ml/training/losses.py` (Composite Loss)

```
Erzeuge die Composite-Loss aus ADR-0002 (Decision-Tree-Harvesting).

FILE 1: code/ml/training/losses.py

from __future__ import annotations
import torch
import torch.nn as nn
import torch.nn.functional as F
from monai.losses import DiceLoss


class CarotisCompositeLoss(nn.Module):
    """
    Loss = α·dice + α·stenosis_mse + β·vuln_bce + γ·reasoning_align 
         + 0.2·feature_ce + 0.1·deep_supervision

    γ wird empirisch via hyperparam-search getuned (siehe 
    scripts/hp_search.py). γ=0 schaltet Reasoning-Alignment-Loss aus 
    (Fallback fuer Notfaelle).
    """

    def __init__(self, alpha=1.0, beta=0.5, gamma=0.3,
                 feature_weight=0.2, deep_super_weight=0.1):
        super().__init__()
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.feature_weight = feature_weight
        self.deep_super_weight = deep_super_weight
        self.dice = DiceLoss(sigmoid=True)
        self.bce = nn.BCEWithLogitsLoss()
        self.mse = nn.MSELoss()
        self.ce = nn.CrossEntropyLoss()

    def forward(self, predictions: dict, targets: dict) -> tuple[torch.Tensor, dict]:
        # predictions keys: segmentation, stenosis, vulnerability, 
        # deciding_feature, side_outputs
        # targets keys: mask, stenosis_pct, vulnerability_4d, 
        # deciding_feature_label, reasoning_region_mask (optional, can be None)

        l_dice = self.dice(predictions["segmentation"], targets["mask"])
        l_stenosis = self.mse(predictions["stenosis"].squeeze(-1), targets["stenosis_pct"])
        l_vuln = self.bce(predictions["vulnerability"], targets["vulnerability_4d"])
        l_feat = self.ce(predictions["deciding_feature"], targets["deciding_feature_label"])

        # Reasoning-Alignment: nur wenn Mask vorhanden
        reasoning_mask = targets.get("reasoning_region_mask")
        if reasoning_mask is not None and self.gamma > 0:
            # Cosine-Similarity zwischen Sigmoid(seg) und reasoning_mask
            seg_sig = torch.sigmoid(predictions["segmentation"])
            seg_flat = seg_sig.flatten(1)
            mask_flat = reasoning_mask.flatten(1).float()
            cos = F.cosine_similarity(seg_flat, mask_flat, dim=1)
            l_align = (1.0 - cos).mean()
        else:
            l_align = torch.tensor(0.0, device=predictions["segmentation"].device)

        # Deep Supervision
        if "side_outputs" in predictions:
            l_deep = sum(
                self.dice(side, targets["mask"])
                for side in predictions["side_outputs"]
            ) / max(len(predictions["side_outputs"]), 1)
        else:
            l_deep = torch.tensor(0.0, device=predictions["segmentation"].device)

        total = (
            self.alpha * (l_dice + l_stenosis)
            + self.beta * l_vuln
            + self.gamma * l_align
            + self.feature_weight * l_feat
            + self.deep_super_weight * l_deep
        )

        return total, {
            "dice": l_dice.detach(),
            "stenosis_mse": l_stenosis.detach(),
            "vulnerability_bce": l_vuln.detach(),
            "reasoning_align": l_align.detach(),
            "feature_ce": l_feat.detach(),
            "deep_super": l_deep.detach(),
            "total": total.detach(),
        }

FILE 2: code/ml/training/test_losses.py
- pytest mit synthetic Tensors:
  - happy path: alle targets vorhanden, Loss > 0, Gradient flowt
  - reasoning_region_mask=None: l_align=0, andere Komponenten OK
  - gamma=0: l_align effektiv 0 in der Total-Berechnung
  - Loss-Wert fuer "perfekte" Vorhersage (seg=mask, stenosis=target, 
    etc.) sollte sehr klein sein

Output: 2 FILE-Header-Codebloecke.

Funktionale Checks: pytest ml/training/test_losses.py
```

---

## K-13 · `code/ml/training/train.py`

```
Erzeuge den Trainings-Script mit MLflow-Logging und 
Auto-Rollback-Logik fuer den Daily-Loop.

FILE 1: code/ml/training/train.py
- argparse CLI: --config (yaml), --resume (ckpt path), --incremental 
  (bool), --max-epochs (int), --early-stopping-patience (int), 
  --output-dir
- yaml-config laden mit alpha, beta, gamma, lr, batch_size, num_workers, 
  data_root, manifest_csv, val_split
- Reproducibility: torch.manual_seed(config.seed), 
  torch.use_deterministic_algorithms(True), 
  numpy.random.seed, random.seed
- Datasets via CarotisDataset + get_train/val_transforms
- Modell instanziieren MFSDUNet
- Loss CarotisCompositeLoss(alpha, beta, gamma)
- Optimizer AdamW(lr=config.lr, weight_decay=1e-4)
- Scheduler CosineAnnealingWarmRestarts
- mlflow.start_run(): log_params(config), log_artifact(config_yaml)
- Per epoch:
  - train_loss, train_dice, train_stenosis_mae, train_vuln_auc
  - val_loss, val_dice, val_stenosis_mae, val_vuln_auc, val_composite
  - mlflow.log_metrics(...)
  - if val_composite > best: best = val_composite, save checkpoint
  - early_stopping if no improvement in patience
- Bei --incremental:
  - Replay-Buffer: 50% neue Daten, 50% historische via 
    ConcatDataset(new, historical_subsample)
  - base_model_composite via separate eval auf hold-out-test
  - Wenn val_composite < base - 0.005: log "rollback_triggered" + 
    return code 1 (kein neuer Checkpoint geschrieben)

FILE 2: code/ml/training/test_train.py
- pytest mit synthetischen 10-Sample-Datasets
- Test 1 Epoch laeuft ohne Error
- Test MLflow-Run wird erstellt
- Test --incremental + intentionally_bad_data → rollback (return code 1)

Output: 2 FILE-Header-Codebloecke.

Funktionale Checks: pytest ml/training/test_train.py
```

---

## K-14 · `code/ml/export_onnx.py`

```
Erzeuge das ONNX-Export-Script.

FILE 1: code/ml/export_onnx.py

from __future__ import annotations
import argparse
from pathlib import Path
import torch
import numpy as np
import onnx
import onnxruntime as ort
import onnxsim

from ml.models.mfsd_unet import MFSDUNet


def export(checkpoint_path: Path, output_path: Path, opset: int = 18) -> None:
    # 1. Modell laden
    model = MFSDUNet()
    state = torch.load(checkpoint_path, map_location="cpu")
    model.load_state_dict(state["model"] if "model" in state else state)
    model.eval()

    # 2. Dummy-Input
    dummy = torch.randn(1, 1, 512, 512)

    # 3. Export
    torch.onnx.export(
        model, dummy, str(output_path),
        opset_version=opset,
        input_names=["input"],
        output_names=["segmentation", "stenosis", "vulnerability", "deciding_feature"],
        dynamic_axes={
            "input": {0: "batch_size"},
            "segmentation": {0: "batch_size"},
            "stenosis": {0: "batch_size"},
            "vulnerability": {0: "batch_size"},
            "deciding_feature": {0: "batch_size"},
        },
        do_constant_folding=True,
    )

    # 4. Verify: re-load + Vergleich PyTorch vs ONNX
    onnx_model = onnx.load(str(output_path))
    onnx.checker.check_model(onnx_model)

    # Simplify
    simplified, ok = onnxsim.simplify(onnx_model)
    if ok:
        onnx.save(simplified, str(output_path))

    # Output-Vergleich
    sess = ort.InferenceSession(str(output_path), providers=["CPUExecutionProvider"])
    onnx_outputs = sess.run(None, {"input": dummy.numpy()})
    with torch.no_grad():
        torch_outputs = model(dummy)
    seg_diff = np.abs(onnx_outputs[0] - torch_outputs["segmentation"].numpy()).max()
    if seg_diff > 1e-4:
        raise RuntimeError(f"ONNX export verification failed: seg_diff={seg_diff}")

    print(f"OK exported to {output_path} (seg_diff_max={seg_diff:.6f})")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--opset", default=18, type=int)
    args = p.parse_args()
    export(args.checkpoint, args.output, args.opset)


if __name__ == "__main__":
    main()

FILE 2: code/ml/test_export_onnx.py
- pytest mit Mini-MFSDUNet (kleinere base_filters=8 fuer Speed)
- random initialisieren, exportieren, re-load, Output-Diff < 1e-4

Output: 2 FILE-Header-Codebloecke.

Funktionale Checks: 
- pytest ml/test_export_onnx.py
- python ml/export_onnx.py --checkpoint <path> --output 
  data/models/mfsd_unet.onnx
```

---

## K-15 · Stage G bundled — Tests + CI (8 Files in 1 Prompt)

```
Erzeuge in EINER Antwort die Test-Suite und CI-Workflows.

FILE 1: code/tests/conftest.py
- Fixtures: test_db (in-memory SQLite), test_app (mit gemockten 
  Settings), test_client (httpx AsyncClient), test_dicom_bytes 
  (synthetic), test_anonymized_dicom, mock_inference_service
- ENV vars werden monkeypatched

FILE 2: code/tests/test_anonymization_bridge.py
- Test Backend rejects DICOM mit PII (Patient Name gesetzt) → 422
- Test Backend accepts anonymized DICOM
- Test scripts/anonymize.py wird aufgerufen wenn Auto-Anon 
  konfiguriert

FILE 3: code/tests/test_decision_tree_validation.py
- Test POST /decision-tree/capture mit valid payload → 200, audit_id
- Test mit missing required field → 422
- Test mit case_id wrong format → 422
- Test mit verdict outside enum → 422

FILE 4: code/tests/test_audit_trail.py
- Test AuditEvent kann inserted werden
- Test AuditEvent.update() raises IntegrityError (append-only enforced)
- Test AuditEvent.delete() raises IntegrityError
- Test jede Inferenz erzeugt einen Audit-Eintrag

FILE 5: code/tests/test_inference_full.py
- End-to-End mit Demo-ONNX-Modell (von 
  scripts/generate_demo_model.py):
  1. Generate Demo-Modell ins tmp_path
  2. Load via InferenceService
  3. Synthetic anonymized DICOM upload
  4. Verify Response-Shape
  5. Verify Audit-Event geschrieben

FILE 6: code/tests/test_ml_pipeline.py
- Test ml/training/train.py mit synthetic 10-Sample-Dataset, 1 Epoch
- Test ml/export_onnx.py roundtrip mit Mini-Modell

FILE 7: code/.github/workflows/ci.yml
GitHub Actions:
- jobs: lint, test-backend, test-ml, test-frontend, security, build
- on: pull_request, push to main
- lint: ruff + black (Python), eslint + tsc (TypeScript)
- test-backend: pytest --cov=app --cov-report=xml, codecov upload
- test-ml: pytest --cov=ml
- test-frontend: typecheck, lint, vitest
- security: bandit, npm audit, plus assertion grep -r 
  "openai\|anthropic" app/services/inference || true (fail wenn 
  Match) — Local-First-Enforcement
- build: docker compose build, smoke (compose up -d, curl health, 
  compose down)

FILE 8: code/.github/workflows/local_smoke.yml
- workflow_dispatch + scheduled wöchentlich
- Job: ollama-setup (image pull, qwen2.5-coder:7b pull als kleinstes), 
  hermes-smoke (depends_on, ping, einfacher Prompt mit 5-Min-Timeout)
- Optional, kein PR-Block

Output: 8 FILE-Header-Codebloecke.

Funktionale Checks (Lou):
- pytest -v in code/ — Coverage-Target ≥ 80% fuer app/services und 
  ml/training, ≥ 90% fuer app/api/routes und scripts/anonymize.py
- act -W .github/workflows/ci.yml (lokal mit `act` Tool, optional)
```

---

## K-16 · Stage H bundled — Hermes Integration (5 Files in 1 Prompt)

```
Erzeuge die Hermes-Agent-Integration in EINER Antwort.

FILE 1: code/hermes/config.toml

[agent]
name = "carotis-helper"
description = "Self-improving agent for Carotis-AI Engineering and Operations"

[provider]
type = "ollama"
endpoint = "http://localhost:11434"
model = "nous-hermes-3-llama-3.1"
timeout_seconds = 1800  # 30 Min fuer lokale Prefills

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
  "../scripts/validate_decision_tree.py",
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
execute_allowlist = "skills"
deny_endpoints = ["api.anthropic.com", "api.openai.com"]

FILE 2: code/hermes/skills/anonymize-batch.md
---
name: anonymize-batch
trigger_phrases: ["anonymisiere DICOM", "anonymize batch", 
                  "DICOM batch anonym"]
required_tools: [bash]
---
# Anonymize-Batch Skill

Action: Ruft scripts/anonymize.py mit dem geforderten Pfad auf, parsed 
das Manifest, gibt eine Zusammenfassung als Markdown.

Steps:
1. Parse user input: extract input_dir und output_dir
2. Run: bash -c "python ../scripts/anonymize.py --input <in> 
   --output <out> --salt $ANONYMIZATION_SALT"
3. Read das output/<batch>.manifest.json
4. Return Markdown mit:
   - Anzahl files: ok / rejected_low_k / rejected_pii_leak
   - Liste der rejected mit Reason
   - SHA-256 des Manifest fuer Audit-Trail

FILE 3: code/hermes/skills/capture-decision-tree.md
---
name: capture-decision-tree
trigger_phrases: ["erfasse Arzt-Entscheidung", "save decision tree", 
                  "capture decision"]
required_tools: [filesystem, bash]
---
# Capture-Decision-Tree Skill

Action: Nimmt JSON-Input (das complete Decision-Tree-Schema), 
validiert, schreibt in memory/decisions/, erzeugt Audit-Event.

Steps:
1. Parse JSON aus user input
2. Run: python ../scripts/validate_decision_tree.py <tmp.json>
3. Bei valid: write to ../memory/decisions/<datum>_<case_id_short>.json
4. Bei invalid: return Fehler-Liste, kein Write
5. POST /audit/event an localhost:8000 (Backend) mit event_type=
   decision_tree_captured, payload={case_id, audit_id}

FILE 4: code/hermes/skills/nightly-retrain.md
---
name: nightly-retrain
trigger_phrases: ["trainiere mit neuen Decision-Trees", 
                  "nightly retrain", "incremental train"]
schedule: "0 22 * * *"  # 22:00 Klinikum-Schliesszeit
required_tools: [bash, filesystem]
---
# Nightly-Retrain Skill

Action: Liest memory/decisions/ since last_run, wenn ≥ 10 neue Trees 
verfuegbar, ruft ml/training/train.py --incremental, vergleicht 
Performance, deploy oder rollback.

Steps:
1. ls ../memory/decisions/ | filter > last_run_timestamp
2. Wenn count < 10: log "skipped, nicht genug Trees", exit
3. Run: python ../ml/training/train.py --incremental --max-epochs 3 
   --config configs/incremental.yaml
4. Bei return-code 1: log "rollback_triggered", senden Alert an Lou 
   (Mail oder Slack via Hermes-Webhook)
5. Bei return-code 0: 
   a. python ../ml/export_onnx.py --checkpoint <new_ckpt> 
      --output ../data/models/mfsd_unet_new.onnx
   b. python ../scripts/sign_model.py (kommt in T-016 aus tasks.jsonl)
   c. atomic mv mfsd_unet_new.onnx → mfsd_unet.onnx
   d. POST /admin/reload-model an Backend (causes lazy reload)
6. Eintrag in ../memory/runs/<datum>_nightly_retrain.md mit 
   Performance-Diff

FILE 5: code/scripts/demo.sh — ERWEITERUNG
WICHTIG: Lou hat bereits eine demo.sh mit Steps 1-4 (Docker check, 
data directories, .env, demo ONNX). NICHT komplett neu schreiben — 
nur die folgenden Steps am Ende ANFUEGEN:

# ── Step 5: Local AI Stack ─────────────────────────────────────────
step "Bootstrapping Hermes + Ollama..."
if ! curl -sf localhost:11434/api/tags > /dev/null 2>&1; then
    bash scripts/install_local_stack.sh
else
    ok "Ollama already running."
fi

step "Verify Hermes Agent..."
if curl -sf localhost:8200/ping > /dev/null 2>&1; then
    ok "Hermes Agent running."
else
    step "Starting Hermes via docker-compose..."
    docker compose -f docker-compose.yml up -d hermes
    sleep 5
    curl -sf localhost:8200/ping > /dev/null || fail "Hermes did not start. Check logs: docker compose logs hermes"
fi

# ── Step 6: Smoke Test ────────────────────────────────────────────
step "Running smoke test..."
docker compose run --rm backend pytest tests/test_smoke.py -q || fail "Smoke test failed"
ok "All systems operational."

banner "Demo Stack Ready"
echo -e "  Backend:   http://localhost:8000"
echo -e "  Frontend:  http://localhost:3000"
echo -e "  Ollama:    http://localhost:11434"
echo -e "  Hermes:    http://localhost:8200"
echo -e "  Dashboard: ../dashboard.html (open in browser)"

Output: 5 FILE-Header-Codebloecke. Hermes-Skill-Files im 
Frontmatter-Format (Hermes-Agent-Standard).

Funktionale Checks (Lou):
- bash code/scripts/demo.sh → alle Steps gruen
- curl localhost:11434/api/tags listet Modelle
- curl localhost:8200/ping antwortet
```

---

## NACH ALLEN PROMPTS — End-to-End-Verifikation

```bash
cd "C:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI"
bash scripts/preflight.sh

cd code
docker compose up -d
sleep 30
curl localhost:8000/health
curl localhost:11434/api/tags
curl localhost:8200/ping
pytest -v
```

Wenn alle 5 Calls gruen + pytest gruen: P0/P1/P2-Code-Fundament steht. Du kannst dann zum Stakeholder-Pfad zurueck (`RUNBOOK_TODAY.md` Schritt 8 — Mail an Prof. Rohde rausschicken).

---

## Token-Saver-Tipps fuer Kimi

1. **Setup-Block einmal pasten**, danach nicht wiederholen — Kimi haelt den Kontext.
2. **Ein Prompt = ein Output-Codeblock-Set** — keine Zwischenfragen.
3. **Bei Halluzination**: kurz "Korrektur in FILE X: <bug>" — Kimi gibt nur den korrigierten File neu, nicht alles.
4. **Lange Files (mfsd_unet.py, train.py)**: pro File ein eigener Prompt, nicht buendeln.
5. **Memory-Disziplin**: 5-Zeilen-Run-Log pro Prompt in 
   `memory/runs/2026-04-28_kimi_K-NN.md` — sonst verlierst du den Engineering-Harness-Vorteil.
6. **Re-Runs minimieren**: wenn Kimi was nicht versteht, lieber den Prompt verfeinern als nochmal pasten. Pro ueberfluessigem Re-Run: 2k-5k Tokens.

---

## Aenderungen gegenueber 09_COPILOT_PROMPT_SEQUENCE.md (Lessons Learned)

| Lesson aus P-01 (Copilot) | Hier korrigiert |
|---|---|
| Line-Count-DoDs sind Muell (Copilot lieferte 76 statt 100, Inhalt komplett) | Hier nur **funktionale Checks** (Sektionen vorhanden, Pfade aufloesbar) |
| PowerShell-Console-Codepage cp1252 garbled UTF-8-Files | Setup-Block erklaert: VS Code reads UTF-8 nativ, PowerShell-Console ist nur Console-Garbling |
| 29 Round-Trips bei Copilot | 16 Round-Trips bei Kimi durch Bundling — 45% weniger |
| Copilot @workspace und Auto-Load von .github/copilot-instructions.md fehlt bei Kimi | Setup-Block laedt den Kontext einmal in die Session |
| Verify-Commands waren PowerShell-zentriert | Hier: VS-Code-Visual-Review oder pytest als Verify |

---

## Sources

- [Jake van Clief — Interpretable Context Methodology (arXiv 2603.16021)](https://arxiv.org/abs/2603.16021)
- [Hermes Agent (Nous Research)](https://github.com/nousresearch/hermes-agent)
- [Hermes-Agent Ollama Setup](https://hermes-agent.ai/blog/hermes-agent-ollama-setup)
- [Kimi K2.6 (Moonshot AI)](https://kimi.moonshot.cn/)
- [Carotid Segmentation MFSD-UNet — Xie 2024 QIMS](https://qims.amegroups.org/article/view/135680/html)

---

**Version:** 1.0 · **Erstellt:** 2026-04-28 · Opus 4.7 (Cowork)
**Adapted from:** 09_COPILOT_PROMPT_SEQUENCE.md (29 Prompts → 16 Prompts durch Bundling)

---
---

# APPENDIX P0a — Demo-Robustheit (K-17 bis K-22)

> **Hinzugefügt:** 2026-04-29 nach K-01..K-16-Abschluss durch Kimi (E2E 22/24 grün, 13 Bugs gefixt — siehe `memory/anomalies/2026-04-29_kimi_e2e_13_bugs.md`).
>
> **Zweck:** Die K-01..K-16 haben den Code-Stack gebaut. P0a macht ihn **demo-bulletproof** für das Rohde-Meeting. Tech-Debt-Items aus dem Anomalie-Bericht + Demo-Daten + Walkthrough-Skript.
>
> **Reihenfolge:** K-17, K-18, K-19 parallel-safe (3 Tabs gleichzeitig). Dann K-20 sequentiell (braucht funktionierenden Stack). Dann K-21 + K-22 parallel.
>
> **Pre-Flight für jeden K-17..K-22-Prompt:** Erinnere Kimi an die Top-3-Anti-Patterns aus `memory/anomalies/2026-04-29_kimi_e2e_13_bugs.md`:
> - B-08: Niemals Settings beim Modul-Import cachen
> - B-04: Niemals `from __future__ import annotations` in FastAPI-Routes mit `UploadFile`
> - B-13: Niemals Unicode-Pfeile in Python-Console-Skripten

---

## K-17 · Tech-Debt Quick-Fixes (Router-Prefix + pytest-asyncio config) [PARALLEL]

```
PRE-FLIGHT: 3 Anti-Patterns aus dem 13-Bugs-Memo respektieren (B-08, 
B-04, B-13).

Zwei Tech-Debt-Items aus memory/anomalies/2026-04-29_kimi_e2e_13_bugs.md 
fixen.

FILE 1: code/backend/app/main.py — patch
Add `/api/v1` als gemeinsames Prefix fuer alle Domain-Router 
(health bleibt root). Ergebnis:
- GET /health (root, kein Prefix)
- POST /api/v1/inference/predict
- POST /api/v1/decision-tree/capture
- GET /api/v1/audit/trail
Aenderung im create_app():
  app.include_router(health.router)
  app.include_router(inference.router, prefix="/api/v1")
  app.include_router(decision_tree.router, prefix="/api/v1")
  app.include_router(audit.router, prefix="/api/v1")

FILE 2: code/backend/tests/test_smoke.py — update
Pfade in den Tests anpassen auf /api/v1/inference/predict, 
/api/v1/decision-tree/capture, /api/v1/audit/trail. /health bleibt 
root.

FILE 3: code/scripts/demo.sh — update
Curl-Befehle am Ende auf /api/v1/-Pfade umstellen (analog).

FILE 4: code/pytest.ini — neu erstellen oder erweitern
[pytest]
asyncio_default_fixture_loop_scope = function
asyncio_mode = auto
filterwarnings =
    error
    ignore::DeprecationWarning:passlib
testpaths = tests backend/tests ml
addopts = --strict-markers -ra

FILE 5: code/frontend/src/lib/apiClient.ts — patch
BASE_URL umstellen auf VITE_API_URL + "/api/v1" als zusaetzliche 
Konstante:
  const API_PREFIX = "/api/v1";
  // dann: fetch(`${BASE_URL}${API_PREFIX}/inference/predict`, ...)
Health-Check bleibt direkt: fetch(`${BASE_URL}/health`).

FUNKTIONALE CHECKS (Lou):
- pytest -v → alle Tests gruen mit neuen Pfaden
- npm run typecheck → 0 Errors
- curl localhost:8000/api/v1/inference/predict mit gueltigem API-Key 
  und Test-DICOM → 200
```

---

## K-18 · DB-Engine Refactor (Engine nicht beim Modul-Import) [PARALLEL]

```
PRE-FLIGHT: 13-Bugs-Memo. Speziell B-08 (Settings nicht beim Import 
cachen) — analog hier fuer Engine.

Anomalie A-03 fixen: code/backend/app/db/database.py erstellt 
async_engine beim Modul-Import. Fuer Tests problematisch (DB-Sharing 
zwischen Test-Sessions).

FILE 1: code/backend/app/db/database.py — refactor

from __future__ import annotations
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import get_settings
from app.db.models import Base


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    """Lazy engine creation. Tests koennen lru_cache clearen + Settings 
    monkeypatchen."""
    settings = get_settings()
    return create_async_engine(
        settings.database_url,
        echo=False,
        future=True,
        pool_pre_ping=True,
    )


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(get_engine(), expire_on_commit=False)


async def init_db() -> None:
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    SessionLocal = get_session_factory()
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def reset_db() -> None:
    """Test-Helper: drop_all + create_all."""
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

FILE 2: code/backend/tests/conftest.py — anpassen
Fixture `test_db` ruft jetzt `await reset_db()` statt manuelles 
drop_all+create_all. Plus: in jedem Test-Setup `get_engine.cache_clear()` 
nach `monkeypatch.setenv("DATABASE_URL", ...)`.

FILE 3: code/backend/app/main.py — anpassen
Lifespan ruft `await init_db()` (unveraendert), aber `app.state.engine` 
wird nicht mehr explizit gesetzt — wer Engine braucht, ruft 
`get_engine()`.

FUNKTIONALE CHECKS (Lou):
- pytest -v → alle Tests weiter gruen
- Insbesondere: 2 Tests parallel mit unterschiedlichen DATABASE_URL 
  envs lassen sich isolieren
- App startet ohne Boot-Error
```

---

## K-19 · Cornerstone3D WASM-Init + Minimal-Rendering [PARALLEL]

```
PRE-FLIGHT: 13-Bugs-Memo. 

Anomalie A-02 fixen: Frontend Cornerstone3D-Init fehlt — DICOMs werden 
nicht gerendert. Demo-kritisch fuer Rohde-Meeting.

FILE 1: code/frontend/src/lib/cornerstoneSetup.ts
Initialisiert Cornerstone3D mit dicom-image-loader, registriert 
Image-Loader Schemes wadouri/wadors, konfiguriert WASM-Pfade.

import { init as csInit, RenderingEngine, Enums, Types, volumeLoader, imageLoader, metaData } from "@cornerstonejs/core";
import { init as csToolsInit, addTool, ToolGroupManager, PanTool, ZoomTool, WindowLevelTool, LengthTool, BrushTool, Enums as csToolsEnums } from "@cornerstonejs/tools";
import dicomParser from "dicom-parser";
import { init as dicomImageLoaderInit, wadouri, wadors } from "@cornerstonejs/dicom-image-loader";

let initialized = false;

export async function initCornerstone() {
  if (initialized) return;
  await csInit();
  await csToolsInit();
  dicomImageLoaderInit({ maxWebWorkers: 1 });
  // metadata wird vom dicom-image-loader providert
  imageLoader.registerImageLoader("wadouri", wadouri.loadImage);
  imageLoader.registerImageLoader("wadors", wadors.loadImage);

  // Tools registrieren
  addTool(PanTool);
  addTool(ZoomTool);
  addTool(WindowLevelTool);
  addTool(LengthTool);
  addTool(BrushTool);

  initialized = true;
}

export const TOOL_GROUP_ID = "carotis-tools";

export function createDefaultToolGroup() {
  const group = ToolGroupManager.createToolGroup(TOOL_GROUP_ID);
  if (!group) return ToolGroupManager.getToolGroup(TOOL_GROUP_ID)!;
  group.addTool(PanTool.toolName);
  group.addTool(ZoomTool.toolName);
  group.addTool(WindowLevelTool.toolName);
  group.addTool(LengthTool.toolName);
  group.addTool(BrushTool.toolName);
  group.setToolActive(PanTool.toolName, { bindings: [{ mouseButton: csToolsEnums.MouseBindings.Auxiliary }] });
  group.setToolActive(WindowLevelTool.toolName, { bindings: [{ mouseButton: csToolsEnums.MouseBindings.Primary }] });
  group.setToolActive(ZoomTool.toolName, { bindings: [{ mouseButton: csToolsEnums.MouseBindings.Secondary }] });
  return group;
}

FILE 2: code/frontend/src/components/DicomViewer/DicomViewer.tsx — refactor
- useEffect ruft initCornerstone() einmal beim Mount
- Erstellt RenderingEngine mit eindeutiger ID per Component-Instance
- Erstellt StackViewport oder VolumeViewport
- Lädt das DICOM via wadouri:url (wenn Backend serviert) oder via 
  upload-flow (DICOM-Bytes im File-State)
- Cleanup: ToolGroupManager.destroyToolGroup() + RenderingEngine.destroy()

FILE 3: code/frontend/src/components/DicomViewer/HeatmapOverlay.tsx
Component die heatmap-array (vom Backend, Float32 512x512) als 
zweite Layer ueber dem DICOM rendert. Opacity-Slider 0-100%. Nutzt 
Canvas-2D-Context (kein Cornerstone-Tool — eigener Layer).

FILE 4: code/frontend/src/components/DicomViewer/index.ts
Barrel-Export.

FILE 5: code/frontend/vite.config.ts — patch
Falls Cornerstone WASM-Files extra Build-Konfiguration brauchen:
- assetsInclude: ['**/*.wasm']
- optimizeDeps.exclude: ['@cornerstonejs/dicom-image-loader']

FILE 6: code/frontend/src/components/DicomViewer/test_DicomViewer.tsx
Vitest mit @testing-library/react. Mock Cornerstone via vi.mock(). 
Smoke-Test: Component rendert ohne Crash bei minimalen Props.

FUNKTIONALE CHECKS (Lou):
- npm run dev → Component rendert ein Test-DICOM (Browser-Konsole 
  ohne Cornerstone-Errors)
- Tools (Pan/Zoom/Window) reagieren auf Maus-Events
- Heatmap-Overlay-Slider verändert Sichtbarkeit
```

---

## K-20 · Demo-Daten-Generator (10 Synthetic Anonymized DICOMs) [SEQUENTIAL nach K-17/18/19]

```
PRE-FLIGHT: 13-Bugs-Memo. Speziell B-13 (kein Unicode in Python-
Console) und B-12 (Schema erlaubt null fuer reasoning).

Erzeuge ein Skript das 10 synthetische, anonymisierte DICOM-Files + 
10 Decision-Tree-Sample-JSONs erzeugt. Die werden im Rohde-Meeting 
als Live-Demo-Daten verwendet (kein PII, kein Klinikum-Daten-Risiko).

FILE 1: code/scripts/generate_demo_data.py

from __future__ import annotations
import argparse
import hashlib
import json
import random
import string
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np
import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid


SALT = "demo-only-salt-do-not-use-in-prod"


def _make_dicom(case_idx: int, output_dir: Path, anonymized: bool = True) -> Path:
    """Erzeugt ein synthetic 512x512 DICOM mit Carotis-Bifurkations-
    aehnlichem Bild. Bereits anonymisiert (alle 33 PII-Tags absent).
    """
    rng = np.random.default_rng(seed=case_idx)
    pixel_array = (rng.normal(120, 30, (512, 512))
                   .clip(-100, 600)
                   .astype(np.int16))
    # Synthetic vessel: kleiner Kontrast-Spot
    cx, cy = rng.integers(200, 312, size=2)
    rr, cc = np.ogrid[:512, :512]
    mask = (rr - cx) ** 2 + (cc - cy) ** 2 < 1500
    pixel_array[mask] = 400

    file_meta = pydicom.dataset.FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = pydicom.uid.CTImageStorage
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    file_meta.ImplementationClassUID = generate_uid()

    ds = FileDataset(str(output_dir / f"case_{case_idx:03d}.dcm"),
                     {}, file_meta=file_meta, preamble=b"\\0" * 128)
    ds.SOPClassUID = pydicom.uid.CTImageStorage
    ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
    ds.Modality = "CT"
    ds.PatientID = ""        # leer = anonymized
    ds.PatientName = ""
    ds.PatientBirthDate = ""
    ds.AccessionNumber = ""
    ds.StudyDate = ""
    ds.Manufacturer = "Demo"
    ds.Rows = 512
    ds.Columns = 512
    ds.BitsAllocated = 16
    ds.BitsStored = 12
    ds.HighBit = 11
    ds.PixelRepresentation = 1
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.RescaleIntercept = 0
    ds.RescaleSlope = 1
    ds.WindowCenter = 200
    ds.WindowWidth = 800
    ds.is_little_endian = True
    ds.is_implicit_VR = False
    ds.PixelData = pixel_array.tobytes()
    output_path = output_dir / f"case_{case_idx:03d}.dcm"
    ds.save_as(output_path)
    return output_path


def _make_decision_tree(case_idx: int, dicom_path: Path) -> dict:
    """Erzeugt einen synthetic Decision-Tree fuer das DICOM.
    Variiert Stenosegrad + Marker fuer realistische Demo-Diversity.
    """
    rng = random.Random(case_idx)
    salt_input = f"{dicom_path.stem}|{SALT}|2026-W18"
    case_id = hashlib.sha256(salt_input.encode()).hexdigest()
    role_salt_input = f"demo-attending|{SALT}"
    role_hash = hashlib.sha256(role_salt_input.encode()).hexdigest()

    ai_stenosis = round(rng.uniform(20, 90), 1)
    physician_stenosis = ai_stenosis + rng.choice([-5, -2, 0, 2, 3, 5])
    physician_stenosis = max(0, min(100, physician_stenosis))
    delta = round(physician_stenosis - ai_stenosis, 1)
    verdict = ("full_agreement" if abs(delta) < 1 else
               "partial_agreement" if abs(delta) < 5 else
               "disagreement")

    markers_pool = ["intraplaque_hemorrhage", "thin_fibrous_cap",
                    "lipid_rich_necrotic_core", "systolic_motion_anomaly"]
    confirmed = rng.sample(markers_pool, k=rng.randint(0, 3))

    return {
        "case_id": case_id,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "physician_role_hash": role_hash,
        "ai_prediction": {
            "stenosis_pct_nascet": ai_stenosis,
            "confidence": round(rng.uniform(0.65, 0.95), 2),
            "vulnerability_markers": {m: round(rng.uniform(0, 1), 2) for m in markers_pool},
            "model_version": "v0.1.0",
            "model_sha": "demo000",
        },
        "physician_decision": {
            "stenosis_pct_nascet": physician_stenosis,
            "confidence_self_reported": rng.choice(["low", "medium", "high", None]),
            "confirmed_markers": confirmed,
            "rejected_markers": [m for m in markers_pool if m not in confirmed and rng.random() < 0.2],
            "added_markers": [],
        },
        "reasoning": None if rng.random() < 0.3 else {
            "deciding_feature": rng.choice([
                "echolucent_zone_dorsal", "calcified_shell_partial",
                "intraplaque_hemorrhage_signal", "fibrous_cap_thinning",
            ]),
            "ruled_out": [],
            "ruled_out_reason": "",
            "would_consult": None,
            "would_re_image_if": None,
        },
        "agreement_with_ai": {
            "verdict": verdict,
            "delta_pct": delta,
            "delta_markers": [],
            "trust_score_for_this_case": rng.randint(2, 5),
        },
        "anonymisation": {
            "method": "DICOM_PS_3.15_basic",
            "salt_version": "v2026-04",
            "audit_id": f"DEMO-{case_idx:03d}",
            "k_anonymity_min": 5,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate 10 synthetic anonymized DICOMs + decision-trees for demo."
    )
    parser.add_argument(
        "--output-dir",
        default=Path("data/demo"),
        type=Path,
        help="Output directory (default: data/demo)",
    )
    parser.add_argument("--count", type=int, default=10)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    dicoms_dir = args.output_dir / "dicoms"
    trees_dir = args.output_dir / "decision_trees"
    dicoms_dir.mkdir(exist_ok=True)
    trees_dir.mkdir(exist_ok=True)

    for i in range(args.count):
        dicom_path = _make_dicom(i, dicoms_dir)
        tree = _make_decision_tree(i, dicom_path)
        tree_path = trees_dir / f"case_{i:03d}.json"
        tree_path.write_text(json.dumps(tree, indent=2), encoding="utf-8")
        print(f"  generated case_{i:03d} -> {dicom_path.name} + {tree_path.name}")

    print(f"\nDemo data ready in {args.output_dir}")
    print(f"  dicoms/      ({args.count} files)")
    print(f"  decision_trees/  ({args.count} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

FILE 2: code/scripts/test_generate_demo_data.py
pytest mit:
- Test alle 10 DICOMs werden erzeugt
- Test alle 10 Decision-Trees validieren gegen 
  schemas/decision_tree.schema.json
- Test alle DICOMs haben 0 PII (pruefe alle 33 PII-Tags absent)
- Test `python scripts/anonymize.py --check --input data/demo/dicoms` 
  exit-code 0

KRITISCH: ASCII-only im stdout (keine Unicode-Pfeile, B-13).

FUNKTIONALE CHECKS (Lou):
- python scripts/generate_demo_data.py
- ls data/demo/dicoms/  (10 Files)
- python scripts/validate_decision_tree.py data/demo/decision_trees/
- pytest scripts/test_generate_demo_data.py
```

---

## K-21 · 5-Min-Demo-Walkthrough-Skript [SEQUENTIAL nach K-20]

```
PRE-FLIGHT: 13-Bugs-Memo durchgelesen.

Erzeuge das Walkthrough-Skript fuer das Rohde-Meeting (laut 
06_ROHDE_MEETING_KIT.md Sektion 4 in 5 Minuten). 

FILE 1: code/scripts/demo_walkthrough.md
Schritt-fuer-Schritt-Anleitung:
- Markdown mit 5 Sektionen entsprechend den 5 Demo-Minuten
- Pro Sektion: was Lou sagt + welche Aktion er auf dem Bildschirm 
  macht + welcher curl/CLI-Befehl ggf. hinten ablaeuft + welche 
  visuelle Reaktion zu erwarten ist

Sections:
1. Min 0:00-1:00 — Dashboard-Tour: dashboard.html im Browser 
   oeffnen, Phase-Status, Tasks-Kanban, Modell-Verteilung zeigen.
2. Min 1:00-2:00 — Architektur: code/HARNESS.md auf Beamer, 
   Routing-Matrix erklaeren, "wir trennen Cloud-Architektur von 
   Lokal-Inferenz".
3. Min 2:00-3:30 — Live-Demo: Frontend laeuft, Lou laedt eines der 
   10 demo-DICOMs hoch, AI-Panel zeigt Stenosegrad + Heatmap. 
   "Decision-Tree-Form" am Beispiel ausfuellen.
4. Min 3:30-4:30 — Audit-Trail: curl localhost:8000/api/v1/audit/trail 
   in Konsole, JSON-Output zeigen, "jede Inferenz ist nachvollziehbar".
5. Min 4:30-5:00 — Engineering Harnessing: 09b_KIMI_PROMPT_SEQUENCE.md 
   zeigen ("hier sind die Prompts mit denen wir Kimi den Code 
   generieren liessen") + memory/runs/-Liste ("hier dokumentiert 
   jede Session was sie gelernt hat").

FILE 2: code/scripts/run_demo.sh
Bash-Skript das alles vorbereitet:
1. Pre-Flight (../scripts/preflight.sh)
2. docker compose up -d (mit Health-Check-Wait)
3. python scripts/generate_demo_data.py (falls noch nicht da)
4. POST data/demo/decision_trees/*.json an /api/v1/decision-tree/capture 
   (10 mal, fuer realistischen Audit-Trail im /trail-Output)
5. Browser oeffnen (xdg-open or start) auf:
   - http://localhost:3000 (Frontend)
   - file:///<dashboard-path> (Dashboard)
6. Output: "DEMO READY. Press any key to open VS Code with 
   demo_walkthrough.md."

FILE 3: code/scripts/run_demo.ps1
PowerShell-Port von run_demo.sh. ASCII-only im Output (B-13).

FILE 4: code/scripts/teardown_demo.sh + .ps1
Cleanup: docker compose down --volumes, rm -rf data/demo (optional 
mit --keep-data Flag).

FUNKTIONALE CHECKS (Lou):
- bash scripts/run_demo.sh ohne Error
- Frontend zeigt DICOM mit Heatmap
- /api/v1/audit/trail zeigt 10 Decision-Tree-Captures
```

---

## K-22 · Dashboard-Update mit completed-Tasks + Status [PARALLEL zu K-21]

```
PRE-FLIGHT: 13-Bugs-Memo. 

Update dashboard.html mit aktuellem Status:
- K-01..K-16 als done markieren (im embedded TASKS-Array)
- K-17..K-22 als pending hinzufuegen
- Phase-Status: P0 als "🔄 80% — Code-Stack done, Demo-Robustness in 
  Progress, Mail an Rohde noch offen"
- Stat: 22 Tests gruen, 13 Bugs gefixt, 16 Round-Trips gespart

FILE 1: dashboard.html — TASKS-Array ersetzen (im script-Block)
Embedded TASKS auf den aktuellen Stand bringen. Status-Werte 
explizit. K-Tasks als separate phase "P0-CODE-STACK" und "P0a" 
markieren damit das Kanban sie sichtbar von den T-Tasks trennt.

FILE 2: dashboard.html — neue Sektion "Recent Sessions"
Liest die letzten 5 Files aus memory/runs/ (statisch eingebettet, 
weil dashboard.html offline laeuft). Pro Session ein Mini-Card 
mit Datum + Modell + Goal-1-Liner.

FILE 3: dashboard.html — neue Stat-Box "Bug-Memos"
Liste der Anomalien aus memory/anomalies/, mit Severity-Badge. 
Click: oeffnet die .md-Datei (file://-Link relativ).

KRITISCH: 
- dashboard.html bleibt OFFLINE-fähig (kein fetch, alles inline)
- HTML+CSS+JS in EINEM File
- Kein neuer Build-Step

FUNKTIONALE CHECKS (Lou):
- dashboard.html im Browser oeffnen (Doppelklick)
- 22 Tests-Stat sichtbar
- 13 Bugs in Anomalies-Sektion
- K-17..K-22 als pending im Kanban
- Stage A done, P0a in progress
```

---

## End-of-K-22 — Demo Ready Check

```bash
# Final Smoke
cd "C:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI"
bash scripts/preflight.sh
cd code
bash scripts/run_demo.sh
# Expected: alle Services up, Demo-DICOMs geladen, Frontend rendert, 
# Audit-Trail enthält 10 Decision-Trees, Browser oeffnet auf 
# localhost:3000.

# Wenn alles gruen: zurueck zu RUNBOOK_TODAY.md → Schritt 8 (Aroob-
# Review) → Schritt 9 (Mail an Rohde rausschicken).
```

---

## Lessons Learned von K-01..K-16 (eingebaut in K-17..K-22)

1. **Settings-Cache:** Nicht beim Modul-Import, immer inline
2. **`from __future__ import annotations`:** Nicht in Routes mit `UploadFile`
3. **Unicode-Console:** ASCII-only in Skripten die auf Windows laufen
4. **DB-Engine:** Lazy via `@lru_cache`, mit `cache_clear()` für Tests
5. **Schema-Pflicht:** Optionale Felder müssen syntaktisch null erlauben (B-12)
6. **SQLEnum:** Immer `values_callable` für String-Enums

Diese 6 Patterns sind in K-17..K-22 hardgecodiert. Künftige Modelle die K-23+ planen sollten sie als „common knowledge" voraussetzen.

---

**Version:** 1.1 · **Aktualisiert:** 2026-04-29 · Opus 4.7 (Cowork)
**Diff zu v1.0:** K-17..K-22 als P0a-Appendix hinzugefügt nach K-01..K-16-Abschluss durch Kimi.

---
---

# APPENDIX P0b — Tacit-Knowledge-Capture (K-23 bis K-27)

> **Hinzugefügt:** 2026-04-29 nach K-22-Abschluss + Lou-Request für Freitext-Eingabe.
>
> **Zweck:** Erweitert das Decision-Tree-Capture um ein Freitext-Feld am Ende der Form. Der Arzt schreibt frei was er entschieden, nicht entschieden, oder offen gelassen hat. Diese Notes werden täglich aggregiert und erweitern Tag-für-Tag den strukturierten Entscheidungsbaum.
>
> **Sicherheitsrahmen:** Freitext = neues PII-Risiko (Hazard H-011 in `regulatory/risk_register.md`, Score 15). Mitigation: Live-Validation gegen DE-NER + Regex, Reject vor Speicherung, Audit-Event bei jedem Reject.
>
> **Neuer Abschnitt in Spec:** `05_DECISION_TREE_HARVESTING.md` Sektion 3.1 (Schema v0.2) und Sektion 4 (UI-Spec mit Freitext-Feld).
>
> **Reihenfolge:** K-23 (Schema/Spec) BLOCKT alle anderen. Dann K-24 + K-25 parallel. K-26 nach K-24. K-27 separat (Aggregator-Pipeline, Hermes-Skill).

---

## SETUP-DELTA für Kimi

> Wenn deine Kimi-Session noch von K-01..K-22 läuft: paste folgenden Delta-Block als kurzes Update. Wenn neu: erst kompletten Setup-Block aus Schritt 0 oben pasten, dann diesen Delta.

```
DELTA-UPDATE 2026-04-29:

Carotis-AI bekommt eine Erweiterung: P0b — Tacit-Knowledge-Capture.

NEUE Funktionalität: Am Ende der Decision-Tree-Form gibt es jetzt ein 
opt-in Freitext-Feld `reasoning.free_text_notes` (max 2000 Zeichen). 
Arzt schreibt frei was offen / unsicher ist. Diese Texte werden:
1. Live PII-gefiltert (Frontend → Backend /check-text Endpoint)
2. Bei PII-Treffer rejected (HTTP 422) mit Span-Markierung im UI
3. Wenn clean: gespeichert in DB + memory/decisions/
4. Nightly aggregiert via aggregate_free_text.py → Topic-Cluster → 
   Vorschläge zur Schema-Erweiterung in memory/anomalies/triage_week<N>.md
5. Lou approved/rejected wöchentlich, neue deciding_feature-Optionen 
   wandern ins strukturierte Schema

NEUE FILES (von dir, K-23..K-27):
- schemas/decision_tree.schema.json — erweitert um free_text_notes
- schemas/decision_tree.sample.json — neues Beispiel mit Notes
- code/backend/app/services/pii_detection_service.py — neu
- code/backend/app/api/routes/decision_tree.py — /check-text Endpoint
- code/frontend/src/components/FreeTextField.tsx — neue Component
- code/frontend/src/components/DecisionTreeForm.tsx — integriert FreeTextField
- code/scripts/aggregate_free_text.py — Nightly-Cron
- code/hermes/skills/aggregate-free-text.md — Hermes-Skill für Wochen-Triage

NEUE ANTI-PATTERNS (zusätzlich zu B-04, B-08, B-13):
- B-14: PII-Check NUR backend-seitig autoritativ — Frontend-Validation 
  ist UX-Hint, nicht Security. Backend MUSS jeden capture()-Call neu 
  prüfen.
- B-15: free_text_notes NIEMALS in Logs (auch nicht structlog DEBUG). 
  Audit-Event speichert nur Span-Count, kein Content.
- B-16: Spacy DE-NER (`de_core_news_lg`) ist 500 MB — NICHT in 
  backend-Image installieren. Eigener Service oder lazy-load mit Cache.

ANTWORTE NUR: "Verstanden. P0b geladen. Bereit für K-23."
```

---

## K-23 · Schema v0.2 + Spec-Update + Validate-Test [BLOCKS K-24..K-27]

```
PRE-FLIGHT: 13-Bugs-Memo (Top-3) + neue B-14/B-15/B-16 aus Setup-Delta.

Erzeuge in EINER Antwort die Schema-Erweiterung und alle Folge-Updates.

FILE 1: schemas/decision_tree.schema.json — patch
Im "reasoning" Block (zwischen "would_re_image_if" und schließender 
Bracket) hinzufügen:

  "free_text_notes": {
    "type": ["string", "null"],
    "maxLength": 2000,
    "description": "Optionale freie Notiz: was hast du entschieden, was nicht, was bleibt offen? Wird PII-gefiltert (DE-NER + Regex) BEVOR Speicherung. Bei PII-Treffer: Reject mit HTTP 422."
  }

KRITISCH: alle bestehenden Felder unverändert lassen. additionalProperties 
bleibt false.

FILE 2: schemas/decision_tree.sample.json — patch
Im "reasoning" Block "free_text_notes" mit einem realistischen Beispiel 
ergänzen:

  "free_text_notes": "Plaque-Form unklar, Verlaufskontrolle in 6 Monaten falls Symptome zunehmen. CTA-Phase war suboptimal."

FILE 3: scripts/validate_decision_tree.py — patch
In _run_self_test() Funktion einen zusätzlichen Test-Block hinzufügen:
- Test 1: Sample mit free_text_notes ist valid
- Test 2: free_text_notes mit > 2000 Zeichen → InvalidationError
- Test 3: free_text_notes = null ist valid
- Test 4: free_text_notes = "" ist valid (leerer String)
- Test 5: reasoning kann insgesamt null sein

FILE 4: code/backend/app/schemas/inference.py — patch
DecisionTreeRequest Pydantic-Model erweitern:
- In reasoning-Sub-Model: `free_text_notes: str | None = Field(None, max_length=2000)`

FILE 5: scripts/test_validate_decision_tree.py — neu (falls nicht da)
pytest mit den 5 Tests aus FILE 3 als pytest-konvertiert.

FUNKTIONALE CHECKS (Lou):
- python scripts/validate_decision_tree.py --self-test → grün
- pytest scripts/test_validate_decision_tree.py → grün
- Bestehende decision_tree.sample.json bleibt schema-valid

OUTPUT: 5 FILE-Header-Codeblöcke. Patches als kompletten ersetzten 
File-Inhalt liefern (kein Diff-Format), damit Lou ihn direkt 
überschreiben kann.
```

---

## K-24 · Backend PII-Detection-Service + /check-text Endpoint [PARALLEL zu K-25]

```
PRE-FLIGHT: 13-Bugs-Memo + B-14 (Backend autoritativ) + B-16 (Spacy 
nicht ins Backend-Image, lazy-load mit Cache).

Erzeuge den PII-Detection-Service mit Spacy DE-NER + Regex-Fallback.

FILE 1: code/backend/requirements.txt — patch
Hinzufügen:
  spacy>=3.7,<4.0
  # de_core_news_lg wird beim ersten Service-Init via 
  # `python -m spacy download de_core_news_lg` lazy-installiert

FILE 2: code/backend/app/services/pii_detection_service.py

from __future__ import annotations
import re
import structlog
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

log = structlog.get_logger()


@dataclass(frozen=True)
class PIISpan:
    start: int
    end: int
    label: str  # PERSON, PHONE, ID, EMAIL
    text: str   # nur als preview im Reject-Response — in Logs NIEMALS


# Regex-Fallbacks (DE-Spezifika)
_PHONE_RE = re.compile(
    r"(?:\+49|0)\s?\d{2,4}[\s/-]?\d{3,8}",
    re.IGNORECASE,
)
_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_ID_RE = re.compile(
    # Patient-IDs / Versicherten-Nr / Studien-Akten-Nr
    r"\b[A-Z]{1,3}[-_]?\d{4,12}\b",
)
_GERMAN_NAME_RE = re.compile(
    # Conservative: 2 capitalized words back-to-back, common German pattern
    r"\b(?:Herr|Frau|Dr|Prof)\.?\s+[A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)?",
)


@lru_cache(maxsize=1)
def _get_nlp():
    """Lazy-load Spacy DE-Modell. ~500 MB beim ersten Aufruf."""
    try:
        import spacy
    except ImportError as e:
        log.warning("spacy_not_installed", error=str(e))
        return None
    try:
        nlp = spacy.load("de_core_news_lg")
        log.info("spacy_loaded", model="de_core_news_lg")
        return nlp
    except OSError:
        log.warning("spacy_model_missing", hint="run: python -m spacy download de_core_news_lg")
        return None


class PIIDetectionService:
    """Detects PII in free-text using Spacy DE-NER + DE-specific regex."""

    def detect(self, text: str) -> list[PIISpan]:
        if not text:
            return []
        spans: list[PIISpan] = []

        # Regex layer (always runs, fast)
        for m in _PHONE_RE.finditer(text):
            spans.append(PIISpan(m.start(), m.end(), "PHONE", m.group()))
        for m in _EMAIL_RE.finditer(text):
            spans.append(PIISpan(m.start(), m.end(), "EMAIL", m.group()))
        for m in _ID_RE.finditer(text):
            spans.append(PIISpan(m.start(), m.end(), "ID", m.group()))
        for m in _GERMAN_NAME_RE.finditer(text):
            spans.append(PIISpan(m.start(), m.end(), "PERSON", m.group()))

        # Spacy NER layer (if available)
        nlp = _get_nlp()
        if nlp is not None:
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ in ("PER", "PERSON"):
                    spans.append(PIISpan(ent.start_char, ent.end_char, "PERSON", ent.text))

        # Dedupe overlapping spans (prefer longer match)
        spans = sorted(set(spans), key=lambda s: (s.start, -(s.end - s.start)))
        deduped: list[PIISpan] = []
        for s in spans:
            if not any(d.start <= s.start and d.end >= s.end for d in deduped):
                deduped.append(s)

        return deduped

    def is_clean(self, text: str) -> bool:
        return len(self.detect(text)) == 0

    def redact(self, text: str) -> str:
        """Replace PII spans with [REDACTED-LABEL] tokens (for optional auto-redact mode)."""
        spans = self.detect(text)
        if not spans:
            return text
        # Sort descending so indices stay valid during replacement
        for s in sorted(spans, key=lambda x: -x.start):
            text = text[: s.start] + f"[REDACTED-{s.label}]" + text[s.end :]
        return text


def get_pii_service() -> PIIDetectionService:
    """FastAPI-Dependency-Helper. Singleton via @lru_cache wäre overkill 
    weil _get_nlp() bereits cached ist."""
    return PIIDetectionService()


FILE 3: code/backend/app/api/routes/decision_tree.py — patch
Neuen Endpoint hinzufügen:

@router.post("/check-text")
async def check_text(
    payload: dict,  # {"text": "..."}
    pii_service: PIIDetectionService = Depends(get_pii_service),
):
    text = payload.get("text", "")
    if not isinstance(text, str):
        raise HTTPException(status_code=422, detail="text must be string")
    if len(text) > 2000:
        raise HTTPException(status_code=422, detail="text exceeds 2000 chars")
    spans = pii_service.detect(text)
    return {
        "is_clean": len(spans) == 0,
        "pii_spans": [
            {"start": s.start, "end": s.end, "label": s.label}
            for s in spans
        ],
    }

KRITISCH: spans im Response enthalten KEINE text-Felder — nur Indizes 
und Labels. Das verhindert PII-Echo in Logs / Network-Traces (B-15).

FILE 4: code/backend/tests/test_pii_detection.py
pytest mit ≥ 20 Test-Cases:
- "Mein Patient Herr Schmidt..." → PERSON detected
- "Tel: 0231/12345-67" → PHONE detected
- "Akte AB-12345" → ID detected
- "kontakt@klinikum-do.de" → EMAIL detected
- Saubere medizinische Texte ohne PII → is_clean=True
- Edge case: leerer String → []
- Edge case: 2001 Zeichen → 422 via Endpoint
- Spacy nicht installiert → Regex-only fallback funktioniert
- Auto-redact ersetzt korrekt alle Spans

FUNKTIONALE CHECKS (Lou):
- pip install spacy && python -m spacy download de_core_news_lg
- pytest backend/tests/test_pii_detection.py -v → grün
- curl -X POST localhost:8000/api/v1/decision-tree/check-text 
  -H "X-API-Key: $KEY" -d '{"text":"Patient Herr Müller, Tel 0231/123-456"}'
  → spans für PERSON + PHONE

OUTPUT: 4 FILE-Header-Codeblöcke.
```

---

## K-25 · Frontend FreeTextField-Component + Integration [PARALLEL zu K-24]

```
PRE-FLIGHT: 13-Bugs-Memo + B-14 (Frontend ist nur UX-Hint).

Erzeuge die FreeTextField-Component und integriere sie in 
DecisionTreeForm.

FILE 1: code/frontend/src/components/FreeTextField.tsx

import { useEffect, useRef, useState } from "react";
import { useDebouncedCallback } from "use-debounce";  // npm install use-debounce
import { apiClient } from "@/lib/apiClient";

interface PIISpan {
  start: number;
  end: number;
  label: string;
}

interface CheckTextResponse {
  is_clean: boolean;
  pii_spans: PIISpan[];
}

interface FreeTextFieldProps {
  value: string;
  onChange: (v: string) => void;
  maxLength?: number;
  placeholder?: string;
  hintText?: string;
}

export function FreeTextField({
  value,
  onChange,
  maxLength = 2000,
  placeholder = "z.B. „Plaque-Form unklar, würde Verlaufskontrolle in 6 Monaten machen wenn Symptome zunehmen."",
  hintText = "Was ist offen oder unsicher? Was würdest du noch klären? Keine Patientennamen — wir filtern automatisch und lehnen den Eintrag ab, wenn welche drin sind.",
}: FreeTextFieldProps) {
  const [spans, setSpans] = useState<PIISpan[]>([]);
  const [checking, setChecking] = useState(false);
  const taRef = useRef<HTMLTextAreaElement>(null);

  const checkText = useDebouncedCallback(async (text: string) => {
    if (!text) {
      setSpans([]);
      return;
    }
    setChecking(true);
    try {
      const r = await apiClient.post<CheckTextResponse>(
        "/decision-tree/check-text",
        { text }
      );
      setSpans(r.pii_spans);
    } catch {
      // Silent fail — Frontend-Check ist UX-Hint, Backend ist autoritativ
      setSpans([]);
    } finally {
      setChecking(false);
    }
  }, 500);

  useEffect(() => {
    checkText(value);
  }, [value, checkText]);

  // Auto-Save in localStorage (5s debounced, separate Hook)
  const saveDraft = useDebouncedCallback((text: string) => {
    localStorage.setItem("dt:free_text_draft", text);
  }, 5000);
  useEffect(() => saveDraft(value), [value, saveDraft]);

  const counterColor =
    value.length > 1900 ? "text-orange-400" : "text-slate-400";
  const hasPII = spans.length > 0;

  return (
    <div className="space-y-2">
      <label className="block text-sm text-slate-200">
        Was ist offen / unsicher? <span className="text-slate-500">(optional)</span>
      </label>
      <div className="relative">
        <textarea
          ref={taRef}
          value={value}
          onChange={(e) => onChange(e.target.value.slice(0, maxLength))}
          placeholder={placeholder}
          rows={4}
          maxLength={maxLength}
          className={`w-full bg-slate-900 border ${
            hasPII ? "border-red-500" : "border-slate-700"
          } rounded p-2 text-sm text-slate-100 focus:outline-none focus:border-cyan-500 resize-none`}
        />
        <div className={`absolute bottom-2 right-3 text-xs ${counterColor}`}>
          {value.length}/{maxLength}
          {checking && <span className="ml-2 text-cyan-400">prüfe…</span>}
        </div>
      </div>
      <p className="text-xs text-slate-400">{hintText}</p>
      {hasPII && (
        <div className="bg-red-950 border border-red-800 rounded p-2 text-xs text-red-200">
          <strong>Mögliche personenbezogene Daten gefunden:</strong>{" "}
          {spans.map((s, i) => (
            <span key={i} className="mx-1 px-1 bg-red-900 rounded">
              {s.label}
            </span>
          ))}
          <br />
          Bitte umformulieren — wir können den Eintrag sonst nicht
          speichern.
        </div>
      )}
    </div>
  );
}

FILE 2: code/frontend/src/components/DecisionTreeForm.tsx — patch
Ergänze State + Submit-Handler + Render:

const [freeText, setFreeText] = useState(() =>
  localStorage.getItem("dt:free_text_draft") || ""
);

// Im Submit:
const payload = {
  // ... bestehende Felder
  reasoning: {
    // ... bestehende reasoning-Felder
    free_text_notes: freeText || null,
  },
};

// Vor SAVE-Button rendern:
<FreeTextField value={freeText} onChange={setFreeText} />

// Nach erfolgreichem Save:
localStorage.removeItem("dt:free_text_draft");

// Bei Backend-422 mit pii_spans:
// Show toast "Backend hat PII gefunden, bitte Text korrigieren"
// (Frontend-Check ist nur Hint, Backend ist autoritativ — B-14)

FILE 3: code/frontend/package.json — patch
Dependency hinzufügen: "use-debounce": "^10.0.0"

FILE 4: code/frontend/src/components/test_FreeTextField.tsx
vitest + @testing-library/react:
- Test rendert mit value=""
- Test character counter zeigt N/2000
- Test counter wird orange bei > 1900
- Test typing trigger checkText (mit fetch-Mock)
- Test PII-spans rendern als Badges
- Test localStorage Auto-Save funktioniert

FUNKTIONALE CHECKS (Lou):
- npm install
- npm run typecheck → 0 errors
- npm run dev → DecisionTreeForm zeigt Textarea, Tippen "Herr Schmidt" 
  → nach 500ms erscheint rote Border + PERSON-Badge
- pytest test_FreeTextField → grün

OUTPUT: 4 FILE-Header-Codeblöcke.
```

---

## K-26 · Backend decision_tree_service.capture() — PII-Check Pflicht [SEQUENTIAL nach K-24]

```
PRE-FLIGHT: 13-Bugs-Memo + B-14 (autoritativer Backend-Check) + B-15 
(kein PII in Logs).

Patch decision_tree_service.capture() so dass es VOR Speicherung 
PII-Check macht.

FILE 1: code/backend/app/services/decision_tree_service.py — patch

class DecisionTreeService:
    def __init__(
        self,
        session_factory,
        pii_service: PIIDetectionService,  # ⬅ neu
    ):
        self._session_factory = session_factory
        self._pii_service = pii_service

    async def capture(
        self,
        case_id: str,
        physician_role_hash: str,
        payload: dict,
    ) -> str:
        # 1. Schema-Validation (bestehend)
        validate_against_schema(payload)

        # 2. NEU: PII-Check auf free_text_notes
        free_text = (
            payload.get("reasoning", {}) or {}
        ).get("free_text_notes")
        if free_text:
            spans = self._pii_service.detect(free_text)
            if spans:
                # Audit-Event MIT span-count, OHNE content (B-15)
                await self._write_audit_event(
                    event_type="decision_tree_pii_reject",
                    actor=physician_role_hash,
                    payload_json=json.dumps({
                        "case_id_short": case_id[:16],
                        "pii_span_count": len(spans),
                        "pii_labels": sorted(set(s.label for s in spans)),
                    }),
                )
                raise SchemaValidationError(
                    f"PII detected in free_text_notes: "
                    f"{len(spans)} span(s) of types "
                    f"{sorted(set(s.label for s in spans))}. "
                    f"Bitte umformulieren."
                )

        # 3. Speichern (bestehende Logik)
        # ... rest unverändert

        return audit_id

FILE 2: code/backend/app/api/routes/decision_tree.py — patch
Im /capture-Endpoint die PIIDetectionService-Dependency injizieren und 
an decision_tree_service.capture() durchreichen:

@router.post("/capture", status_code=200)
async def capture(
    payload: DecisionTreeRequest,
    db: AsyncSession = Depends(get_db),
    pii_service: PIIDetectionService = Depends(get_pii_service),
):
    service = DecisionTreeService(get_session_factory(), pii_service)
    try:
        audit_id = await service.capture(...)
    except SchemaValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {"audit_id": audit_id, "status": "ok"}

FILE 3: code/backend/tests/test_decision_tree_validation.py — erweitern
Neue Test-Cases:
- Test capture mit clean free_text_notes → 200 + audit_id
- Test capture mit "Herr Müller" in free_text_notes → 422
- Test Audit-Event nach PII-Reject hat span_count, KEINE content
- Test free_text_notes=null → 200 (optional)
- Test free_text_notes="" → 200 (leerer String erlaubt)

FUNKTIONALE CHECKS (Lou):
- pytest backend/tests/test_decision_tree_validation.py -v → grün
- Audit-Trail nach PII-Reject zeigt event_type=decision_tree_pii_reject 
  ohne den Original-Text

OUTPUT: 3 FILE-Header-Codeblöcke.
```

---

## K-27 · Nightly Free-Text-Aggregator + Hermes-Skill [SEPARATE]

```
PRE-FLIGHT: 13-Bugs-Memo + B-14/15/16. Plus: Aggregator läuft auf 
gespeicherten Decision-Trees (also bereits PII-clean), aber Output muss 
trotzdem keine raw-snippets enthalten — nur Topics und anonyme 
Beispiele.

Erzeuge den Nightly-Cron + Hermes-Skill.

FILE 1: code/scripts/aggregate_free_text.py

"""
Nightly Free-Text Aggregator.

Liest alle decision_trees seit letztem Run, extrahiert free_text_notes,
clustert via BERTopic (oder fallback: Hermes/Ollama LLM-Cluster),
schreibt Topic-Report nach memory/anomalies/triage_week<N>.md.

Trigger: Hermes-Skill aggregate-free-text (cron @ 22:30) oder manuell.
"""
from __future__ import annotations
import argparse
import json
import logging
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

# ---- Strategy A: BERTopic (preferred wenn installiert) -----------------

def _try_bertopic_cluster(texts: list[str]) -> list[dict]:
    try:
        from bertopic import BERTopic
        from sentence_transformers import SentenceTransformer
    except ImportError:
        return []
    embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    topic_model = BERTopic(embedding_model=embedder, language="german",
                           min_topic_size=3, calculate_probabilities=False)
    topics, _ = topic_model.fit_transform(texts)
    info = topic_model.get_topic_info()
    clusters = []
    for _, row in info.iterrows():
        if row["Topic"] == -1:
            continue  # noise
        clusters.append({
            "topic_id": int(row["Topic"]),
            "size": int(row["Count"]),
            "keywords": [w for w, _ in topic_model.get_topic(row["Topic"])[:5]],
            "example_indices": [
                i for i, t in enumerate(topics) if t == row["Topic"]
            ][:3],
        })
    return clusters


# ---- Strategy B: Hermes/Ollama LLM-Cluster (Fallback) ------------------

def _try_hermes_cluster(texts: list[str]) -> list[dict]:
    """LLM-basierte Cluster-Analyse via lokalen Ollama-Endpoint."""
    import requests
    prompt = (
        "Du bist Cluster-Analyst. Hier sind Notizen von Radiologen "
        "nach Befundungen. Gruppiere sie in 3-7 Topics. Pro Topic: "
        "kurzes Label, Schlüsselwörter, Anzahl. NIEMALS einzelne "
        "Snippets zitieren — nur Aggregat. Antworte als JSON-Liste.\n\n"
        + "\n---\n".join(f"[{i}] {t}" for i, t in enumerate(texts[:200]))
    )
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "nous-hermes-3-llama-3.1", "prompt": prompt,
                  "stream": False, "format": "json"},
            timeout=120,
        )
        r.raise_for_status()
        return json.loads(r.json()["response"])
    except Exception as e:
        logger.warning("hermes_cluster_failed: %s", e)
        return []


def aggregate(db_path: Path, output_dir: Path,
              since_days: int = 7) -> Path:
    """Hauptlauf. Returnt Pfad zum Triage-Report."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=since_days)

    conn = sqlite3.connect(db_path)
    cur = conn.execute(
        "SELECT data_json FROM decision_trees WHERE captured_at >= ?",
        (cutoff.isoformat(),),
    )
    notes: list[str] = []
    for (data_json,) in cur:
        data = json.loads(data_json)
        text = (data.get("reasoning") or {}).get("free_text_notes")
        if text and len(text.strip()) > 5:
            notes.append(text.strip())
    conn.close()

    if len(notes) < 5:
        logger.info("not_enough_notes count=%d skipping", len(notes))
        return None

    # Versuche BERTopic, fallback auf Hermes
    clusters = _try_bertopic_cluster(notes) or _try_hermes_cluster(notes)
    if not clusters:
        logger.warning("no_clustering_method_available")
        return None

    # Schreibe Report
    week_iso = datetime.now(timezone.utc).strftime("%Y-W%V")
    report_path = output_dir / f"triage_{week_iso}.md"
    output_dir.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Wöchentlicher Triage-Report — {week_iso}",
        "",
        f"**Stand:** {datetime.now(timezone.utc).isoformat()}",
        f"**Notes analysiert:** {len(notes)}",
        f"**Cluster gefunden:** {len(clusters)}",
        "",
        "## Top-Clusters",
        "",
    ]
    for c in clusters:
        lines.append(f"### Topic {c.get('topic_id', c.get('label','?'))} — Size {c.get('size','?')}")
        kw = c.get("keywords", [])
        if kw:
            lines.append(f"**Keywords:** {', '.join(kw)}")
        lines.append("")
    lines.extend([
        "## Vorschläge zur Schema-Erweiterung",
        "",
        "_Lou reviewed wöchentlich. Approved Topics werden zu neuen "
        "deciding_feature-Werten in schemas/decision_tree.schema.json._",
        "",
        "## Compliance-Hinweis",
        "",
        "Dieser Report enthält KEINE einzelnen Note-Snippets — nur "
        "Topic-Cluster. Original-Notes verbleiben in der lokalen "
        "Audit-DB des Klinikums.",
    ])
    report_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("triage_report_written path=%s", report_path)
    return report_path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--db", type=Path, default=Path("data/carotis.db"))
    p.add_argument("--output-dir", type=Path,
                   default=Path("../memory/anomalies"))
    p.add_argument("--since-days", type=int, default=7)
    args = p.parse_args()
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s")
    result = aggregate(args.db, args.output_dir, args.since_days)
    if result is None:
        print("No report generated (not enough notes or clustering failed).")
        return 0
    print(f"Report: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

FILE 2: code/hermes/skills/aggregate-free-text.md
---
name: aggregate-free-text
trigger_phrases: ["aggregiere Freitext-Notes", "wöchentliche Triage", 
                  "topic-cluster decision-trees"]
schedule: "30 22 * * 0"  # Sonntag 22:30
required_tools: [bash, filesystem]
---
# Aggregate Free-Text Skill

Action: Wöchentlicher Topic-Cluster der gespeicherten Decision-Tree-
Notes. Output: triage_week<N>.md in memory/anomalies/.

Steps:
1. Run: python ../scripts/aggregate_free_text.py 
   --db /data/carotis.db 
   --output-dir ../memory/anomalies/ 
   --since-days 7
2. Wenn Report > 0 Cluster: kurze Zusammenfassung als Markdown 
   zurückgeben + Vorschläge welche neuen deciding_feature-Werte ins 
   strukturierte Schema sollen
3. Lou sieht den Report, approved/rejected wöchentlich
4. Bei Approval: Schema-Update via separater K-Prompt (nicht 
   automatisch — Schema-Änderung ist Lou-Decision)

FILE 3: code/scripts/test_aggregate_free_text.py
pytest:
- Test mit synthetischen 20 Notes über 4 Topics → Report enthält 
  Cluster
- Test BERTopic-Pfad (wenn installiert) generiert mind. 2 Topics
- Test Hermes-Fallback wird aufgerufen wenn BERTopic fehlt
- Test < 5 Notes → return None (kein Report)
- Test Report enthält KEINE einzelnen Notes (nur Aggregat)

FILE 4: code/ml/requirements.txt — patch
Hinzufügen (optional, für BERTopic-Pfad):
  bertopic>=0.16,<0.18
  sentence-transformers>=2.7,<3.0

FUNKTIONALE CHECKS (Lou):
- python scripts/aggregate_free_text.py --since-days 7 (mit ein paar 
  Test-Trees in DB) → Report in memory/anomalies/
- Report enthält KEINE Original-Notes-Snippets
- pytest scripts/test_aggregate_free_text.py → grün
- Hermes-Skill via "trigger aggregate-free-text" → manueller Run

OUTPUT: 4 FILE-Header-Codeblöcke.
```

---

## End-of-K-27 — Demo-Stack mit Tacit-Knowledge-Capture

```bash
cd "C:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI"
bash scripts/preflight.sh "free_text"
cd code
docker compose up -d
sleep 30
# Generiere ein paar Trees mit free_text_notes
python scripts/generate_demo_data.py --count 30 --with-free-text
# Test PII-Reject
curl -X POST localhost:8000/api/v1/decision-tree/capture \
  -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"case_id":"...","reasoning":{"free_text_notes":"Patient Herr Müller war..."}}'
# → 422 mit PII-Spans
# Wöchentliche Triage trigger
python scripts/aggregate_free_text.py --since-days 7
ls ../memory/anomalies/triage_*.md
```

Wenn alle Calls grün und Triage-Report existiert: P0b done. Code-Stack hat jetzt das vollständige Decision-Tree-Capture mit Tacit-Knowledge-Capture und Daily-Aggregation.

---

## Lessons Learned aus K-23..K-27 (für künftige Modelle)

1. **PII-Check Backend-autoritativ** (B-14) — Frontend-Validation ist UX-Hint, niemals Security-Boundary.
2. **PII niemals in Logs** (B-15) — Audit-Events speichern Span-Count + Labels, nie Content.
3. **Spacy DE-Modell ~500 MB lazy-load** (B-16) — `@lru_cache` auf `_get_nlp()`, Modell wird beim ersten Aufruf geladen, nicht beim Container-Boot.
4. **Schema-Erweiterung ist Lou-Decision** — Aggregator schlägt Topics vor, wandert aber nicht automatisch ins Schema. Wöchentlicher Approval-Loop.
5. **Reports enthalten keine Snippets** — Topic-Cluster + Keywords + Counts ja, einzelne Original-Notes nein. Auch wenn die Notes selbst PII-clean sind, kann Aggregation versehentlich rückidentifizieren.

---

**Version:** 1.2 · **Aktualisiert:** 2026-04-29 · Opus 4.7 (Cowork)
**Diff zu v1.1:** APPENDIX P0b (K-23..K-27) für Tacit-Knowledge-Capture mit Freitext-Feld + PII-Filter + Daily-Aggregation.
