# ULTRAPLAN — Carotis-AI Agent Pre-Flight Protocol

> **Version:** 2026-04-30 · **Agent:** Kimi / Claude / Codex / Opus
> **Scope:** Vollständiges Co-Working-Protokoll für den Carotis-AI Stack auf Windows
> **Basis:** COPILOT_STATUS_REPORT + AGENTS.md + CLAUDE.md + 50+ Session-Stunden

---

## 1. SYSTEM-KONTEXT (Dieser Computer)

### 1.1 Hardware & OS
| Attribut | Wert |
|----------|------|
| OS | Windows 10/11 |
| Shell | PowerShell (NICHT bash/WSL für Standard-Ops) |
| Python | 3.14.0 (System) |
| Node.js | 22.x (für Frontend) |
| Git | Verfügbar, authentifiziert für `DiggAiHH/CarotisAi` |

### 1.2 Kritische PowerShell-Limitierungen
```powershell
# ❌ FALSCH — funktioniert NICHT in PowerShell:
cd x && python script.py
cd x || echo "fail"

# ✅ RICHTIG — verwende ; oder separate Befehle:
cd "x"; python script.py
cd "x"; if (-not $?) { echo "fail" }

# ✅ Pfade mit Leerzeichen IMMER in Anführungszeichen:
cd "c:\Users\...\Carotis AI\code"
```

### 1.3 Python-Umgebung
| Umgebung | Pfad | Status | Nutzung |
|----------|------|--------|---------|
| System-Python | `python` | Python 3.14.0 | Fallback, nicht alle Deps |
| Linux-venv | `code/.venv/` | `bin/` statt `Scripts/` | **NICHT auf Windows nutzbar** |
| Windows-venv | `code/.venv313/` | Unbekannt | Prüfen vor Nutzung |

**Regel:** Wenn Backend-Skripte laufen sollen, entweder:
1. Neuen Windows-venv erstellen: `python -m venv .venv_win`
2. Oder System-Python mit `pip install -r requirements.txt`
3. Oder Docker nutzen

### 1.4 Env-Variablen (Pflicht)
```powershell
$env:CAROTIS_API_KEY = "a" * 32   # Mindestens 32 Zeichen!
```
- Pydantic-Settings validiert `API_KEY` auf Länge ≥ 32
- Ohne diese Variable: **ALLE** Backend-Skripte crashen sofort

---

## 2. REPO-STRUKTUR & GIT

### 2.1 Remote
- **Repo:** `https://github.com/DiggAiHH/CarotisAi`
- **Branch:** `master`
- **Auth:** Bereits konfiguriert (keine manuelle Eingabe nötig)

### 2.2 Git-Workflow
```powershell
# Standard-Commit-Pipeline:
git add -A
git commit -m "type: description in english imperative"
git push origin master

# Commit-Types:
# feat:     neue Feature
# fix:      Bugfix
# docs:     Dokumentation
# test:     Tests
# refactor: Code-Änderung ohne Funktionsänderung
# deploy:   Deployment-Config
```

### 2.3 Git-PowerShell-Artefakte
- `git push` zeigt manchmal Exit Code 1 + `RemoteException` — das ist ein **PowerShell-Bug**, nicht echter Fehler
- Prüfe stattdessen: `git log --oneline -3` ob der Push erfolgreich war
- LF/CRLF-Warnungen beim Commit sind harmlos

---

## 3. TOOL-MATRIX (Wann welches Tool)

### 3.1 Shell vs. ReadFile/WriteFile/Glob/Grep
| Aufgabe | Tool | Warum |
|---------|------|-------|
| Datei lesen | `ReadFile` | Schneller, zuverlässiger, Zeilennummern |
| Datei schreiben | `WriteFile` | Atomar, überschreibt nie aus Versehen |
| String ersetzen | `StrReplaceFile` | Präzise, multi-line, keine Regex-Fehler |
| Dateien finden | `Glob` | Pattern-Matching, kein `ls -R` |
| Code suchen | `Grep` | Ripgrep, schnell, context |
| Befehle ausführen | `Shell` | Nur wenn nötig, PowerShell-Limitierungen beachten |
| Bild/Video | `ReadMediaFile` | Nicht für Text nutzen |

