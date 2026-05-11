# Stride-V2-Re-Frame Prompts — Forschungsprototyp-Sprache

**Datum:** 2026-05-10
**Quelle:** `memory/domain/zweckbestimmung_master_2026-05-06.md`
**Auftraggeber:** Lou
**Zielgruppe:** Lou führt jeden Stride-Prompt eigenständig in Word/LibreOffice aus (CLAUDE.md-konform: "Office-Dokument-Edits direkt von einem Modell — Modelle generieren Stride-Prompts, Lou führt sie aus")
**Eingabe:** 7 Doks im Ordner `Stride V2/`
**Ausgabe:** 7 Doks v3 (Forschungsprototyp-konform, MDR-Class-IIa-frei)

---

## Globale Substitutions-Tabelle (in JEDEM Dok mit Find/Replace)

Word: `Strg+H` → "Suchen und Ersetzen" → ganzes Dokument.

| Suchen (alt) | Ersetzen (neu) |
|---|---|
| Diagnoseassistent | Workflow- und Decision-Tree-Capture-Tool |
| Diagnose-Assistent | Workflow- und Decision-Tree-Capture-Tool |
| Stenose-Messung | Aufmerksamkeits-Heatmap |
| Stenosemessung | Aufmerksamkeits-Heatmap |
| KI-Befund | Forschungs-Referenz-Overlay |
| Plaque-Vulnerability-Score | Forschungsmerkmals-Aggregat |
| Plaque-Vulnerability | Forschungs-Merkmals-Cluster |
| automatische Quantifizierung | strukturierte Datenerfassung |
| Klinikum-Pilot | Forschungsbeobachtung |
| Validierung gegen Goldstandard | Übereinstimmungs-Forschung |
| MDR-Pfad | Forschungsexemption + § 11 MPDG-Optionalität |
| CE-Marke | Forschungsexemption |
| Class IIa | Forschungsprototyp (kein Medizinprodukt) |
| Anwender | Forscher |
| Nutzer | Forschungsteilnehmer |
| Befund-Output | Forschungs-Datensatz |
| Diagnose-Output | Forschungs-Datensatz |
| MDR-Zertifizierung | Spätere § 11 MPDG-Eigenherstellung (Klinikum-Verantwortung) |

**Globaler Header-Banner (oben in jedem Dok einfügen, vor erstem Inhaltsabschnitt):**

> **Status:** Forschungsprototyp · kein Medizinprodukt im Sinne der MDR (EU 2017/745) bzw. § 3 Nr. 1 MPDG · keine klinische Diagnose- oder Therapiegrundlage.

**Globaler Footer (auf jeder Seite, klein):**

> RESEARCH USE ONLY · Forschungsverwendung · Kein Medizinprodukt

---

## Dok 1 — `Anschreiben_Aroob_an_Rohde_v2.docx`

**Status:** Veraltet — Autorenschaft-Frame muss raus, da Aroob noch nicht informiert ist (siehe Aroob_Status_Briefing_v1).

