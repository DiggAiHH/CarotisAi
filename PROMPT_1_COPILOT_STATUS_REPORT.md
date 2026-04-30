# PROMPT 1 — Copilot Plan Mode: Erstelle vollständigen Projekt-Status-Report

> **Anweisung für Lou:** Kopiere den Text zwischen `--- PROMPT START ---` und `--- PROMPT END ---` in VS Code Copilot Chat (Modell: Sonnet 4.6, Mode: Plan). Warte bis Copilot fertig ist. Speichere die generierte Markdown-Datei als `COPILOT_STATUS_REPORT.md` im Projekt-Root (`C:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI\`). Push sie zu GitHub. Dann zeig sie Kimi.

--- PROMPT START ---

# Aufgabe: Vollständiger Projekt-Status-Report für Carotis-AI

Analysiere das komplette Repository `C:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI\` und erstelle eine Markdown-Datei `COPILOT_STATUS_REPORT.md` im Projekt-Root mit folgender Struktur. Sei extrem gründlich — jede Datei, jeder offene Punkt, jede Lücke zählt.

## ABSOLUTE PFLICHT-REGELN

1. **NUR lesen, NICHT schreiben/ändern.** Dies ist reine Analyse.
2. Wenn du eine Datei nicht verstehst, markiere sie als `"needs_review"`.
3. Wenn ein Pfad nicht existiert, schreibe `"NOT_FOUND"`.
4. Nutze `@workspace` für alle Datei-Referenzen.

---

## 1. REPO-ÜBERSICHT (Top-Level)

Für JEDE Top-Level-Datei und JEDEN Ordner (außer `.git/`, `node_modules/`, `.venv/`, `__pycache__/`):
- Name
- Zweck (1 Satz)
- Status: `COMPLETE` / `PARTIAL` / `MISSING` / `NEEDS_REVIEW`
- Letztes Änderungsdatum (aus Git)

---

## 2. BACKEND-STATUS (`code/backend/`)

### 2.1 Struktur-Tree
Vollständigen Datei-Tree ausgeben (alle `.py`, `.txt`, `.yml`, `.toml`).

### 2.2 Pro Datei: Status-Karte
Für jede Python-Datei:
```yaml
file: app/core/config.py
purpose: Pydantic-Settings, API-Key-Validierung, SQLite-Enforcement
status: COMPLETE  # oder PARTIAL / MISSING / NEEDS_REVIEW
lines: ~45
last_modified: 2026-04-30
issues: []  # oder Liste von offenen Punkten
todo_count: 0  # Anzahl # TODO / FIXME / XXX Kommentare im Code
test_coverage: YES/NO/PARTIAL  # Gibt es Tests dafür?
```

### 2.3 API-Endpunkte-Inventory
Liste ALLE definierten FastAPI-Router und Endpunkte:
```
GET  /health              → health.py          → PUBLIC
GET  /health/ready        → health.py          → PUBLIC
GET  /health/live         → health.py          → PUBLIC
POST /api/v1/inference/predict   → inference.py → AUTH + RATE-LIMIT
...
```
Markiere fehlende Endpunkte aus der Spec (z.B. `GET /api/v1/demo/whoami`, `GET /schemas/decision_tree.schema.json`).

### 2.4 Datenbank-Schema
Liste alle SQLAlchemy-Modelle mit Feldern, Constraints, Indizes.
Fehlt eine Tabelle aus der Architektur?

### 2.5 Offene TODOs im Backend-Code
Suche nach `# TODO`, `# FIXME`, `# XXX`, `# HACK`, `# REVIEW` in allen `.py`-Dateien.
Liste sie mit Datei + Zeile + Text.

### 2.6 Test-Status
- Anzahl Test-Dateien in `tests/`
- Welche Module haben KEINE Tests?
- Letzter pytest-Run: erfolgreich / fehlgeschlagen / unbekannt

---

## 3. FRONTEND-STATUS (`code/frontend/`)

### 3.1 Struktur-Tree
Vollständigen Datei-Tree (alle `.tsx`, `.ts`, `.css`, `.json`).

### 3.2 Pro Komponente: Status-Karte
Für jede `.tsx`-Datei in `src/components/`:
```yaml
file: components/AiPanel/AiPanel.tsx
purpose: Zeigt Stenose-%, Konfidenz, Vulnerability-Marker
status: COMPLETE
props_interface: YES/NO
connected_to_api: YES/NO  # Ruft es direkt den Backend an?
i18n_compliance: YES/NO   # Nutzt es t() oder hartkodierte Strings?
walkthrough_ready: YES/NO # Hat es data-walkthrough Attribute?
tests: YES/NO
```

### 3.3 State-Management-Map
- Zustand-Store (Zustand): welche Felder? Wer schreibt?
- TanStack Query: welche Queries/Mutations? Wo werden sie genutzt?
- localStorage-Keys: welche werden verwendet?

### 3.4 API-Client-Status
- `apiClient.ts`: welche Methoden? Welche fehlen?
- Auth: wird `X-Demo-Token` korrekt injiziert?
- Fehler-Handling: 401, 429, 503 — wo werden sie behandelt?

### 3.5 Routing / Navigation
- Gibt es React Router? Wenn nein, ist das beabsichtigt?
- AuthGate: wo wird es gerendert? Funktioniert der Flow?

### 3.6 Offene TODOs im Frontend-Code
Suche nach `TODO`, `FIXME`, `XXX`, `HACK` in allen `.ts`/`.tsx`-Dateien.

### 3.7 Test-Status
- Anzahl `.test.tsx` / `.test.ts` Dateien
- Vitest-Config: jsdom? Coverage?
- Letzter Run: grün / rot / hängt

---

## 4. ML-PIPELINE-STATUS (`code/ml/`)

### 4.1 Struktur-Tree
### 4.2 Modelle: was ist implementiert? Was fehlt?
### 4.3 Training: gibt es einen lauffähigen Train-Loop?
### 4.4 ONNX-Export: funktioniert der Export?
### 4.5 Offene TODOs

---

## 5. INFRASTRUKTUR-STATUS

### 5.1 Docker
- `docker-compose.yml`: alle Services definiert? Health-Checks?
- `Dockerfile`s: Backend, Frontend, Hermes — alle vorhanden?
- `.dockerignore`?

### 5.2 CI/CD
- `.github/workflows/ci.yml`: Jobs definiert? Laufen sie grün?
- `.github/workflows/local_smoke.yml`?

### 5.3 Hermes / Local AI
- `hermes/config.toml`: korrekt?
- Skills in `hermes/skills/`: welche existieren? Welche fehlen?

---

## 6. DOKUMENTATIONS-STATUS

### 6.1 Root-Level MD-Dateien
Für jede `.md` im Root:
- Name, Zweck, Letztes Update, Status

### 6.2 ADRs (`regulatory/adr/`)
- Welche ADRs existieren? Welche fehlen aus der Architektur?

### 6.3 Memory-Struktur
- `memory/runs/`: wie viele Logs? Letzter Eintrag?
- `memory/anomalies/`: leer oder befüllt?
- `memory/decisions/`: leer oder befüllt?

---

## 7. OFFENE PUNKTE & TECHNISCHE SCHULDEN (Priorisiert)

### 7.1 🔴 KRITISCH (Blockiert Demo / Funktionalität)
Liste alle Issues, die das System momentan unbenutzbar machen würden.

### 7.2 🟡 HOCH (Blockiert P0f / Rohde-Meeting)
Liste alle Issues, die für den Production-Demo-Pivot nötig sind.

### 7.3 🟢 MITTEL (P1-Readiness)
Liste alle Issues, die für P1 (Ethikantrag) nötig sind.

### 7.4 🔵 NIEDRIG (Nice-to-have)
Liste Verbesserungen, die warten können.

---

## 8. NÄCHSTE SCHRITTE (Empfohlene Reihenfolge)

Gib eine nummerierte Liste der nächsten 10 Tasks, priorisiert nach:
1. Abhängigkeiten (was blockiert was)
2. P0f-Ziel (Production-Demo für Rohde)
3. Aufwand vs. Impact

Für jeden Task:
```yaml
id: NEXT-001
title: "..."
priority: CRITICAL/HIGH/MEDIUM/LOW
blocked_by: []  # oder Liste von Task-IDs
blocks: []      # oder Liste von Task-IDs
estimated_effort: XS/S/M/L/XL  # T-Shirt-Size
files_to_touch: []  # Liste von Dateipfaden
acceptance_criteria: []
```

---

## 9. ARCHITEKTUR-LÜCKEN

Vergleiche den aktuellen Code mit der Spec aus `05_DECISION_TREE_HARVESTING.md`, `04_MASTER_PLAN.md`, und `AGENTS.md`. Welche Features sind spezifiziert aber NICHT implementiert?

---

## 10. TEST-GAP-ANALYSE

Welche Module / Funktionen haben **keine** Tests? Liste sie pro Layer:
- Backend-Services
- API-Routes
- Frontend-Komponenten
- ML-Module
- Utilities / Scripts

---

**AUSGABE-REGEL:**
- Schreibe die Datei `COPILOT_STATUS_REPORT.md` ins Projekt-Root.
- Verwende YAML-Code-Blocks für strukturierte Daten.
- Sei ehrlich: wenn etwas schlecht aussieht, schreib es auf.
- Keine Auslassungen mit "..." — entweder vollständig oder `NEEDS_REVIEW`.

--- PROMPT END ---
