---
name: harness_v1_kickoff
description: Initial Harness v1.0 erstellt für Carotis-AI; Office-Prompts geschrieben; Paper-Recherche M1
type: run
last_updated: 2026-04-27
---

# Session 2026-04-27 · Opus 4.7 (Cowork) · Harness v1.0 + Office-Prompts + Paper-Recherche

## Goal

Lou wechselt von Kimi K2.6 auf Opus 4.7. Der Auftrag:
1. Engineering-Harness für Carotis-AI bauen, analog Elbtronika (`Prompts & Engineering Harnessing/`)
2. Memory-System aufsetzen, mit dem Modelle Run-by-Run klüger werden
3. Decision-Tree-Harvesting als Innovation gegenüber bisherigen Carotis-CTA-Lösungen spezifizieren
4. Paper-Recherche zu Attention-Mechanism (seit 2020), insb. Carotis + CTA + XAI
5. Master-Plan v1.0 (analog Elbtronika v1.0)
6. Rohde-Meeting-Kit + Office-Agent-Stride-Prompts, damit Lou die bestehenden 7 Office-Files diese Woche aktualisieren kann

## Done

13 neue Dateien im `Carotis AI/` Workspace:
- `00_INDEX.md` — Single-Page-Einstieg
- `01_HARNESS.md` — Modell-Routing-Matrix, Pre-Flight, DoD, Memory-Hierarchie
- `02_ROADMAP.md` — Phasen P0–P7 (24-Monats-Plan)
- `03_PROMPT_TEMPLATES.md` — 9 Copy-Paste-Prompts (1 mehr als Elbtronika: Stakeholder-Communication als T9)
- `04_MASTER_PLAN.md` — v1.0-Plan mit Architektur-Diagramm + Stakeholder-Map + Risiken
- `05_DECISION_TREE_HARVESTING.md` — JSON-Schema, UI-Spec, Anonymisierungs-Pipeline, Trainings-Loss-Komponente, Daily-Loop
- `06_ROHDE_MEETING_KIT.md` — Kontaktstrategie, Agenda 30 Min, FAQ 1–10, Notfall-Plan
- `07_OFFICE_AGENT_PROMPTS.md` — 8 Stride-Prompts (A–H) mit Reihenfolge, Konvention, Run-Log-Pflicht
- `08_RESEARCH_ATTENTION_2020-2026.md` — 27+ Paper-Inventar, kategorisiert nach Foundation/ViT/Carotid/Reviews/Hybrid/Ultraschall/XAI/KAN
- `CLAUDE.md` — Working Memory, < 200 Zeilen
- `MEMORY.md` — Index aller Langzeit-Memorys
- `tasks.jsonl` — 13 atomare P0-Tasks (T-001 bis T-013)
- `memory/README.md` — Hierarchie-Beschreibung
- `memory/runs/2026-04-27_opus47_harness_v1.md` — diese Datei

## Surprised by

- Das alte "Prompts & Engineering Harnessing"-Verzeichnis ist nicht für Elbtronika, sondern bereits für `dr-aroob-ki` (das Frontend-Repo). Lou hat das in seiner Kommunikation nicht klar getrennt — er nennt beides "Elbtronika-Pattern". In Realität ist die Trennung: Elbtronika-Memory-Stil ist in der Kimi-CLAUDE.md, der Harness-Pattern selbst ist im dr-aroob-ki-Setup. Wir haben für Carotis-AI beides synthetisiert.
- Die Office-Dokumente von Stride sind teilweise schon gut — der Office-Agent hat das Decision-Tree-Harvesting noch nicht erfasst. Das ist die wichtigste Lücke, die jetzt durch Prompt H + Prompt C gefüllt wird.
- Prof. Rohde hat in Wirklichkeit nicht "Nein" gesagt, sondern "Ja unter Bedingung" (Hausaufgabe gegeben). Das ist ein viel besseres Verhandlungs-Setting, als die ursprüngliche Mail-Strategie annahm. Die Mail-Vorlage von Kimi war zu defensiv. Die jetzige (Prompt A) ist Engineering-selbstbewusst, ohne überheblich zu sein.

## Avoided

- Nicht direkt die `.docx` Files mit Python-docx editiert. Lou's Feedback (Memory `fb_office_docs.md`): Modelle dürfen Office-Diff nicht direkt schreiben, weil ein menschliches Review unmöglich ist. Stattdessen: Stride-Prompts, die Lou im UI ausführt und visuell prüft.
- Nicht versucht, `dr-aroob-ki` Repo direkt zu klonen oder zu editieren. Das ist eine separate Code-Base mit eigenem Lifecycle. Hier nur Pointer-Referenz.
- Nicht alle 27+ Papers gelesen. Nur Titel + Abstract der Top-10 (C1–C8 in Sektion 3 von `08_RESEARCH`). Detaillierte Methodik-Reads kommen in P1.
- Nicht die Decision-Tree-Loss-Implementation als Code geschrieben. Das ist eine P3-Aufgabe — hier nur die Spec.

## Next

**Diese Woche (Lou):**
1. T-001 bis T-008 ausführen (Stride-Prompts G, H, C, D, E, F, B, A in dieser Reihenfolge)
2. T-009: gemeinsamer Review mit Aroob
3. T-010: Aroob schickt Mail an Rohde raus
4. T-011: dieser Run-Log + ggf. erste `domain/` Files schreiben (user_role, project_carotis)

**Wenn Rohde antwortet (Lou + Aroob):**
5. T-012: Template 9 (Stakeholder-Communication) nutzen für die passende Reply
6. T-013: Termin-Prep gemäß `06_ROHDE_MEETING_KIT.md` Sektion 7

**Nach Rohde-Approval (P1-Kickoff):**
- Opus 4.7 Session mit Template 1 starten: "Plane P1 (Ethikantrag + Datenvertrag + DSGVO-Setup) als atomare Tasks"
- Folge: ~10–15 neue Tasks in tasks.jsonl, vorwiegend Opus + Sonnet (Compliance-Texte)

## Memory updates

- `MEMORY.md` Index angelegt (zeigt auf alle erwarteten domain/ Files — die selbst noch geschrieben werden müssen)
- `memory/README.md` neu (Hierarchie-Beschreibung)
- `memory/runs/2026-04-27_opus47_harness_v1.md` neu (diese Datei)
- `memory/domain/*` noch leer — wird in T-011 gefüllt

## Hinweise an die nächste Session

1. **Lies zuerst:** `00_INDEX.md` — Eine Seite, die dich orientiert. Dann `CLAUDE.md` + `MEMORY.md`.
2. **Wenn du im P0-Mode bist:** schau in `tasks.jsonl` — die T-001 bis T-013 Sequenz ist exakt geplant.
3. **Wenn du in einem späteren Phasen-Mode bist:** triggere Opus mit Template 1, und sag *„Plane P<N> als atomare Tasks. Beachte Pre-Flight aus 01_HARNESS.md."*
4. **Decision-Tree-Harvesting** ist noch Spec, kein Code. Wenn jemand fragt *„Wo läuft das?"*: Antwort ist *„P3 (Backend) + P4 (UI) — vorher nicht."*
5. **Wenn Rohde negativ antwortet:** sofort `06_ROHDE_MEETING_KIT.md` Sektion 6 lesen — Plan B (Tolg) und Plan C (van Stevendaal) sind vorbereitet.
