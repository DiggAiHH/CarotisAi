# Stride V3 Prompt W-10: Office-Docs v3 — Alle 7 Dokumente (Master-Prompt)

## Ziel
Alle 7 Office-Dokumente aus Stride V2 auf Version 3 heben. Kern-Unterschied zu V2: Live-Demo-Verweis (`carotis.diggai.de`), Test-Coverage-Zahlen (107/107 pytest, 12/12 Vitest), Rohde-Token, und der Strategie-Shift von "Konzept" zu "gebaut".

## Allgemeine Regeln fuer alle V3-Dokumente
- Keine Umlaute im Prompt-Text (ae/oe/ue), damit Stride sauber verarbeitet
- Jeder Prompt endet mit: "Output: .docx, speichere unter Stride V3/[Dateiname]_v3.docx"
- Nach Erstellung: Lou fuehrt Stride-Prompt aus, prueft Output, speichert final

---

## Prompt 1/7: Anschreiben Aroob an Rohde v3

**Quelle:** `Stride V2/Anschreiben_Aroob_an_Rohde_v2.docx`

**Aenderungen:**
- Betreff aendern zu: "Re: Doktorarbeit – Live-Demo verfuegbar + Carotis-AI Update"
- Absatz 2 ersetzen: Statt "Anlage 2: Konzeptpapier" -> "Anlage 2: Konzeptpapier + Live-Demo-URL + persoenlicher Token"
- Neuen Absatz einfuegen nach Absatz 1: "Die Demo ist live unter https://carotis.diggai.de. Ihr persoenlicher 30-Tage-Token: [TOKEN]. In 5 Minuten sehen Sie die erste Analyse."
- Absatz 4 (Akademischer Mehrwert): Ergaenzen um "Engineering-Harnessing-Framework dokumentiert in 40+ Run-Logs, reproducible"
- Anlagen-Liste erweitern: + "Anlage 4: 3-Minuten-Demo-Video (MP4)"

**Output:** `Stride V3/Anschreiben_Aroob_an_Rohde_v3.docx`

---

## Prompt 2/7: Carotis-AI Konzept v3

**Quelle:** `Stride V2/Carotis_AI_Konzept_v2.docx`

**Aenderungen:**
- Titelseite: "Version 3.0 – mit Live-Demo" statt "Version 2.0"
- Executive Summary: Ergaenzen um "Prototyp live deployt auf carotis.diggai.de, 107/107 Tests passing"
- Kapitel 2 (Stand der Technik): Floy-Analyse erweitern um Vergleich mit Live-System (Local-First vs. Cloud)
- Kapitel 3 (Architektur): Ergaenzen um Deploy-Architektur (Fly.io Frontend + Hetzner Backend), DNS-Setup
- Kapitel 4 (Methodik): Ergaenzen um "107 pytest + 12 Vitest als Qualitaets-Gate"
- Kapitel 5 (Roadmap): P0f als "DONE" markieren, P1 als "Next"
- Anhang: Neue Sektion "Demo-Zugang" mit URL, Token-Anforderung, Systemanforderungen

**Output:** `Stride V3/Carotis_AI_Konzept_v3.docx`

---

## Prompt 3/7: Carotis-AI Rohde-Praesentation v3

**Quelle:** `Stride V2/Carotis_Ai_Rohde_v2.docx` (PowerPoint-Content)

**Aenderungen:**
- Folie 2 (Agenda): Ersetzen durch "Live-Demo first, dann Details"
- Folie 3 (Problem): Ergaenzen um Screenshot der Demo-UI
- Folie 4 (Loesung): Ergaenzen um "Deployiert auf carotis.diggai.de"
- Folie 5 (Architektur): Ersetzen durch aktuelles Diagramm (Fly + Hetzner)
- Folie 6 (Demo): QR-Code zu carotis.diggai.de einfuegen
- Folie 7 (Trust): Ergaenzen um Trust-Score-UI-Screenshot
- Folie 8 (Decision-Tree): Ergaenzen um Formular-Screenshot
- Folie 9 (Team): Unveraendert
- Folie 10 (Publikationen): Unveraendert
- Folie 11 (Timeline): P0f als "Complete", P1 als "In Progress"
- Folie 12 (Ask): Ergaenzen um "Token fuer 30 Tage Demo-Zugang"

**Output:** `Stride V3/Carotis_Ai_Rohde_v3.pptx`

---

## Prompt 4/7: Expose Carotis-AI Rohde v3

**Quelle:** `Stride V2/Expose_Carotis_AI_Rohde_v2.docx`

