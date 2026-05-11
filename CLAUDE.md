# CLAUDE.md — Carotis-AI Working Memory  · v1.1

> Diese Datei wird in **jeder** Claude-Session geladen. Sie enthält das, was jedes Modell sofort wissen muss. Halte sie unter ~200 Zeilen — alles Tiefere gehört in `memory/` und wird über `MEMORY.md` indiziert.

---

## AI Mode — Engineering Harness

Terse. Drop fluff. Technical exact. Code unchanged.
Pattern: [thing] [action] [reason]. [next step].
Caveman always on. Off: "normal mode". Commits/PRs: normal English.
Use caveman-compress on memory files to cut input tokens.

**Theoretische Basis:** Jake van Clief — *Interpretable Context Methodology / Model Workspace Protocol* (arXiv 2603.16021). Numbered Folders = Stages. Markdown = Prompts. Scripts = mechanische Arbeit. Filesystem ersetzt Framework-Orchestrierung.

**Local-AI-Stack:** Ollama (`localhost:11434`) als Inference-Endpoint + Hermes Agent (Nous Research) als Self-Improving-Layer + caveman/caveman-compress für Token-Budget. Wiederverwendbar für jedes lokal gehostete OSS-Projekt — nur das Modell hinter `localhost:11434` wechselt.

**Multi-Model-Routing:**
- Cloud-Claude Opus → Architektur, ADR, Stakeholder-Mails (begrenzt)
- Cloud-Claude Sonnet → Code-Review, Office-Drafts (begrenzt)
- GitHub Copilot Sonnet 4.6 / Codex 5.3 → Code-Implementation in `code/` (€10/Monat-Plan)
- Hermes via Ollama → Tool-Use, Memory, Skills (lokal, unbegrenzt)
- Caveman via Ollama → Compression, Boilerplate (lokal, schnell)

---

## Project (April 2026)

**Carotis-AI** — lokales, erklärbares KI-System zur Quantifizierung der Carotis-Stenose und Plaque-Vulnerability aus CTA-Bildern. Promotionsprojekt am Klinikum Dortmund.

**Hauptklage gegen alle anderen Lösungen:** Cloud-Abhängigkeit (DSGVO-Risiko), keine Erklärbarkeit, kein Decision-Tree-Harvesting, generisch statt Carotis-spezifisch.

**Unsere Antwort:** Local-First Edge AI + Grad-CAM XAI + Decision-Tree-Harvesting + Daily-Learning-Loop.

---

## People

| Wer | Rolle | Kontakt |
|-----|-------|---------|
| **Lou (Laith Alshdaifat)** | Projektleiter, Medizintechnik HAW Hamburg, Schwager der Kandidatin | shdaifatss@gmail.com / diggai@tutanota.de |
| **Dr. med. Aroob Alrawashdeh / Apo** | Kandidatin; aktuelle Rolleninformation laut Lou 2026-05-02: NVIDIA. Dortmund/Rohde-Bezug historisch formulieren, nicht als aktuelle Klinikum-Dortmund-Anstellung. | TBD |
| **Prof. Dr. med. Stefan Rohde** | Ziel-Betreuer, Klinikum Dortmund, Direktor (Neuroradiologie) | über Aroob/Apo bzw. historischen Kontakt |
| **Prof. Dr. Petra Margaritoff** | HAW Hamburg, DIN EN 62304, Medical Embedded Systems | LinkedIn |
| **Prof. Dr. Boris Tolg** | HAW Hamburg, Dekan Life Sciences, SIMLab, VR in Medicine | HAW |
| **Prof. Dr. Udo van Stevendaal** | HAW Hamburg, Vorsitz Medizintechnik-Hamburg | HAW |
| **Dr. Islam Shdaifat** | JoVision, Computer Vision, 4 Patente, AI-Architekt | LinkedIn |
| **Eng. Yassine Daghfous** | Data Engineer, Cloud + Pipelines | LinkedIn |
| **Dr. med. Christina Klaproth** | bestehende Praxis-Kooperation, Gefäßmedizin | praxis-fuer-gefaessmedizin.de |
| **Sarah Specialty Hospital, Jordanien** | klinischer Validierungspartner | sarahspecialtyhosp.wixsite.com |

