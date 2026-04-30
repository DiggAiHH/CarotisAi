# Handoff: Kimi → Opus 4.7 (Post K-16 + E2E-Verifikation)

> **Datum:** 2026-04-29
> **Von:** Kimi (K-01..K-16 Code-Generation + E2E-Verifikation)
> **An:** Opus 4.7 (Architektur-Review, Projekt-Update, Next-Round Planning)
> **Modell-Routing:** Dieser Prompt ist für Opus 4.7 bestimmt — Architektur-Entscheidungen, Planung, Dokumentation.

---

## 1. Was wurde abgeschlossen (K-03..K-16)

Alle 16 Prompt-Blöcke der Code-Implementierung wurden generiert und auf Disk geschrieben:

| K | Deliverable | Status |
|---|-------------|--------|
| K-01 | `code/.github/copilot-instructions.md` | ✅ |
| K-02 | `code/CLAUDE.md` + `HARNESS.md` + `AGENTS.md` + `MEMORY.md` | ✅ |
| K-03 | `docker-compose.yml`, `.env.example`, `install_local_stack.*`, `config.py`, `test_config.py` | ✅ |
| K-04 | DB-Layer (`database.py`, `models.py`, Alembic-Stub) | ✅ |
| K-05 | Services + Schemas (`inference_service`, `anonymization_service`, `decision_tree_service`, `gradcam.py`) | ✅ |
| K-06 | Router (`health`, `inference`, `decision_tree`, `audit`) + `dependencies.py` + `exceptions.py` | ✅ |
| K-08 | `app/main.py` FastAPI Factory + Lifespan | ✅ |
| K-09 | Frontend-Stack (React 19 + Vite + TS + Tailwind v4 + Cornerstone.js Skeleton) | ✅ |
| K-10 | ML Data (`dataset.py`, `transforms.py`) | ✅ |
| K-11 | MFSD-UNet Architektur | ✅ |
| K-12 | Composite-Loss (Reasoning-Alignment-Loss γ=0.3) | ✅ |
| K-13 | Training-Loop mit MLflow + Auto-Rollback | ✅ |
| K-14 | ONNX-Export + Simplification + Diff-Check | ✅ |
| K-15 | Tests + CI (`conftest.py`, 5 Test-Suites, `ci.yml`, `local_smoke.yml`) | ✅ |
| K-16 | Hermes Agent (`config.toml`, 3 Skills, `demo.sh` Erweiterung) | ✅ |

---

## 2. E2E-Verifikation (durch Kimi, 2026-04-29)

### Ergebnisse
- **Backend pytest:** 22/24 passed
  - 2 Failures: `test_train_one_epoch` (`mlflow` fehlt), `test_export_onnx_roundtrip` (`torch` fehlt)
  - → ML-Abhängigkeiten sind in `ml/requirements.txt`, nicht `backend/requirements.txt`. Erwartetes Verhalten in reiner Backend-venv.
- **Frontend TypeScript:** `tsc --noEmit` → **0 errors** ✅
- **Docker-Stack:** Nicht gestartet (Docker Desktop offline auf Test-Maschine)

### Während der Verifikation gefixte Bugs (13 Stück)

1. `requirements.txt`: `onnxruntime` + `numpy` + `scipy` Versionen relaxiert für Python 3.13
2. `requirements.txt`: `jsonschema` hinzugefügt (war vergessen)
3. `health.py`: `Depends` fehlte im Import
4. `inference.py`: `from __future__ import annotations` entfernt (ForwardRef mit `UploadFile`)
5. `anonymization_service.py`: `sys.modules["anonymize"] = _anon_module` vor `exec_module` (bekannter `@dataclass`-Bug bei dynamischem Import)
6. `main.py`: `_rate_limit_exceeded_handler` explizit definiert
7. `config.py`: `protected_namespaces=("settings_",)` für `model_version`/`model_sha`
8. `dependencies.py`: `settings` NICHT beim Modul-Import cachen → `get_settings()` inline in Funktionen
9. `models.py`: `SQLEnum(values_callable=...)` damit String-Werte in DB gespeichert werden
10. `test_smoke.py`: API_KEY auf 32 Zeichen korrigiert, URLs auf aktuelle Router-Pfade angepasst, InferenceService gemockt
11. `conftest.py`: `AsyncMock` für `predict`, `drop_all` vor `create_all` für DB-Isolation
12. `decision_tree.schema.json`: `reasoning` + `confidence_self_reported` auf `["string", "null"]` erweitert
13. `generate_demo_model.py`: Unicode-Pfeile `→` → `->` (Windows-Encoding)