**Aenderungen:**
- Titel: "Expose zur Promotionsarbeit: Carotis-AI (v3.0 – Live-Prototyp)"
- Zusammenfassung: Ergaenzen um "Prototyp deployt, 107/107 Tests, Demo verfuegbar"
- Kapitel 1.3 (Forschungsstand): Floy-Vergleich erweitern um Live-System-Vorteile
- Kapitel 2 (Methodik): Ergaenzen um "Test-Driven Development mit 107 pytest, 12 Vitest"
- Kapitel 3 (Zeitplan): P0f als abgeschlossen, P1 Start-Datum konkretisieren
- Kapitel 4 (Ressourcen): Ergaenzen um "Hosting: Fly.io + Hetzner (laufende Kosten < 50 EUR/Monat)"
- Anhang: Demo-Zugangsbeschreibung, Screenshot-Seite

**Output:** `Stride V3/Expose_Carotis_AI_Rohde_v3.docx`

---

## Prompt 5/7: KI-Tools Marktanalyse v3

**Quelle:** `Stride V2/KI_Tools_Marktanalyse_v2.pdf`

**Aenderungen:**
- Dieses Dokument ist ein PDF (nicht editierbar via Stride)
- Stattdessen: Zusammenfassungs-Seite erstellen, die die Marktanalyse auf V3 hebt
- Neue Sektion: "Vergleich: Carotis-AI vs. Markt" — Tabelle mit Floy, Aidoc, Quantib, Carotis-AI
- Spalten: Cloud/Local, Carotis-Spezifisch, Erklaerbarkeit, Decision-Tree-Harvesting, DSGVO-Konform, Preis
- Carotis-AI in jeder Spalte gruen markiert

**Output:** `Stride V3/KI_Tools_Marktanalyse_v3_SUMMARY.docx`

---

## Prompt 6/7: Tech Description Klinikum v3

**Quelle:** `Stride V2/Tech_Description_Klinikum_v2.docx`

**Aenderungen:**
- Titel: "Technische Beschreibung Carotis-AI v3.0 (Live-System)"
- Kapitel 1 (Overview): Ergaenzen um "Deploy-Status: Frontend Fly.io, Backend Hetzner DE"
- Kapitel 2 (System-Architektur): Ersetzen durch aktuelles Diagramm (React 19 + Vite + Cornerstone3D / FastAPI + SQLite + ONNX Runtime / Fly + Hetzner)
- Kapitel 3 (Datenfluss): Ergaenzen um "INWX DNS: api.carotis A 204.168.230.127, carotis CNAME fly.dev"
- Kapitel 4 (Security): Ergaenzen um "Demo-Token-System mit Quota und Expiry"
- Kapitel 5 (Integration): Unveraendert (HL7/FHIR geplant)
- Kapitel 6 (Tests): Ergaenzen um "107 pytest, 12 Vitest, 0 Security-Critical Issues"
- Anhang: Caddyfile-Konfiguration, docker-compose.demo.yml Auszug

**Output:** `Stride V3/Tech_Description_Klinikum_v3.docx`

---

## Prompt 7/7: Value Proposition Klinikum v3

**Quelle:** `Stride V2/Value_Proposition_Klinikum_v2.docx`

**Aenderungen:**
- Titel: "Value Proposition Carotis-AI v3.0 — Von Konzept zu Live-System"
- Executive Summary: Ergaenzen um "Prototyp live, 107/107 Tests, bereit fuer klinische Evaluierung"
- Sektion 1 (Problem): Ergaenzen um "Cloud-Tools wie Floy nicht DSGVO-konform fuer Carotis"
- Sektion 2 (Loesung): Ergaenzen um Screenshot der Demo-UI
- Sektion 3 (Business Case): Ergaenzen um "Hosting-Kosten < 50 EUR/Monat, keine Lizenzgebuehren"
- Sektion 4 (ROI): Ergaenzen um "Zeitersparnis: 15 Min/Befund -> 5 Min/Befund (geschuetzt)"
- Sektion 5 (Risk): Ergaenzen um "Kein Vendor-Lock-In, Open-Source-Stack, lokale Datenhaltung"
- Sektion 6 (Next Steps): Ersetzen durch "1. Rohde-Termin, 2. Ethikantrag, 3. Pilot-Evaluierung"
- Anhang: Demo-Zugang, QR-Code, Kontakt

**Output:** `Stride V3/Value_Proposition_Klinikum_v3.docx`

---

## Post-Processing (Lou nach Stride-Ausfuehrung)

1. Alle 7 Dateien in `Stride V3/` pruefen
2. Dateien auf konsistente Formatierung pruefen (Schriftart, Groesse, Farben)
3. Screenshot-Platzhalter durch echte Screenshots ersetzen (wenn Demo live)
4. PDF-Export fuer alle .docx Dateien
5. Anlagen-Liste in Anschreiben v3 auf Vollstaendigkeit pruefen
6. Pre-Send-Checklist aus W-09 durchgehen
