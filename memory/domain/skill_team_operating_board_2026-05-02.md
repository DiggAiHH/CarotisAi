---
name: skill_team_operating_board_2026-05-02
type: operating_board
phase: P0f
status: active
source: memory/domain/skill_team_harness_2026-05-02.md
---

# Skill-Team Operating Board 2026-05-02

## Zweck

Dieses Board macht aus der Skill-Team-Matrix eine laufende Arbeitssteuerung. Es priorisiert konkrete, sichere Runs fuer die naechsten Sessions. Default: read-only, keine Patientendaten, keine Secrets, keine Provider-Writes.

## Mission

P0f von "Dokumentiert" zu "Demo-ready Handoff" bringen:

1. Demo sichtbar pruefen.
2. Rohde-Material greifbar machen.
3. Memory/Runbook kurz halten.
4. Video-Asset vorbereiten, ohne Scaffold.
5. Provider-Blocker nur lesen, nicht veraendern.

## Lanes

| Lane | Skill | Zweck | Stop |
|---|---|---|---|
| Visual Verify | `browser-harness` | Screenshots, Claude Design, local demo | Login, Token, DNS Save, Deploy |
| Signal | `caveman` | Status, Handoff, Triage | Legal/Safety ambiguity |
| Memory Diet | `compress` | Summary-first compression planning | Core-memory overwrite |
| Knowledge Graph | `obsidian` | Backlinks and note map | External vault write |
| Rohde Video | `remotion-best-practices` | 3-min sequence plan | Scaffold/render without task |

## Next 15 Safe Runs

| Pri | Run | Skill | Output | Status |
|---:|---|---|---|---|
| 1 | Local frontend visual smoke | browser-harness | `artifacts/browser/demo_smoke_desktop.png` plan or screenshot | ready |
| 2 | Mobile visual smoke | browser-harness | `artifacts/browser/demo_smoke_mobile.png` plan or screenshot | ready |
| 3 | Claude Design read-only reconnect | browser-harness | Prototype status note | ready |
| 4 | Provider read-only blocker map | browser-harness | Fly/Hetzner/INWX visible-state checklist | ready |
| 5 | P0f 3-line status | caveman | `Stand / Blocker / Next` block in run-log | ready |
| 6 | Deploy blocker triage | caveman | `Blocker / Owner / Next / Stop` | ready |
| 7 | Recent run summary | compress | `memory/domain/recent_runs_summary_YYYY-MM-DD.md` | ready |
| 8 | Core-memory compression candidates | compress | candidate table, no overwrite | ready |
| 9 | Rohde backlink map | obsidian | local note draft with wikilinks | ready |
| 10 | P0f knowledge map | obsidian | backlinks between deploy, Rohde, runbooks | ready |
| 11 | Remotion scene lock | remotion-best-practices | final 5400-frame scene table | ready |
| 12 | Remotion asset manifest | remotion-best-practices | local-only asset list | ready |
| 13 | One-frame render checklist | remotion-best-practices | frame checkpoints 30/900/1560/... | ready |
| 14 | Skill availability check | local script | `scripts/check_codex_skills.ps1` output | done |
| 15 | Run-log pointer hygiene | caveman + obsidian | `MEMORY.md` pointer audit | ready |

## Execution Template

```markdown
## Skill Run
Skill:
Goal:
Inputs:
Allowed writes:
Stop conditions:
Output:
Verify:
Run-log pointer:
```

## Safety Gates

- Browser runs: start with new tab, read-only, screenshot after meaningful action.
- Obsidian runs: project search first, no external vault write without explicit user approval.
- Compress runs: summaries first, no overwrite of `CLAUDE.md`, `MEMORY.md`, `ULTRAPLAN.md`, `AGENTS.md`, `01_HARNESS.md`.
- Remotion runs: no `npm install`, no scaffold, no render unless task explicitly asks.
- Caveman runs: pause compression for security, DSGVO, MDR, clinical safety, irreversible actions.

## Today Board

| Item | Owner | Status | Note |
|---|---|---|---|
| Skill availability check | Codex | done | `scripts/check_codex_skills.ps1` added |
| Skill availability result | Codex | done | 5/5 `SKILL.md` present; `browser-harness` command not on PATH in current shell |
| Operating board | Codex | done | This file |
| Real visual smoke | next agent | pending | Needs running frontend/browser command |
| Recent run summary | next agent | pending | Summary-only, no overwrite |
| Rohde video implementation | blocked | pending | Needs explicit implementation task |
