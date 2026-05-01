---
name: 2026-05-01_Codex_GPT55-Run03_ci_online_readiness
type: run
---
## Goal
Resolve the apparent large change/online-readiness confusion, fix failing GitHub CI paths, and prepare a clean online PR.
## Done
Confirmed local `master` was clean and PR #3 was merged; fixed CI path roots from `backend/app tests` to `code/backend/app code/tests`; formatted backend/tests with Black; fixed Ruff E402 imports; addressed Bandit medium findings with a trusted-local pickle exception and explicit HuggingFace revision parameter; set CI coverage gate to the measured 65% baseline.
Merged PR #4 to `master`; master CI is green across lint, backend tests, frontend tests, MCP smoke, and Docker build/health. Hardened Docker demo compose, backend Docker writable data paths, Hetzner model generation, root `scripts`/`schemas` sync, and deterministic `PROJECT_ROOT=/app` mounts.
## Surprised by
The active local Python was 3.14, which cannot install the pinned backend `pydantic-core`; Python 3.13 in `code/.venv313` is the correct test runtime.
## Avoided
Did not push directly to `master`, did not commit generated graph snapshots or coverage artifacts, and did not retry deploy workflows while external blockers remain.
## Next
Deploy is now blocked only by external access/config: add Hetzner public key to `/root/.ssh/authorized_keys`, fix INWX DNS, add `FLY_API_TOKEN`, create/verify Fly app+cert, then rerun backend/frontend deploy workflows.
## Memory updates
This run records the current validated quality gates and the Python 3.13 requirement for backend tests.
