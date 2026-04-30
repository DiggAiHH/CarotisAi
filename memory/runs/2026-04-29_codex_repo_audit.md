---
name: 2026-04-29_codex_repo_audit
type: run
---

## Goal
Lokalen Carotis-AI Repo-Stand auditieren und die verbleibenden Implementierungsluecken fuer Trust, Simplicity, Completeness und Production-Readiness identifizieren.

## Done
- Pflichtkontext gelesen: `CLAUDE.md`, `MEMORY.md`, relevante Run-Logs und Anomaly-Memo.
- Ist-Stand in Frontend, Backend, Tests, CI, Deployment und Doku direkt aus dem Repo geprueft.
- Kritische Drift zwischen Memory/Handoffs und aktuellem Dateistand isoliert.
- Harte Checks verifiziert: `npm test -- --run` scheitert wegen fehlendem Script; lokales `pytest tests/test_smoke.py -q` scheitert in der aktuellen Umgebung an fehlendem `pydicom`; `.git` fehlt sowohl im Workspace-Root als auch unter `code/`.

## Surprised by
- Der Frontend-Code enthaelt zwei konkurrierende API-/Typen-/Panel-Stacks gleichzeitig (`AIPanel.tsx` vs `AiPanel/AiPanel.tsx`, `lib/apiClient.ts` vs `services/api.ts`, `types/api.ts` vs `types/index.ts`).
- `audit_service.py` ist zwar nicht mehr dupliziert, aber weiterhin auf ein altes Datenmodell verdrahtet und damit faktisch toter Code.
- Mehrere Backend-Pfade nutzen `Path(...).parents[4]`, was auf dem Host funktioniert, im Container aber sehr wahrscheinlich bricht.

## Avoided
- Keine Code-Aenderungen am Produktpfad.
- Kein breitflaechiges Re-Planning von bereits erledigten K-Tasks.
- Kein Web-Browsing ausser dem fuer den UI-Audit verpflichtenden Guideline-Fetch.

## Next
- Audit-Ergebnis an den User zur Priorisierung geben.
- Falls gewuenscht: zuerst Frontend-Vertragsbereinigung + CI/Test-Harness oder alternativ Deployment/Container-Fixes als kritischen Pfad abarbeiten.

## Memory updates
- `MEMORY.md` um diesen Run-Log-Pointer erweitert.