---

## Stack (April 2026)

- **Frontend:** React 19 + Vite + TypeScript + Tailwind v4 (aus `dr-aroob-ki` Repo)
- **DICOM-Viewer:** Cornerstone.js oder OHIF Viewer
- **Backend (Edge):** Python FastAPI, ONNX Runtime, lokal auf Praxis-Server
- **Modell:** MFSD-UNet-Architektur (U-Net + Swin Transformer + Deep Supervision); ggf. plus ResNet/EfficientNet als Klassifikator
- **XAI:** HiResCAM für Heatmap-Generierung (ADR-005); SHAP für tabellarische Vulnerability-Features
- **Confidence Calibration:** Platt/Isotonic Scaling + Trust Score Service (Composite: confidence 0.5, calibration 0.3, transparency 0.2)
- **Datenbank:** SQLite (lokal, für Audit-Trail) + DICOM-Filesystem
- **Anonymisierung:** DICOM PS 3.15 De-Identification Profiles
- **Integration:** HL7/FHIR an Klinikum-PVS
- **Hosting Demo:** Online auf Hetzner: `https://carotis.diggai.de/` und `https://api.carotis.diggai.de/` liefern 200; `/health/` ist OK. Fly.io bleibt wegen Trial/Billing blockiert und darf nicht als DNS-Ziel genutzt werden, solange `trial has ended` besteht. Master-Demo-Zugang ist als gehashter `master-admin-demo` Token im Backend aktiv; Rohwert kennt Lou aus dem Prompt und wird nicht in Memory/Docs wiederholt. Niemals echte Patientendaten.
- **AI-Dev-Tooling:** Anthropic Claude Sonnet 4.6 / Opus 4.7, GitHub Copilot, Claude.ai/design

---

## Critical Path

```
P0 (Rohde-Meeting + Floy-Recherche)
  ↓
P1 (Ethikantrag + Datenvertrag + DSGVO-Setup)
  ↓
P2 (Datenakquise retrospektiv n≥500, Anonymisierung)
  ↓
P3 (Modell-Training MFSD-UNet, ONNX-Export)
  ↓
P4 (Edge-Server-Integration, UI, Decision-Tree-Capture)
  ↓
P5 (Klinische Validierung DE + Jordanien)
  ↓
P6 (Manuskript Radiology / JNIS, Disputation)
  ↓
P7 (MDR-Zertifizierung, Skalierung)
```

P0 ist gerade aktiv. Alles weitere ist **blocked by P0** bis Rohde sein Go gegeben hat.

---

## Phase Status

| Phase | Status | Block |
|-------|--------|-------|
| P0 — Stakeholder + Code-Stack | 🔄 Läuft | Stride V2 done (alle 7 Office-Docs in `Stride V2/`). Mail an Rohde noch nicht raus — wird Teil von P0f. |
| P0a — Demo-Robustheit | ✅ DONE | K-17..K-22 done. Walkthrough + Demo-Daten + Dashboard. |
| P0d — Codex-NN Trust+Calibration | ✅ DONE | K-NN Alpha/Beta/Gamma + ADR-006 + ONNX-Calibration-Export. |
| P0e — Code-Stack Robustheit | ✅ DONE | K-35..K-46 done. 101/101 pytest, 12/12 Vitest, 6/6 Anomalien fixed. T-017 done. |
| **P0f — Production-Demo-Pivot** | ✅ **ONLINE — Pre-Send-Smoke offen** | **Aktueller Online-Stand 2026-05-04:** INWX DNS ist final: `carotis.diggai.de A 204.168.230.127`, `api.carotis.diggai.de A 204.168.230.127`. Hetzner CX23 bedient Frontend + Backend unter `https://carotis.diggai.de/` und `https://api.carotis.diggai.de/`; `/health/` liefert 200. Caddy ist healthy und TLS fuer `carotis.diggai.de` wurde via Let’s Encrypt ausgestellt. Fly.io bleibt wegen Trial/Billing (`trial has ended`) blockiert und ist nicht mehr DNS-Ziel. **Bei Prompts wie "Deploy", "mach online", "carotis erreichbar machen": zuerst `memory/domain/p0f_deploy_state_compact_2026-05-02.md`, `memory/runs/2026-05-04_Codex_GPT55-Run15_dns_hetzner_proxy.md`, `deploy/Caddyfile.backend`, `deploy/hetzner-backend.compose.yml` lesen.** |
| P1 | 🔒 Blocked | wartet auf P0f → Rohde-Antwort |
| P2–P7 | 🔒 Blocked | wartet auf P1 |

