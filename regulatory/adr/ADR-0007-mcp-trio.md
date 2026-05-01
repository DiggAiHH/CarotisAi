# ADR-0007 — MCP-Trio: Obsidian + Graphify + Hermes (+ Browser Harness)

- **Status:** Proposed (2026-04-30)
- **Decision-Owner:** Lou
- **Phase:** P0f → P1
- **Supersedes:** —
- **Related:** ADR-0001 (Local-First), ADR-0002 (Decision-Tree-Harvesting), `memory/domain/hermes_workflow.md`

---

## Context

Carotis-AI Working-Memory-System ist Markdown-Filesystem (CLAUDE.md, MEMORY.md, runs/, decisions/, anomalies/, regulatory/). Hermes existiert als HTTP-API auf `localhost:8200` (Ollama-backed Self-Improving-Layer). Browser-Harness existiert als Skill-Spec, jedoch ohne durchgängige Tool-Bindung an Claude. Knowledge-Graph fehlt ganz.

**Problem:** Claude (Cloud-Modelle) sieht das System nur durch CLAUDE.md + MEMORY.md. Kein semantischer Graph, keine Backlink-Suche, keine direkte Hermes-Skill-Ausführung, kein Browser-Auto-Run innerhalb einer Session. Pro Run muss alles manuell zusammengeführt werden — kostet Tokens und Zeit.

**Anforderung Lou:**
1. Memory-Sync Claude ↔ Obsidian Vault pro Run
2. Knowledge-Graph wird pro Run neu gebaut
3. Hermes als lokaler Orchestrator + Function-Calling-Agent + Self-Improving-Layer
4. MCP-Server für alle drei
5. Browser-Harness läuft mit

---

## Decision

**4-MCP-Architektur, Claude lädt alle vier pro Run.**

| MCP | Server | Aufgabe | Endpoint |
|-----|--------|---------|----------|
| `obsidian-mcp` | Python/FastMCP, lokal stdio | Vault-CRUD, Backlinks, Search, List-Notes | stdio |
| `graphify-mcp` | Python/FastMCP, lokal stdio | Graph-Aggregation aus `[[wikilinks]]` + frontmatter, JSON-Snapshot, Neighbor/Path-Queries | stdio |
| `hermes-mcp` | Python/FastMCP, lokal stdio | Proxy zu Hermes API :8200 — Skill-Calls, Reflektion, Function-Calling | stdio → http://localhost:8200 |
| `chrome-mcp` | Cowork-built-in | Browser-Harness — PubMed, Radiopaedia, ESC, ACR | bestehend |

**Vault = Carotis-AI-Workspace selbst.** Kein Mirror, kein Sync-Layer. `.obsidian/` wird im Workspace-Root angelegt, Graphify als Community-Plugin installiert.

**Per-Run-Loop:**
```
Pre-Flight:  cat CLAUDE.md, MEMORY.md, last 3 runs  ──>  graphify_mcp.snapshot()  ──>  hermes_mcp.health()
In-Run:      memory writes via obsidian_mcp.write_note()  ──>  graphify_mcp.reindex_on_change()
Post-Flight: hermes_mcp.reflect(run_log)  ──>  obsidian_mcp.write_note(reflection)  ──>  graphify_mcp.export_graph()
```

---

## Consequences

### Positive

- **Token-Effizienz:** Claude muss nicht mehr alle MEMORY-Files in Kontext laden — gezielte `obsidian_mcp.search()` + `graphify_mcp.query_neighbors()` reichen. Prognose: −40 % Input-Tokens pro Run.
- **Local-First strikt erfüllt:** Alle 3 MCPs laufen lokal, kein Patientendaten-Egress, kein Cloud-Roundtrip für Memory.
- **Self-Improving-Loop schließt sich:** Hermes reflektiert jeden Run automatisch, schreibt Reflektion in `memory/reflections/`, beim nächsten Run lädt Claude die jüngste Reflektion mit.
- **Graphify visualisiert das Wissen:** Lou kann den Graph in Obsidian öffnen und navigieren. Modelle bekommen den Graph als JSON.
- **Browser-Harness produktiv:** Cowork-Chrome-MCP plus `clinical-research-harness` Hermes-Skill — keine Doppelinfrastruktur.

