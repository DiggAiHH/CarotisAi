---
name: project_status_p0
description: Aktueller Phasenstatus P0 - Stakeholder-Approval (Rohde), Office-Doc-Update, Floy-Recherche-Abschluss.
type: project_status
last_updated: 2026-05-01
phase: P0f
---

# Status P0f - Stakeholder + Demo-Deploy

## Goal

Prof. Dr. med. Stefan Rohde soll ein belastbares Stakeholder-Paket bekommen: Office-Dokumente v2, Live-Demo-Hinweis, Rohde-Anleitung, Video-Skript und eine synthetische Local-First-Demo ohne Patientendaten.

## Status

| Komponente | Status | Block |
|------------|--------|-------|
| Engineering-Harness erstellt | done | - |
| Stride-Prompts A-H geschrieben | done | - |
| Office-Docs v2 | done | `Stride V2/` |
| Floy/Marktanalyse v2 | done | `Stride V2/KI_Tools_Marktanalyse_v2.pdf` |
| Konzept v2 | done | `Stride V2/Carotis_AI_Konzept_v2.docx` |
| Mail-Plaintext-Backup | done | `Mail_Aroob_an_Rohde_DRAFT.txt` |
| V3 Mail-/Office-Prompts | done | `Stride V3/` |
| Rohde-E2E + Pre-Send-Runbook | done | `deploy/runbook_pre_send.md` |
| Live-Deploy | blocked | `FLY_API_TOKEN`, Hetzner SSH, DNS/Fly-App |
| Mail an Rohde | human pending | wartet auf Versandentscheidung nach Demo-Unblock |
| Termin im Kalender | blocked | wartet auf Rohde-Antwort |

## Aktive Risiken

| Risiko | Status | Mitigation |
|--------|--------|------------|
| Deploy nicht live | extern blockiert | `deploy/runbook_pre_send.md` + GitHub Actions nach Secret/SSH/DNS |
| Office-Output halluziniert klinische Fakten | reduziert | Aroob-Review-Pflicht + Stride-Prompts statt direkter Doc-Edits |
| Echte Patientendaten landen in Demo | nicht erlaubt | nur synthetische DICOMs, Local-First-Regel, Runbook-Check |

## Next Concrete Steps for Lou

1. `deploy/runbook_pre_send.md` durchgehen.
2. Externe Deploy-Blocker loesen: Fly Token, Hetzner SSH-Key, DNS/Fly-App.
3. Nach Live-Smoke: Aroob final review + Mail v3 versenden.
4. Bei Rohde-Antwort: `memory/runs/2026-04-30_t012_rohde_reply_kit.md` nutzen.

## When P0f -> P1

- Erst nach Rohde-Go oder konkreter Rohde-Bedingung.
- Dann Opus-Session mit Template 1: P1 atomar planen.
- Diese Datei archivieren und `project_status_p1.md` neu anlegen.
- `CLAUDE.md` Phase-Status aktualisieren.