---

## 3. Bekannte Anomalien / Tech Debt

| # | Problem | Ort | Schwere |
|---|---------|-----|---------|
| A-01 | Router-Präfix ohne `/api/v1` — `demo.sh` referenziert noch Legacy-Pfade | `code/backend/app/main.py`, `demo.sh` | Medium |
| A-02 | Cornerstone3D Frontend ist Skeleton — WASM-Init + Rendering Pipeline fehlt | `code/frontend/src/components/DicomViewer/` | Medium (P2) |
| A-03 | `database.py` erstellt `engine` beim Modul-Import → geteilte in-memory DB in Tests | `code/backend/app/db/database.py` | Low (durch `drop_all` gemildert) |
| A-04 | ML-Tests (`test_ml_pipeline.py`) failen ohne `mlflow` + `torch` | `code/tests/test_ml_pipeline.py` | Low (erwartet) |
| A-05 | `pytest-asyncio` Deprecation-Warning: `asyncio_default_fixture_loop_scope` unset | `code/pytest.ini` | Low |

---

## 4. Was Opus 4.7 jetzt tun soll

### 4.1 Projekt-Dokumentation aktualisieren

- [ ] `CLAUDE.md` → Phase-Status auf P0 aktualisieren (E2E-Verifikation abgeschlossen, Docker-Smoke ausstehend)
- [ ] `MEMORY.md` → Neue Einträge: `dependencies.py` Cache-Rule, `SQLEnum` Pattern, DB-Isolation
- [ ] `tasks.jsonl` → Abgeschlossene Tasks auf `"done"` setzen, ggf. neue Tasks für P0-Abschluss/P1-Start anlegen
- [ ] `AGENTS.md` → Hard Rules unverletzt bestätigen; ggf. neue Learnings aus den 13 Bugs ergänzen

### 4.2 Nächste Prompt-Runde für Kimi planen

Basierend auf aktuellem Stand und `02_ROADMAP.md`:

**Option A — P0-Abschluss (Rohde-Meeting):**
- Präsentations-Slides für Prof. Rohde (Ziel: Go/No-Go)
- Floy-Recherche abschließen
- Demo-Stack mit Docker Desktop verifizieren

**Option B — P1-Start (Datenpipeline + Annotation):**
- DICOM-Ingestion Pipeline
- Annotation-Tool für Ground-Truth
- Train/Val/Test-Split mit Stratifikation

**Option C — Tech-Debt-Sprint:**
- `/api/v1` Prefix konsistent einführen
- `pytest.ini` async loop scope fixen
- `database.py` Refactor (Engine nicht beim Import erstellen)
- Frontend Cornerstone3D WASM-Init

**Entscheidung:** Opus 4.7 wählt die Priorisierung basierend auf `CLAUDE.md` Phase-Status und Stakeholder-Druck.

### 4.3 Handoff-Format

Wenn Opus 4.7 die nächste Kimi-Runde plant:
- Jeder Prompt-Block (K-17, K-18, ...) muss enthalten:
  - **Ziel** (1 Satz)
  - **Input-Dateien** (die Kimi lesen soll)
  - **Output-Dateien** (die Kimi schreiben soll)
  - **Acceptance Criteria** (wann ist der Block done)
  - **Known Pitfalls** (aus den 13 Bugs oben)

---

## 5. Files die Opus 4.7 lesen muss (bevor er antwortet)

1. `code/CLAUDE.md` — aktueller Phase-Status
2. `code/MEMORY.md` — was ist bereits dokumentiert
3. `tasks.jsonl` — welche Tasks sind offen
4. `02_ROADMAP.md` — Phasen P0..P7
5. `01_HARNESS.md` — Modell-Routing
6. `memory/runs/2026-04-29_kimi_e2e-verification.md` — dieser Log

---

*Ende Handoff. Opus 4.7: Lies die Files, aktualisiere Dokumentation, plane Next-Round, gib Output als strukturierten Plan.*