### Negative / Risiken

- **+4 Prozesse pro Session.** Mitigation: `scripts/start_mcp_trio.ps1` startet alle, `stop_mcp_trio.ps1` killt sauber.
- **Graphify-Plugin ist Community-Code.** Mitigation: Eigener Graph-Builder als Fallback in `graphify-mcp` (parst `[[wikilink]]` selbst, exportiert JSON). Plugin nur Visualisierung für Lou.
- **stdio-MCPs sind 1:1 zu Claude-Session.** Bei parallelen Sessions: zweite Instanz blockiert nicht (stdio multiplexing pro Subprocess), aber Schreibkonflikte auf Vault möglich. Mitigation: Lockfile `memory/.run.lock` mit PID.
- **Obsidian läuft nicht headless.** Mitigation: Vault-Operationen via `obsidian-mcp` (Filesystem direkt), nicht via Obsidian-API. Obsidian ist nur die UI.

### Neutral

- **Compliance-Footprint identisch zu vorher.** Alle Datenströme bleiben lokal, neue Komponenten greifen nur auf bereits-erlaubte Pfade zu (`memory/`, `data/anonymized/`).

---

## Implementation Plan

| Wave | Artefakt | Task |
|------|----------|------|
| G-01 | ADR-0007 (dieses Dokument) | DONE |
| G-02 | `code/mcp_servers/obsidian_mcp.py` | TaskID 2 |
| G-03 | `code/mcp_servers/graphify_mcp.py` | TaskID 3 |
| G-04 | `code/mcp_servers/hermes_mcp.py` | TaskID 4 |
| G-05 | `code/mcp_servers/run_loop.py` | TaskID 5 |
| G-06 | `deploy/claude_desktop_config.example.json` + `.mcp.json` + `deploy/MCP_SETUP.md` | TaskID 6 |
| G-07 | `code/mcp_servers/test_mcp_trio.py` (Smoke + E2E) | TaskID 7 |

---

## Tool-Surface (Auszug)

### `obsidian-mcp`
- `vault_search(query, k=10) → [{path, score, snippet}]`
- `vault_read(path) → {content, frontmatter, backlinks[]}`
- `vault_write(path, content, append=False) → {bytes_written, sha256}`
- `vault_list(glob, limit=100) → [paths]`
- `vault_backlinks(path) → [paths]`

### `graphify-mcp`
- `graph_snapshot(force_rebuild=False) → {n_nodes, n_edges, path_to_json}`
- `graph_neighbors(node_path, depth=1) → [{path, edge_type}]`
- `graph_path(from, to) → [path_steps]`
- `graph_orphans() → [paths]`
- `graph_hubs(top_k=10) → [{path, degree}]`

### `hermes-mcp`
- `hermes_health() → {ollama, hermes, models[], uptime}`
- `hermes_call_skill(skill, args, timeout_s=300) → {output, tokens, duration_ms}`
- `hermes_reflect(run_log_path) → {reflection_path, novelty_score, suggestions[]}`
- `hermes_compress(file_path, target_tokens=1500) → {compressed_path, ratio}`
- `hermes_function_call(name, args) → {result}`

---

## Verification

DoD für ADR-0007:

- [ ] `code/mcp_servers/obsidian_mcp.py` antwortet auf `vault_search("Rohde")` mit ≥1 Hit
- [ ] `code/mcp_servers/graphify_mcp.py` exportiert valides JSON nach `memory/graph_snapshots/latest.json`
- [ ] `code/mcp_servers/hermes_mcp.py` proxied `hermes_health()` an :8200, gibt Ollama-Status zurück
- [ ] `code/mcp_servers/run_loop.py` läuft Pre+Post in <10 s
- [ ] `scripts/test_mcp_trio.py` exit 0
- [ ] `deploy/MCP_SETUP.md` reproduziert Setup auf einem zweiten Rechner

---

*Letztes Update: 2026-04-30 — Lou (caveman-mode)*
