# Dissertations-Hypothesen v1 — Carotis-AI Forschungsprototyp

**Stand:** 2026-05-06
**Kontext:** Kumulative Promotion Aroob (3 First-Author-Paper über 30–36 Monate) + Senior-Authorships für Rohde + Senior/Methods-Autorenschaften für Lou. Aroob-Budget max ~50h über 36 Monate. Lou-Budget ~25–35h/Woche. Forschungsprototyp-Frame nach `memory/domain/zweckbestimmung_master_2026-05-06.md` — keine Hypothese behauptet diagnostische Überlegenheit gegenüber dem Arzt; alle Hypothesen testen Workflow, Verhalten, Technik oder Privacy.

---

## Übersicht — Ranking nach „Impact pro Aroob-Stunde"

| # | Hypothese | Aroob h | Lou h | T2P | Target | IF (~) | Risiko | Score* |
|---|---|---|---|---|---|---|---|---|
| H6 | Edge-Latency | 1 | 40 | 5 Mo | J Digit Imaging | 2.6 | sehr niedrig | 9.0 |
| H3 | Attention-Concordance (public data) | 3 | 60 | 6 Mo | Insights into Imaging | 4.7 | niedrig | 8.5 |
| H1 | Reading-Time-Reduction | 5 | 80 | 9 Mo | JACR / J Digit Imaging | 4.2 | niedrig | 7.6 |
| H5 | Trust-Score & AI-Akzeptanz | 6 | 90 | 12 Mo | NPJ Digital Medicine | 12.4 | mittel | 7.4 |
| H7 | Federated Decision-Tree DE↔Jordan | 4 | 110 | 15–18 Mo | Lancet Digit Health | 30.8 | hoch | 7.0 |
| H4 | Decision-Tree-Cluster („Reading Styles") | 5 | 100 | 12 Mo | Acad Radiol | 3.0 | mittel | 6.6 |
| H2 | Inter-Rater-Variability-Reduction | 8 | 120 | 12 Mo | Eur Radiol | 5.9 | mittel | 6.0 |

*Score = (Impact-Faktor × 1 / (Aroob-h × Time-to-Pub)) normalisiert. Heuristik, kein wissenschaftlicher Index.

---

## Empfohlener Dissertations-Stack (3 von 7)

**Pflicht-Bündel für kumulative Dr.-Arbeit Aroob:**

1. **H3 Attention-Concordance** — Methoden-Erstpaper, public data, schnellster Track. *Erstautor: Aroob (formal), Lou (Co-First-Author oder Methods-Lead).*
2. **H1 Reading-Time-Reduction** — Workflow-Studie, retrospektive Cases, hoher klinischer Wow-Effekt für Rohde. *Erstautor: Aroob.*
3. **H5 Trust-Score** — Human-AI-Interaction, hoher Impact-Faktor, internationale Sichtbarkeit, NVIDIA-/Aroob-Profil-Match. *Erstautor: Aroob.*

**Begleit-Papers (nicht Pflicht, aber Senior-Karriere-Hebel):**
- **H6 Edge-Latency** als Technical Note → Lou Erstautor, Aroob Co-Autor, Rohde Senior. Schnell, niedrige Aroob-Last.
- **H7 Federated** als Drittmittel-Hebel → DFG/BMBF/Industrie-Antrag mit Aroob+Rohde+Sarah-Hospital.

**Reserve falls H3/H1/H5 stockt:** H4 (Reading-Style-Cluster) oder H2 (Inter-Rater).

**Promotionsordnung-Wahl noch offen:** HAW Hamburg (Dr. rer. medic. via van Stevendaal/Margaritoff) vs. Klinikum Dortmund (Dr. med. via Rohde). H3+H1+H5 erfüllen formal beide.

---

## H1 — Reading-Time-Reduction

**Hypothese.** Bei Carotis-CTA reduziert die Anzeige eines KI-Aufmerksamkeits-Heatmap-Overlays die ärztliche Lesezeit im Mittel um ≥30 % bei nicht unterlegener Übereinstimmung mit dem Goldstandard-Befund (Non-Inferiority-Margin 5 % Cohen's Kappa).

**Forschungslücke.** Reading-Time-Studien existieren für Mammographie und CT-Lung-Nodule, aber nicht systematisch für Carotis-CTA mit Decision-Tree-Capture. Bisherige Studien messen entweder Zeit ODER Übereinstimmung, selten beides mit explizitem Reasoning-Capture.

**Operationalisierung.** Crossover-Design: jeder Radiologe liest 30 Cases, 15 mit Overlay, 15 ohne, randomisierte Reihenfolge. Capture: Zeitstempel pro Annotationsschritt, finale Stenose-Kategorie (NASCET-Kategorien).

**Daten.** Retrospektiv n=30 anonymisierte Carotis-CTA aus Klinikum Dortmund oder Klaproth-Praxis. Goldstandard: Konsensus zweier Senior-Radiologen (kann Rohde mit-übernehmen — kontrolliert ihn ein in das Tool und liefert ihm gleichzeitig Co-Author-Material).

**Statistik.** Primärer Endpunkt: mittlere Lesezeit in Sekunden, paired-t-test oder Wilcoxon. Sekundär: Cohen's Kappa Overlay-vs-Goldstandard. Power-Analyse für 30%-Reduktion bei SD ≈ 30s, n=5 Reader × 30 Cases = 150 Lesungen → Power > 0.95 für α=0.05.

**Aroob-Aufwand.** ~5h: 1× Konzept-Review, 1× Methods-Section-Review, 1× Discussion-Beitrag, Co-Lesung von 10 Cases als Goldstandard-Mit-Rater.

**Lou-Aufwand.** ~80h: Studienprotokoll, Anonymisierung, Tool-Setup, Datenakquise-Koordination, Statistik, Manuskript.

**Time-to-Publication.** 9 Monate (3 Mo Datenakquise + 2 Mo Lesungen + 4 Mo Manuskript/Review).

**Target-Journal.** *Journal of the American College of Radiology* (JACR, IF ~4.2) oder *Journal of Digital Imaging* (IF ~2.6). JACR bevorzugt wegen klinischer Relevanz.

**Risiken.** (1) Ethikantrag retrospektiv — meist nur konsultatives Votum, niedriges Risiko. (2) Reader-Recruitment — 5 Radiologen-Ja-Quote über Rohde-Netzwerk wahrscheinlich. (3) Overlay-Effekt eventuell <30% — Pre-Registration bei AsPredicted senkt Bias-Vorwurf.

**MDR-Frame.** Workflow-Studie, kein Diagnoseanspruch des Tools. Tool dient als Forschungsinstrument zur Zeitmessung — Goldstandard bleibt der menschliche Konsensus-Befund.

---

## H2 — Inter-Rater-Variability-Reduction durch Decision-Tree-Capture

**Hypothese.** Strukturierte Decision-Tree-Erfassung reduziert die Inter-Rater-Variabilität bei NASCET-Stenose-Klassifikation (50–69 % vs. 70–99 %) um ≥20 % gemessen als Reduktion der Disagreement-Rate.

**Forschungslücke.** Inter-Rater-Studien zu Carotis-CTA zeigen 15–25 % Disagreement an Klassifikations-Schwellen. Strukturierte Reasoning-Capture (statt freier Befundtext) ist dafür nicht systematisch untersucht — wir messen, ob das Erzwingen explizierter Reasoning-Schritte allein schon Variabilität reduziert.

**Operationalisierung.** Block-Design: Phase 1 freie Befundung (n=50 Cases, 3 Rater); Phase 2 nach 4-Wochen-Washout dieselben 50 Cases mit Decision-Tree-Notebook. Vergleich Cohen's Kappa pro Klassifikations-Schwelle.

**Daten.** n=50 retrospektive anonymisierte Cases; 3 Rater (Aroob + 2 Junior- oder Mid-Level-Radiologen via Rohde).

**Statistik.** Primär: Differenz Cohen's Kappa Phase-2 vs. Phase-1 (Bootstrap-CI). Sekundär: Reasoning-Step-Konkordanz, Lesezeit pro Phase.

**Aroob-Aufwand.** ~8h (sie ist eine der Rater + Methods-Lead).

**Lou-Aufwand.** ~120h (Decision-Tree-Tool-Härtung, Datensetup, Analyse, Manuskript).

**Time-to-Publication.** 12 Monate.

**Target-Journal.** *European Radiology* (IF ~5.9) oder *American Journal of Neuroradiology* (AJNR, IF ~3.5).

**Risiken.** Memory-Effekt zwischen Phase 1 und 2 — Washout muss strikt 4+ Wochen sein. Carryover-Bias.

**MDR-Frame.** Studie über ärztliches Reasoning-Verhalten. Tool ist Capture-Werkzeug, kein Diagnose-Instrument.

---

## H3 — Attention-Map-Concordance auf Public Data

**Hypothese.** HiResCAM-generierte Aufmerksamkeitsregionen des MFSD-UNet-Modells überlappen mit ärztlich annotierten Plaque-/Stenose-Regions of Interest mit Dice ≥ 0.7 (Mittelwert über Validierungs-Set).

**Forschungslücke.** XAI-Concordance-Studien sind für Lung-Nodule, Mammographie und Brain-MRI publiziert, jedoch nicht für Carotis-CTA mit HiResCAM. Generelle Frage „schaut das Modell auf radiologisch sinnvolle Regionen?" ist publikationsreif als Methodenpaper.

**Operationalisierung.** Public-Dataset CADA Challenge 2020 (oder vergleichbar OpenNeuro/NIH) + retrospektive Aroob-/Junior-ROI-Annotationen auf einer Substichprobe. Dice-Score zwischen Heatmap-Threshold und manueller ROI.

**Daten.** Public CADA: n ≈ 100 Carotis-MRA/CTA. ROI-Annotationen auf Substichprobe n=30 — Aroob annotiert 10, 2 Junior-Rater je 10 als Konsensus.

**Statistik.** Mittlerer Dice + 95-%-Bootstrap-CI. Sub-Analyse pro Stenose-Schweregrad.

**Aroob-Aufwand.** ~3h (10 ROI-Annotationen + Plausibility-Review).

**Lou-Aufwand.** ~60h (Public-Data-Pipeline, HiResCAM-Implementation reuse aus bestehendem Code, Dice-Computation, Manuskript).

**Time-to-Publication.** 6 Monate.

**Target-Journal.** *Insights into Imaging* (IF ~4.7, open access) oder *European Radiology Experimental* (IF ~3.5).

**Risiken.** Dice < 0.5 → Resultat ist trotzdem publizierbar als „Limitations of HiResCAM in Carotis-CTA", nur weniger glamourös. Sub-Risiko.

**MDR-Frame.** Pure Methodik auf Public-Data, kein Patientenbezug am Klinikum, keine Ethik-Antrag-Notwendigkeit, ideal als „Reference Implementation accompanying Publication".

---

## H4 — Decision-Tree-Pattern-Clustering („Reading Styles")

**Hypothese.** Ärztliche Entscheidungspfade bei Carotis-CTA-Begutachtung lassen sich in 3–5 reproduzierbare Cluster gruppieren, die mit Berufsjahren und Subspezialisierung korrelieren.

**Forschungslücke.** „Reading Styles" sind in der Mammographie-Literatur beschrieben (z. B. „search vs. evaluation strategies"), aber nicht für Carotis-CTA und nicht via maschinelles Clustering von Decision-Tree-Logs. Behavioral-Studie mit Novelty-Anspruch.

**Operationalisierung.** 8–12 Radiologen lesen je 20 Cases, Decision-Tree-Logs aufgezeichnet. Feature-Extraktion: Reihenfolge der Schritte, Verweildauer pro ROI, Bezugsschritte zwischen Plaque-Komponenten. Hierarchical Clustering + UMAP-Visualisierung. Cluster-Stability via Bootstrap.

**Daten.** Decision-Tree-Logs vom Tool, 8–12 Reader × 20 Cases ≈ 200 Logs. Cases können retrospektiv oder synthetisch (Demo-DICOM-Daten) sein.

**Statistik.** Silhouette-Score, Dunn-Index, Stability-Index. Sekundär: Korrelation Cluster-Zugehörigkeit mit Berufsjahren (Spearman).

**Aroob-Aufwand.** ~5h (eine der Reader + Discussion-Beitrag).

**Lou-Aufwand.** ~100h (Feature-Engineering, Clustering, UMAP, Manuskript).

**Time-to-Publication.** 12 Monate.

**Target-Journal.** *Academic Radiology* (IF ~3.0) oder *Radiology AI* (IF ~9.8 — wenn Methodik stark genug).

**Risiken.** Reader-Rekrutierung 8+ ist Aufwand. Synthetic Cases als Alternative reduzieren ökolog. Validität.

**MDR-Frame.** Verhaltens-Forschung über Radiologen. Tool dient als Verhaltens-Logger.

---

## H5 — Trust-Score & AI-Akzeptanz

**Hypothese.** Der Composite-Trust-Score (Confidence 0.5 + Calibration 0.3 + Transparency 0.2; siehe ADR-006) korreliert mit ärztlicher Akzeptanz von KI-Overlays mit r ≥ 0.6 — signifikant höher als ein alleiniger Confidence-Score (Δr ≥ 0.2).

**Forschungslücke.** Human-AI-Trust ist 2024–2026 ein heißes Feld (NPJ Digit Med, Nat Mach Intell). Spezifisch für radiologische Overlays mit Composite-Trust gibt es Lücken. Aroob-NVIDIA-Profil-Match liefert internationalen Sichtbarkeitsbonus.

**Operationalisierung.** 15 Radiologen × 30 Cases. Bedingung A: Confidence-Score allein, Bedingung B: Composite-Trust-Score. Akzeptanz operationalisiert als (1) Übernahme-Rate des Overlay-Vorschlags, (2) post-hoc Likert-Survey, (3) Modifikations-Rate.

**Daten.** Retrospektiv anonymisiert n=30 Cases. 15 Reader (gemischt Junior/Mid/Senior).

**Statistik.** Pearson-Korrelation Trust-Score vs. Akzeptanz. Vergleich mit Fisher-z-Test. Mixed-Effects-Modell mit Reader als Random-Effect.

**Aroob-Aufwand.** ~6h.

**Lou-Aufwand.** ~90h (Survey-Design, Trust-Score-Implementation reuse, Statistik, Manuskript).

**Time-to-Publication.** 12 Monate.

**Target-Journal.** *npj Digital Medicine* (IF ~12.4) oder *Journal of Digital Imaging* (IF ~2.6) als Sicherheits-Fallback.

**Risiken.** Reader-Rekrutierung 15 ist nicht trivial — Rohde-Netzwerk + Klaproth + ggf. HAW-Klinik-Partnerschaft. Survey-Bias durch Reihenfolge → randomisieren.

**MDR-Frame.** Human-AI-Interaction-Studie. Tool dient als Reizmaterial; klinische Entscheidung wird im Studienkontext explizit nicht aus Tool-Output getroffen.

---

## H6 — Edge-Latency-Benchmark (Local-First Validation)

**Hypothese.** Edge-deployed ONNX-Inference des MFSD-UNet auf einem typischen Klinik-Edge-Server (z. B. RTX-A4000-Klasse oder CPU-only) liefert Carotis-Heatmap-Overlay in ≤ 2.0 Sekunden Median bei Modell-Qualität (Dice) ≤ 2 % unter dem Cloud-GPU-Referenz-Build.

**Forschungslücke.** Local-First / Edge-Inference für Carotis-XAI ist als Konzept präsent, aber latenz-/qualitätsvergleichende Benchmarks publiziert fast niemand transparent. Technical Note mit hohem Sichtbarkeits-Wert in DSGVO-affinem EU-Markt.

**Operationalisierung.** Public-Dataset (CADA), Inference auf 3 Hardware-Profilen: (a) Cloud-GPU-Reference, (b) Edge-GPU, (c) CPU-only. Latenz-Verteilung (p50, p90, p99), Dice-Vergleich.

**Daten.** Public-Dataset, keine Patientendaten.

**Statistik.** Latenz-Verteilungen + Mann-Whitney; Dice-Differenz mit Bootstrap-CI; TOST für Non-Inferiority.

**Aroob-Aufwand.** ~1h (Sign-off + Co-Authorship).

**Lou-Aufwand.** ~40h (Benchmark-Pipeline, Hardware-Setup, Manuskript).

**Time-to-Publication.** 5 Monate.

**Target-Journal.** *Journal of Digital Imaging* (IF ~2.6) oder SPIE Medical Imaging Conference Proceedings.

**Risiken.** Edge-Hardware-Verfügbarkeit. Lösung: Cloud-Edge-Emulation auf gemieteter Instance reicht für Methodik-Beweis.

**MDR-Frame.** Reine technische Benchmark-Studie. Kein Patient-Bezug, kein Diagnose-Anspruch.

---

## H7 — Federated Decision-Tree Aggregation DE↔Jordanien

**Hypothese.** Federated Aggregation von Decision-Tree-Pattern-Statistiken zwischen zwei klinischen Standorten (Klinikum Dortmund + Sarah Specialty Hospital, Amman) liefert Cluster-Strukturen, die mit zentralisierter Aggregation übereinstimmen (Adjusted Rand Index ≥ 0.7), ohne dass Patient- oder Befund-Daten den jeweiligen Standort verlassen.

**Forschungslücke.** Federated Learning für Bildgebung ist publiziert, aber federated Aggregation von Decision-Tree-Reasoning-Patterns als Privacy-Engineering-Beitrag ist weitgehend unbearbeitet. Hoher Hebel für Lancet Digit Health / Nat Med wegen DSGVO-Storyline + internationaler Komponente.

**Operationalisierung.** Aggregations-Protokoll: jeder Standort berechnet Cluster-Statistiken lokal, austauscht nur aggregierte Zentroide+Counts (k-Anonymity ≥ 5). Vergleich mit hypothetisch-zentralisierter Aggregation als Goldstandard auf Cross-Validation-Hold-Out.

**Daten.** Decision-Tree-Logs aus beiden Standorten, Substichprobe je n ≈ 100 Logs. Keine Patientenbilder, keine PII verlassen die jeweilige Einrichtung. AVV/Datenschutz-Vereinbarung Klinikum-↔-Sarah erforderlich.

**Statistik.** Adjusted Rand Index, Mutual Information. Privacy-Audit: Pseudonymisierungs-Stärke, k-Anonymity-Verifikation.

**Aroob-Aufwand.** ~4h (NVIDIA-Bezug + Federated-Learning-Domänenwissen + Sarah-Hospital-Brücke).

**Lou-Aufwand.** ~110h (Federated-Protokoll, Crypto/Aggregation-Implementierung, internationale Koordination, Manuskript).

**Time-to-Publication.** 15–18 Monate.

**Target-Journal.** *Lancet Digital Health* (IF ~30.8) oder *npj Digital Medicine* (IF ~12.4).

**Risiken.** Internationale Datenvereinbarung → 3–6 Monate Vertragsanbahnung. Sarah-Hospital-Bandwidth ungewiss. Mitigation: starten mit Klinikum-Dortmund + HAW Hamburg als Standort 2.

**MDR-Frame.** Privacy-Engineering-Studie. Tool dient als Aggregations-Referenz, keine klinische Diagnose involviert.

---

## Reserve-Hypothesen (H8–H10, falls Plan B nötig)

- **H8 — Reporting-Quality.** Decision-Tree-Capture verbessert die Vollständigkeit strukturierter Carotis-Befunde gegenüber freiem Befundtext (CARDS-/RADS-Konformität-Score).
- **H9 — Resident vs. Senior Reading-Patterns.** Decision-Tree-Cluster unterscheiden Assistenzärzte und Fachärzte auf Basis von Reasoning-Pfaden (Klassifikator-AUC).
- **H10 — Annotation-Burden vs. Yield.** Trade-off-Studie: wie viel Annotations-Aufwand pro Reasoning-Insight liefert das Tool?

Diese drei sind nur skizziert — bei Bedarf voll ausarbeiten.

---

## 36-Monats-Plan

```
Monat  1  3  5  7  9  11 13 15 17 19 21 23 25 27 29 31 33 35
H6     ████ Submit
H3     ██████ Submit
H1     █████████ Submit
H5     █████████████ Submit          (Aroob Mid-PhD)
H7     █████████████████ Submit
       (parallel Drittmittelantrag laufend)
H4     ██████████████████ Submit (optional — falls H7 stockt)
```

- **Monat 5:** H6 submitted (Lou first-author Technical Note).
- **Monat 6:** H3 submitted (Aroob first-author + Lou co-first oder Methods-Lead).
- **Monat 9:** H1 submitted (Aroob first-author).
- **Monat 12:** H5 submitted (Aroob first-author, NVIDIA-Profile-Match).
- **Monat 15–18:** H7 submitted oder als Drittmittelantrag-Hebel.
- **Monat 24:** Aroob hat 3 First-Author-Papers → Promotion einreichbar.
- **Monat 30–36:** Disputation.

---

## Multi-AI-Workflow pro Hypothese

| Schritt | Tool | Wer |
|---|---|---|
| Studienprotokoll-Skelett | Claude Opus 4.7 | Lou |
| Lit-Review (1 M-Context) | Gemini 2.5 Pro | Lou |
| Code/Pipeline | Claude Sonnet 4.6 + Copilot | Lou |
| Statistik-Plan + Power | GPT-5.5 second opinion | Lou |
| Manuskript Erstdraft | Opus 4.7 | Lou |
| Peer-Review-Simulation | Opus 4.7 (Reviewer-Rolle) | Lou |
| Stride/Office-Doc-Generation | Stride V2 / M365 Copilot | Lou |
| Aroob-Touchpoint-PDF | Opus 4.7 + Microsoft 365 | Lou |
| Submit-Cover-Letter | Opus 4.7 | Lou |

**Aroob-Touchpoint-Format pro Paper:** 1 PDF (Final-Draft mit 3 explizit markierten *„Hier 3 Sätze ergänzen"*-Stellen) + 1 Loom-Video (5 Min Status) + 1 Slack-Thread für Rückfragen. Sie öffnet eines, kommentiert, fertig.

---

## Notion-Import-Instructions

**Variante A — Schnellster Import (5 Min):**

1. In Notion: neuer Page → `Import` → Markdown.
2. Diese Datei (`outputs/dissertation_hypotheses_v1_2026-05-06.md`) hochladen.
3. Notion erkennt Tabellen + Headings korrekt.

**Variante B — Volle Database-Integration (30 Min):**

1. In Notion: Neue Page → Database → Table.
2. Properties anlegen:

```
Title (Text)            → Hypothese-Titel
ID (Text)               → H1..H7
Aroob_h (Number)        → 1..8
Lou_h (Number)          → 40..120
T2P_months (Number)     → 5..18
Target_Journal (Select) → JACR / Eur Radiol / NPJ Digit Med / ...
IF (Number)             → 2.6..30.8
Risk (Select)           → niedrig / mittel / hoch
Status (Select)         → Backlog / In-Progress / Submitted / Published
First_Author (Select)   → Aroob / Lou
Phase (Select)          → P0g / P1 / P2 / P3
Tags (Multi-Select)     → Workflow / Behavior / Privacy / Tech / XAI
```

3. 7 Datensätze anlegen aus der Übersichtstabelle oben.
4. Sub-Page pro Hypothese mit dem jeweiligen Detailblock H1..H7.
5. Optional Linked-View pro Phase im 36-Monats-Plan.

**Variante C — CSV-Import:** ich liefere auf Anfrage ein 7-Zeilen-CSV mit den Feldern oben (`gp csv`).

---

## Nächste konkrete Schritte

1. Stack-Entscheidung: H3 + H1 + H5 als Pflicht-Bündel bestätigen oder umpriorisieren.
2. Promotionsordnung-Wahl: HAW Hamburg (Margaritoff/van Stevendaal) vs. Klinikum Dortmund (Rohde) — bestimmt Erstgutachter und damit Formalia.
3. H6 als „Quick-Win" sofort starten — Lou allein, ~5 Monate, kaum Aroob-Last → liefert frühen Beweis für Rohde, dass produktiv geliefert wird.
4. H3 parallel: Public-CADA-Daten ziehen, Heatmap-Pipeline aus bestehender Codebasis hochfahren.
5. Aroob-Briefing-PDF (1 Seite) mit den drei Pflicht-Hypothesen + ihrer Rolle pro Paper.
6. Rohde-Anschreiben-Update: nicht „24-Monate-Roadmap" pitchen, sondern konkret „1 Konferenz-Abstract + 3 Paper als Senior-Autor, ~12h Ihrer Zeit total".

---

## Verbindung zur kanonischen Zweckbestimmung

Alle 7 Hypothesen sind kompatibel mit `memory/domain/zweckbestimmung_master_2026-05-06.md`. Keine Hypothese behauptet diagnostische Überlegenheit des Tools über den Arzt. Tool dient durchgängig als:
- **Workflow-Logger** (H1, H2, H4)
- **Verhaltens-Capture-Werkzeug** (H4, H5)
- **Methodik-Referenz** (H3, H6)
- **Privacy-Aggregations-Referenz** (H7)

Submit-Cover-Letter zitiert Block B aus der Master-Zweckbestimmung als Methods-Disclaimer.

**Letztes Update:** 2026-05-06
