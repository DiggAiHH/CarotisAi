# Handoff: Opus 4.7 — P0a Demo-Robustheit komplett, Mail an Rohde offen

> **Von:** Kimi K2.6 (K-17..K-22, 6 Prompts)  
> **An:** Opus 4.7  
> **Datum:** 2026-04-29  
> **Phase:** P0 (80 % done) — P0a Demo-Robustheit abgeschlossen. Blocker: T-010 (Mail an Rohde).

---

## Was sich seit dem letzten Handoff geändert hat

### K-17..K-22: P0a Demo-Robustheit (6 Prompts, 22/22 funktionale Checks grün)

| Prompt | Deliverable | Status |
|--------|-------------|--------|
| K-17 | Router-Prefix `/api/v1` für alle Domain-Router; pytest.ini `asyncio_default_fixture_loop_scope` | ✅ 6/6 pytest grün |
| K-18 | DB-Engine lazy init via `@lru_cache`; `reset_db()` Test-Helper; `AsyncSessionLocal`→`get_session_factory()` in 2 Route-Files | ✅ 6/6 pytest grün |
| K-19 | Cornerstone3D WASM-Init (`cornerstoneSetup.ts`); `DicomViewer/` mit StackViewport, File-Upload, HeatmapOverlay (Canvas-2D + Opacity-Slider); `vite.config.ts` WASM-Assets | ✅ tsc 0 errors |
| K-20 | `generate_demo_data.py` — 10 synthetische 512x512 CT-DICOMs + 10 Schema-valide Decision-Trees; `test_generate_demo_data.py` (5 Tests: 10 DICOMs, 1 PII, anonymize check, 10 Trees, Schema-Validation) | ✅ 5/5 pytest grün |
| K-21 | `demo_walkthrough.md` (5 Sektionen, 5 Minuten); `run_demo.sh` + `run_demo.ps1` (Pre-Flight, Docker, Demo-Data, Tree-Seeding, Browser-Open, VS Code Prompt); `teardown_demo.sh` + `.ps1` | ✅ Syntax validiert |
| K-22 | `dashboard.html` — K-01..K-22 im Kanban (P0-CODE-STACK + P0a Phasen); Phase P0 "80% done"; Recent Sessions (5 Cards); Anomaly-Memos (13-Bugs); Code-Stack Stats (22 Tests, 13 Bugs, 16 Round-Trips) | ✅ Tag-Balance OK |

### Architektur-Entscheidungen während P0a

1. **Router-Prefix-Strategie:** Domain-Router behalten interne Prefixe (`/inference`, `/decision-tree`, `/audit`); `main.py` setzt äußeren Wrapper `/api/v1`. Health bleibt root. Rationale: Minimale Invasivität, bestehende Tests brauchen nur Pfad-Anpassung.

2. **DB-Engine Lazy Init:** `@lru_cache(maxsize=1)` auf `get_engine()`; `cache_clear()` in Fixture für Test-Isolierung. Rationale: Verhindert Modul-Import-Seiteneffekte (B-08-Analogon).

3. **Cornerstone3D Loader-Registrierung:** `dicomImageLoaderInit()` registriert `wadouri`/`wadors` automatisch via `registerLoaders()`. Manuelle `imageLoader.registerImageLoader()` sind redundant und verursachen Type-Inkompatibilitäten (Return-Type `IImageLoadObject` vs `ImageLoaderFn`).

4. **Demo-Daten `model_sha`:** SHA256-Hash statt Platzhalter-String, um JSON-Schema-Regex `^[a-f0-9]{7,64}$` zu matchen.

5. **Anonymize.py `--check`:** Braucht `--output` + `--min-k 1` für Demo-Daten (Default k=5 ist zu hoch für 10 Files).

### 13-Bugs-Memo als gelehrtes Wissen

`memory/anomalies/2026-04-29_kimi_e2e_13_bugs.md` dokumentiert alle während K-01..K-16 gefixten Bugs. Top-3 Anti-Patterns die in K-17..K-22 hartkodiert wurden:
- B-08: Settings nicht beim Modul-Import cachen
- B-04: Kein `from __future__ import annotations` in Routes mit `UploadFile`
- B-13: ASCII-only in Python-Console-Skripten (Windows cp1252)

