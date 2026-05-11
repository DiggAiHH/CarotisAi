# Zweckbestimmung-Master — Carotis Forschungstool v1.0

**Status:** Kanonische Quelle. Alle Stride-V2-Dokumente, Code-Disclaimer, Mails, Ethikantrag, Paper-Abschnitte beziehen sich hierauf.
**Erstellt:** 2026-05-06
**Kontext:** Regulatory-Pivot von Class IIa MDR-Medizinprodukt → Forschungsprototyp ohne MDR-Pflicht (siehe Strategie-Memo gleicher Tag).
**Begründung:** Class IIa-Pfad nicht durchführbar als Solo-Dev + Promotion (Notified Body, ISO 13485, 50–200k €). Forschungsprototyp-Frame nutzt MDR Art. 1(2) Erwägungsgrund + § 11 MPDG-Optionalität.

---

## A — Master-Langform (Ethikantrag, Stride V2 Cover, README intro, Anwaltsgutachten)

> **Zweckbestimmung — Carotis Workflow- und Decision-Tree-Capture-Tool (Forschungsprototyp)**
>
> Das vorliegende Werkzeug ist ein **wissenschaftlicher Forschungsprototyp** zur Erfassung ärztlicher Entscheidungspfade, Lese- und Annotationszeiten sowie Workflow-Charakteristika in der neuroradiologischen Begutachtung von Carotis-Computertomographie-Angiographie-Aufnahmen (Carotis-CTA).
>
> **Bestimmungsgemäße Verwendung:** Strukturierte Datenerfassung in einem Forschungskontext durch qualifizierte Forscherinnen und Forscher. Die ärztliche Beurteilung, Diagnose und Behandlungsentscheidung verbleiben ausschließlich beim behandelnden Arzt und werden durch das Werkzeug weder ersetzt noch substanziell beeinflusst.
>
> **Optionale KI-Segmentierungs-Overlay-Funktion:** Eine als Forschungs-Referenzimplementierung beigefügte Bildverarbeitungs-Komponente kann visuelle Aufmerksamkeits-Heatmaps darstellen. Diese sind ausdrücklich **nicht** als quantitative Stenose-Messung, Plaque-Charakterisierung oder Therapieempfehlung bestimmt. Es erfolgt **keine** automatische Befundausgabe.
>
> **Ausschlüsse:** Das Werkzeug ist nicht für die klinische Diagnostik, nicht für Therapieentscheidungen, nicht für Triage und nicht für Patientenkommunikation bestimmt. Es ist **kein Medizinprodukt** im Sinne der Verordnung (EU) 2017/745 (MDR) bzw. § 3 Nr. 1 MPDG, sofern es entsprechend dieser Zweckbestimmung verwendet wird.
>
> **Hinweis zur klinischen Anwendung:** Eine etwaige klinische Nutzung im Rahmen der Eigenherstellung in Gesundheitseinrichtungen gemäß § 11 MPDG / Art. 5(5) MDR liegt in der Verantwortung der jeweiligen Einrichtung und ist nicht Teil dieser Lieferung.

---

## B — Mittellang (Stride V2 Brief-Body, Paper Methods-Abschnitt, Konferenz-Disclosure)

> Carotis-AI ist ein Forschungsprototyp zur Erfassung ärztlicher Entscheidungspfade und Workflow-Daten in der neuroradiologischen Carotis-CTA-Begutachtung. Klinische Diagnose- und Therapieentscheidungen verbleiben vollständig beim behandelnden Arzt. Das Werkzeug erzeugt keine automatischen Befunde, keine quantitativen Stenose-Werte und keine Therapieempfehlungen. Es ist **kein Medizinprodukt** im Sinne der MDR (EU 2017/745) bzw. des MPDG.

---

## C — Kurzform (Splash-Screen, E-Mail-Footer, Slide-Footer, README-Header)

> **Forschungsprototyp** — keine klinische Entscheidungsgrundlage. Kein Medizinprodukt im Sinne der MDR / MPDG.