**Aktion:** Aktuell **nicht** überarbeiten. Erst nach Aroob-Sync-Call freigeben oder ersetzen durch neues Mail-Drafting (Task #9 Rohde-Mail v4).

**Sondervermerk:** Diese Datei in `Stride V2/_archiv/` verschieben, damit kein versehentlicher Versand passiert.

---

## Dok 2 — `Carotis_AI_Konzept_v2.docx`

**Stride-Prompt (in Word ausführen):**

1. Globale Substitutions-Tabelle laufen lassen (siehe oben).
2. Header-Banner einfügen.
3. Suche Abschnitt "Zweckbestimmung" oder "Intended Use" — komplett ersetzen durch Master-Zweckbestimmung Variante A (Langform) aus `memory/domain/zweckbestimmung_master_2026-05-06.md` §A. Wörtlich übernehmen.
4. Suche Abschnitt "Regulatorischer Pfad" oder "MDR" — ersetzen durch:
   > Carotis-AI ist als Forschungsprototyp positioniert und unterfällt nicht den Anforderungen der MDR (EU 2017/745). Eine etwaige spätere klinische Anwendung im Rahmen der Eigenherstellung in Gesundheitseinrichtungen gemäß § 11 MPDG / Art. 5(5) MDR liegt in der Verantwortung der jeweiligen Einrichtung und ist nicht Teil dieser Lieferung.
5. Falls Modul-Tabelle vorhanden: Modul E (CDS / Stenose-Quantifizierung) als "deaktiviert per Feature-Flag" markieren.
6. Footer-Watermark auf jeder Seite einfügen (Word: "Einfügen → Kopf-/Fußzeile → Fußzeile bearbeiten").
7. Speichern als `Carotis_AI_Konzept_v3.docx`.

---

## Dok 3 — `Carotis_Ai_Rohde_v2.docx`

**Stride-Prompt:**

1. Globale Substitutions-Tabelle.
2. Header-Banner.
3. Erster Absatz / Pitch-Hook — falls medizinisch-diagnostisch formuliert, ersetzen durch:
   > Carotis-AI ist ein lokal ausführbarer Forschungsprototyp zur strukturierten Erfassung ärztlicher Entscheidungspfade und Workflow-Charakteristika in der neuroradiologischen Carotis-CTA-Begutachtung. Das Werkzeug ist kein Medizinprodukt und nicht zur klinischen Diagnostik bestimmt.
4. Abschnitt "Was bisher gebaut wurde" — abgleichen gegen `Aroob_Status_Briefing_v1.md` §2 (Online-Demo carotis.diggai.de, Viewer, HiResCAM, Workflow-Capture, Audit, Splash-Gate). Übernehmen.
5. Abschnitt "Mehrwert für Klinikum Dortmund" — neu formulieren:
   > Forschungsbeitrag zur retrospektiven Auswertung dokumentierter Carotis-CTA-Entscheidungspfade mit Anschlussmöglichkeit an das DeGIR/DGNR-Register-Subset des Klinikums. Anbindung an die etablierte UKE-Hamburg-KI-Kooperation methodisch denkbar.
6. Falls "Diagnose-Genauigkeit" / "Sensitivität-Spezifität" als Verkaufsargument auftaucht: ersetzen durch "methodische Reproduzierbarkeit auf öffentlichen Referenz-Datensätzen (ImageCAS, CADS-Dataset)".
7. Footer-Watermark.
8. Speichern als `Carotis_Ai_Rohde_v3.docx`.

---

## Dok 4 — `Expose_Carotis_AI_Rohde_v2.docx`

**Stride-Prompt:**

1. Globale Substitutions-Tabelle.
2. Header-Banner.
3. Studientitel-Vorschlag im Kopfteil — wenn alter Titel medizinprodukthaft, ersetzen durch Master-Zweckbestimmung §F Variante 3 (empfohlen für Ethikkommission):
   > **Reading-Time- und Annotation-Pattern-Analyse bei der Carotis-CTA-Begutachtung — eine retrospektiv-strukturierte Forschungsbeobachtung am Klinikum Dortmund.**
4. "Hypothesen" / "Fragestellung" — schärfen auf workflow-orientierte Endpunkte, weg von diagnostischen Endpunkten:
   - Primär: Reading-Time-Verteilung in der Carotis-CTA-Begutachtung mit/ohne Workflow-Capture-Tool
   - Sekundär: Konkordanz Junior- vs. Senior-Reader in Decision-Tree-Verzweigungen
   - Tertiär: Übereinstimmungs-Forschung (vormals "Validierung") gegen retrospektive Klinikum-Befunde
5. "Methodik" — ergänzen mit Verweis auf öffentliche Datensätze (ImageCAS 1.000 Fälle, CADS-Dataset 167 Strukturen) als methodische Reproduktions-Basis und auf Guo et al. 2024 *Frontiers in Neurology* als Single-Center-Baseline, deren Multi-Center-Reproduktion das Projekt leistet.
6. "Klinische Relevanz" — umformulieren in "Wissenschaftliche Relevanz". Begründung: Workflow-Daten in der Neuroradiologie sind methodisch unter-erforscht; das Werkzeug schließt diese Lücke ohne diagnostischen Anspruch.
7. "Risiko / Compliance" — ergänzen:
   > Die Studie beinhaltet keine prospektive Patientenintervention. Es werden ausschließlich retrospektiv und anonymisiert dokumentierte CTA-Aufnahmen ausgewertet. Eine Ethikvotum-Anfrage am Klinikum Dortmund ist vorgesehen.
8. Footer-Watermark.
9. Speichern als `Expose_Carotis_AI_Rohde_v3.docx`.

---

## Dok 5 — `KI_Tools_Marktanalyse_v2.pdf`

**Stride-Prompt:**

PDF — Lou hat keine Word-Quelle? Falls Quelle existiert, dort editieren. Falls nur PDF: in LibreOffice/Word importieren, oder in Markdown nachziehen.

1. Globale Substitutions-Tabelle (LibreOffice Find&Replace funktioniert auf importierten PDFs).
2. Header-Banner.
3. **Wichtig** — Markt-Übersicht aktualisieren mit Recherche-Befunden vom 2026-05-10:
   - **Carotis-spezifisch (FDA cleared):** Qure.ai qER-CTA (LVO ICA + ACM M1)
   - **Plaque-Analyse FDA cleared (übertragbar):** Elucid PlaqueIQ, Circle CVI cvi42|Plaque, HeartFlow Plaque (Next Gen, +21% Detection), Caristo CaRi-Plaque
   - **Synthetische CTA via DL** (Aorta + Carotis, methodisch relevant): mehrere Studien 2024–2025 in *European Radiology* / *Radiology AI*
   - **Methodische Single-Center-Baseline:** Guo et al. 2024 *Frontiers in Neurology* DOI 10.3389/fneur.2024.1480792 — Diagnosezeit ~6 Sekunden vs. signifikant längere Radiologen-Lesezeiten
4. Eigene Positionierung re-formulieren als Forschungsprototyp:
   > Carotis-AI positioniert sich nicht im FDA-510(k)/CE-Markt, sondern als methodischer Forschungs-Wrapper, der validierte öffentliche Bausteine (TotalSegmentator MIT-lizenziert, MONAI Bundles, HiResCAM XAI) zu einem reproduzierbaren Workflow-Capture-Tool integriert.
5. Footer-Watermark.
6. Speichern als `KI_Tools_Marktanalyse_v3.pdf` (ggf. via "Datei → Drucken → Als PDF speichern").

---

## Dok 6 — `Tech_Description_Klinikum_v2.docx`

**Stride-Prompt:**

1. Globale Substitutions-Tabelle.
2. Header-Banner.
3. "System-Architektur" — abgleichen gegen aktuellen P0f-Stand:
   - Frontend: React 19 + Vite + TypeScript + Tailwind v4 + Cornerstone.js DICOM-Viewer
   - Backend: Python FastAPI + ONNX Runtime
   - Modell: TotalSegmentator (MIT) für ICA-Segmentierung — **Update:** früher als MFSD-UNet beschrieben, ist aktuell als TotalSegmentator-Wrapper geplant ab Phase B
   - XAI: HiResCAM (ADR-005)
   - Confidence: Platt/Isotonic Scaling + Trust Score (ADR-006)
   - Datenbank: lokale SQLite Audit-Trail
   - Deployment: Hetzner CX23 (`carotis.diggai.de` / `api.carotis.diggai.de`) — TLS via Let's Encrypt
4. "Modul-Architektur" — Module A–E gemäß Master-Zweckbestimmung §H:
   - A — DICOM Viewer + Annotator (Non-Device / Class I MDDS)
   - B — Workflow-Logger (Reading-Time, Klick-Sequenzen)
   - C — Decision-Tree-Notebook
   - D — KI-Forschungsbibliothek (Heatmap-Overlay, kein Befund)
   - E — Clinical Decision Support / Stenose-Quantifizierung — **deaktiviert per Feature-Flag in Phase A**
5. "Datenschutz / DSGVO" — ergänzen: Audit-Service redigiert 9 PII-Keys nach DICOM PS 3.15. Keine Cloud-Abhängigkeiten für Patientendaten.
6. "Compliance / Regulatorik" — ersetzen:
   > Carotis-AI ist als Forschungsprototyp ohne MDR-Pflicht positioniert. Eine spätere klinische Nutzung am Klinikum erfolgt im Rahmen der Eigenherstellung gemäß § 11 MPDG / Art. 5(5) MDR, in Verantwortung der Einrichtung.
7. Footer-Watermark.
8. Speichern als `Tech_Description_Klinikum_v3.docx`.

---

## Dok 7 — `Value_Proposition_Klinikum_v2.docx`

**Stride-Prompt:**

1. Globale Substitutions-Tabelle.
2. Header-Banner.
3. **Wichtigster Re-Frame:** Value-Proposition darf nicht "diagnostischer Mehrwert" sein, sondern "Forschungs- und Workflow-Mehrwert".

**Alte Value-Props ersetzen durch:**

- **Workflow-Erfassung statt Befund-Generierung** — Das Tool erfasst Reading-Time, Annotation-Pattern und Decision-Tree-Verzweigungen retrospektiv und ohne Eingriff in den klinischen Workflow.
- **Lokal-First-Architektur** — Keine Cloud-Abhängigkeit für Patientendaten, DSGVO-konform per Architektur statt per Compliance-Anhang.
- **Erklärbare Aufmerksamkeits-Visualisierung** — HiResCAM-Heatmap als Forschungs-Referenz-Overlay (kein automatischer Befund).
- **Anschlussfähigkeit an DeGIR/DGNR-Register und UKE-Kooperation** — Etablierte methodische Pipelines des Klinikums werden nicht ersetzt, sondern um eine Workflow-Ebene erweitert.
- **Promotionsstruktur-Anbindung** — Plattform unterstützt klinisch-retrospektive Promotionsarbeiten in der Sektion Biomedizinische Physik.
- **Kein regulatorischer Aufwand für das Klinikum** — Forschungsprototyp ohne MDR-Pflicht; spätere Eigenherstellungs-Optionalität nach § 11 MPDG bleibt offen.

4. **ROI-Argumente entfernen** falls vorhanden — ROI-Sprache ist Medizinprodukt-Marketing, nicht Forschungs-Sprache.

5. Footer-Watermark.

6. Speichern als `Value_Proposition_Klinikum_v3.docx`.

---

## Reihenfolge der Bearbeitung (empfohlen, ~3-4h Lou-Aufwand)

1. **Dok 1 archivieren** (5 min)
2. **Dok 6 (Tech_Description)** — am wichtigsten, weil Architektur-Stand v3 dann Referenz für andere Doks ist (45 min)
3. **Dok 2 (Konzept)** — Master-Zweckbestimmung Übernahme + Substitutions-Sweep (30 min)
4. **Dok 7 (Value_Proposition)** — Forschungs-Frame statt Markt-Frame (30 min)
5. **Dok 4 (Expose)** — Studientitel + Hypothesen schärfen (30 min)
6. **Dok 3 (Carotis_Ai_Rohde)** — Pitch-Hook neu (20 min)
7. **Dok 5 (Marktanalyse PDF)** — Update mit Recherche-Befunden 2026-05-10 (40 min)

## DoD pro Dok

- [ ] Globale Substitutions-Tabelle gelaufen (Find&Replace-Log notiert: x Treffer)
- [ ] Header-Banner oben sichtbar
- [ ] Footer-Watermark auf jeder Seite
- [ ] Spezifische Re-Frame-Punkte aus Stride-Prompt umgesetzt
- [ ] Datei als `_v3.docx` / `_v3.pdf` gespeichert (alte Version bleibt)
- [ ] Lou-Quick-Read-Through (5 min pro Dok)

## Nach Abschluss

- Alle 7 v3-Doks committed nach `Stride V2/`
- Alte v2-Versionen archiviert in `Stride V2/_archiv_v2/`
- Update Run-Log: `memory/runs/2026-05-1x_stride_v2_reframe.md` (5-Zeilen-Schema)
- Tasks.jsonl: Task #8 auf completed setzen
- Bereit für Stakeholder-Versand (nach Aroob-Sync und Code-Disclaimer-Build-Abschluss)
