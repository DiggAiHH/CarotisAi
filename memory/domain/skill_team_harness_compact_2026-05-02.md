# Skill-Team Harness Compact 2026-05-02

Neue Skills operationalisiert:

- `browser-harness`: Browser-/Provider-/Claude-Design-Verifikation. Default read-only. Stop bei Login, Token, DNS-Save, Deploy, Patientendaten.
- `caveman`: knappe Status-, Triage-, Handoff-, Run-Log-Kommunikation. Pausieren bei Security, Legal, MDR, DSGVO, Patientensafety.
- `compress`: Memory-Prosa verdichten. Core-Memorys nur Summary-first, kein Overwrite ohne Freigabe.
- `obsidian`: lokale Notizen, Search, Backlinks. Externe Vault-Writes nur mit Freigabe, keine Secrets/Patientendaten.
- `remotion-best-practices`: lokales Rohde-Demo-Video planen. 30fps, `Sequence`, `interpolate`, lokale Assets, keine CSS-Animationen, kein Scaffold ohne Auftrag.

Detailmatrix: `memory/domain/skill_team_harness_2026-05-02.md`.
Operating Board: `memory/domain/skill_team_operating_board_2026-05-02.md`.
Local Check: `powershell -ExecutionPolicy Bypass -File scripts/check_codex_skills.ps1`.

Preflight-Zusatz:

1. Standard-Preflight zuerst.
2. Passenden Skill + Detaildatei lesen.
3. Read-only starten.
4. Keine Patientendaten/Secrets/Provider-Writes.
5. Ergebnis in Run-Log + `MEMORY.md` verlinken.
