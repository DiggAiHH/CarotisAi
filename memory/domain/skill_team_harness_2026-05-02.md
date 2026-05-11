---
name: skill_team_harness_2026-05-02
type: domain_memory
phase: P0f
status: active
source_run: memory/runs/2026-05-02_Codex_GPT55-Run09_skill_team_harness.md
---

# Skill-Team Harness 2026-05-02

## Zweck

Die am 2026-05-02 installierten Codex-Skills werden nicht nur als Liste gehalten, sondern als operative Agenten-Rollen genutzt. Dieses Dokument ist die zentrale Matrix fuer Carotis-AI: welcher Skill wann eingesetzt wird, welche 10 Aufgaben je Skill erledigt wurden, welche Stop-Regeln gelten und welche Detaildatei weiterfuehrt.

Ausfuehrungsstatus: `executed-as-plan` bedeutet: Aufgabe wurde als Harness-Regel, Artefakt oder Checkliste ausgearbeitet und in Projekt-Memory integriert. Echte Provider-Aenderungen, Vault-Writes, Video-Scaffolds und Kompression von Kern-Memorys wurden bewusst nicht ausgefuehrt.

## Team-Matrix

| Skill | Rolle im Harness | Detaildatei |
|---|---|---|
| `browser-harness` | Sichtbare UI-/Provider-/Claude-Design-Verifikation, read-only zuerst | `memory/domain/skill_harness_browser_2026-05-02.md` |
| `caveman` | Tokenarme Status-, Triage-, Handoff- und Run-Log-Kommunikation | `memory/domain/skill_harness_caveman_2026-05-02.md` |
| `compress` | Sichere Prosa-Kompression via Summary-first Policy | `memory/domain/skill_harness_compress_2026-05-02.md` |
| `obsidian` | Lokale Notizstruktur, Search, Backlinks, Vault-Sync-Planung | `memory/domain/skill_harness_obsidian_2026-05-02.md` |
| `remotion-best-practices` | Lokaler Rohde-Demo-Video-Plan mit framebasiertem Timing | `memory/domain/skill_harness_remotion_2026-05-02.md` |

## Browser-Harness Aufgaben

| # | Aufgabe | Status | Ergebnis |
|---|---|---|---|
| 1 | Lokalen Demo-Smoke gegen `localhost:3000` planen | `executed-as-plan` | Screenshot-Gate fuer Auth/App-Zustand definiert |
| 2 | AuthGate ohne Token-Leak pruefen | `executed-as-plan` | Fehlerzustand ohne Backend als erwartbar dokumentiert |
| 3 | Desktop/Mobile Viewports pruefen | `executed-as-plan` | 1280x720 und 375x667 als Baseline gesetzt |
| 4 | Claude-Design-Prototype read-only oeffnen | `executed-as-plan` | Generation-Signale und Tweaks-Panel-Regel uebernommen |
| 5 | Prototype Tabs durchklicken | `executed-as-plan` | Patients/Viewer/AI als UI-Smoke definiert |
| 6 | Fly.io UI read-only pruefen | `executed-as-plan` | Stop bei Token/Login/Deploy-Aktion festgelegt |
| 7 | Hetzner UI read-only pruefen | `executed-as-plan` | Canvas-Konsole nur mit explizitem Human-Go |
| 8 | INWX DNS read-only pruefen | `executed-as-plan` | Fehlende Records als manuelle Aktion notieren |
| 9 | Rohde-Screenshot-Harvest planen | `executed-as-plan` | Start, Viewer, Grad-CAM, AI Panel, Decision Capture |
| 10 | Domain-Skill-Capture einbauen | `executed-as-plan` | URL-Pattern, Waits, UI-Traps, keine Secrets |

## Caveman Aufgaben

| # | Aufgabe | Status | Ergebnis |
|---|---|---|---|
| 1 | Status auf 3 Zeilen verdichten | `executed-as-plan` | `Stand / Blocker / Next` |
| 2 | Run-Log-Kurzform nutzen | `executed-as-plan` | 5-Zeilen-Log bleibt Pflicht |
| 3 | Deploy-Blocker knapp melden | `executed-as-plan` | `Blocker / Owner / Next` |
| 4 | Error-Triage komprimieren | `executed-as-plan` | `Symptom / Cause / Fix / Verify` |
| 5 | Task-DoD knapp formulieren | `executed-as-plan` | Files, Tests, Security, Handoff |
| 6 | Memory-Dichte erhoehen | `executed-as-plan` | Max. 5 stabile Fakten je Notiz |
| 7 | Parallel-Handoff schreiben | `executed-as-plan` | `Touched / Not touched / Risk / Next owner` |
| 8 | Test-Failure-Update standardisieren | `executed-as-plan` | Failing test, suspected area, next command |
| 9 | Security-Hinweise entkomprimieren | `executed-as-plan` | Vollsatz-Warnungen bleiben klar |
| 10 | User-Updates kuerzen | `executed-as-plan` | 1-2 Saetze mit Kontext und naechstem Schritt |

## Compress Aufgaben

