---
name: 2026-04-30_Kimi_K26-Run02_ultraplan_harness_v3
type: run
---

## Goal
ULTRAPLAN v3 erstellen — "Harness The Whole Knowledge" aus der Session. Tool-Matrix, Anti-Patterns, E2E-Lessons, Skills-Inventar, Memory-Disziplin.

## Done
- ULTRAPLAN.md v3 geschrieben (615 -> 820+ Zeilen). 18 Sektionen.
- Tool-Matrix (4.1-4.9): Shell, ReadFile, WriteFile, StrReplaceFile, Grep, Glob, Agent, gh, MCP/Playwright
- Tool-Anti-Patterns (§5): 11 Anti-Patterns mit Warum + Stattdessen
- E2E-Test-Wissen (§12): Env-Setup vor Import, Mock-Service, ASGITransport, Unique Tokens, DecisionTreeRequest Schema exakt, Audit dual-auth
- Skills-Inventar komplett: 40+ Skills in 8 Kategorien + 3 MCP-Connectors
- Anomalien-Register erweitert: A-01..A-12 (A-10 sklearn, A-11 UNIQUE case_id, A-12 vulnerability_markers keys)
- Memory-Disziplin formalisiert: 5-Zeilen-Run-Log, Pfad-Konvention, MEMORY.md Update-Regel
- S1-S17 Completion Tabelle in §18 dokumentiert

## Surprised by
- `decision_trees.case_id` hat UNIQUE-Constraint — Cross-Test-Fehler wenn verschiedene Testdateien denselben case_id verwenden.
- `vulnerability_markers` required 4 spezifische Keys — leeres Dict `{}` fuehrt zu 422.
- PowerShell `$PWD/.venv` als Expression bricht wegen `/` als Operator, nicht als Pfad-Trenner.

## Avoided
- Secrets in ULTRAPLAN.md (nur Secret-Namen, nie Werte)
- Veraltete Info aus v2 (Linux-style `bin/` in venv wurde bereinigt)
- Nicht alle 40 Skills detailliert beschreiben (nur Tabelle, keine Duplikation von SKILL.md)

## Next
- AGENTS.md und MEMORY.md mit v3-Referenz aktualisieren
- Run-Log Pointer in MEMORY.md setzen
