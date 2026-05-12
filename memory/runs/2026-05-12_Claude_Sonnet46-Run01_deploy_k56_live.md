# Run: 2026-05-12 — Claude Sonnet 4.6 — Run 01

**Goal:** Finish all open coding tasks (K-56 deploy + test isolation fix), push to master, trigger Hetzner deploy.

---

## What happened

### 1. Test isolation fix (conftest.py)
- Root cause: `backend/.env` sets `DATABASE_URL=sqlite+aiosqlite:///./data/carotis.db`
- File `code/data/carotis.db` on read-only OneDrive mount had 1 stale `decision_trees` record
- `os.environ.setdefault()` was insufficient — pydantic-settings v2 reads os.environ before .env file, but `setdefault` doesn't override if env var already set (it wasn't — it was `.env` file being read)
- Fix: changed `os.environ.setdefault("DATABASE_URL", ...)` → `os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"` (forced)
- Result: **127 passed, 12 skipped** (torch/onnx skips expected in sandbox)

### 2. K-56 scope verified
All K-56 features were already implemented from previous sessions:
- `backend/app/api/routes/splash_confirmation.py` — POST /api/v1/splash-confirmation
- `backend/app/core/feature_flags.py` — CDS gate (`cdsEnabled: false`)
- `backend/app/main.py` — splash_confirmation router wired
- `frontend/src/components/ResearchSplashGate/` — disclaimer gate
- `frontend/src/components/Watermark/` — viewport watermark
- `frontend/src/App.tsx` — featureFlags wired, CDS panel gated, DEMO_CASES cleaned

### 3. Git commit + push
- **153 files changed, 10935 insertions, 926 deletions**
- Commit: `6ad423a feat(K-56): ResearchSplashGate, Watermark, FeatureFlags, test isolation`
- Pushed to `origin/master`
- GitHub Actions `deploy-backend-hetzner.yml` triggered automatically (paths: code/backend/**, code/frontend/**)

### 4. Deploy smoke (pre-GitHub Actions completion)
- `https://api.carotis.diggai.de/health/` → 200 OK ✅
- `https://carotis.diggai.de/` → 200 OK, HTML served ✅
- GitHub Actions full deploy (Docker build + frontend npm build) takes ~5-8 min after push

---

## Technical notes

- `.git/index.lock` was stale on OneDrive mount — removed via `mcp__Windows-MCP__PowerShell` `Remove-Item -Force`
- Desktop Commander cmd shell: `&&` not supported in PowerShell mode, paths with spaces need special handling — use `& $git -C $repo` pattern in PowerShell instead
- git binary: `C:\Program Files\Git\cmd\git.exe`
- git `-C <path>` flag works cleanly with PowerShell `&` invocation operator

---

## Open after this session
- **Post-deploy smoke**: After GitHub Actions completes, verify ResearchSplashGate appears on `https://carotis.diggai.de/` and no NASCET/Vulnerability/% visible without confirmation
- **W-12 Mail an Rohde**: Still human-blocked (Lou to send)
- **P1+**: Blocked by Rohde response

---

## Artifacts
- Commit: `6ad423a` on `master`
- Tests: 127 passed, 12 skipped
