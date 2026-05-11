# Carotis-AI Compress Harness Input - 2026-05-02

## Zweck

Operative Eingabe fuer den frisch installierten Skill `compress`.
Ziel: Carotis-AI Memory- und Runbook-Prosa tokenarm machen, ohne Kern-Memorys, Code, Config, Secrets, Patientendaten oder Office-Artefakte zu veraendern.

Hinweis: `executed-as-plan` bedeutet hier: als Harness-Regel ausgearbeitet und fuer spaetere Ausfuehrung freigegeben. In dieser Session wurde keine Kern-Memory-Datei komprimiert und kein `.original.md` Backup erzeugt.

## Konkrete Compress-Aufgaben

| Nr. | Aufgabe | Status | Ergebnis / Artefakt |
|---:|---|---|---|
| 1 | `CLAUDE.md` als Kern-Memory klassifizieren. | `executed-as-plan` | Nur Summary-Datei erzeugen, z.B. `memory/domain/claude_compressed_summary_YYYY-MM-DD.md`; kein Overwrite ohne Lou-Freigabe. |
| 2 | `MEMORY.md` als Index schuetzen. | `executed-as-plan` | Nicht direkt komprimieren; nur veraltete, lange Abschnitte in separatem Index-Summary spiegeln. Links und Pfade bleiben exakt. |
| 3 | `ULTRAPLAN.md` als Preflight-Kern schuetzen. | `executed-as-plan` | Erst Summary fuer Agenten-Input erstellen; Original bleibt Quelle der Wahrheit, weil Stop-Regeln, Tool-Matrix und Anomalien exakt bleiben muessen. |
| 4 | `AGENTS.md` und `01_HARNESS.md` als Steuerdateien markieren. | `executed-as-plan` | Keine direkte Kompression im Normalbetrieb; nur komprimierte Lesefassung, wenn Token-Budget knapp ist. |
| 5 | `RUNBOOK_TODAY.md`, `deploy/*.md` und operative Runbooks pruefen. | `executed-as-plan` | Komprimierbar, wenn stabil und rein prose-lastig; bei aktiven Deploy-Runbooks zuerst `*_summary.md`, danach optional Overwrite mit Auto-Backup. |
| 6 | Alte Run-Logs in `memory/runs/*.md` batch-faehig machen. | `executed-as-plan` | Kandidaten: aelter als letzte 3 Logs, abgeschlossen, keine offenen Secrets/Blocker. Ziel: 150-300 Woerter pro Run oder 40-60 Prozent Token-Reduktion. |
| 7 | Letzte 3 Run-Logs vom Overwrite ausschliessen. | `executed-as-plan` | Sie bleiben Preflight-Rohkontext. Nur kurze Sammel-Summary erlaubt, z.B. `memory/domain/recent_runs_summary_YYYY-MM-DD.md`. |
| 8 | Domain-Memorys in `memory/domain/*.md` staffeln. | `executed-as-plan` | `project_status_p0.md`, `project_carotis.md`, `user_role.md`, `fb_local_first.md`, `fb_office_docs.md` zuerst als Summary kopieren; Overwrite nur nach Review. |
| 9 | Anomalien in `memory/anomalies/*.md` konservativ behandeln. | `executed-as-plan` | Keine direkte Kompression bei Bug-/Safety-Regeln. Falls noetig: Summary mit Bug-IDs, Fixes, Codebloecken und Anti-Patterns exakt erhalten. |
| 10 | Backup- und Token-Budget-Regel festlegen. | `executed-as-plan` | Skill-Backup ist `<filename>.original.md`; nie Backups erneut komprimieren. Preflight-Input-Ziel: Kernkontext unter 6k Tokens, einzelne Summaries unter 800 Tokens. |

## Preflight-Integration

- Vor jedem `compress`-Einsatz `C:\Users\tubbeTEC\.codex\skills\compress\SKILL.md` lesen und Ziel-Dateiendung pruefen.
- Vor Overwrite Zielklasse setzen: `core-memory`, `run-log`, `runbook`, `briefing`, `archive`; Core-Memorys nur Summary.
- Vor Batch-Lauf `rg` auf bestehende `.original.md` Backups und letzte 3 Run-Logs pruefen; Backups und aktuelle Logs skippen.
- Nach Kompression Links, Backticks, Codebloecke, Pfade, Commands, Daten, Versionen und Tabellenstruktur gegen das Original pruefen.
- Wenn Write-Set eingeschraenkt ist, keine `tasks.jsonl`, `MEMORY.md` oder Run-Log-Aenderung erzwingen; Konflikt im Abschluss nennen.

## Anti-Patterns

1. `compress` auf `.py`, `.ts`, `.tsx`, `.js`, `.json`, `.env`, `.docx` oder andere Code-/Config-Dateien anwenden.
2. `CLAUDE.md`, `MEMORY.md`, `ULTRAPLAN.md`, `AGENTS.md` oder `01_HARNESS.md` im ersten Schritt ueberschreiben.
3. Backups wie `*.original.md` erneut komprimieren oder als neue Quelle der Wahrheit behandeln.
4. Codebloecke, Inline-Code, URLs, Dateipfade, Commands, Versionen oder medizinische/regulatorische Begriffe umschreiben.
5. Dateien mit Patientendaten, Secrets, Tokenwerten, Mailversand-Inhalten oder aktiven Office-Artefakten in den Compress-Flow geben.

## Sichere Kompressions-Policy Fuer Dieses Repo

Erlaubt: reine Prosa-Dateien mit `.md`, `.txt`, `.typ`, `.typst`, `.tex` oder ohne Extension, sofern sie keine Patientendaten oder Secrets enthalten.

Tabu: `.py`, `.ts`, `.tsx`, `.js`, `.json`, `.jsonl`, `.env`, `.docx`, `.yaml`, `.yml`, `.toml`, `.lock`, `.css`, `.html`, `.xml`, `.sql`, `.sh`, Binary-Dateien, DICOM, Modelle, Screenshots und Office-Exports.

Kern-Memorys: `CLAUDE.md`, `MEMORY.md`, `ULTRAPLAN.md`, `AGENTS.md`, `01_HARNESS.md`, `tasks.jsonl`. Fuer diese Dateien gilt: erst Kopie oder Summary, kein Overwrite im normalen Harness-Lauf.

Backup-Regel: Wenn Overwrite explizit freigegeben ist, erzeugt `compress` automatisch `<filename>.original.md`. Dieses Backup bleibt human-readable, wird nicht komprimiert und nicht geloescht.

Token-Budget: Preflight soll die operative Wahrheit erhalten, aber knapp bleiben. Zielwerte: Kern-Summary <= 800 Tokens pro Datei, Run-Log-Summary <= 300 Tokens pro Run, kompletter Harness-Input <= 6k Tokens.
