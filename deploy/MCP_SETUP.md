# MCP Trio Setup — Obsidian + Graphify + Hermes (+ Browser-Harness)

> ADR: `regulatory/adr/ADR-0007-mcp-trio.md`. Local-First. Lokal Python + Ollama. Keine Cloud.

---

## 0 · Voraussetzungen (einmalig)

```powershell
# Python 3.11+
python --version

# Ollama läuft + Modelle gepullt
ollama serve            # Hintergrund
ollama pull mistral:7b
ollama pull qwen3:4b

# Hermes-Container läuft (siehe code/docker-compose.yml, Service "hermes")
docker compose -f code/docker-compose.yml up -d hermes
curl http://localhost:8200/health    # erwartet 200 OK
```

## 1 · MCP-Pakete

```powershell
cd "C:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI\code\mcp_servers"
pip install -r requirements.txt --break-system-packages
```

## 2 · Smoke-Test (vor Claude-Registrierung)

```powershell
cd "C:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI"
python code\mcp_servers\run_loop.py status
# Erwartet: vault stats + graph stats + hermes/ollama reachable=true
python code\mcp_servers\run_loop.py loop
# Erwartet: pre+post läuft, Reflektions-Datei in memory/reflections/
```

## 3 · Obsidian Vault initialisieren

1. Obsidian installieren — https://obsidian.md
2. „Open folder as vault" → `C:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI`
3. Settings → Community Plugins → Turn on → Browse → suche **Graphify**
4. Install → Enable
5. Graphify-Settings: Index-Path = `memory/graph_snapshots/`
6. Optional: Plugin **Dataview** für Frontmatter-Queries

> Hinweis: Unsere `graphify-mcp` ist unabhängig vom Plugin. Plugin = UI-Visualisierung für Lou. MCP = Modell-Zugriff auf Graph.

## 4 · Claude Desktop registrieren

1. Datei kopieren: `deploy\claude_desktop_config.example.json` → `%APPDATA%\Claude\claude_desktop_config.json`
2. Falls Datei schon existiert: `mcpServers`-Block mergen, nicht überschreiben.
3. Claude Desktop komplett beenden + neu starten.
4. In neuer Session: „Liste alle MCP-Server auf" → erwartet: `carotis-obsidian`, `carotis-graphify`, `carotis-hermes` aktiv.

## 5 · Claude Code (Cowork-Mode) registrieren

`.mcp.json` liegt bereits im Repo-Root. Beim Öffnen des Projekts in Claude Code wird automatisch geladen.

## 6 · Browser-Harness verbinden

Cowork hat Chrome-MCP built-in. Für Hermes-Side-Browser:

```powershell
docker compose -f code/docker-compose.yml exec hermes npx @playwright/mcp --port 8201 &
```

oder über Hermes-Skill: `clinical-research-harness` ruft browser-harness intern.

## 7 · Per-Run-Loop verdrahten

In jedem Claude-Session-Start:

```powershell
python code\mcp_servers\run_loop.py pre
```

Am Session-Ende:

```powershell
python code\mcp_servers\run_loop.py post
```

Optional — Auto-Hook in CLAUDE.md ergänzen (Pre-Flight-Block).

## 8 · Verifikation

```powershell
python code\mcp_servers\test_mcp_trio.py
# erwartet: alle 4 Komponenten grün, exit 0
```

---

## Troubleshooting

| Symptom | Ursache | Fix |
|---------|---------|-----|
| `mcp` ImportError | Paket fehlt | `pip install mcp` |
| `hermes_reachable=false` | Hermes-Container down | `docker compose up -d hermes` |
| `ollama: reachable=false` | Service nicht gestartet | `ollama serve` |
| `vault_write deny` | Pfad nicht in ALLOW_WRITE_GLOBS | Pfad anpassen oder Glob in `obsidian_mcp.py` ergänzen |
| Graphify-Plugin findet keinen Index | Pfad falsch | Settings → Index-Path = `memory/graph_snapshots/latest.json` |
| `lock_acquired=false` | Lockfile alt | `del memory\.run.lock` |
| `browser_navigate` fehlt | Playwright nicht installiert | `pip install playwright>=1.40 && playwright install chromium` |
| Combined startet nicht | Sub-Modul fehlt | `pip install -r requirements.txt` |

---

## 9 · Browser-MCP Setup

```powershell
pip install playwright>=1.40
playwright install chromium
```

Claude Desktop Config → `carotis-browser` Eintrag (siehe `claude_desktop_config.example.json`).

Tools: `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_evaluate`, `browser_close`.

## 10 · Combined-Mode (Ressourcen-sparend)

Statt 4 Prozessen → 1 Prozess:

```powershell
python code\mcp_servers\combined_mcp.py
```

Enthält **alle** Tools von Obsidian + Graphify + Hermes + Browser. Nur ein stdio-Channel.

## 11 · Auto-Start

`run_loop.py pre` startet Hermes + Ollama automatisch wenn down:

```powershell
$env:CAROTIS_AUTO_START="1"  # Default
python code\mcp_servers\run_loop.py pre
```

## Datei-Karte

```
code/mcp_servers/
├── __init__.py
├── requirements.txt
├── obsidian_mcp.py     ← Vault-CRUD + Backlinks + Search
├── graphify_mcp.py     ← Graph-Build + Neighbors + Path + Tags
├── hermes_mcp.py       ← Hermes-Proxy + Skill-Calls + Reflection
├── browser_mcp.py      ← Playwright-Browser-Automation
├── combined_mcp.py     ← Alle 4 Server in einem Prozess
├── run_loop.py         ← Pre/Post-Hook + Auto-Start
└── test_mcp_trio.py    ← Smoke + E2E

deploy/
├── claude_desktop_config.example.json   ← Claude Desktop
└── MCP_SETUP.md                          ← Diese Datei

.mcp.json                                 ← Claude Code
```

---

*Letztes Update: 2026-04-30 — Lou (caveman-mode)*
