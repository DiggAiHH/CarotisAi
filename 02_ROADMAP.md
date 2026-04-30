# 02_ROADMAP — Carotis-AI (24 Monate Promotion)

> **Stand:** 2026-04-27
> **Modell-Strategie:** Phasen-Planung mit Opus 4.7 → Tasks ausführen mit Haiku/Sonnet
> **Gesamtziel:** Promotion + lokal lauffähiges, MDR-konformes CDSS + Publikation in Radiology / JNIS

---

## Phasen-Übersicht

| Phase | Goal | Risiko | Wert | Modell-Mix | Zeit | Status |
|---|---|---|---|---|---|---|
| **P0** | Stakeholder-Approval (Rohde) + Office-Docs aktualisiert + Floy-Recherche | mittel (politisch) | hoch | Opus 50% + Sonnet 50% | 2 Wochen | 🔄 LÄUFT |
| **P1** | Ethikantrag + Datenvertrag + DSGVO-Setup | hoch (regulatorisch) | hoch | Opus 70% + Sonnet 30% | M1–M2 | 🔒 Block |
| **P2** | Datenakquise retrospektiv (n≥500), DICOM-Anonymisierung, Ground-Truth-Labelling | hoch (Datenqualität) | sehr hoch | Sonnet 50% + Haiku 50% | M3–M5 | 🔒 Block |
| **P3** | Modell-Training MFSD-UNet + Plaque-Vulnerability-Klassifikator + ONNX-Export | hoch (technisch) | sehr hoch | Sonnet 60% + Opus 30% + Haiku 10% | M6–M9 | 🔒 Block |
| **P4** | Edge-Server-Integration + UI + Decision-Tree-Capture im Klinikum-Workflow | mittel | sehr hoch | Sonnet 50% + Haiku 40% + Opus 10% | M10–M15 | 🔒 Block |
| **P5** | Klinische Validierung DE (Klinikum Dortmund) + JO (Sarah Hospital), Daily-Learning-Loop aktiv | hoch (klinisch) | sehr hoch | Sonnet 40% + Opus 40% (Anomalie-Triage) + Haiku 20% | M16–M21 | 🔒 Block |
| **P6** | Manuskript Radiology / JNIS + Disputation | hoch (akademisch) | sehr hoch | Opus 80% + Sonnet 20% | M22–M24 | 🔒 Block |
| **P7** | MDR-Class-IIa-Zertifizierung + Skalierung an weitere Kliniken | mittel | hoch | Opus 50% + Sonnet 50% | nach M24 | 🔒 Block |

---

## P0 — Stakeholder + Office-Docs (NÄCHSTE PHASE — START)

**Goal:** Termin mit Prof. Rohde am Klinikum Dortmund. Alle bestehenden Office-Dokumente sind auf das neue Setting umgestellt (Klinikum statt Praxis, Aroob als Ärztin in Weiterbildung, Rohde als Empfänger). Floy-Recherche + Carotis-AI-Konzept liegen Aroob fertig vor.

### Deliverables

1. **Aktualisierte Office-Dokumente** (von Lou via Stride-Prompts in `07_OFFICE_AGENT_PROMPTS.md`):
   - `Anschreiben_Dr_Alrawashdeh_Rohde_v2.docx` — neue Mail an Prof. Rohde
   - `Ki_Carotis_Expose_Rohde_v2.docx` — Klinikum-Setting + Engineering-Harness-Absatz
   - `Ki_Carotis_Diagnostik_Klinikum_v2.docx` — technische Beschreibung
   - `Value_Proposition_Klinikum_v2.docx` — auf Rohde + Klinikum zugeschnitten
   - `Carotis_Ai_v2.pptx` — neue Folie 2.5 (Engineering Harnessing) + 11.5 (Warum Klinikum Dortmund)
2. **Floy-Recherche-Dokument** (`Ki_Tools_Marktanalyse.docx` ist die Basis — wird in der Mail als Anlage 1 verschickt)
3. **Carotis-AI-Konzeptpapier** (`Carotis_Ai_Konzept.docx` ist die Basis — Anlage 2)
4. **Mail von Aroob an Prof. Rohde rausgegangen**
5. **Termin im Kalender**

### Akzeptanzkriterien

- Office-Docs reviewt von Lou + Aroob
- Mail rausgeschickt
- Eintrag in `memory/runs/2026-04-27_p0_kickoff.md`

### Modell-Routing

| Aufgabe | Modell |
|---|---|
| Office-Update-Prompts schreiben | Opus 4.7 (politisch sensibel — Rohde-Tonality) |
| Mail-Text finalisieren | Opus 4.7 |
| Floy-Recherche-Plus-Up (Faktenchecks) | Sonnet 4.6 |
| Termin-Tracking | Du (Calendar-MCP) |

---

## P1 — Ethikantrag + Datenvertrag + DSGVO-Setup

**Goal:** Rechtliche Basis für Datenakquise und Modell-Training steht.

### Deliverables

1. **Ethikantrag** bei der Ethikkommission der Ärztekammer NRW (Klinikum Dortmund)
   - Retrospektive + prospektive Datenerhebung
   - Patienteninformation + Einwilligungserklärung (Opt-in für Decision-Tree-Capture)
