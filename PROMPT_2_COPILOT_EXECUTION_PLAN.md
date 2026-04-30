# PROMPT 2 — Copilot Plan Mode: Vollständiger Implementierungs-Plan

> **STATUS:** Dies ist ein VORAB-ENTWURF basierend auf dem aktuellen Wissensstand. Er wird verfeinert, sobald `COPILOT_STATUS_REPORT.md` von Prompt 1 vorliegt.
> 
> **Anweisung für Lou:** Führe erst Prompt 1 aus. Wenn Kimi den Report gesehen hat, wird dieser Prompt 2 hier aktualisiert. DANN kopiere den finalen Prompt 2 in Copilot.

--- PROMPT START ---

# Aufgabe: Implementiere ALLE offenen Punkte aus COPILOT_STATUS_REPORT.md

Du hast soeben den `COPILOT_STATUS_REPORT.md` gelesen. Deine Aufgabe ist es, einen schrittweisen Implementierungsplan zu erstellen und ihn dann DATEI FÜR DATEI auszuführen.

## Phase 0: Setup (5 Min)

1. Lese `AGENTS.md` im Projekt-Root
2. Lese `CLAUDE.md` im Projekt-Root
3. Lese `COPILOT_STATUS_REPORT.md`
4. Prüfe Git-Status: `git status`
5. Erstelle Branch: `git checkout -b feat/p0f-complete`

## Phase 1: Kritische Blocker 🔴 (Sofort)

Arbeite die 🔴 KRITISCH-Einträge aus dem Report ab. Für jeden:
- Analysiere Root-Cause
- Implementiere Fix
- Schreibe / Update Test
- Verifiziere: `npm run typecheck` (Frontend) bzw. `pytest` (Backend)
- Commit mit Conventional-Commit-Message

## Phase 2: P0f-Demo-Completion 🟡 (Parallel wo möglich)

Arbeite die 🟡 HOCH-Priorität-Einträge ab. Nutze maximale Parallelität:

### Track A: Frontend (eigener Plan-Tab)
- Alle Platzhalter-UI-Elemente durch echte Implementation ersetzen
- Cornerstone3D-Rendering-Pipeline vervollständigen
- Patient-List mit Demo-Daten füllen
- Walkthrough data-tour-id Attribute auf allen Ziel-Elementen

### Track B: Backend (eigener Plan-Tab)
- Fehlende API-Endpunkte implementieren
- Demo-Token-System vervollständigen (`/demo/whoami`, `/demo/validate`)
- Anonymisierungs-Pipeline End-to-End testen

### Track C: Tests (eigener Plan-Tab)
- Test-Gaps schließen
- Frontend: Vitest stabilisieren (jsdom + WASM-Issue)
- Backend: pytest auf 100% Coverage für Patientendaten-Pfade

## Phase 3: Integration & Smoke-Test

1. `docker compose up --build` laufen lassen
2. Alle Health-Checks prüfen
3. End-to-End Flow testen:
   - Login mit Demo-Token
   - DICOM-Upload
   - Inferenz
   - Heatmap-Anzeige
   - Decision-Tree-Submit
4. `npm run typecheck` + `npm run lint` + `pytest` — alle grün?

## Phase 4: Finalisierung

1. Run-Log schreiben: `memory/runs/2026-04-30_copilot_p0f_complete.md`
2. `CLAUDE.md` aktualisieren (Phase-Status)
3. `AGENTS.md` aktualisieren (neue Anomalien / Fixed-List)
4. Commit & Push
5. PR erstellen oder direkt auf `master` mergen

---

## HARD RULES (niemals brechen)

1. **Local-First:** Kein Cloud-API-Call für Patientendaten. Nie.
2. **TypeScript strict:** `npm run typecheck` muss grün sein nach jeder Änderung.
3. **Tests:** Jeder Fix braucht einen Test. Jede neue Feature braucht Tests.
4. **i18n:** Keine hartkodierten deutschen Strings. Alles über `t('key')`.
5. **Memory-Disziplin:** Nach jeder Session Run-Log in `memory/runs/`.
6. **Commit-Messages:** Englisch, imperativ, Conventional Commits (`feat:`, `fix:`, `test:`).

--- PROMPT END ---