---

## Pre-Flight (Pflicht — JEDES Modell, JEDE Session)

```bash
# 0. Agent Pre-Flight Protocol
cat ULTRAPLAN.md

# 1. Working memory frisch?
cat CLAUDE.md
cat MEMORY.md

# 2. Letzte 3 Run-Logs überfliegen
ls -t memory/runs/ | head -3

# 3. Bei Code-Arbeit: existiert die Lösung schon?
grep -r "<feature-keyword>" memory/runs/

# 4. Bei Modell-Arbeit: bekannte Anomalien?
ls memory/anomalies/

# 5. Wenn alles klar: Task in tasks.jsonl auf in_progress setzen
```

---

## Engineering Harness Tools (geerbt aus Elbtronika)

| Tool | Zweck | Befehl |
|------|-------|--------|
| **caveman** | Output-Token –75 % | `claude plugin install caveman@caveman` |
| **caveman-compress** | Input-Token –46 % | `/caveman:compress CLAUDE.md` |
| **codeburn** | Token-Kosten Dashboard | `npx codeburn` |
| **browser-harness** | Sichtbare Browser-/Provider-/Claude-Design-Verifikation | `browser-harness -c 'new_tab(\"http://localhost:3000\")'` |
| **obsidian** | Lokale Notizen, Search, Wikilinks | Detailregeln in `memory/domain/skill_team_harness_2026-05-02.md` |
| **remotion-best-practices** | Lokale Rohde-Demo-Video-Planung | 30fps, `Sequence`, lokale Assets, keine CSS-Animation |
| **skill-team-harness** | 50 operative Skill-Aufgaben + Stop-Regeln | `memory/domain/skill_team_harness_2026-05-02.md` |
| **designlang** | Design aus URL → Tailwind/shadcn | `npx designlang <url>` |

---

## Preferences (Lou)

- Deutsch als Arbeitssprache, Code + Commits Englisch
- **Local-First** ist religiös — kein Patientendatenexport, niemals
- Privacy-by-Design vor Privacy-by-Compliance (Datenschutz im Architektur-Diagramm, nicht im Vertragsanhang)
- Solo-Dev mit Claude — Freigabe-Gate vor jedem Code-Commit
- Code-Sessions als Agenten-Orchester planen: maximale sinnvolle Subagenten-Parallelität, aber nur mit disjunkten Datei-/Ownership-Grenzen und klarer Integrationsrunde danach.
- Reverse Social Engineering: Mittelsmänner werden eliminiert (kein SaaS, keine Cloud-Provider, kein externes IT-Outsourcing)
- Familienprojekt → Reputations-Cost ist immer mitgedacht
- Doku nach jedem Phase-DoD: Notion + Airtable + Miro + lokal + GitHub

---

## Verbote

- ❌ Patientendaten in Cloud / externe API / E-Mail / Slack
- ❌ Modell-Training auf nicht-anonymisierten Daten
- ❌ Code-Änderungen ohne Pre-Flight-Check (siehe oben)
- ❌ Run-Ende ohne Eintrag in `memory/runs/`
- ❌ Office-Dokument-Edits direkt von einem Modell — Modelle generieren Stride-Prompts, Lou führt sie aus
- ❌ Reflexives Vertrauen in Memory-Records — vor Aktion immer Realität prüfen (siehe Auto-Memory-Doc des Systems)

---

**Letztes Update:** 2026-05-04 (v2.2 — Codex GPT-5.5: Master-Demo-Token als gehashter `master-admin-demo` Backend-Zugang aktiviert und live verifiziert; weiterhin INWX/Hetzner online, Fly.io durch Trial/Billing blockiert. Refs: `memory/runs/2026-05-04_Codex_GPT55-Run15_dns_hetzner_proxy.md`, `memory/runs/2026-05-04_Codex_GPT55-Run16_master_demo_token.md`).