2. **Datenvertrag** Klinikum Dortmund ↔ Lou/HAW
   - DSGVO-Auftragsverarbeitungsvertrag (AVV)
   - Datenfluss-Diagramm (PACS → Anonymisierung → lokaler Training-Server)
3. **EU AI Act High-Risk-System-Dokumentation** (Vorbereitung für P3 schon hier beginnen)
4. **DIN EN 62304 Plan-File** (Software-Lebenszyklus)

### Akzeptanzkriterien

- Ethikvotum positiv
- Datenvertrag unterschrieben
- Compliance-Pakete versioniert in `regulatory/`

### Modell-Routing

| Aufgabe | Modell |
|---|---|
| Ethikantrag-Draft | Opus 4.7 (regulatorischer Text) |
| Datenvertrag-Draft | Opus 4.7 + Lou-Review |
| AI-Act-Doku | Opus 4.7 |
| 62304-Plan-File | Opus 4.7 + Prof. Margaritoff Review |

---

## P2 — Datenakquise + Anonymisierung + Ground Truth

**Goal:** ≥500 retrospektive CTA-Studien mit Ground Truth (Aroob + Konsens) sind anonymisiert, gehasht, manifestiert und auf dem Training-Server.

### Deliverables

1. **DICOM-Export-Skript** vom Klinikum-PACS (Air-Gap zur Cloud)
2. **Anonymisierungs-Pipeline** nach DICOM PS 3.15 (alle 33 Tags)
3. **Manifest-File** `data/manifest.csv` (SHA-256, Anonymisierungs-Datum, Studientyp)
4. **Labelling-Tool** (kann das `dr-aroob-ki` Repo werden — minimaler DICOM-Viewer + Stenose-Annotation)
5. **n≥500 gelabelt** durch Aroob (NASCET, ECST, Plaque-Vulnerability-Marker)
6. **Inter-Observer-Subset** (n=50 von zweitem Radiologen) — für Variabilitäts-Baseline

### Akzeptanzkriterien

- 0 PII in finalem Datensatz (`dicom-anonymizer --audit`)
- Coverage: alle 4 Plaque-Vulnerability-Marker in mind. 30% der Fälle
- Cohen's Kappa zwischen Aroob und Zweit-Labeller in `memory/domain/labeling_quality.md` dokumentiert

### Modell-Routing

| Aufgabe | Modell |
|---|---|
| Anonymisierungs-Skript | Sonnet 4.6 |
| Audit-Script (PII-Leak-Detection) | Sonnet 4.6 + Opus für Schema-Review |
| Labelling-UI in dr-aroob-ki | Sonnet 4.6 |
| Manifest-Generator (Bash/Python) | Haiku 4.5 |

---

## P3 — Modell-Training (MFSD-UNet + Klassifikator)

**Goal:** Trainiertes Modell mit Dice ≥0.90 für Vessel-Segmentierung und AUC ≥0.85 für Plaque-Vulnerability, exportiert als ONNX, lauffähig auf Edge-Hardware.

### Deliverables

1. **Datenpipeline** (PyTorch DataLoader mit Augmentation, Train/Val/Test-Split stratifiziert)
2. **MFSD-UNet-Implementation** (U-Net Backbone + Swin Transformer Bottleneck + Deep Supervision)
3. **Plaque-Vulnerability-Klassifikator** (Multi-Task-Head: 4 Klassen — IPH, ThinCap, LRNC, SystolicMotion)
4. **Training-Loop** mit MLflow-Logging
5. **ONNX-Export** + Inference-Benchmark auf Ziel-Hardware
6. **Grad-CAM-Implementation** für XAI
7. **Modell-Card** + Bias-Audit + Reproduzierbarkeits-Doku

### Akzeptanzkriterien

- Dice ≥ 0.90 (Vessel)
- AUC ≥ 0.85 (Plaque-Vulnerability)
- Inference < 3 s auf Ziel-Hardware
- Reproduzierbar (Seed → identische Metrics ±0.5%)

### Modell-Routing

| Aufgabe | Modell |
|---|---|
| Architektur-Entscheidungen (Backbone, Loss, etc.) | Opus 4.7 + Dr. Islam Konsultation |
| DataLoader, Training-Loop | Sonnet 4.6 |
| Augmentation-Pipeline | Sonnet 4.6 |
| Hyperparam-Search-Skript | Sonnet 4.6 |
| Modell-Card-Draft | Sonnet 4.6 |
| Bias-Audit-Plan | Opus 4.7 |

---

## P4 — Edge-Integration + UI + Decision-Tree-Capture

**Goal:** Carotis-AI läuft auf einem Edge-Server im Klinikum, integriert ins PVS via FHIR, mit UI für Aroob/Rohde und Decision-Tree-Capture-Hook (siehe `05_DECISION_TREE_HARVESTING.md`).

### Deliverables

