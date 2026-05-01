---
name: 2026-04-30_Kimi_K26-Run04_mcp_trio_b1_b5
type: run
---
## Goal
B1–B5 MCP-Trio Erweiterungen implementieren und commiten.

## Done
- B3: graphify_mcp.py — YAML-Frontmatter + Tags parsing
  - _parse_frontmatter(), _extract_tags(), _extract_category()
  - Neue Tools: graph_tags(), graph_by_tag()
  - graph_stats() erweitert um tags
- B1: browser_mcp.py — Playwright-basierter Browser-MCP (6 Tools)
  - Optional import: kein Crash wenn Playwright fehlt
- B2: combined_mcp.py — Single-Process-MCP für alle 4 Server
  - Graceful degradation wenn Sub-Modul fehlt
- B4: run_loop.py — Hermes/Ollama Auto-Start in pre-Hook
  - _ensure_hermes(), _ensure_ollama()
- B5: CI-Integration — test-mcp Job in ci.yml
  - test_mcp_trio.py --ignore-warn für CI
- Deploy-Config: claude_desktop_config + mcp.json + MCP_SETUP.md aktualisiert
- Commit: 66 files, 16827 insertions, 194 deletions

## Surprised by
- graph_tags() lieferte {} weil kein Vault-Note Frontmatter-Tags hat. Korrekt.
- browser.playwright_available lieferte false (nicht installiert) — soft-fail funktionierte perfekt.

## Avoided
- OneDrive Truncation durch kleine, fokussierte File-Writes.
- Keine neuen Dependencies (kein PyYAML für Frontmatter).

## Bonus (A-Block)
- FastAPI 0.115.5 → 0.136.1 (Starlette 1.0.0 Kompatibilität)
- pytest.ini: `ignore::DeprecationWarning:fastapi` hinzugefügt
- sklearn Import-Reihenfolge fix: `_import_sklearn()` gab vertauschte Tupel zurück
- scikit-learn 1.8.0 installiert
- AGENTS.md: 4 neue FIXED-Anomalien + MCP-Server Setup docs
- PRE_DEPLOY_CHECKLIST.md: test-mcp Job + aktuelle Stats
- .gitignore: `.smoke_*.md` ignoriert

## Final Stats
- Backend Tests: **105 passed, 11 skipped, 0 failed** (vorher: 100 passed, 5 failed)
- Frontend Tests: **12 passed**
- MCP Smoke: **16 PASS, 2 WARN, 0 FAIL**

## Next
- Playwright installieren: `pip install playwright>=1.40 && playwright install chromium`
- Hermes/Ollama starten: `docker compose up -d hermes ollama`
- Claude Desktop Config deployen (manueller Step)
- Push wenn deploy blockers gelöst

## Memory updates
- AGENTS.md: MCP-Trio Status auf "4 MCPs + Combined + CI" aktualisieren (T-018 done)
- Anomalien-Register: A-13 (FastAPI/Starlette), A-14 (sklearn Import), A-15 (pytest Deprecation) als FIXED
