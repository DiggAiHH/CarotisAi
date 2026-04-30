# 04_MASTER_PLAN — Carotis-AI v1.0

> Analog zu **Elbtronika v1.0**: ein einziges Dokument, das das ganze Projekt fasst. Wenn jemand fragt "Was macht ihr da eigentlich?" → diese Datei.

---

## 1. North Star

**Ein lokal betriebenes, erklärbares KI-System, das die Carotis-Stenose-Diagnostik aus CTA-Bildern unterstützt — und sich täglich aus den Entscheidungen der Radiologen verbessert. Nicht der Befund wird gelernt. Die Begründung wird gelernt.**

Der Kern-Pitch in einem Satz:
> *"Während alle anderen die Bilder anschauen, schauen wir, wie der Arzt schaut."*

---

## 2. Kontext

- **Promotionsprojekt** von Aroob Alrawashdeh (Ärztin in Weiterbildung Radiologie, Klinikum Dortmund)
- **Ziel-Betreuer:** Prof. Dr. med. Stefan Rohde (Klinikum Dortmund, Neuroradiologie)
- **Technische Leitung:** Lou (Laith Alshdaifat, Medizintechnik HAW Hamburg)
- **Wissenschaftliche Beratung:** Prof. Margaritoff (DIN EN 62304), Prof. Tolg (SIMLab/VR), Prof. van Stevendaal (Medizintechnik), Dr. Islam Shdaifat (CV/AI)
- **Klinischer Validierungspartner:** Sarah Specialty Hospital, Jordanien
- **Bestehende Infrastruktur:** [DiggAI.de](https://diggai.de) (ePA, Telefon-Agent, IT-Mgmt) — wir bauen darauf auf, kein Greenfield
- **Repos:** `https://github.com/DiggAiHH/dr-aroob-ki`, `https://github.com/DiggAiIT/Dr-Aroob-Portal`

---

## 3. Die wissenschaftliche Lücke

### Stand der Technik

In den letzten 5 Jahren (2020–2026) ist die Carotis-CTA-AI-Forschung explodiert:

- **Segmentierung:** Swin-UNet mit Multi-Scale Deep Supervision — Dice 0.91, Sensitivity 0.99 ([Xie 2024 QIMS](https://qims.amegroups.org/article/view/135680/html))
- **Plaque-Vulnerability:** ML-Modelle mit AUC 0.96 für symptomatische Plaques ([Le 2024 Circulation Imaging](https://www.ahajournals.org/doi/10.1161/CIRCIMAGING.123.016274))
- **Explainability:** SHAP + Grad-CAM mit AUC 0.90 für Symptom-Klassifikation ([2025 Frontiers Neurology](https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2025.1679861/abstract))
- **Reviews:** Decade-of-Progress-Synthese ([2025 PubMed](https://pubmed.ncbi.nlm.nih.gov/41025057/))

### Was alle vermissen

**Kein einziges System lernt, WIE der Radiologe denkt.** Sie lernen Pixel → Label. Nicht Pixel → Frage → Hypothese → Auswertung → Label. Die ärztliche Entscheidungs­findung — der eigentliche Wert von 10 Jahren Facharzt — wird weggeworfen.

Zusätzlich:
- Alle aktuellen Lösungen sind **Cloud-basiert** → DSGVO-Risiko in Deutschland.
- Keine systematische **transnationale Validierung** (Westen vs. Globaler Süden).
- Keine **EU-AI-Act-konforme Implementation** bisher publiziert.

### Was wir machen

**Wir bauen drei Schichten:**

1. **Layer 1 — Pixel-Modell** (State-of-the-Art): MFSD-UNet aus der Literatur, lokal trainiert auf anonymisierten Klinikum-Dortmund-Daten + Jordanien-Daten.
2. **Layer 2 — Decision-Tree-Harvesting** (Innovation): Nach jeder Befundung eine 30-Sekunden-Mini-UI, die Aroob/Rohde fragt: *"Welches Feature hat dich überzeugt? Was hast du ausgeschlossen? Wie sicher bist du?"* — strukturiert geloggt, anonymisiert, in einen Decision-Tree-Korpus.
3. **Layer 3 — Daily-Learning-Loop**: Jeden Abend trainiert das System inkrementell auf den neuen Decision-Trees + Anomalien (Fälle, in denen KI und Mensch sich nicht einig waren). Performance-Vergleich vor/nach. Rollback wenn schlechter.

**Das Resultat:** Ein Modell, das nicht nur sagt *"70 % NASCET, Confidence 89 %"*, sondern *"70 % NASCET, weil das Feature X ausschlaggebend ist; ein erfahrener Radiologe würde hier auch noch Y prüfen — möchtest du das?"*.

---

## 4. Architektur-Diagramm (Local-First)

```
┌─────────────────────────────────────────────────────────────────┐
│                  KLINIKUM DORTMUND (geschlossen)                │
│                                                                 │
│  ┌──────────┐    ┌──────────────┐    ┌────────────────────┐    │
│  │   PACS   │ →  │  CAROTIS-AI  │ →  │   AROOB / ROHDE    │    │
│  │  (DICOM) │    │  Edge-Server │    │   UI (DICOM +      │    │
│  └──────────┘    │  • ONNX RT   │    │    AI-Panel +      │    │
│                  │  • FastAPI   │    │    Decision-Form)  │    │
│                  │  • Audit-DB  │    └────────────────────┘    │
│                  └──────────────┘             │                 │
│                          ↑                    │                 │
│                          │              Decision-Tree           │
│                          │              + ggf. Anomaly-Flag     │
│                          ↓                    │                 │
│                  ┌──────────────────────────────┐               │
│                  │  DAILY-LEARNING-LOOP (Cron)  │               │
│                  │  • Anonymisiert neue Cases   │               │
│                  │  • Inkrementelles Training   │               │
│                  │  • Performance-Vergleich     │               │
│                  │  • Auto-Rollback bei Verlust │               │
│                  └──────────────────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓ (anonymisiert, signiert, monatlich)
┌─────────────────────────────────────────────────────────────────┐
│  CENTRAL TRAINING (HAW Hamburg / JoVision Workstation)          │
│  • Konsolidierung Klinikum DE + Sarah Hospital JO               │
│  • Modell-Releases mit Modell-Card + Bias-Audit                 │
│  • Push zurück zu Klinikum nur als signiertes ONNX-Bundle       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  SARAH SPECIALTY HOSPITAL (Jordanien) — identisches Setup       │
│  • Identische Edge-Hardware                                     │
│  • Lokale prospektive Validierungs-Daten                        │
│  • Eigener Decision-Tree-Korpus (Multi-Center)                  │
└─────────────────────────────────────────────────────────────────┘
```

**Kein Patientenpfad führt durch eine Cloud.** Jeder Pfeil zwischen den Boxen ist entweder anonymisiert oder ein signiertes Modell-Artefakt. Kein PII verlässt jemals den jeweiligen Standort.

---

## 5. Die 4 Prinzipien (aus Lou's Reverse-Social-Engineering-Doktrin)

| Prinzip | Konkrete Umsetzung in Carotis-AI |
|---------|-----------------------------------|
| **Full Automation + Human in the Loop** | KI schlägt vor, Arzt entscheidet. Jede Entscheidung loggt das System mit Begründung — diese Begründung trainiert das Modell weiter. |
| **Maßschneidung statt Vast-AI** | Nur Carotis-Bifurkation. Kein generisches "Radiology Foundation Model". Modell ist klein, schnell, lokal lauffähig auf 1 Edge-Server. |
| **Integration + Härtung** | Modul in [DiggAI.de](https://diggai.de) integriert. Air-Gapped Training. Signierte Modelle. Keine Backdoors. Audit-Trail jeder Inferenz. |
| **Local-First mit Batch-Code** | Modell als signiertes ONNX-Bundle (`.exe` / `.dmg` Wrapper). Kein API-Call zum Inferenzieren. Tägliches Retraining lokal. |

---

## 6. Engineering-Harnessing-Methodik

Wir trennen drei Wissensströme und harnessen sie systematisch:

### 6.1 Code-Wissen
- **Repos:** dr-aroob-ki + Dr-Aroob-Portal
- **Harness:** dieser Ordner — CLAUDE.md + MEMORY.md + memory/runs/
- **Modell-Routing:** Opus plant, Sonnet/Haiku führen aus. Jeder Run hinterlässt einen Eintrag in `memory/runs/`.

### 6.2 Klinisches Wissen (das Neue)
- **Capture-Punkt:** Decision-Tree-Mini-UI nach jeder Befundung (siehe `05_DECISION_TREE_HARVESTING.md`)
- **Storage:** `memory/decisions/` (anonymisiert) + `memory/anomalies/` (KI-Mensch-Diskrepanzen)
- **Trainings-Pfad:** Decision-Trees fließen ein als zusätzliche Loss-Komponente (Reasoning-Alignment-Loss — siehe Methodik-Sektion in 05).

### 6.3 Regulatorisches Wissen
- **Quellen:** EU AI Act, MDR 2017/745, DSGVO, DIN EN 62304, ISO 14971
- **Storage:** `regulatory/` (Verträge, ADRs, Risk-Files, Klinische Bewertung)
- **Modell-Pflicht:** keine Antwort an Behörden / Ethikkommission ohne Opus-Review

**Diese drei Ströme reden miteinander:** ein Build-Bug in Layer 1, der eine Anomalie in Layer 2 produziert, die ein Compliance-Risiko in Layer 3 wird, ist ein einziger Audit-Trail-Eintrag, nicht drei. Das ist die eigentliche Engineering-Harness-Idee.

---

## 7. 24-Monats-Plan (Kurzfassung — Detail in 02_ROADMAP.md)

| Phase | Monat | Goal | Status |
|-------|-------|------|--------|
| P0 | jetzt | Rohde-Approval + Office-Docs aktualisiert | 🔄 |
| P1 | M1–M2 | Ethikantrag + Datenvertrag + DSGVO-Setup | 🔒 |
| P2 | M3–M5 | Datenakquise n≥500, Anonymisierung | 🔒 |
| P3 | M6–M9 | Modell-Training MFSD-UNet + Plaque-Klassifikator | 🔒 |
| P4 | M10–M15 | Edge-Integration + UI + Decision-Tree-Capture | 🔒 |
| P5 | M16–M21 | Klinische Validierung DE+JO, Daily-Learning-Loop aktiv | 🔒 |
| P6 | M22–M24 | Manuskript Radiology / JNIS + Disputation | 🔒 |
| P7 | nach M24 | MDR-Class-IIa-Zertifizierung + Skalierung | 🔒 |

---

## 8. Verkaufs­argumente — wer will was

| Stakeholder | Was sie wirklich wollen | Was wir liefern |
|-------------|-------------------------|------------------|
| **Prof. Rohde** | Publikation als Senior-Author + Reputation Klinikum + null DSGVO-Risiko | First-Author-Paper für Aroob (Senior für ihn), Local-First-Architektur, Engineering-Harnessing-Methodik publizierbar als eigenes Paper |
| **Aroob** | Doktor-Titel + nicht 5 Jahre für nichts arbeiten + Ihr Schwager bleibt im Boot | 24-Monats-Plan, klare Deliverables, technisches Team das liefert |
| **Klinikum Dortmund** | KI-Profil aufbauen ohne Datenschutz-Skandal, Förderung aus BMBF | Erste DSGVO-konforme KI-Implementation am Haus, drittmittel-fähig (siehe BMBF KI-in-der-Medizin) |
| **Prof. Margaritoff** | Zeigt-her-was-meine-Schüler-bauen-Material für die HAW | DIN EN 62304-konformer Software-Lebenszyklus, dokumentiert von Anfang an |
| **Prof. Tolg** | Aroob (gute Studentin im Umfeld), VR/Sim-Anbindung möglich | Wir können den Decision-Tree-Korpus in SIMLab-VR-Trainings einbinden — separates Folge-Paper |
| **Dr. Islam** | Patent-Familie ausbauen, JoVision-Profil | Co-Inventor auf Decision-Tree-Harvesting-Patent (USPTO-Provisional in P3) |
| **Sarah Hospital** | Internationale Forschungspartner­schaft, klinische Reputation | Co-Author-Paper, Multi-Center-Validierung-Credit, identisches Edge-System geschenkt |
| **Lou** | Diggai-Plattform mit echtem Medizin-Use-Case validieren, Familienreputation | Carotis-AI als Diggai-Modul nach P5, Skalierung auf weitere Praxen ab P7 |

**Niemand muss aus seiner Komfortzone — wir bringen ihnen die Phase-Outputs zu**.

---

## 9. Risiko-Register (Top 5)

| Risiko | Wahrscheinlichkeit | Schaden | Mitigation |
|--------|---------------------|---------|------------|
| Rohde sagt nein / will nicht betreuen | mittel | hoch | Plan B: Prof. Tolg als Erstgutachter (Aroob ist im HAW-Umfeld), Rohde als Klinik-Mentor — Promotion läuft trotzdem |
| Ethikvotum negativ | niedrig | hoch | Antrag von Opus 4.7 + Margaritoff-Review; minimal-invasives Studiendesign (retrospektiv anonymisiert) |
| Modell erreicht Performance-Ziele nicht | mittel | mittel | Literatur zeigt: MFSD-UNet schafft Dice 0.91 reproduzierbar. Plan B: Modell-Bibliothek mit MONAI/SwinUNETR als Fallback |
| Decision-Tree-Capture wird im Alltag nicht ausgefüllt | hoch | hoch | UX-Design: 30-Sek max, optional, mit Auto-Skip nach 24h. Bei <30 % Coverage: Pflicht-Modus für 4 Wochen pro Quartal |
| Sarah Hospital fällt als Validator weg (Politik / Logistik) | mittel | mittel | Fallback: nur DE-Validierung mit erweiterter Stichprobe (n≥800) — verlässt zwar das transnationale USP, bleibt aber publikationsfähig |

---

## 10. Erste Aktionen (Diese Woche)

| # | Wer | Was | Wann |
|---|-----|-----|------|
| 1 | Lou | `07_OFFICE_AGENT_PROMPTS.md` in Stride ausführen → 5 aktualisierte Office-Docs | heute |
| 2 | Lou + Aroob | Docs gemeinsam reviewen | heute Abend |
| 3 | Aroob | Mail an Prof. Rohde rausschicken (mit Anhängen) | morgen |
| 4 | Lou | Termin-Backup vorbereiten: 12-Folien-Demo-Skript polieren | morgen |
| 5 | Lou | Memory-System initialisieren: `memory/runs/2026-04-27_p0_kickoff.md` schreiben | heute |
| 6 | Lou | Bei Antwort von Rohde: Template 9 (Stakeholder) für Reply nutzen | bei Eingang |

---

## 11. Wann gilt v1.0 als überholt?

- Wenn Rohde nein sagt → Plan B kicken → v2.0 mit Tolg als Erstgutachter
- Wenn Ethikvotum auflagen-pflichtig → v1.1 mit angepasstem Studiendesign
- Bei Phasen-Wechsel von P0 → P1: Master-Plan nicht neu, nur Status-Update am Anfang dieser Datei
- Bei Modell-Fehler in P3, der die Architektur zerlegt: v2.0 mit neuer technischer Architektur

Versionierung: alte Versionen wandern als `04_MASTER_PLAN_<DATUM>_archive.md` ins `archive/`.

---

**Letzte Aktualisierung:** 2026-04-27 · Opus 4.7 (Cowork)
**Nächster Review-Termin:** sobald Rohde antwortet ODER spätestens 2026-05-11 (in 2 Wochen, falls keine Antwort)