**Regel:** Bevorzuge `ReadFile/WriteFile/StrReplaceFile` über Shell. Shell nur für:
- `npm run typecheck`
- `pytest`
- `git commit/push`
- `docker compose up`

### 3.2 MCP-Tools (Wann nutzen)
| MCP | Wann | Was vermeiden |
|-----|------|---------------|
| **GitHub** | Repos, Issues, PRs, Commits, File-Contents | Niemals Secrets/Keys committen |
| **Playwright** | Browser-Automation, Screenshots, E2E | Niemals Patientendaten in Browser eingeben |
| **Context7** | Dokumentation von Libraries/Frameworks | Nicht für Projekt-interne Doku nutzen |

### 3.3 Subagent-Tool
| Agent-Typ | Wann | Parallel? |
|-----------|------|-----------|
| `coder` | Code-Implementierung, Bugfix, Refactoring | Ja, bei disjunkten Dateien |
| `explore` | Codebase-Exploration, Research | Ja, unabhängige Fragen |
| `plan` | Architektur-Entscheidungen, komplexe Planung | Nein, sequentiell |

**Subagent-Regel:** Maximal sinnvolle Parallelität, aber nur mit **disjunkten Datei-/Ownership-Grenzen** und klarer Integrationsrunde danach.

---

## 4. FRONTEND-WORKFLOW (React 19 + Vite + Tailwind v4)

### 4.1 Verifizierungs-Pipeline
```powershell
cd "code\frontend"
npm run typecheck    # tsc --noEmit — MUSS grün sein
npm run lint         # ESLint 9 Flat Config — MUSS grün sein
npm run build        # Vite Production-Build — MUSS success sein
```

### 4.2 Test-Limits
- `npm test -- --run` → Vitest + jsdom + @testing-library
- **Vitest hängt manchmal** bei jsdom + Cornerstone3D WASM (Timeout 60s → abbrechen)
- Das ist ein **bekanntes Problem**, nicht durch Code-Änderung verursacht
- Wenn hängt: `npm run typecheck` + `npm run lint` als Alternative

### 4.3 Code-Style-Enforcement
| Regel | Werkzeug | Konsequenz bei Bruch |
|-------|----------|----------------------|
| TypeScript strict | `tsc --noEmit` | Build fail |
| ESLint 9 Flat Config | `eslint src` | CI fail |
| Keine hartkodierten DE-Strings | `t('key')` aus `@/lib/i18n.ts` | Review fail |
| Path Alias `@/*` | Vite config | Import-Fehler |
| Named Exports | `export function Component` | Tree-shaking |
| Props als `interface Props` | Direkt über Komponente | Type-Safety |

### 4.4 React-Spezifika
- **Keine `default export`** für Komponenten — immer Named Export
- **Props-Interface** direkt über der Komponente
- **Custom Hooks** mit `use` Prefix
- **State Updates** funktional: `setCount(prev => prev + 1)`
- **Spread statt Mutation:** `const updated = { ...obj, key: val }`

---

## 5. BACKEND-WORKFLOW (FastAPI + SQLite + async)

### 5.1 Verifizierungs-Pipeline
```powershell
cd "code"
$env:CAROTIS_API_KEY = "a" * 32
$env:PYTHONPATH = "backend"
pytest tests/ -v -p no:warnings    # 101/101 Tests grün
```