---

## Aktueller Stack-State (verifiziert)

### Backend
- **Tests:** `pytest tests/test_smoke.py` → 6 passed (Router-Prefixe, Auth, DICOM-Upload, Decision-Tree Capture/Recent)
- **Config:** pydantic-settings v2, `protected_namespaces=("settings_",)`
- **DB:** SQLAlchemy 2.0 async, lazy engine, append-only AuditEvent
- **API:** `/health` (root), `/api/v1/inference/predict`, `/api/v1/decision-tree/capture`, `/api/v1/decision-tree/recent`, `/api/v1/audit/trail`
- **Rate-Limiting:** slowapi 30/min auf Inference

### Frontend
- **TypeScript:** `tsc --noEmit` → 0 errors
- **Cornerstone3D:** v2.19.16, WASM-Init, StackViewport, Pan/Zoom/WindowLevel Tools
- **Build:** Vite 5, React 19, Tailwind CSS v4

### ML
- **Demo-Modell:** `data/models/mfsd_unet.onnx` (via `generate_demo_model.py`)
- **Demo-Daten:** `data/demo/dicoms/` (10 DICOMs), `data/demo/decision_trees/` (10 JSONs)

### Docker
- **Status:** Docker Desktop offline während Session — Stack lokal via pytest/venv verifiziert
- **Compose:** backend + frontend + ollama + hermes definiert

---

## Offene Punkte / Blocker

| ID | Blocker | Besitzer | Next Action |
|----|---------|----------|-------------|
| T-010 | Mail an Prof. Rohde | Aroob | Schritt 9 in `RUNBOOK_TODAY.md` — Stide-Prompt A ausführen (`Mail_Aroob_an_Rohde_v2.docx`) |
| T-009 | Review v2-Dokumente | Lou + Aroob | Schritt 8 in `RUNBOOK_TODAY.md` — gemeinsamer Review vor Mail-Versand |
| K-22-implizit | Dashboard-Anomalies: `file://`-Links funktionieren nur wenn Dashboard im Projekt-Root geöffnet | Lou | Kein Bug, nur Einschränkung dokumentieren |

---

## Run-Logs & Artefakte

| File | Zweck |
|------|-------|
| `memory/runs/2026-04-28_kimi_K-NN.md` | Master-Log mit 5-Zeilen-Einträgen für K-17..K-22 |
| `memory/runs/2026-04-29_kimi_K-{17..22}.md` | Detail-Logs pro Prompt |
| `memory/anomalies/2026-04-29_kimi_e2e_13_bugs.md` | 13 Bugs als Lehre für künftige Modelle |
| `09b_KIMI_PROMPT_SEQUENCE.md` | Vollständige K-01..K-22 Prompts (v1.1) |
| `06_ROHDE_MEETING_KIT.md` | Meeting-Vorbereitung für Prof. Rohde |
| `dashboard.html` | Offline-fähiges Status-Dashboard |
| `code/scripts/demo_walkthrough.md` | 5-Minuten Walkthrough-Script |

---

## Empfohlene Next Actions für Opus 4.7

1. **P0-Abschluss:** Stide-Prompt A (`Mail_Aroob_an_Rohde_v2.docx`) reviewen und finalisieren — Aroob muss die Mail abschicken.
2. **Rohde-Meeting-Kit:** `06_ROHDE_MEETING_KIT.md` Sektion 4 mit `demo_walkthrough.md` synchronisieren (Walkthrough existiert jetzt, Kit kann auf vollständiges Script verweisen).
3. **P1-Vorbereitung:** Sobald Rohde-Approval eintrifft, P1 (Ethik + DSGVO + Datenvertrag) planen — Opus 4.7 only für regulatorische Texte.
4. **ADR schreiben:** Die 5 Architektur-Entscheidungen oben als formale ADRs in `regulatory/adr/` festhalten.

---

*Handoff geschrieben von: Kimi K2.6 (K-17..K-22 Implementierung)*  
*Format: Opus 4.7 Handoff-Style (Architektur-Entscheidungen + Blocker + Next Actions)*