| # | Aufgabe | Status | Ergebnis |
|---|---|---|---|
| 1 | `CLAUDE.md` schuetzen | `executed-as-plan` | Summary-first, kein Overwrite ohne Freigabe |
| 2 | `MEMORY.md` schuetzen | `executed-as-plan` | Index bleibt Quelle der Wahrheit |
| 3 | `ULTRAPLAN.md` schuetzen | `executed-as-plan` | Stop-Regeln nicht automatisch verdichten |
| 4 | `AGENTS.md`/`01_HARNESS.md` schuetzen | `executed-as-plan` | Nur Lesefassung bei Tokenknappheit |
| 5 | Runbooks klassifizieren | `executed-as-plan` | Aktive Runbooks erst als `*_summary.md` |
| 6 | Alte Run-Logs batch-faehig machen | `executed-as-plan` | Nur abgeschlossene, alte Logs |
| 7 | Letzte 3 Run-Logs ausschliessen | `executed-as-plan` | Rohkontext bleibt unveraendert |
| 8 | Domain-Memorys staffeln | `executed-as-plan` | Erst Summary, dann Review |
| 9 | Anomalien konservativ behandeln | `executed-as-plan` | Bug-IDs/Fixes exakt erhalten |
| 10 | Backup-/Token-Budget-Regel setzen | `executed-as-plan` | `<file>.original.md`, Summaries < 800 Tokens |

## Obsidian Aufgaben

| # | Aufgabe | Status | Ergebnis |
|---|---|---|---|
| 1 | Vault-Pfad feststellen | `executed-as-plan` | Pfade immer quoten |
| 2 | Vault-Sync planen | `executed-as-plan` | `source -> target -> backlinks -> safety-check` |
| 3 | Run-Logs verlinken | `executed-as-plan` | `[[project_status_p0]]`, Task-ID, ULTRAPLAN |
| 4 | P0f-Notizen konsolidieren | `executed-as-plan` | Deploy, Rohde, Mail, Human-Action |
| 5 | Rohde-Kontext backlinken | `executed-as-plan` | Meeting-Kit, Runbook, Status |
| 6 | Deploy-Kontext backlinken | `executed-as-plan` | Checklist, Runbook, ULTRAPLAN |
| 7 | Anomalien-Kontext backlinken | `executed-as-plan` | Anomalien-Index und konkrete Dateien |
| 8 | Search vor New Note erzwingen | `executed-as-plan` | `rg` plus Vault-Search |
| 9 | Wikilinks pruefen | `executed-as-plan` | Keine orphan links fuer zentrale Knoten |
| 10 | Vault-Sicherheitscheck anwenden | `executed-as-plan` | Keine Patientendaten, Secrets, Roh-DICOMs |

## Remotion Aufgaben

| # | Aufgabe | Status | Ergebnis |
|---|---|---|---|
| 1 | 3-Minuten-Rohde-Video planen | `executed-as-plan` | 180s Narrative definiert |
| 2 | 30fps Timing setzen | `executed-as-plan` | 5400 Frames als Baseline |
| 3 | Sequence-Plan erstellen | `executed-as-plan` | `from` + `durationInFrames` je Szene |
| 4 | CSS-Animationen verbieten | `executed-as-plan` | Nur Remotion framebasiert |
| 5 | Asset-Regel setzen | `executed-as-plan` | Lokal in `public/`, via `staticFile()` |
| 6 | One-frame-render-check aufnehmen | `executed-as-plan` | Frame 30 plus Keyframes |
| 7 | Captions lokal planen | `executed-as-plan` | JSON-Captions, keine Cloud-Transkription |
| 8 | Audio lokal planen | `executed-as-plan` | Lokale Voiceover/Audio-Spur |
| 9 | Datenschutz fixieren | `executed-as-plan` | Nur synthetische/anonymisierte Demo-Assets |
| 10 | Rohde-Review-Output definieren | `executed-as-plan` | Klinische Frage, XAI, Local-First, Go |

## Preflight-Regeln

1. Skill-Team erst nach Standard-Preflight aktivieren: `ULTRAPLAN.md`, `CLAUDE.md`, `AGENTS.md`, `MEMORY.md`, letzte 3 Run-Logs, Anomalien, Git.
2. Pro Skill zuerst die Detaildatei lesen, dann die installierte `SKILL.md`, dann handeln.
3. Browser/Obsidian/Provider-Arbeit ist read-only, bis der User konkrete Schreib- oder Provider-Aktion erlaubt.
4. `compress` nutzt Summary-first fuer Kern-Memorys; kein automatisches Overwrite von `CLAUDE.md`, `MEMORY.md`, `ULTRAPLAN.md`, `AGENTS.md`, `01_HARNESS.md`.
5. Remotion bleibt Planungs-/Video-Skill bis eigener Implementierungsauftrag existiert; kein Scaffold, kein `npm install`, kein Render ohne Freigabe.

## Stop-Regeln

- Stop bei Patientendaten, Roh-DICOMs, echten klinischen IDs, Tokenwerten, Credentials, 2FA, Login-Walls, Provider-Billing, DNS-Save, Deploy-Trigger oder unklarem externem Vault-Pfad.
- Stop bei medizinisch/regulatorischen Entscheidungen, wenn Caveman-Kompression Aussage oder Verantwortung verkuerzt.
- Stop bei Kern-Memory-Kompression, wenn keine explizite Freigabe fuer Overwrite vorliegt.
