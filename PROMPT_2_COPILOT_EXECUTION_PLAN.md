# PROMPT 2 - Copilot Plan Mode: Vollstaendiger Implementierungs-Plan

> STATUS: FINALISIERT - `COPILOT_STATUS_REPORT.md` liegt vor.
>
> Anweisung fuer Lou: `COPILOT_STATUS_REPORT.md` im Projekt-Root oeffnen und als Kontext in Copilot laden, dann diesen Prompt ausfuehren.

--- PROMPT START ---

# Aufgabe: Implementiere ALLE offenen Punkte aus COPILOT_STATUS_REPORT.md

Du hast soeben den `COPILOT_STATUS_REPORT.md` gelesen. Deine Aufgabe ist es, einen schrittweisen Implementierungsplan zu erstellen und ihn dann DATEI FUER DATEI auszufuehren.

## Phase 0: Setup

1. Lies `AGENTS.md` im Projekt-Root.
2. Lies `CLAUDE.md` im Projekt-Root.
3. Lies `COPILOT_STATUS_REPORT.md`.
4. Lies `REPO_CLEANUP_AND_DEPLOY_HANDOFF.md`.
5. Pruefe Git-Status: `git status`.
6. Pruefe Remote: `git remote -v` muss auf ein Carotis-only Repo zeigen, niemals auf Anamnese.
7. Erstelle Branch: `git checkout -b feat/p0f-complete`.

## Phase 1: Kritische Blocker

Arbeite die KRITISCH-Eintraege aus dem Report ab. Fuer jeden:

- Analysiere Root-Cause.
- Implementiere Fix.
- Schreibe oder aktualisiere Test.
- Verifiziere: `npm run typecheck` fuer Frontend bzw. `pytest` fuer Backend.
- Commit mit Conventional-Commit-Message.

## Phase 2: P0f-Demo-Completion

Arbeite die HOCH-Prioritaet-Eintraege ab. Nutze maximale Parallelitaet mit disjunkten Dateien.

### Track A: Frontend auf Fly.io

- Alle Platzhalter-UI-Elemente durch echte Implementation ersetzen.
- Cornerstone3D-Rendering-Pipeline vervollstaendigen.
- Patient-List mit Demo-Daten fuellen.
- Walkthrough `data-tour-id` Attribute auf allen Ziel-Elementen.
- Deploy-Ziel: Fly.io, Domain `carotis.diggai.de`.
- Keine Netlify- oder Render-Konfiguration verwenden.

### Track B: Backend auf Hetzner

- Fehlende API-Endpunkte implementieren.
- Demo-Token-System vervollstaendigen (`/demo/whoami`, `/demo/validate`, falls Report es fordert).
- Anonymisierungs-Pipeline End-to-End testen.
- Deploy-Ziel: Hetzner, Domain `api.carotis.diggai.de`.
- Deployment-Ordner auf Hetzner: `/opt/carotis-ai`.
- Nicht in den Anamnese-Stack deployen.

### Track C: Tests

- Test-Gaps schliessen.
- Frontend: Vitest stabilisieren.
- Backend: pytest fuer Patientendaten-Pfade ausbauen.
- Keine Tests entfernen, nur weil sie langsam oder unbequem sind.

## Phase 3: Integration & Smoke-Test

1. Lokal: `docker compose up --build` oder passendes Demo-Compose laufen lassen.
2. Alle Health-Checks pruefen.
3. End-to-End Flow testen:
   - Login mit Demo-Token
   - DICOM-Upload
   - Inferenz
   - Heatmap-Anzeige
   - Decision-Tree-Submit
4. Verifikation:
   - `npm run typecheck`
   - `npm run lint`
   - `npm test -- --run`
   - `pytest`

## Phase 4: Finalisierung

1. Run-Log schreiben: `memory/runs/2026-04-30_copilot_p0f_complete.md`.
2. `CLAUDE.md` aktualisieren.
3. `AGENTS.md` aktualisieren.
4. Commit & Push auf Feature-Branch.
5. PR erstellen; nicht direkt auf `master` mergen.

## HARD RULES

1. Local-First: Kein Cloud-API-Call fuer Patientendaten.
2. TypeScript strict: `npm run typecheck` muss gruen sein nach jeder Aenderung.
3. Tests: Jeder Fix braucht einen Test. Jede neue Feature braucht Tests.
4. i18n: Keine hartkodierten deutschen UI-Strings. Alles ueber `t('key')`.
5. Memory-Disziplin: Nach jeder Session Run-Log in `memory/runs/`.
6. Commit-Messages: Englisch, imperativ, Conventional Commits (`feat:`, `fix:`, `test:`).
7. Repo-Schutz: Carotis-AI muss ein eigenes GitHub-Repo haben. Nie ins Anamnese-Repo pushen.
8. Deploy-Ziel: Frontend auf Fly.io, Backend auf Hetzner. Netlify/Render nicht verwenden.
9. Secrets: Keine Tokens in Chat, Dateien oder Remote-URLs. Nur GitHub Secrets verwenden.

--- PROMPT END ---
