---
name: refs_regulatory
description: Regulatorische Quellen — EU AI Act, MDR 2017/745, DSGVO/GDPR, DIN EN 62304, ISO 14971. Pointer auf offizielle Texte + lokale Auslegungs-Notizen.
type: reference
last_updated: 2026-04-27
---

# Regulatorischer Rahmen — Quellen & Auslegung

## EU AI Act (Verordnung (EU) 2024/1689)

- **Offizieller Text:** EUR-Lex 32024R1689 — https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- **Carotis-AI Klassifikation:** **High-Risk AI System** (Annex III, Punkt 5 — KI für medizinische Diagnose)
- **Relevante Artikel:**
  - **Art. 9** — Risk Management System (verpflichtend, kontinuierlich)
  - **Art. 10** — Data and Data Governance (Trainings­daten dokumentiert, bias-getestet, repräsentativ)
  - **Art. 11** — Technical Documentation (Annex IV-Format)
  - **Art. 12** — Record-keeping (Audit-Trail jedes Inferenz-Events)
  - **Art. 13** — Transparency and Provision of Information (Grad-CAM erfüllt das in unserer Lesart)
  - **Art. 14** — Human Oversight (Human-in-the-Loop ist Pflicht; wir designen das nativ ein)
  - **Art. 15** — Accuracy, Robustness, Cybersecurity (Performance-Threshold + Auto-Rollback)
- **Inkrafttreten:** schrittweise, High-Risk-Provisions ab 02.08.2026
- **Carotis-AI-Status:** wir bauen ab P0 darauf hin, MDR-Bundle in P7 enthält AI-Act-Konformitäts-Erklärung

## MDR — Medical Device Regulation (Verordnung (EU) 2017/745)

- **Offizieller Text:** EUR-Lex 32017R0745 — https://eur-lex.europa.eu/eli/reg/2017/745/oj
- **Carotis-AI Klassifikation:** **Klasse IIa** (Rule 11 Annex VIII — Software für Diagnose-Information ohne autonome Entscheidung)
- **Wenn wir auf Klasse IIb hochstufen** (z.B. wenn das System direkt Therapie-Entscheidungen treibt): Annex IX vollständige QM-Audits + benannte Stelle
- **Wir bleiben in IIa**, weil: HITL-Design, Arzt entscheidet final, keine autonome Befundung
- **Folgen für die Tech-Doc:** Annex II vollständig, klinische Bewertung nach Annex XIV
- **Status:** Tech-Doc-Skelett in P1 starten, Vollständigkeit zur Disputation in P6

## DSGVO / GDPR — Datenschutz-Grundverordnung

- **Offizieller Text:** EUR-Lex 32016R0679 — https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Relevante Artikel:**
  - **Art. 9** — Besondere Kategorien (Gesundheitsdaten, ausdrückliche Einwilligung erforderlich)
  - **Art. 25** — Privacy by Design and by Default (unser Local-First-Setup erfüllt das nativ)
  - **Art. 32** — Sicherheit der Verarbeitung (Verschlüsselung, Pseudonymisierung)
  - **Art. 35** — Datenschutz-Folgenabschätzung (DPIA) — bei High-Risk-AI verpflichtend
- **Carotis-AI-Setup:**
  - DPIA-Skelett in P1 (`ethics/dpia_skelett.md`)
  - AVV (Auftragsverarbeitungs­vertrag) zwischen Klinikum Dortmund und Lou/HAW
  - DICOM PS 3.15 Anonymisierungs-Profile vor jedem Modell-Training

## DIN EN 62304 — Software-Lebenszyklus für Medizinprodukte

- **Offiziell:** beim Beuth-Verlag kostenpflichtig
- **HAW-Hamburg-Zugang:** über Prof. Margaritoff verfügbar (sie lehrt 62304)
- **Anwendung in Carotis-AI:** Software-Sicherheitsklasse **B** (Verletzung möglich, kein Tod) — pragmatisch, weil HITL
- **Pflicht-Doku:** Software-Plan, Software-Entwicklungs-Prozess, Risk-Management, Configuration-Management, Problem-Resolution
- **Templates:** in P1 erstellen, Margaritoff reviewt Quartal 1

## ISO 14971 — Risk Management for Medical Devices

- **Offiziell:** ISO direkt, kostenpflichtig
- **HAW-Zugang:** vorhanden
- **Carotis-AI Risk File:** `risk_register.md` ist erster Stand (Hazard-Identifikation), wird in P1 nach 14971-Format erweitert
- **Risk Control Measures müssen** im Modell + UI + Workflow + Doku verankert sein. Auto-Rollback im Daily-Loop ist eine ISO-14971-RCM.

## BSI — Bundesamt für Sicherheit in der Informationstechnik

- **IT-Grundschutz-Kompendium:** https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/IT-Grundschutz/it-grundschutz_node.html
- **Krankenhauskontext:** B 2.18 (Krankenhausinformations­system) — Local-First-Architektur erfüllt erhöhte Schutzbedarfsklasse
- **Status:** als Sekundär-Quelle für Audit-Trail-Design genutzt

## Lokale Auslegungs-Notizen

### „High-Risk" vs. „Limited-Risk" KI

Wir argumentieren **High-Risk** offensiv, nicht defensiv. Begründung: dadurch sind die Compliance-Strukturen stabil unter Updates der KI-Regulierung. Hochstufen kostet nichts, runterstufen wäre Aufwand.

### „Software as a Medical Device" (SaMD) vs. „Software in a Medical Device" (SiMD)

Carotis-AI ist **SaMD** — eigenständiges Software-Produkt, nicht eingebettet in ein Hardware-Gerät. Konsequenz: eigene MDR-Klassifikation, eigene CE-Kennzeichnung, eigene technische Doku.

### „Forschungs-Software" vs. „Medizinprodukt"

In den ersten 18 Monaten (P0–P5) ist Carotis-AI **Forschungs-Software** — nicht-zertifiziert, nur in der klinischen Studie unter Aufsicht. Erst in P7 nach Disputation: regulatorischer Übergang zu Medizinprodukt mit CE.

Wichtig für Aroob's Promotion: die Studienteilnehmer­einwilligung muss explizit machen, dass das System **Forschungs-Software** ist.

## Wartung

Bei jedem neuen Auslegungs-Hinweis (z.B. Margaritoff-Konsultation, BSI-Update, EU-AI-Act-Implementing-Act):
- 1-Zeile in „Lokale Auslegungs-Notizen" oben
- Wenn substanziell: ADR in `regulatory/adr/` schreiben
