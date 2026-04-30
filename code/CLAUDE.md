# code/CLAUDE.md — Working Memory for Code Sessions

> This file is the **session entry point** for all engineering work inside `code/`.  
> For project-wide context see [`../CLAUDE.md`](../CLAUDE.md).  
> For a guided tour see [`../00_INDEX.md`](../00_INDEX.md).

## Sub-Project Definition

`code/` is the **implementation directory**. It contains the runnable stack: backend, frontend, ML pipeline, local AI agent, tests, and infrastructure scripts. Nothing outside `code/` is executed in production or demo environments.

## Stack (executed versions)

| Layer | Technology |
|-------|------------|
| Frontend | React 19 + Vite 5 + TypeScript 5.5 + Tailwind CSS 4 |
| DICOM Viewer | Cornerstone.js 2.8 |
| Backend | Python 3.11 + FastAPI 0.115 + Pydantic v2 + SQLAlchemy 2.0 async |
| Inference | ONNX Runtime 1.20 (CPU-only, local) |
| ML Training | PyTorch 2.5 + MONAI 1.4 + timm 1.0 |
| Local AI | Ollama + Hermes Agent (Port 8200) |
| Anonymization | pydicom 3.0 — DICOM PS 3.15 Basic Profile |
| Database | SQLite (async via aiosqlite) |

## Critical Path

```
data anonymized → ML trained → ONNX exported → Backend loads ONNX
        ↓
Frontend calls Backend → Decision-Tree captured → Daily-Loop trains next
```

Every code change must keep this pipeline intact.

## Pre-Flight (every code session)

1. Run `../scripts/preflight.sh` (or `preflight.ps1` on Windows).
2. Check `git status` — uncommitted work?
3. Run `pytest -q` — all green?
4. Read the last 3 run-logs: `../memory/runs/<YYYY-MM-DD>_*.md`.
5. Check `../tasks.jsonl` for blocked tasks.

## Hard Rules (shortened)

| # | Rule |
|---|------|
| 1 | **No cloud API calls for patient data.** Local inference only. |
| 2 | **No training on non-anonymized data.** DICOM PS 3.15 is mandatory. |
| 3 | **No bare `except`.** Custom exceptions in `app/core/exceptions.py`. |
| 4 | **No `print()`.** `structlog` only, never PII in logs. |
| 5 | **Schema-first.** `../schemas/decision_tree.schema.json` is source of truth. |
| 6 | **Tests for every service method.** Critical paths 100 % coverage. |
| 7 | **UI in German, code in English.** |

## Escalation

- Unclear API contract → ask Lou.
- Patient-data handling in doubt → ask Lou.
- Requirement contradicts a hard rule → ask Lou.

---

*Last updated: 2026-04-28*
