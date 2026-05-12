---
name: 2026-05-12_codex_K-57_smoke_test
type: run
agent: Codex GPT-5.5
task: K-57
---

## Goal
Create `code/scripts/smoke_test.py` for Docker Compose and CI full-stack checks.

## Done
- Added `code/scripts/smoke_test.py` with five checks: `/health/`, `/api/v1/health`, inference upload with `tests/test_data/real_mri/MR000000.dcm`, splash GET 405, splash POST audit response.
- Added `/api/v1/health` by registering the existing health router under the versioned API prefix in `code/backend/app/main.py`.
- Added and closed `K-57` in `tasks.jsonl`.

## Surprised by
The first local backend start failed because the inherited shell environment had `DEBUG=kimi-sdk:*`; explicit smoke env values fixed startup.

## Avoided
- Did not edit `backend/app/core/config.py`, `code/tests/conftest.py`, or anything under `deploy/`.
- Did not touch the unrelated dirty frontend/website changes already present in the worktree.

## Next
Wire `python scripts/smoke_test.py` into the desired CI/Compose job after deciding where the stack startup waits should live.

## Verification
- `python -m py_compile scripts/smoke_test.py`
- `ruff check backend/app/main.py scripts/smoke_test.py`
- `black --check backend/app/main.py scripts/smoke_test.py`
- `pytest tests/test_smoke.py tests/test_splash_confirmation.py -q -p no:warnings` -> 8 passed
- Local backend smoke with explicit env -> 5/5 steps passed