### 5.2 Python-Konventionen
| Regel | Beispiel |
|-------|----------|
| Imports | `from app.services import ...` (absolut, nie relativ) |
| Type Hints | `from __future__ import annotations` in jeder Datei |
| Dataclasses | `dataclasses` für interne Strukturen |
| API Schemas | `pydantic.BaseModel` mit `ConfigDict(extra="forbid")` |
| Logging | `structlog` — `logger.info("event", key=value)`, **nie `print()`** |
| Error Handling | Strukturierte Exceptions in `app/core/exceptions.py` |
| Naming | `snake_case.py`, `PascalCase` Klassen, `UPPER_SNAKE_CASE` Konstanten |

### 5.3 SQLite-Enforcement
- `DATABASE_URL`-Validator in `config.py` lehnt Nicht-SQLite-URLs ab
- Kein Postgres, kein Cloud-DB — **SQLite only**
- Async via `aiosqlite`

### 5.4 Security-Hard-Rules
| Regel | Warum |
|-------|-------|
| Keine Cloud-API für Patientendaten | DSGVO / Local-First |
| `X-API-Key` Header-Auth | Kein Bearer-Token, kein OAuth |
| Rate-Limiting via `slowapi` | 30/min Inference, 60/min Decision-Tree |
| CORS strikt auf localhost | `http://localhost:3000` |
| Anonymisierung vor Verarbeitung | `DicomService.parse_and_anonymise()` |
| Audit-Trail append-only | SQLAlchemy Event-Listener blockiert UPDATE/DELETE |

---

## 6. MODELL-ROUTING (Welches Modell wann)

| Aufgabe | Modell | Begründung |
|---------|--------|------------|
| Architektur-Entscheidungen, ADRs | **Opus 4.7** | Politisch/regulatorisch sensibel |
| Code-Implementierung, Bugfix | **Sonnet 4.6** | Balance Speed/Quality |
| Atomare Edits, i18n, Rename | **Haiku 4.5** | Schnell, präzise bei Spec |
| ML-Training, ONNX-Export | **Codex 5.3** | Python-schwere Pipelines |
| Medizinische/regulatorische Entscheidungen | **Opus 4.7 only** | MDR, DSGVO, Ethik |
| Office-Doc Prompts | **Opus 4.7** | Tonality, politische Sensibilität |
| TDD/Test-Suites | **TDD-Workflow Skill** | 80%+ Coverage Enforcement |

---

## 7. MEMORY-DISZIPLIN (Nicht verhandelbar)

### 7.1 Run-Log-Format
```markdown
---
date: YYYY-MM-DD
model: <agent-name>
session: <kurzes-thema>
---

## Goal
Was sollte erreicht werden?

## Done
Was wurde tatsächlich erledigt?

## Surprised by
Was war unerwartet?

## Avoided
Was wurde vermieden / was ging schief?

## Next
Was ist der nächste Schritt?
```

### 7.2 Run-Log-Speicherort
```
memory/runs/YYYY-MM-DD_<agent>_<thema>.md
```

**Beispiele:**
- `memory/runs/2026-04-30_kimi_B1-inference-flow.md`
- `memory/runs/2026-04-30_opus47_p0f_pivot_plan.md`
- `memory/runs/2026-04-30_codex_W-02.md`

### 7.3 MEMORY.md Index
Nach jeder Session: Pointer-Zeile in `MEMORY.md` ergänzen.

### 7.4 Kein Session-Ende ohne Run-Log
**Hard Rule:** Wenn kein Run-Log geschrieben wurde, ist die Session nicht beendet.

---

## 8. DEPLOY-WORKFLOW (Fly.io + Netlify)

### 8.1 Frontend (Netlify)
```powershell
# Website ist in code/website/
# netlify.toml existiert bereits
# Deploy via GitHub-Integration oder Netlify CLI
```

### 8.2 Backend (Fly.io)
```powershell
# fly.toml existiert in deploy/fly.toml
# Dockerfile.demo ist Multi-Stage (Node + Python + nginx)
# SQLite persistiert in Volume /data

fly deploy --config deploy/fly.toml
```

