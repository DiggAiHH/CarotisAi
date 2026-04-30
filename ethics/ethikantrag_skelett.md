# Ethikantrag — Skelett

**An:** Ethikkommission der Ärztekammer Westfalen-Lippe
**Adresse:** Gartenstraße 210–214, 48147 Münster
**Online-Portal:** [aekwl.de Ethikkommission](https://www.aekwl.de/fuer-aerzte/ethikkommission/)

---

## Antragstellende

| Feld | Wert |
|------|------|
| **Studienleiterin** | Aroob Alrawashdeh, Ärztin in Weiterbildung für Radiologie |
| **Klinik / Institut** | Klinik für Radiologie und Neuroradiologie, Klinikum Dortmund |
| **Wissenschaftlicher Betreuer (PI)** | Prof. Dr. med. Stefan Rohde, Direktor (Klinik für Radiologie und Neuroradiologie, Klinikum Dortmund) |
| **Co-Studienleiter (technisch)** | Laith Alshdaifat, Medizintechnik-Ingenieur, HAW Hamburg |
| **Wissenschaftliche Beratung** | Prof. Dr. Petra Margaritoff (HAW Hamburg, Medical Software / DIN EN 62304); Prof. Dr. Boris Tolg (HAW Hamburg, SIMLab); Prof. Dr. Udo van Stevendaal (HAW Hamburg, Medizintechnik) |
| **Externe Kooperation** | Sarah Specialty Hospital, Amman, Jordanien (klinische Validierung) |
| **Kontakt** | [Aroob Klinikum-Mail] |

---

## 1. Titel der Studie

„Entwicklung und transnationale Validierung eines lokal betriebenen, erklärbaren KI-basierten Clinical Decision Support Systems (CDSS) zur Quantifizierung der Carotis-Stenose und Plaque-Vulnerability aus CT-Angiographie-Bilddaten unter Berücksichtigung der DSGVO und des EU AI Act"

**Kurztitel:** Carotis-AI

---

## 2. Wissenschaftliche Fragestellung

**Primäre Frage:** Inwiefern kann ein lokal betriebenes, erklärbares MFSD-UNet-basiertes Clinical Decision Support System die Inter-Observer-Variabilität bei der Carotis-Stenose-Quantifizierung aus CTA-Bildern reduzieren und vulnerable Plaques zuverlässiger identifizieren als die konventionelle Befundung?

**Sekundäre Frage:** Verbessert die systematische Erfassung der ärztlichen Begründungs-Strukturen („Decision-Tree-Harvesting") die Performance des Modells über die Zeit messbar?

**Endpunkte:**
- **Primär:** Reduktion der Inter-Observer-Variabilität (Cohen's Kappa) um ≥ 30 %
- **Sekundär 1:** Sensitivity ≥ 0.92 für Stenose-Detektion (vs. Konsens-Ground-Truth)
- **Sekundär 2:** AUC ≥ 0.85 für Plaque-Vulnerability-Klassifikation
- **Sekundär 3:** Messbare Performance-Verbesserung über mind. 8 Trainings-Iterationen

---

## 3. Hintergrund und Begründung

[Aroob füllt aus — siehe `04_MASTER_PLAN.md` Sektion 3 als Vorlage und `08_RESEARCH_ATTENTION_2020-2026.md` für Literatur-Belege]

Kernpunkte:
- Carotis-Stenose ist Risikofaktor Nr. 1 für ischämischen Schlaganfall
- Inter-Observer-Variabilität bei Stenose-Quantifizierung 15–30 %
- Bestehende KI-Lösungen sind cloud-basiert (DSGVO-Risiko), nicht erklärbar (EU-AI-Act-relevant), nicht spezifisch für Carotis
- Lücke: keine local-first, erklärbare, carotis-spezifische Lösung publiziert

---

## 4. Studiendesign

**Studientyp:** Kombiniert retrospektiv-prospektiv, monozentrisch (Klinikum Dortmund) mit transnationaler Validierungs-Komponente (Sarah Hospital).

**Phase Retrospektiv (M3–M5):**
- n ≥ 500 CTA-Studien aus dem Klinikum-PACS, anonymisiert
- Ground Truth durch Aroob (Erst-Befundung) + Konsens-Lesung mit Zweit-Radiologe für n=50-Inter-Observer-Subset

**Phase Prospektiv (M16–M21):**
- n ≥ 200 prospektiv DE (Klinikum Dortmund)
- n ≥ 100 prospektiv JO (Sarah Hospital)
- Standardisierte Befundung mit aktivem KI-Vorschlag + 30-Sekunden-Decision-Tree-Capture

**Patienteneinschluss:**
- Erwachsene Patienten (≥ 18 Jahre)
- CTA der Carotis aus klinischer Routine (keine Studien-spezifische Bildgebung)
- Schriftliche Einwilligung (für prospektiven Teil) bzw. Opt-Out-Verfahren (für retrospektiven anonymisierten Teil — siehe Sektion 7)

**Patientenausschluss:**
- Patienten unter 18 Jahre
- CTA mit nicht-diagnostischer Bildqualität
- Schwangere
- Aktiver Widerspruch zur wissenschaftlichen Datennutzung im Patienten-Stammdatensatz

---

## 5. Datenfluss

```
Klinikum-PACS  →  DICOM-Export-Skript  →  Anonymisierungs-Pipeline (DICOM PS 3.15 Basic
                                          + k-Anonymity ≥ 5)  →  Lokaler Training-Server
                                          (geschlossen, ohne Internet-Anbindung)

Lokaler Training-Server  →  signiertes ONNX-Modell-Bundle  →  Edge-Server im Klinikum
(kein Patientendaten-Pfad zurück)

Edge-Server  →  AI-Vorschlag + Decision-Tree-Form  →  Aroob (Bestätigung / Korrektur)  →  Audit-DB lokal
```

**Kein Patientendaten-Pfad führt durch eine Cloud oder ein externes Netzwerk.** Sarah-Hospital-Daten werden in JO anonymisiert und nur als signiertes Modell-Update zurück nach DE transportiert (Air-Gap zu DE-Patientendaten).

---

## 6. Anonymisierung & Datensicherheit

- **DICOM-Anonymisierung:** DICOM PS 3.15 Basic Application Confidentiality Profile, alle 33 PII-Tags entfernt
- **k-Anonymity:** Mindest-Level k ≥ 5 für jede Quasi-Identifier-Kombination (Alter-Bucket × Geschlecht × Modalität × Studienjahr × Land)
- **Salt-Rotation:** quartalsweise; Re-Identifizierung selbst durch Insider erfordert Salt-Datenbank, die nur lokal in Klinikum-Audit-Trail liegt
- **Verschlüsselung:** Edge-Server-Disk verschlüsselt (LUKS), Modell-Bundles signiert (Sigstore o. ä.)
- **Audit-Trail:** jede AI-Inferenz und jede Arzt-Entscheidung wird mit Timestamp + Versions-Hash geloggt
- **Penetration-Tests:** quartalsweise durch Prof. Margaritoff oder externen Auditor

Detail in `regulatory/risk_register.md` Hazard H-001 + RCMs sowie `scripts/anonymize.py` (Implementierung mit Tests).

---

## 7. Patienteneinwilligung

**Retrospektive Phase:** Patientendaten der letzten 5 Jahre werden nach DICOM PS 3.15 + k-Anonymity ≥ 5 anonymisiert. Wir argumentieren auf Basis von §27 BDSG (Forschungs-Privileg) und Art. 9 Abs. 2 lit. j DSGVO, dass eine Re-Einwilligung nicht erforderlich ist, weil:
- Daten-Anonymisierung verhindert Re-Identifizierung
- Patient könnte zustimmen, hat aber kein berechtigtes Interesse am Widerspruch (Forschungs-Privileg)
- Klinikum-Aushänge informieren über die laufende Forschungs-Tätigkeit (Opt-Out im Patienten-Stammdatensatz)

**Prospektive Phase:** Schriftliche Einwilligung (siehe `einwilligungserklaerung.md`) mit voller Patientenaufklärung über:
- Studienzweck
- KI-Unterstützung der Befundung
- Kein Einfluss auf die individuelle Behandlung (HITL — Arzt bleibt Entscheider)
- Recht auf Widerruf jederzeit, ohne Folgen für die medizinische Versorgung
- Datenanonymisierung vor jeder weiteren Verarbeitung

---

## 8. Risikobewertung für die Studienteilnehmer

**Direkte Risiken durch die Studie: keine.**
- Keine zusätzliche Bildgebung über die klinische Routine hinaus
- Keine zusätzliche Strahlenbelastung
- Keine Eingriffe oder zusätzlichen Untersuchungen
- Keine Therapie-Änderung (KI ist nur Assistenz, Arzt entscheidet wie bisher)

**Indirekte Risiken:**
- Anonymisierungs-Leck: Severity S5, Likelihood L1, Score 5 nach RCM (siehe `risk_register.md` H-001)
- Falscher AI-Vorschlag wird unkritisch übernommen: durch HITL + Konfidenz-Anzeige + Grad-CAM mitigiert (H-002)

---

## 9. Datenschutz-Folgenabschätzung (DPIA)

Separates Dokument: `dpia_skelett.md`. Wird parallel mit dem Datenschutz-Office des Klinikums Dortmund erstellt und ist Anlage 3 dieses Antrags.

---

## 10. Statistik

**Power-Berechnung:** Für die primäre Hypothese (Reduktion der Inter-Observer-Variabilität um ≥ 30 %) bei α = 0.05 und Power = 0.80 ergibt sich aus Vergleichbarkeits­tabellen für Cohen's Kappa eine Mindest-Stichprobe von n = 200 prospektiv (Detail-Berechnung in Statistik-Anhang).

**Auswertungs-Methoden:**
- Cohen's Kappa für Inter-Observer-Variabilität (vor / nach KI)
- Sensitivity / Specificity / Dice / AUC mit 95% CIs
- Bland-Altman für Stenosegrad-Übereinstimmung
- Lernkurven für Daily-Learning-Loop-Effekt

---

## 11. Datenarchivierung & -löschung

- Anonymisierte Daten: 10 Jahre nach Studienabschluss (akademischer Standard)
- Audit-Trail: 25 Jahre (regulatorische Anforderung)
- Original-Patienten-Mapping: nicht vorhanden — niemand kann zurück auf Patient identifizieren
- Modell-Bundles: dauerhaft archiviert mit Hash + Reproducibility-Manifest

---

## 12. Veröffentlichungs-Plan

- Klinisches Validierungs-Paper: Radiology oder Journal of NeuroInterventional Surgery
- Methodisches Paper (Decision-Tree-Harvesting): Medical Image Analysis oder NEJM AI
- Beide mit Prof. Rohde als Senior-Author
- Open-Access angestrebt (HAW-Förderung möglich)

---

## 13. Finanzierung

- Eigenmittel / Familieninvestition (Lou Alshdaifat / DiggAI)
- HAW-Hamburg-Infrastruktur (Beratung + Workstation für Modell-Training)
- Klinikum-Dortmund stellt nur Workspace + Edge-Server bereit (keine Drittmittel über die Klinik nötig)
- Sarah-Hospital trägt eigene Edge-Hardware-Kosten in JO

---

## Anlagen

1. `patienteninformation.md` (für prospektive Teilnehmer)
2. `einwilligungserklaerung.md` (für prospektive Teilnehmer)
3. `dpia_skelett.md` (Datenschutz-Folgenabschätzung)
4. `risk_register.md` (ISO-14971-Format Risk-Register)
5. CV Aroob Alrawashdeh
6. CV Lou Alshdaifat (`CV_Laith_Alshdaifat.md`)
7. Studienprotokoll-Detail (separates Dokument, P1)

---

**Stand:** Skelett 2026-04-27
**Status:** Vor Einreichung MUSS reviewed werden durch Aroob, Lou, Prof. Margaritoff, Datenschutz-Office Klinikum, Anwalt Medizinrecht.