1. **FastAPI-Backend** (lokal, ohne Internet-Auth) mit ONNX-Runtime
2. **React-UI** (basiert auf `dr-aroob-ki`) — DICOM-Viewer + AI-Panel + Decision-Tree-Form
3. **HL7/FHIR-Bridge** zum Klinikum-PVS
4. **Audit-Trail-Logger** (jede AI-Inferenz + Arzt-Entscheidung versioniert)
5. **Decision-Tree-Capture-UI** (30-Sek-Form nach jeder Befundung — siehe Spec)
6. **Daily-Retraining-Job** (Cron, läuft nachts auf der jeweils anonymisierten neuen Datenscharge — siehe `05_DECISION_TREE_HARVESTING.md`)

### Modell-Routing

| Aufgabe | Modell |
|---|---|
| FastAPI-Schema | Sonnet 4.6 |
| React-Komponenten | Sonnet 4.6 |
| FHIR-Mapping | Sonnet 4.6 + Opus für Edge-Cases |
| Audit-Trail-DB-Schema | Opus 4.7 |
| Decision-Tree-Capture-UI | Sonnet 4.6 |
| Daily-Retraining Cron + Watchdog | Sonnet 4.6 |
| Bug-Fixes Edge-Hardware | Sonnet 4.6 |

---

## P5 — Klinische Validierung + Daily-Learning-Loop

**Goal:** Prospektive Validierung an Klinikum Dortmund + Sarah Hospital. AI-Modell verbessert sich messbar Run-by-Run durch Decision-Tree-Daten.

### Deliverables

1. **Studienprotokoll** prospektiv (eingereicht in P1)
2. **Validierungs-Sample** n≥200 prospektiv DE + n≥100 JO
3. **Performance-Reports** wöchentlich (Sensitivity, Specificity, AUC, Inter-Observer-Reduktion)
4. **Anomaly-Log** populiert — jede AI-Mensch-Diskrepanz in `memory/anomalies/`
5. **Decision-Tree-Korpus** ≥1000 Trees in `memory/decisions/` (PII-frei)
6. **Wöchentliches Modell-Update** mit Performance-Vergleich vor/nach
7. **Lernkurven-Plot** zeigt Verbesserung über die Zeit

### Akzeptanzkriterien

- Sensitivity ≥ 0.92 für Stenose-Detektion (vs. Konsens-Ground-Truth)
- Inter-Observer-Variabilität reduziert um ≥30 %
- Modell verbessert sich messbar über 8 Trainings-Iterationen

### Modell-Routing

| Aufgabe | Modell |
|---|---|
| Anomaly-Triage (warum hat Aroob anders entschieden?) | Opus 4.7 — Pattern-Matching über alle Anomalien |
| Wöchentliche Performance-Reports | Sonnet 4.6 |
| Notebook-Updates für Lernkurven | Sonnet 4.6 |
| Stat-Tests (Cohen's Kappa, Bland-Altman) | Sonnet 4.6 |

---

## P6 — Manuskript + Disputation

**Goal:** First-Author-Paper in Radiology oder JNIS mit Prof. Rohde als Senior-Author. Erfolgreiche Disputation.

### Deliverables

1. **Manuskript-Draft** (Format Radiology / JNIS)
2. **Supplementary Material** (Anonymisierter Decision-Tree-Korpus, Modell-Card, Code-Repo)
3. **Submission** an Zieljournal
4. **Disputations-Vortrag** + Prüfungs-Vorbereitung

### Modell-Routing

| Aufgabe | Modell |
|---|---|
| Methodik-Sektion (am wichtigsten) | Opus 4.7 |
| Results + Figures | Sonnet 4.6 |
| Discussion + Limitations | Opus 4.7 |
| Referenzen-Management | Haiku 4.5 (Zotero-Sync) |
| Cover-Letter | Opus 4.7 |

---

## P7 — MDR-Zertifizierung + Skalierung

**Goal:** Carotis-AI als Class-IIa-Medizinprodukt nach MDR auf dem Markt. Erste 3 weitere Kliniken angebunden.

### Deliverables

1. **Technische Dokumentation** komplett nach MDR Annex II
2. **Klinische Bewertung** abgeschlossen
3. **Benannte Stelle** Audit bestanden
4. **CE-Kennzeichnung**
5. **Erste 3 Folge-Kliniken** angebunden (Multi-Site-Capable)

---

## Was steht NICHT auf dieser Roadmap

- Allgemeine Radiologie-AI (wir sind Carotis-fokussiert)
- US/Kanada-Markt (zuerst DACH, dann EU, dann Welt)
- Refinanzierungs-Pfad (separate `docs/finance/`-Doc — Familienfinanzierung deckt P0–P5)

---

## Wie diese Roadmap weiterentwickeln

Alle 4 Wochen oder beim Phasen-Wechsel:

1. Sonnet/Haiku haben Phasen-Tasks geleert → Trigger Opus mit Template 7 (Roadmap-Update)
2. Neue Roadmap-Version wird Datum-gestempelt archiviert (`02_ROADMAP_2026-04-27.md` → `02_ROADMAP_archive_2026-04-27.md`)
3. Erste 3 Tasks der nächsten Phase werden mit Template 1 zu atomaren Tasks
4. CLAUDE.md Phase-Status-Tabelle aktualisiert
