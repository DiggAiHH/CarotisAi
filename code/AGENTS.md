# code/AGENTS.md — Hermes Agent Specification

> Local agent configuration for the `code/` implementation directory.

## Agent Identity

| Attribute | Value |
|-----------|-------|
| `name` | `carotis-helper` |
| `model` | `nous-hermes-3-llama-3.1` |
| `endpoint` | `http://localhost:11434` |
| `context_window` | 32k tokens |
| `compression_trigger` | > 24k tokens → compress via Caveman (`qwen2.5-coder:7b`) |
| `language` | German (UI/docs), English (code/commits) |

## Persistent Memory

At startup the agent reads in this order:

1. [`../CLAUDE.md`](../CLAUDE.md) — project master memory
2. [`../MEMORY.md`](../MEMORY.md) — long-term memory index
3. [`code/CLAUDE.md`](CLAUDE.md) — code session memory
4. Last 3 run-logs: `../memory/runs/<YYYY-MM-DD>_*.md` (newest first)

## Skills

Three built-in skills live in `code/hermes/skills/`:

1. **`anonymize-batch`** — Executes `scripts/anonymize.py` over a directory of DICOM files. Verifies k-anonymity ≥ 5 before returning the output path. Logs every file hash to the audit trail.

2. **`capture-decision-tree`** — Accepts a JSON payload, validates it against `../schemas/decision_tree.schema.json`, and appends it to `data/decision_trees/`. Rejects payloads that fail schema validation with a detailed error report.

3. **`nightly-retrain`** — Triggers the daily learning loop: reads new decision trees, merges them into the training set, runs a short fine-tuning epoch, exports to ONNX, and validates against a hold-out set. Auto-rollback if validation loss increases.

## Tool Permissions Allowlist

| Operation | Allowed Paths | Notes |
|-----------|--------------|-------|
| **Read** | `../**`, `code/**`, `schemas/**`, `memory/**` | Full project visibility |
| **Write** | `memory/**`, `data/anonymized/**`, `data/models/**`, `code/hermes/skills/**` | No write to `backend/`, `frontend/`, `ml/` without human approval |
| **Execute** | `scripts/anonymize.py`, `scripts/preflight.sh`, `scripts/validate_decision_tree.py`, `scripts/generate_demo_model.py` | No arbitrary shell execution |

## Denied Endpoints

The following endpoints are **blocked** for any path that handles patient data, DICOM bytes, or non-anonymized inference results:

- `api.anthropic.com`
- `api.openai.com`
- `generativelanguage.googleapis.com`

Aggregated, fully anonymized model-update bundles may be transferred via signed bundles only (see ADR-0001).

## Self-Improvement Loop

Every Monday at 05:00 UTC, Hermes:

1. Reads all run-logs from `../memory/runs/` of the past 7 days.
2. Identifies recurring pain points, missing skills, or outdated context.
3. Writes proposals to `../memory/proposals/<YYYY-MM-DD>_hermes.md`.
4. Proposals are reviewed by Lou; approved proposals become new skills or memory updates.

---

*Last updated: 2026-04-28*