### 8.3 Health-Checks
```bash
curl https://app.carotis.diggai.de/health/
curl -H "X-Demo-Token: <token>" https://app.carotis.diggai.de/api/v1/demo/whoami
```

---

## 9. ANOMALIEN-REGISTER (Bekannte Stolpersteine)

| ID | Problem | Workaround | Status |
|----|---------|------------|--------|
| A-01 | `&&` / `||` in PowerShell | `;` oder `if (-not $?)` verwenden | Permanent |
| A-02 | Linux-venv auf Windows | Neuen Windows-venv erstellen oder Docker nutzen | Permanent |
| A-03 | Vitest hängt bei jsdom+WASM | Timeout abbrechen, typecheck+lint als Fallback | Permanent |
| A-04 | Git Push Exit Code 1 | PowerShell-Artefakt, `git log` prüfen | Permanent |
| A-05 | `CAROTIS_API_KEY` fehlt | `$env:CAROTIS_API_KEY = "a"*32` setzen | Permanent |
| A-06 | CORS_ORIGINS hardcoded | `${CORS_ORIGINS:-http://localhost:3000}` verwenden | Fixed |
| A-07 | docker-compose healthcheck fehlt | `/health/` Pfad, nicht `/api/v1/health/` | Fixed |

---

## 10. VERBOTENE AKTIONEN (Niemals)

| # | Verbot | Konsequenz |
|---|--------|------------|
| 1 | Patientendaten in Cloud / externe API | DSGVO-Verstoß, Projektende |
| 2 | Modell-Training auf nicht-anonymisierten Daten | Ethik-Verstoß |
| 3 | Code-Änderungen ohne Pre-Flight | Regressionen |
| 4 | Session-Ende ohne Run-Log | Kontextverlust |
| 5 | Office-Dokumente direkt editieren | Nur Stride-Prompts generieren |
| 6 | `print()` statt `structlog` | Log-Qualität sinkt |
| 7 | Bare `except:` | Silent Failures |
| 8 | Relativen Imports in Python | `from app.x import y` verwenden |
| 9 | Hartkodierte Secrets | `.env` + `pydantic-settings` |
| 10 | `git commit` ohne `typecheck` + `lint` | CI fail |

---

## 11. PRE-FLIGHT CHECKLISTE (Vor JEDER Session)

```markdown
- [ ] `CLAUDE.md` gelesen
- [ ] `MEMORY.md` gelesen
- [ ] Letzte 3 Run-Logs überflogen: `ls -t memory/runs/ | head -3`
- [ ] Bekannte Anomalien geprüft: `memory/anomalies/`
- [ ] Task-Status in `tasks.jsonl` auf `in_progress` gesetzt
- [ ] Windows PowerShell-Limitierungen im Kopf
- [ ] `$env:CAROTIS_API_KEY` gesetzt (wenn Backend-Arbeit)
```

---

## 12. SKILLS-INVENTAR (Verfügbare Fähigkeiten)

| Skill | Pfad | Wann nutzen |
|-------|------|-------------|
| `coding-standards` | `~/.claude/skills/coding-standards/` | TypeScript/React Code-Quality |
| `tdd-workflow` | `~/.claude/skills/tdd-workflow/` | Tests schreiben, Coverage prüfen |
| `kimi-cli-help` | `~/.kimi/skills/kimi-cli-help/` | Kimi-spezifische Fragen |
| `python-patterns` | `~/.claude/skills/python-patterns/` | Pythonic Code |
| `frontend-patterns` | `~/.claude/skills/frontend-patterns/` | React/State-Management |
| `security-review` | `~/.claude/skills/security-review/` | Auth, Input-Validation |
| `verification-loop` | `~/.claude/skills/verification-loop/` | Pre-Release Checks |

---

*Erstellt: 2026-04-30 · Letztes Update: 2026-04-30 · Status: ACTIVE*
*Basis: AGENTS.md + CLAUDE.md + COPILOT_STATUS_REPORT.md + 50+ Session-Stunden*
