# Carotis-AI - Engineering Harness v1.1

> Lies das hier zuerst. Eine Seite, die dich und jedes AI-Modell durch das Projekt-Paket fuehrt.

---

## Was ist das?

Carotis-AI ist ein lokaler Forschungsprototyp fuer die Carotis-CTA-Begutachtung. Das Projekt verbindet Dr.-med.-Promotion, local-first Software, erklaerbare KI-Overlays und Decision-Tree-Capture.

Der aktuelle Frame seit 2026-05-06:

> **Forschungsprototyp zur Erfassung von Workflow-, Annotation- und Entscheidungspfad-Daten. Kein Medizinprodukt, keine klinische Entscheidungsgrundlage, keine automatische Befundausgabe.**

Methodik: schwere Architektur- und Strategiearbeit mit Opus, Umsetzung mit Codex/Sonnet/Kimi, Verifikation mit Tests und Run-Logs. Jeder Run schreibt seine Lehren in `memory/`, damit der naechste Run nicht bei Null anfaengt.

---

## Aktueller Stand 2026-05-11

- Neue Tagesunterlage fuer Aroob: `outputs/Aroob_Today_Briefing_2026-05-11.md`.
- Kanonische Zweckbestimmung: `memory/domain/zweckbestimmung_master_2026-05-06.md`.
- Dual-Track-Plan: Aroob Dr.-med.-Track + Lou Bachelor-Track in `memory/domain/execution_plan_dual_track_2026-05-10.md`.
- Live-Demo: `https://carotis.diggai.de/`; Backend: `https://api.carotis.diggai.de/`; beide auf Hetzner. Fly.io ist wegen Trial/Billing kein Ziel mehr.
- Online-Demo nutzt nur synthetische DICOMs. Keine echten Patientendaten online.
- Kritischer Code-Disclaimer-Audit vom 2026-05-10: Splash-Gate, Watermark, CDS-Feature-Flags und UI-Begriffe muessen vor externem Stakeholder-Versand final integriert und getestet werden.

---

## Dateien in diesem Paket

| Datei | Zweck |
|---|---|
| `00_INDEX.md` | Einstieg und aktueller Stand |
| `01_HARNESS.md` | Modell-Routing, Pre-Flight, DoD, Eskalation |
| `02_ROADMAP.md` | Aktualisierte Forschungsprototyp-Roadmap |
| `03_PROMPT_TEMPLATES.md` | Copy-Paste-Prompts pro Anwendungsfall |
| `04_MASTER_PLAN.md` | Masterplan und Stakeholder-Logik |
| `05_DECISION_TREE_HARVESTING.md` | Spec fuer Lernen aus aerztlichen Entscheidungen |
| `06_ROHDE_MEETING_KIT.md` | Rohde-Meeting-Prep; vor Versand gegen neuen Frame pruefen |
| `07_OFFICE_AGENT_PROMPTS.md` | Stride-Prompts; v2/v3 Inhalte muessen Re-Frame nutzen |
| `08_RESEARCH_ATTENTION_2020-2026.md` | Literatur-Inventar |
| `CLAUDE.md` | Working Memory, bei jeder Session lesen |
| `MEMORY.md` | Index der Langzeit-Memorys |
| `tasks.jsonl` | Maschinenlesbare Task-Liste |
| `memory/` | Run-Logs, Domain-Wissen, Anomalien, Decisions |

---

## Aktuelle Phase: P0g - Regulatory-Pivot + Aroob/Rohde Alignment

**Goal:** Forschungsprototyp-Frame sauber in Code, Roadmap, Office-/Rohde-Kommunikation und Aroob-Briefing ziehen. Erst danach Rohde/Margaritoff-Versand.

**Was jetzt zu tun ist:**

1. `outputs/Aroob_Today_Briefing_2026-05-11.md` mit Aroob durchgehen.
2. Code-Disclaimer-Sprint schliessen: `ResearchSplashGate`, `Watermark`, Feature-Flags, Audit-Log.
3. Rohde-Mail v4 und Margaritoff-Mail erst nach erfolgreichem Re-Audit versenden.

Sobald Rohde positiv reagiert, startet P1 Setup + Ethik. Sobald Margaritoff positiv reagiert, wird Lous Bachelor-Track formal vorbereitet.

---

## So benutzt du das ab heute

### Rohde/Aroob vorbereiten

1. Lies `outputs/Aroob_Today_Briefing_2026-05-11.md`.
2. Lies `memory/domain/zweckbestimmung_master_2026-05-06.md`.
3. Pruefe alle Rohde-/Aroob-Texte auf verbotene Begriffe: Diagnoseassistent, KI-Befund, automatische Quantifizierung, MDR Class IIa als aktueller Pfad.

### Code/Modell weiterbauen

1. Pre-Flight aus `ULTRAPLAN.md` und `CLAUDE.md` ausfuehren.
2. Aufgabe in `tasks.jsonl` auf `in_progress` setzen.
3. Bestehende Loesung suchen, dann erst editieren.
4. Verifizieren, Run-Log schreiben, `MEMORY.md` aktualisieren.

### Arzt-Entscheidung erfassen

1. `05_DECISION_TREE_HARVESTING.md` lesen.
2. Nur anonymisierte, PII-freie Inhalte in `memory/decisions/` oder `memory/anomalies/` schreiben.
3. Keine Patientendaten in Chat, Cloud, GitHub, E-Mail oder externe APIs.

---

## Wichtigste Regeln

- Patientendaten verlassen niemals den lokalen Klinik-/Edge-Kontext.
- Office-Dokumente werden nicht direkt von Modellen bearbeitet; Modelle liefern Stride-Prompts.
- Vor Code-Arbeit: Pre-Flight, bestehende Runs, Anomalien, Git-Status.
- Nach jeder Session: Run-Log in `memory/runs/` + Pointer in `MEMORY.md`.
- Medizinische/regulatorische Aussagen immer gegen `memory/domain/zweckbestimmung_master_2026-05-06.md` pruefen.

---

## Wichtige Hinweise

- **Workspace:** `C:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI`
- **Repo:** `https://github.com/DiggAiHH/CarotisAi.git`
- **Live-Demo:** `https://carotis.diggai.de/`
- **Backend:** `https://api.carotis.diggai.de/`
- **Stack:** React 19 + Vite + TypeScript + Tailwind v4; FastAPI + SQLite + ONNX Runtime; MFSD-UNet/MONAI/HiResCAM; Hetzner/Caddy fuer P0f-Demo.
- **Compliance-Frame:** Forschungsprototyp + DSGVO Privacy-by-Design + DICOM PS 3.15 + DIN EN 62304-Dokumentationslogik. MDR Class IIa nur als spaetere Option, nicht P0/P1-Zweckbestimmung.

---

## Naechster Schritt

1. Aroob-Briefing oeffnen: `outputs/Aroob_Today_Briefing_2026-05-11.md`.
2. Mit Aroob die 5 Entscheidungen in Abschnitt 9 klaeren.
3. Danach Code-Disclaimer-Sprint fertigstellen und Re-Audit laufen lassen.

---

**Letztes Update:** 2026-05-11 - Codex GPT-5.5: Forschungsprototyp-Pivot, Hetzner-Live-Stand und Aroob-Tagesbriefing eingepflegt.
