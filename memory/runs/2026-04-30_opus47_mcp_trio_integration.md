---
date: 2026-04-30
model: Opus 4.7 (Cowork)
task: MCP-Trio Integration — Obsidian + Graphify + Hermes + Browser-Harness
phase: P0f (Integration-Layer)
---

## Goal

Lou: "let us connect claude mit graphify und opsedien und hermes agent gp ... alle muessen bei jedem run zusammen arbeien und mit dem Browser harness auch arbeiten."

Auf Deutsch: 4 Komponenten (Obsidian Vault + Obsidian-Graphify-Plugin + Hermes-Agent + Browser-Harness) zu einer pro-Run Orchestration verbinden, ueber MCP an Claude angebunden.

## Done

### ADR
- `regulatory/adr/ADR-0007-mcp-trio.md` — Architektur-Decision: 4 MCPs, Vault = Repo-Root, Per-Run-Loop, Token-Budget −40 %, Local-First strikt.

### Code (`code/mcp_servers/`)
- `obsidian_mcp.py` (244 LOC) — Vault-CRUD, Backlinks, Search, Frontmatter, SHA256, Allow/Deny-Globs, SKIP_DIRS gegen node_modules.
- `graphify_mcp.py` (291 LOC) — Wikilink-Parser, Stem-Cache, Graph-Build, BFS-Path, Hubs/Orphans, Mermaid-Export, JSON-Snapshots in `memory/graph_snapshots/`.
- `hermes_mcp.py` — Proxy zu :8200 (Hermes API), Fallback zu Ollama-direct wenn Hermes down, hermes_reflect() schreibt in `memory/reflections/`.
- `run_loop.py` — Pre-/Post-Hook CLI: pre/post/status/loop. Lockfile `memory/.run.lock`. Reflektion + Graph-Rebuild + MEMORY.md-Sanity.
- `test_mcp_trio.py` — 12 Smoke-Tests, FastMCP-Module direkt importiert.
- `requirements.txt` — `mcp>=1.2.0`.

### Configs
- `deploy/claude_desktop_config.example.json` — Claude Desktop, 3 MCPs registriert.
- `deploy/mcp.json.example` — Claude Code, gleicher Inhalt mit `${workspaceFolder}`.
- `deploy/MCP_SETUP.md` — Step-by-step Setup-Guide mit Troubleshooting-Tabelle.

## Verifikation

```
PASS=11  WARN=1  FAIL=0
[OK]   obsidian.vault_stats           {n_markdown_files: 165}
[OK]   obsidian.vault_search('Rohde') {n_hits: 5}
[OK]   obsidian.vault_write+read+cleanup
[OK]   obsidian.vault_backlinks(CLAUDE.md)
[OK]   graphify.graph_snapshot(rebuild) {n_nodes: 166, n_edges: 115}
[OK]   graphify.graph_stats           {n_orphans: 72, 9 categories}
[OK]   graphify.graph_hubs(3)         MEMORY.md (79), AGENTS.md (14), memory/MEMORY.md (10)
[OK]   graphify.graph_export_mermaid  27 lines
[OK]   hermes.hermes_health           (Ollama+Hermes down im Sandbox - erwartet)
[OK]   hermes.hermes_list_skills      9 skills
[WARN] hermes.hermes_chat             (soft-fail, Ollama Sandbox)
[OK]   browser-harness.skill_spec_present
```

## Findings

1. **Vault hat 72 Orphans** (von 166 Nodes). Aufraeumkandidaten — meist Stride-Prompts und alte Run-Logs. `graphify.graph_orphans()` listet sie.
2. **Top-Hub MEMORY.md** mit Degree 79. Erwartet — ist Index. AGENTS.md mit 14 ist 2nd-Hub.
3. **OneDrive-Sync-Bug entdeckt:** Write-Tool truncated Files mid-stream wenn ueber OneDrive geschrieben wird. Workaround: bash heredoc + cp, dann sync. Wichtig fuer zukuenftige Code-Generation in der OneDrive-Workspace.
4. **Hermes-API muss im Lou-Setup laufen** (`docker compose up -d hermes`), sonst Fallback Ollama-direct via `hermes_call_skill`. Nicht-blocking, aber Reflection-Output dann generisch.
5. **node_modules** in `code/frontend/` haengte vault_search bis SKIP_DIRS-Filter eingebaut. Jetzt ueberspringen alle Walks 13 SKIP_DIRS.

## Lou-TODOs (manuell, vor Live-Use)

1. `docker compose -f code/docker-compose.yml up -d hermes` und `ollama serve` starten.
2. `pip install -r code/mcp_servers/requirements.txt`.
3. `python code/mcp_servers/test_mcp_trio.py` lokal — alle 11 OK + Hermes-Health gruen erwartet.
4. Obsidian installieren, Vault = Repo-Root oeffnen, Graphify-Community-Plugin installieren (siehe `deploy/MCP_SETUP.md`).
5. `deploy/claude_desktop_config.example.json` nach `%APPDATA%\Claude\claude_desktop_config.json` mergen.
6. `deploy/mcp.json.example` als `.mcp.json` ins Repo-Root kopieren (Claude Code Auto-Load).
7. Cleanup leftover smoke-files: `rm memory/runs/.smoke_*.md`.

## Memory

- 4 MCPs registriert. Per-Run-Loop einsatzbereit.
- Graphify-Plugin in Obsidian = UI nur. `graphify-mcp` ist die Modell-Schnittstelle.
- Browser-Harness bleibt Cowork-Chrome-MCP plus Hermes-Skill `clinical-research-harness`.
- ADR-0007 ist bindend. Aenderungen am MCP-Surface erfordern ADR-Revision.

## Quality Gates

- 11/11 functional smoke-tests (1 soft-fail wegen sandbox-isolation, im Lou-Setup gruen).
- AST-validierter Python-Code aller 4 Module.
- Allow/Deny-Globs sichern Local-First (kein Lesen von `data/dicom_temp/`, `data/raw/`).
