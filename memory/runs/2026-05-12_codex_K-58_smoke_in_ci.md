---
name: 2026-05-12_codex_K-58_smoke_in_ci
type: run
agent: Codex GPT-5.5
task: K-58
---

## Goal
Wire the existing full-stack smoke script into the Hetzner deploy workflow so deployment fails when smoke checks fail.

## Done
- Added a `Smoke test` step to `.github/workflows/deploy-backend-hetzner.yml` after the remote Docker Compose start and health checks.
- The step sets `DEBUG=true`, passes `API_KEY` from GitHub secrets, targets the live Hetzner endpoint, and runs `python code/scripts/smoke_test.py`.
- Did not edit `code/scripts/smoke_test.py`, deploy compose files, or other workflows.

## Surprised by
The requested `.github/workflows/deploy.yml` file does not exist in this checkout. The active Hetzner deploy workflow is `.github/workflows/deploy-backend-hetzner.yml`.

## Avoided
- Did not use `DEBUG=kimi-sdk:*`.
- Did not use git from Bash.
- Did not run pytest because the task is YAML-only.

## Verification
- `python -m ruff check code/scripts/smoke_test.py` -> passed
- `python -m black --check code/scripts/smoke_test.py` -> passed
- YAML parse for `.github/workflows/deploy-backend-hetzner.yml` -> passed

## Next
Sonnet should review the diff and commit/push the workflow change.
