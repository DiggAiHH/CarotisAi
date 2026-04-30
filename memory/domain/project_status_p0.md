---
name: project_status_p0
description: Aktueller Phasenstatus P0 — Stakeholder-Approval (Rohde), Office-Doc-Update, Floy-Recherche-Abschluss. WIRD AKTUALISIERT bei Phasen-Wechsel; alte Versionen nach archive/.
type: project_status
last_updated: 2026-04-27
phase: P0
---

# Status P0 — Stakeholder + Office-Docs

## Goal

Termin mit Prof. Dr. med. Stefan Rohde (Klinikum Dortmund) bekommen. Bestehende Office-Dokumente sind auf das Klinikum-Setting umgestellt. Floy-Recherche und Carotis-AI-Konzept liegen Aroob fertig vor.

## Status

| Komponente | Status | Block |
|------------|--------|-------|
| Engineering-Harness erstellt (Files 00–08, CLAUDE, MEMORY, tasks.jsonl, memory/) | ✅ done | — |
| Stride-Prompts geschrieben (Prompts A–H in 07_OFFICE_AGENT_PROMPTS.md) | ✅ done | — |
| Mail-Plain-Text fertig (Mail_Aroob_an_Rohde_DRAFT.txt) | ✅ done | — |
| Lou's CV (Anlage 3) | ✅ done als Markdown — Lou rendert PDF | — |
| Office-Docs v2 (Stride-Output) | 🔄 läuft (T-001 bis T-008 in tasks.jsonl) | Lou muss Stride durchziehen |
| Aroob's Review aller v2-Docs (T-009) | 🔒 blocked | wartet auf v2-Docs |
| Mail an Rohde rausgeschickt (T-010) | 🔒 blocked | wartet auf Aroob's Review |
| Termin im Kalender (T-012) | 🔒 blocked | wartet auf Rohde's Antwort |
| Termin durchgeführt (T-013 + Demo) | 🔒 blocked | wartet auf Termin |

## Risks (aktiv)

| Risiko | Wahrscheinlichkeit | Schaden | Status |
|--------|---------------------|---------|--------|
| Rohde antwortet nicht binnen 7 Tagen | mittel | mittel | Erinnerung in Lou's Kalender für 2026-05-04 |
| Stride-Output halluziniert klinische Fakten | mittel | hoch | Aroob's Review-Pflicht (T-009) ist Mitigation |
| PowerPoint v2 Layout zerlegt | niedrig | mittel | Stride hat Slide-Master-Verständnis besser als python-pptx |

## Next Concrete Steps for Lou (jetzt)

1. `cat RUNBOOK_TODAY.md` — Schritt-für-Schritt-Anleitung was jetzt zu tun ist
2. Stride aufmachen, Prompt G durchziehen (Floy-Recherche v2)
3. Sequenziell weiter: H, C, D, E, F, B, A
4. Aroob's Review koordinieren
5. Mail rausschicken (T-010)

## When P0 → P1

- Sobald Rohde's Approval da ist (auch bedingt: "Ja, wenn ihr noch X liefert")
- Dann Opus-Session mit Template 1: "Plane P1 atomar"
- Diese Datei wird verschoben nach `memory/archive/` und `project_status_p1.md` neu angelegt
- `CLAUDE.md` Phase-Status-Tabelle aktualisiert