---

## D — Mikro (Watermark auf jedem Export, PDF-Header, UI-Statusleiste)

> RESEARCH USE ONLY · Forschungsverwendung · Kein Medizinprodukt

---

## E — Splash-Gate-Bestätigungsdialog (Pflicht-Klick beim Start, mit Audit-Log)

> Sie sind im Begriff, Carotis-AI zu starten — einen Forschungsprototyp zur Erfassung von Workflow- und Entscheidungspfad-Daten in der Carotis-CTA-Begutachtung.
>
> Mit der Bestätigung erklären Sie:
> 1. Ich nutze dieses Werkzeug ausschließlich zu Forschungszwecken.
> 2. Ich treffe alle klinischen Entscheidungen eigenständig und stütze sie nicht auf die Ausgaben dieses Werkzeugs.
> 3. Ich werde keine Werkzeug-Ausgaben in Patientenakten als diagnostische Aussagen übernehmen.
>
> ☐ Ich bestätige · ☐ Abbrechen
>
> *Diese Bestätigung wird mit Zeitstempel, Nutzer-ID und Sitzungs-ID lokal protokolliert.*

---

## F — Studientitel-Vorschläge (Ethikantrag)

1. **Erfassung ärztlicher Entscheidungspfade und Workflow-Charakteristika in der neuroradiologischen Carotis-CTA-Begutachtung — eine retrospektiv-strukturierte Forschungsbeobachtung**
2. **Decision-Tree-Capture in der Carotis-Diagnostik: ein Forschungswerkzeug zur Untersuchung radiologischer Reasoning-Muster**
3. **Reading-Time- und Annotation-Pattern-Analyse bei der Carotis-CTA-Begutachtung** (kürzeste Variante, am wenigsten Diskussion in Ethikkommission)

**Empfehlung:** Variante 3 als Studientitel — minimal-invasiv für Ethikkommission, größtmöglicher inhaltlicher Spielraum.

---

## G — Begriffe-Substitution-Tabelle (überall durchziehen)

| Alt (medizinprodukthaft) | Neu (forschungsneutral) |
|---|---|
| Diagnoseassistent | Workflow- und Decision-Tree-Capture-Tool |
| Stenose-Messung | Aufmerksamkeits-Heatmap |
| KI-Befund | Forschungs-Referenz-Overlay |
| Plaque-Vulnerability-Score | Forschungsmerkmals-Aggregat (im Backend, nicht UI) |
| automatische Quantifizierung | strukturierte Datenerfassung |
| Klinikum-Pilot | Forschungsbeobachtung |
| Validierung gegen Goldstandard | Übereinstimmungs-Forschung (sekundärer Endpunkt) |
| MDR-Pfad / CE-Marke | Forschungsexemption + § 11 MPDG-Optionalität |
| Anwender / Nutzer | Forscher / Forschungsteilnehmer |
| Befund-Output | Forschungs-Datensatz |

---

## H — Modul-Dekomposition (technische Stütze der Zweckbestimmung)

| Modul | Funktion | Klassifizierung |
|---|---|---|
| A — DICOM Viewer + Annotator | Bilder anzeigen, manuelle Annotation | Non-Device / Class I MDDS |
| B — Workflow-Metric-Logger | Lesezeit, Throughput, Annotation-Pattern | Non-Device |
| C — Decision-Tree-Capture-Notebook | Arzt-Reasoning + Feature-Extraktion | Non-Device |
| D — AI-Segmentations-Forschungsbibliothek | ONNX-Modell als Reference-Implementation | Forschungsartefakt (nicht in Verkehr gebracht) |
| E — Clinical Decision Support | Stenose-% mit Empfehlung | Class IIa — **deferred, in Forschungsversion deaktiviert** |

**Distribution-Build:** A + B + C + D aktiv. E per Feature-Flag im Code, Build-Flag nicht gesetzt. Aktivierung nur via § 11 MPDG-Pfad oder spätere Zertifizierung.

