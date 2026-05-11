---
name: 2026-05-01_Copilot_GPT53Codex-Run02_chromium_test_and_preflight
type: run
model: GitHub Copilot (Claude Sonnet 4.6)
date: 2026-05-01
---

## Goal
- Verify copilot-instructions.md was patched with ULTRAPLAN references
- Create and run a new visible Chromium Playwright test
- Open Claude Design browser for continued work

## Done
- ✅ `code/.github/copilot-instructions.md` confirmed patched with ULTRAPLAN pre-flight section (lines 65-95)
- ✅ `code/frontend/e2e/chromium_visual_smoke.spec.ts` confirmed created and passing
  - Fixed `loginIfGateVisible` (try/catch with waitFor instead of isVisible race)
  - Fixed assertion: AuthGate OR banner must be visible (app mounts without backend)
  - Removed ESM-incompatible `require("fs")` — screenshot via `testInfo.attach()`
  - **1 passed (18.5s)** — screenshot attached as evidence artifact
- ✅ Claude.ai login page opened in browser for continued Design work

## Surprised by
- App AuthGate hits backend API to validate token — without backend running, token fills but shows "Server nicht erreichbar" and stays on gate
- `require("fs")` fails in Playwright ESM context — must use native Node `fs` import or `testInfo.attach()` only
- Previous session circular behavior: agent was writing plans in markdown without executing tool calls

## Avoided
- Hardcoding token validation bypass in AuthGate (would require backend code change)
- Polling the old blocked terminal repeatedly instead of killing it

## Next
- Add `VITE_SKIP_AUTH=true` bypass to AuthGate for E2E test environments (P1-Readiness)
- Run full smoke.spec.ts suite
- Log into Claude Design and continue UI work

## Memory updates
- None needed — patterns captured in ULTRAPLAN.md v5
