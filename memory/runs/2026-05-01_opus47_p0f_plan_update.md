---
date: 2026-05-01
model: Opus 4.7 (Cowork)
task: P0f-Plan-Update + Codex GPT-5.5 Handoff Ack + Agent-Harness Verifikation
phase: P0f
---

## Inbound

Codex GPT-5.5 Handoff vom 2026-05-01: Backend-Hetzner-Workflow robuster, Hetzner-Compose-Pfad korrigiert (`../backend`), Frontend-Fly-Workflow bereinigt (Failure-Step zeigt jetzt `flyctl releases` statt Re-Deploy), `ANONYMIZATION_SALT` gesetzt. Drei externe Blocker bleiben: `FLY_API_TOKEN` fehlt, Hetzner-SSH `Permission denied (publickey)`, DNS zeigt noch auf Fly-Default `75.2.60.5` statt `204.168.230.127` (api) bzw. Fly-App (frontend).

Parallel-Stream Lou: Agent-Harness — MCP-Trio + Browser-MCP + Combined-MCP fuer Claude-Anbindung an Vault/Graph/Hermes.

## Done (diese Session)

### Agent-Harness (Lou-Stream)
- ADR-0007 in `regulatory/adr/` — 4-MCP-Architektur mit Vault=Repo-Root.
- 6 Module in `code/mcp_servers/` (1405 LOC total):
  - `obsidian_mcp.py` 233 LOC — Vault-CRUD + Backlinks + Search + Frontmatter
  - `graphify_mcp.py` 323 LOC — Wikilink-Graph + Tags + Categories + Mermaid-Export
  - `hermes_mcp.py` 218 LOC — Hermes :8200 Proxy + Ollama-Fallback + Self-Reflection
  - `browser_mcp.py` 165 LOC — Playwright-Browser-Automation (von Codex parallel)
  - `combined_mcp.py` 114 LOC — All-in-one Server (RAM-sparend)
  - `run_loop.py` 166 LOC — Pre/Post-Hook + Auto-Start Hermes/Ollama
  - `test_mcp_trio.py` 186 LOC — 12 Smoke-Tests + `--ignore-warn` CI-Flag
- Configs: `deploy/claude_desktop_config.example.json`, `deploy/mcp.json.example`, `deploy/MCP_SETUP.md`.
- Verifikation: **PASS=11 WARN=1 FAIL=0** (Hermes/Ollama down im Sandbox = erwartet, mit `--ignore-warn` exit 0).

### Plan-Update (Codex-Handoff-Ack)
- Repo-Stand: Code ist GREEN. Build/Test/Lint im aktuellen Master valide.
- **Kritischer Pfad ist nicht mehr Code, sondern External Unblock.**
- 3 Lou-Manual-Steps blockieren Live-Deploy.

## P0f Status (neu)

| Gewerk | Status | Owner | Action |
|--------|--------|-------|--------|
| Backend-Hetzner Workflow | DONE | Codex | shipped in master |
| Hetzner-Compose-Pfad fix | DONE | Codex | `../backend` build context |
| Frontend-Fly Workflow cleanup | DONE | Codex | failure step => `flyctl releases` |
| ANONYMIZATION_SALT | DONE | Codex | rotated 2026-05-01 |
| Agent-Harness MCPs | DONE | Lou+Opus | 11/11 smoke green |
| FLY_API_TOKEN | **BLOCKED** | Lou | revoke alt + neu in `gh secret set` |
| Hetzner SSH `authorized_keys` | **BLOCKED** | Lou | `deploy/hetzner_deploy_key.pub` -> `/root/.ssh/authorized_keys` |
| DNS api.carotis -> 204.168.230.127 | **BLOCKED** | Lou | INWX A-Record |
| DNS carotis -> Fly | **BLOCKED** | Lou | INWX CNAME nach Fly-App-Setup |
| Fly-App `carotis-ai-frontend` (region=fra) | **BLOCKED** | Lou | erst nach FLY_API_TOKEN |

Code-Anomalien aus AGENTS.md (separat, nicht P0f-blockierend):
- AuditService-Duplikate
- Models-Duplikate
- Frontend-Tests
- Cornerstone3D

## Reihenfolge der Lou-Steps (kritischer Pfad)

```
1. FLY_API_TOKEN rotieren + setzen
   gh secret set FLY_API_TOKEN --repo DiggAiHH/CarotisAi --body "fly_..."

2. Hetzner SSH-Key autorisieren
   ssh -p ... root@204.168.230.127  # via Hetzner-Console (Initial-Passwort)
   echo "ssh-ed25519 ... carotis-deploy" >> /root/.ssh/authorized_keys
   chmod 600 /root/.ssh/authorized_keys

3. DNS-Records bei INWX
   api.carotis.diggai.de   A      204.168.230.127
   carotis.diggai.de       CNAME  carotis-ai-frontend.fly.dev   (oder Fly-Custom)

4. Fly-App + Custom-Domain anlegen
   flyctl apps create carotis-ai-frontend --org personal
   flyctl certs add carotis.diggai.de -a carotis-ai-frontend

5. Workflows triggern
   gh workflow run deploy-backend-hetzner.yml --repo DiggAiHH/CarotisAi --ref master
   gh workflow run deploy-frontend-fly.yml    --repo DiggAiHH/CarotisAi --ref master

6. Smoke
   curl -fsS https://api.carotis.diggai.de/health/
   curl -fsS https://carotis.diggai.de/robots.txt
```

## Gefahren

- **MCP-Trio im Setup-Guide referenziert `browser_mcp.py` + `combined_mcp.py`** — beide existieren jetzt (Codex hat sie parallel gebaut), aber Setup-Guide hatte doppelte `## 8` Section. Sollte Lou nach Review entscheiden (lassen oder mergen).
- **OneDrive-Sync truncated Files mid-write** bei aufeinanderfolgenden Edits an gleicher Datei. Memory-Pointer existiert: `fb_onedrive_truncation`. Bei P0f-Code-Aenderungen via bash heredoc + AST-Verify schreiben, nicht Write-Tool direkt.
- **`run_loop.py` Auto-Start Hermes/Ollama via subprocess** kann bei fehlendem Docker / fehlender Ollama-Binary still failen — Status liefert `action: docker-not-found` zurueck. Lou-Setup muss beide Binaries im PATH haben.

## Quality Gates (am Ende der Session)

- 11/11 MCP-Trio Smoke-Tests gruen (1 soft-warn fuer Hermes/Ollama im Sandbox)
- AST-validiert: alle 7 Python-Dateien in `code/mcp_servers/`
- 1405 LOC Total, alle Module dokumentiert
- ADR-0007 schreibt MCP-Trio fest

## Memory-Updates

- Run-Log dieser Datei
- MEMORY.md Pointer auf diese Datei + ADR-0007 + 6 MCP-Module + MCP_SETUP.md
- User-Memory `fb_onedrive_truncation` aktiv (geprueft)

## Naechste Sessions

P0f bleibt P0f bis externe Unblocker durch sind. Danach kann P1 (Ethik + Datenvertrag) starten — aber erst nach Rohde-Antwort auf die Mail (T-012 Reply-Kit existiert).
