---
name: recent_runs_summary_2026-05-02
type: compact_memory
phase: P0f
mode: summary-first
---

# Recent Runs Summary 2026-05-02

## Stand

- Run08 installierte 5 Codex-Skills: `browser-harness`, `caveman`, `compress`, `obsidian`, `remotion-best-practices`.
- Run09 operationalisierte die Skills per Subagent-Team: 50 Aufgaben, Detaildateien, zentrale Matrix, Preflight-Integration.
- Run10 baute ein Operating Board und `scripts/check_codex_skills.ps1`; 5/5 Skill-Dateien vorhanden, `browser-harness` nicht auf PATH in aktueller Shell.

## Aktive Regeln

- Core-Memorys nicht ueberschreiben: `CLAUDE.md`, `MEMORY.md`, `ULTRAPLAN.md`, `AGENTS.md`, `01_HARNESS.md`.
- Memory-Verdichtung nur Summary-first.
- Browser/Provider/Vault Default read-only, bis eine konkrete sichere Aktion noetig ist.
- Keine Patientendaten, Roh-DICOMs, echten klinischen IDs oder Secrets in Dateien/Logs.
- Run-Log und `MEMORY.md` Pointer bleiben Pflicht.

## Jetzt Relevant

- User meldet: Standard-SSH-Key sei gesetzt.
- User lieferte weitere Zugangsdaten im Chat; diese duerfen nicht in Dateien, Outputs oder Run-Logs persistiert werden.
- Naechster technischer Pfad: lokale Secret-Surface bereinigen, SSH/GitHub/Workflow/Health pruefen, danach Frontend/Backend Smoke.

## Next

1. `add_ssh_key.py` secretfrei halten.
2. Secret-Scan ausfuehren.
3. SSH-Key-Zugang zu Hetzner pruefen.
4. GitHub Actions / Deploy-Workflows pruefen.
5. Online-Health und lokaler Visual-Smoke durchfuehren.

## Run11 Update

- Memory wurde summary-first verdichtet, kein Core-Overwrite.
- Frontend ist live und visueller Chromium-Smoke ist gruen.
- Backend-Smoke lokal ist gruen: `tests/test_smoke.py` 6/6.
- Backend online bleibt blockiert: SSH-Key-Auth gegen Hetzner verweigert, Deploy-Workflow failt an `Prepare Hetzner host`.
- Lokale Secret-Dateien wurden sanitisiert; keine neuen Secrets persistiert.
