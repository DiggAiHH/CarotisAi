# Plan: Hermes + Browser Harness Integration

## Ziel
Hermes Agent vollständig in Carotis-AI integrieren + Browser Harness (Playwright MCP) für ärztliches Knowledge Harnessing.

## Hermes-Status
- Ollama läuft (localhost:11434) — Modelle: mistral:7b, qwen3:4b, gpt-oss:20b
- Config verweist auf nicht-existierende Modelle (nous-hermes-3, qwen2.5-coder)
- 4 Skills existieren (anonymize, capture, aggregate, retrain)

## Tasks

### 1. Hermes Config Fix
- Modelle auf verfügbare umbiegen (mistral:7b als Default, qwen3:4b als Fallback)
- Endpoint korrekt setzen

### 2. Neue Skills für Doctor Knowledge Harnessing
- `doctor-knowledge-capture.md` — Echtzeit-Erfassung + Browser-Hilfe für Begründungen
- `clinical-research-harness.md` — PubMed/Leitlinien-Recherche via Playwright
- `decision-pattern-miner.md` — Mustererkennung in Decision-Trees
- `trust-calibration-monitor.md` — Trust-Score-Monitoring + Alerts

### 3. Browser Harness Integration
- Playwright MCP ist bereits verbunden
- Hermes-Skills erweitern um Browser-Tool-Calls
- Prozess: Arzt stellt Frage → Hermes recherchiert via Browser → Ergebnis in Decision Tree

### 4. Management-Integration
- `docker-compose.yml` erweitern (Hermes-Service + Ollama-Healthcheck)
- Prozess-Doku: `memory/domain/hermes_workflow.md`
- Settings: `code/hermes/settings/knowledge_harness.json`

### 5. Verify
- Hermes startet ohne Fehler
- Skills sind ladbar
- Browser-Harness-Skill funktioniert (Mock-Test)