---

## I — Anwendungs-Checklist (wo überall einbauen)

```
[ ] Stride V2/01_Cover_Letter.docx          → Block B in Einleitung, Block C in Footer
[ ] Stride V2/02_Project_Synopsis.docx      → Block A komplett als §2
[ ] Stride V2/0X_*.docx (alle Stride V2)    → Block C in Footer + Substitutionen aus G
[ ] README.md (carotis-ai Repo)             → Block C im Header, Block A im Abschnitt "Intended Use"
[ ] Frontend Splash-Screen                  → Block E als Pflicht-Dialog
[ ] Frontend UI Statusleiste                → Block D dauerhaft sichtbar
[ ] Backend /health/ Response               → "research_prototype: true" Flag
[ ] PDF-/PNG-Export Watermark               → Block D als Wasserzeichen
[ ] Ethikantrag                             → Block A vollständig + Variante F-3 als Titel
[ ] Rohde-Mail (P0f)                        → Block B in Absatz 2
[ ] Margaritoff-Mail                        → Block A als Anhang zur Bestätigungsanfrage
[ ] GitHub Repo Description                 → Block C
[ ] Zenodo DOI Metadata                     → Block C + Keyword "research-prototype"
[ ] Konferenz-Abstract (ESNR/ECR)           → Block B in Abschnitt "Methods"
[ ] Paper Methods-Abschnitt                 → Block B + Disclaimer-Footnote
[ ] api.carotis.diggai.de Frontend          → Block D im Footer
[ ] Demo-Walkthrough (Loom/Remotion)        → Block C als erstes Frame, 3 Sek
```

---

## J — Risiken (offen dokumentiert)

1. **Off-Label-Use durch Ärzte:** wenn Tool tatsächlich klinisch eingesetzt wird, kann Behörde die Zweckbestimmung als „rein zum Schein" werten. Gegenmaßnahme: technische Gates müssen real funktionieren (Splash, Watermark, deaktivierter CDS-Modul, Audit-Log) — nicht nur Disclaimer.
2. **MDCG 2019-11 = Auslegungsleitlinie, kein Gesetz.** Behörden können enger auslegen. Vor Veröffentlichung schriftliches Statement von Margaritoff oder MDR-Anwalt einholen.
3. **DSGVO bleibt unabhängig** — Forschungsprototyp ≠ DSGVO-frei. Patientendaten weiterhin streng (Privacy-by-Design ohnehin im Stack verankert).
4. **Kommerzielle Nutzung bricht Forschungs-Frame** — sobald jemand das Tool kommerziell anbietet (z. B. Klaproth-Praxis als Service), zurück zu MDR. Dieser Pfad kauft 24–36 Monate, danach Spin-Off-GmbH oder DiGA.

---

## K — Nächste konkrete Schritte (P0g — Regulatory-Pivot)

1. Margaritoff-Mail mit Block A als Anhang → 30-Min-Call zur Bestätigung der Zweckbestimmungs-Strategie.
2. Re-Branding aller `Stride V2/`-Dokumente nach Checklist I.
3. Frontend Splash-Gate (Block E) + UI-Watermark (Block D) implementieren — technisch belastbar, nicht nur kosmetisch.
4. ADR-007 oder ADR-008: Modul-Dekomposition A–E im Code festschreiben, CDS-Feature-Flag verifizieren.
5. Anwaltsgutachten-Kostenvoranschlag bei 2–3 MDR-Kanzleien (Berlin/München/Hamburg) — 800–1500 € als Versicherung.
6. Rohde-Pitch-Re-Write mit „kein Medizinprodukt, keine Produkthaftung"-Frame.

---

**Letztes Update:** 2026-05-06
**Pflege:** bei jeder substantiellen Änderung der Zweckbestimmung in *einer* Quelle muss diese Datei mitgepflegt werden — sonst driftet die Re-Branding-Konsistenz auseinander.
