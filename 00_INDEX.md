# Carotis-AI — Engineering Harness v1.0

> **Lies das hier zuerst.** Eine Seite, die dich (und jedes AI-Modell) durch das ganze Projekt-Paket führt.

---

## Was ist das?

Ein **Engineering-Harness** für das Promotionsprojekt von Aroob Alrawashdeh (Ärztin in Weiterbildung, Klinikum Dortmund). Ziel: ein lokal betriebenes, erklärbares KI-System für die Carotis-Stenose-Diagnostik aus CTA-Bildern, das **die Entscheidungs­findung der Radiologen lernt — nicht nur die Bilder**.

Methodik: schwere Denkarbeit einmal mit **Opus 4.7** machen, dann **Sonnet 4.6** und **Haiku 4.5** die atomaren Tasks ausführen. Jeder Run schreibt seine Lehren in `memory/`, sodass der nächste Run nicht bei Null anfängt.

---

## Files in diesem Paket

| Datei | Wer liest? | Wofür |
|---|---|---|
| **`00_INDEX.md`** | Du + alle Modelle | Einstieg (diese Datei) |
| **`01_HARNESS.md`** | Alle Modelle | Modell-Routing, Pre-Flight, DoD, Eskalation |
| **`02_ROADMAP.md`** | Opus + du | Phasen P0–P7 (Promotion: 24 Monate) |
| **`03_PROMPT_TEMPLATES.md`** | Du | 9 Copy-Paste-Prompts pro Anwendungsfall |
| **`04_MASTER_PLAN.md`** | Alle | Der v1.0-Plan analog Elbtronika v1.0 |
| **`05_DECISION_TREE_HARVESTING.md`** | Alle | Spec für das Lernen aus Arzt-Entscheidungen |
| **`06_ROHDE_MEETING_KIT.md`** | Du + Aroob | Meeting-Prep für Prof. Rohde |
| **`07_OFFICE_AGENT_PROMPTS.md`** | Du | Stride-Prompts zum Update der bestehenden Docs |
| **`08_RESEARCH_ATTENTION_2020-2026.md`** | Du + Aroob | Literatur-Inventar Attention-Mechanism |
| **`CLAUDE.md`** | Alle Modelle | Working Memory — bei jeder Session lesen |
| **`MEMORY.md`** | Alle Modelle | Index der Langzeit-Memorys |
| **`tasks.jsonl`** | Sonnet + Haiku | Maschinen-lesbare Task-Liste |
| **`memory/`** | Alle Modelle | Run-Logs, Decision-Trees, Anomalien, Domain-Wissen |

Bestehende Aroob-Dokumente (`.docx`, `.pptx`, `.html`, `.md`) bleiben wo sie sind — sie sind die **Outputs**, nicht das **Harness**.

---

## So benutzt du das ab heute

### Szenario 1 — Du willst das Rohde-Meeting vorbereiten
1. Lies `06_ROHDE_MEETING_KIT.md` (Agenda, Demo-Skript, Floy-Vergleich, Pitch).
2. Nutze `07_OFFICE_AGENT_PROMPTS.md` → kopiere die Prompts in Microsoft 365 Copilot/Stride, um die bestehenden `.docx`/`.pptx` auf Klinikum Dortmund + Prof. Rohde zu aktualisieren.
3. Geht die Mail raus → Eintrag in `memory/runs/`.

### Szenario 2 — Du willst Code/Modell weiterbauen
1. **Plane** mit Opus → `03_PROMPT_TEMPLATES.md` Template 1 → erzeugt Tasks in `tasks.jsonl`.
2. **Führe aus** mit Sonnet (Template 3) oder Haiku (Template 2).
3. **Verifiziere** mit Template 5 (Code-Review) oder Template 8 (Debug).
4. Jeder Run logt am Ende kurz in `memory/runs/<datum>_<sessionID>.md`: was geklappt hat, was nicht, was die nächste Session wissen sollte.

### Szenario 3 — Du willst eine Arzt-Entscheidung erfassen
1. Lies `05_DECISION_TREE_HARVESTING.md` — Schema und Mini-UI.
2. Trag die anonymisierte Entscheidung in `memory/decisions/<datum>_<case-hash>.md` ein.
3. Wenn KI und Arzt uneinig waren: zusätzlich `memory/anomalies/<datum>_<case-hash>.md`.

---

## Die wichtigste Regel — Pre-Flight Check

**Vor jeder neuen Datei/Komponente** prüft jedes Modell:

1. `MEMORY.md` lesen — was wissen wir schon?
2. `memory/runs/` durchscrollen — ist die Aufgabe schon mal versucht worden?
3. `memory/anomalies/` checken — gibt es einen bekannten Stolperstein?

Wenn die Aufgabe schon erledigt ist: **nicht neu machen**, bestehende Lösung erweitern.
Wenn sie schon mal gescheitert ist: **die Begründung lesen**, Pfad ändern, nicht wiederholen.

---

## Modell-Strategie auf einen Blick

```
┌─────────────────────────────────────────────────────────┐
│  OPUS 4.7  → planen, ADR, Decision-Tree-Schema, Pitch    │
│  ↓                                                       │
│  Output: atomare Tasks mit Pseudo-Code in tasks.jsonl    │
│  ↓                                                       │
│  SONNET 4.6 → Code, Tests, Refactor, Office-Drafts       │
│  HAIKU 4.5  → atomare Edits, i18n, Verify, Boilerplate   │
└─────────────────────────────────────────────────────────┘
```

Erwartete Verteilung: ~50% Haiku · ~40% Sonnet · ~10% Opus.

---

## Aktuelle Phase: P0 — Stakeholder & Dokumentation

**Goal:** Termin mit Prof. Rohde (Klinikum Dortmund) bekommen, Office-Dokumente auf Klinikum-Setting umstellen, Floy-Recherche abschließen.

**Was tun:**
1. `06_ROHDE_MEETING_KIT.md` lesen.
2. `07_OFFICE_AGENT_PROMPTS.md` Prompts in Stride ausführen → aktualisierte Docs.
3. Aroob die finale Mail an Prof. Rohde rausschicken lassen.

Sobald Termin steht → P1 starten (Datenvertrag, Ethikantrag).

---

## Wichtige Hinweise

- **Workspace-Pfad:** `C:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI`
- **Repo (UI/Frontend):** `https://github.com/DiggAiHH/dr-aroob-ki` und `https://github.com/DiggAiIT/Dr-Aroob-Portal`
- **Verbundene MCPs:** Slack, Gmail, Google Calendar, Drive, Notion, Airtable
- **Sprache:** Doku Deutsch (für Aroob/Rohde); Code-Kommentare + Commits Englisch (für Industrie-Standard)
- **Compliance:** EU AI Act (High-Risk), MDR Class IIa, DSGVO Privacy-by-Design, DIN EN 62304

---

## Nächster Schritt für dich

1. Lies `04_MASTER_PLAN.md` (10 Min — du verstehst das ganze Projekt)
2. Lies `06_ROHDE_MEETING_KIT.md` (5 Min — du weißt, was diese Woche zu tun ist)
3. Ausführen → `07_OFFICE_AGENT_PROMPTS.md` in Stride

---

**Letztes Update:** 2026-04-27 · Harness v1.0 erstellt durch Opus 4.7 (Cowork Session)
