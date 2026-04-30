# 2026-04-30 · Stride-Prompts G + H (Microsoft 365 Copilot)

**Goal:** Zwei aktualisierte Stride-Prompts für Lou erstellen, damit er `Ki_Tools_Marktanalyse.docx` und `Carotis Ai Konzept.docx` über Microsoft 365 Copilot / Stride auf das Klinikum-Dortmund-Setting aktualisieren kann.

**Done:** Prompts G und H als Copy-Paste-Blöcke mit Global Context, Prompt, Output-Format und Verify-Schritten.

**Next:** Lou führt Prompts in Stride aus → Review mit Aroob → Speicherung als `_v2.docx`.

**Memory updates:** Keine (bestehende Dokumente referenziert).

---

## Anleitung für Lou

1. Öffne Microsoft 365 Copilot / Stride.
2. Lade das Ausgangsdokument hoch (`Ki Tools Marktanalyse.docx` bzw. `Carotis Ai Konzept.docx`).
3. Kopiere den **Global Context** in den Chat.
4. Kopiere anschließend den jeweiligen **Prompt** (G oder H).
5. Warte auf den Output, prüfe mit den **Verify-Schritten**, speichere als `_v2.docx`.

---

## ─────────────────────────────────────────
## PROMPT G — Ki_Tools_Marktanalyse_v2.docx
## ─────────────────────────────────────────

### 1. Global Context (vor dem Prompt einfügen)

```
SETTING-UPDATE:
- Empfänger: Prof. Dr. med. Stefan Rohde, Klinikum Dortmund (Direktor / Klinik für Radiologie und Neuroradiologie)
- Absender: Aroob Alrawashdeh, Ärztin in Weiterbildung für Radiologie, Klinikum Dortmund
- Institution: durchgehend "Klinikum Dortmund" (NIE "Praxis")
- Aroob's Titel: "Ärztin in Weiterbildung für Radiologie" (NIE "Fachärztin")
- Heute ist der 30. April 2026.
- Sprache: Deutsch, formell, akademisch-präzise. Engineering-Begriffe korrekt.
- Tonalität: respektvoll und Engineering-selbstbewusst. KEIN Bittstellertum. KEINE Übertreibungen.
- Konkrete Fakten, keine Marketing-Floskeln.

KEYWORDS, die im Dokument vorkommen müssen:
- "Local-First Edge AI"
- "Decision-Tree Harvesting"
- "DSGVO-konform by Design"
- "EU AI Act, Art. 10/13/14/15"
- "Klinikum Dortmund"

Output-Anforderungen:
1. Vollständiger aktualisierter Text in Word-importierbarem Format
2. Diff-Liste am Ende (was wurde geändert vs. v1)
3. Speichern als KI_Tools_Marktanalyse_v2.docx (NICHT überschreiben)
```

### 2. Der Prompt

```
Aktualisiere das Dokument "Ki Tools Marktanalyse.docx" auf das Setting "Klinikum Dortmund / Prof. Rohde" und erweitere es um die folgenden Inhalte.

GLOBALE TEXTERSETZUNGEN:
- "Praxis" → "Klinikum Dortmund"
- "Fachärztin" → "Ärztin in Weiterbildung für Radiologie"
- Datumsangaben auf 2026-04-30 aktualisieren

NEUES KAPITEL 1: "Executive Summary — Warum Carotis-AI?"
Füge direkt nach dem Titel / Deckblatt eine 1-seitige Executive Summary ein:
- Problem: Cloud-basierte KI-Tools (z.B. Floy) erzeugen DSGVO-Compliance-Risiken in deutschen Kliniken und sind für Carotis-Stenose nicht spezialisiert.
- Lösung: Carotis-AI — eine Local-First Edge-AI-Lösung, die direkt am Klinikum-Server läuft, keine Patientendaten exportiert und auf die Carotis-Diagnostik optimiert ist.
- Hauptstandort: Klinikum Dortmund — akademisches Lehrkrankenhaus mit etablierter Forschungstradition in der Neuroradiologie.
- Innovation: Decision-Tree-Harvesting — das System lernt aus den anonymisierten Begründungsstrukturen der Befunder, nicht nur aus den Bildern.
- Zielgruppe: Radiologen und Ärzte in Weiterbildung am Klinikum Dortmund.

NEUES KAPITEL 2: "Vergleich Floy vs. Carotis-AI"
Füge vor dem Fazit ein neues Kapitel mit einer strukturierten Vergleichstabelle ein (als Word-Tabelle formatiert):

| Kriterium | Floy | Carotis-AI |
|-----------|------|------------|
| Architektur | Cloud-basiert | Local-First Edge AI |
| DSGVO-Konformität | erhöhte Anforderungen (Cloud-Export) | by Design konform (kein Datenexport) |
| Spezialisierung | CT-Thorax (Lungennoduli, Pneumonie) | Carotis-Stenose + Plaque-Vulnerability |
| Erklärbarkeit (XAI) | Bounding-Box + Konfidenzwert | Grad-CAM + SHAP + Reasoning-Capture |
| EU AI Act | teilweise konform | proaktiv konform (Art. 10/13/14/15) |
| Decision-Tree-Harvesting | nein | ja, als Trainings-Loss |
| Multi-Center-Validierung | nicht dokumentiert | transnational DE/Jordanien geplant |
| Vendor Lock-In | hoch (proprietär) | null (Open-Source-Stack + ONNX) |
| Lizenzkosten | wiederkehrend (SaaS) | einmalig (HAW-Förderung / Eigenmittel) |
| Hardware-Anforderung | Internet + Cloud-Account | lokaler Edge-Server (GPU optional) |

Erläuterungstext unter der Tabelle (ca. 150 Wörter):
- Floy ist eine valide Lösung für CT-Thorax, aber nicht für Carotis.
- Carotis-AI schließt eine regulatorische und wissenschaftliche Lücke.

NEUES KAPITEL 3: "Preisgestaltung und Lizenzmodelle"
Füge vor dem Fazit ein Kapitel mit drei Preis-Tiers ein. Die Preise sind Planungswerte für ein späteres MDR-Class-IIa-Produkt (nach P7). Aktuell ist das Projekt Promotions-finanziert und kostet das Klinikum nichts.

Tabelle:
| Tier | Name | Zielgruppe | Funktionsumfang | Preis (Planung) |
|------|------|-----------|-----------------|-----------------|
| Budget | Carotis-AI Essential | Einzelpraxen / kleine Radiologie-Institute | Grundlegende Stenose-Quantifizierung (NASCET/ECST), Basic Grad-CAM, kein Decision-Tree-Harvesting | 4.900 € einmalig + 980 €/Jahr Support |
| Mittel | Carotis-AI Professional | Mittelgroße Kliniken (bis 500 Betten) | Vollständige Plaque-Vulnerability-Analyse (IPH, ThinCap, LRNC), SHAP + Grad-CAM, Basic Decision-Tree-Capture, FHIR-Integration | 14.900 € einmalig + 2.980 €/Jahr Support |
| Premium | Carotis-AI Enterprise | Universitätsklinika / Klinikverbünde | Alles aus Professional + Daily-Learning-Loop, Multi-Center- Dashboard, Custom Model-Training, Prioritäts-Support, MDR-Compliance-Paket | 29.900 € einmalig + 5.980 €/Jahr Support |

Erläuterungstext (ca. 100 Wörter):
- Aktuell (P0–P5) wird das System im Rahmen der Promotion kostenfrei am Klinikum Dortmund entwickelt und betrieben.
- Die Preisgestaltung ist eine Planungsgröße für die MDR-Zertifizierung und Skalierung ab P7.
- Das Klinikum Dortmund erhält als Entwicklungspartner eine dauerhafte Enterprise-Lizenz zu Konditionen.

FAZIT-AKTUALISIERUNG:
Erweitere das Fazit um:
- Klinikum Dortmund als akademischer Hauptstandort mit Reputationsgewinn durch KI-Vorreiterrolle.
- Local-First Edge AI als nicht-verhandelbarer Standard für Gesundheitsdaten.
- Decision-Tree-Harvesting als wissenschaftlicher Mehrwert gegenüber reinen Pixel-Modellen.

Speichere als: KI_Tools_Marktanalyse_v2.docx
```

### 3. Erwartetes Output-Format

- Word-Dokument mit gleicher Formatierung wie das Original (Überschriften-Stile beibehalten)
- Neue Kapitel als "Überschrift 1" / "Überschrift 2"
- Tabellen als echte Word-Tabellen (nicht als Text)
- Seitenumbrüche an sinnvollen Stellen
- Am Ende des Dokuments: eine Seite "Änderungsübersicht (Diff v1 → v2)" mit Bullet-Points

### 4. Verify-Schritte für Lou

Nachdem Stride das Dokument erstellt hat:

- [ ] Datei heißt `KI_Tools_Marktanalyse_v2.docx` und liegt im Projekt-Root.
- [ ] Das Wort "Praxis" kommt nirgendwo mehr vor (Suche mit Strg+F).
- [ ] Aroob wird als "Ärztin in Weiterbildung für Radiologie" bezeichnet.
- [ ] Die Tabelle "Floy vs. Carotis-AI" hat alle 10 Zeilen und ist als echte Tabelle formatiert.
- [ ] Die Preis-Tabelle hat 3 Zeilen (Budget / Mittel / Premium).
- [ ] Im Preis-Kapitel steht der Hinweis, dass das Klinikum aktuell nichts zahlt.
- [ ] "Local-First Edge AI", "Decision-Tree Harvesting" und "Klinikum Dortmund" kommen mindestens einmal vor.
- [ ] Die Diff-Liste am Ende ist vollständig und nachvollziehbar.
- [ ] Keine Übertreibungen wie "weltweit erste" oder "revolutionär".

---

## ─────────────────────────────────────────
## PROMPT H — Carotis_AI_Konzept_v2.docx
## ─────────────────────────────────────────

### 1. Global Context (vor dem Prompt einfügen)

```
SETTING-UPDATE:
- Empfänger: Prof. Dr. med. Stefan Rohde, Klinikum Dortmund (Direktor / Klinik für Radiologie und Neuroradiologie)
- Absender: Aroob Alrawashdeh, Ärztin in Weiterbildung für Radiologie, Klinikum Dortmund
- Institution: durchgehend "Klinikum Dortmund" (NIE "Praxis")
- Aroob's Titel: "Ärztin in Weiterbildung für Radiologie" (NIE "Fachärztin")
- Ziel-Betreuer: Prof. Dr. med. Stefan Rohde (Direktor, Klinikum Dortmund)
- Heute ist der 30. April 2026.
- Sprache: Deutsch, formell, akademisch-präzise. Engineering-Begriffe korrekt.
- Tonalität: respektvoll und Engineering-selbstbewusst. KEIN Bittstellertum. KEINE Übertreibungen.
- Konkrete Fakten, keine Marketing-Floskeln.

KEYWORDS, die im Dokument vorkommen müssen:
- "Engineering Harnessing"
- "Local-First Edge AI"
- "Decision-Tree Harvesting"
- "Daily Learning Loop"
- "MFSD-UNet"
- "Klinikum Dortmund"
- "Human in the Loop"
- "DSGVO-konform by Design"
- "EU AI Act, Art. 10/13/14/15"
- "MDR Class IIa"
- "DIN EN 62304"
- "Plaque-Vulnerability-Marker (IPH, ThinCap, LRNC)"

Output-Anforderungen:
1. Vollständiger aktualisierter Text in Word-importierbarem Format
2. Diff-Liste am Ende (was wurde geändert vs. v1)
3. Speichern als Carotis_AI_Konzept_v2.docx (NICHT überschreiben)
```

### 2. Der Prompt

```
Aktualisiere das Dokument "Carotis Ai Konzept.docx" auf das neue Setting und ersetze alle veralteten Phasen-Bezeichnungen (M1–M5) durch das aktuelle P0–P7-System.

GLOBALE TEXTERSETZUNGEN:
- "Praxis" → "Klinikum Dortmund"
- "Fachärztin" → "Ärztin in Weiterbildung für Radiologie"
- "Dr. Aroob Alrawashdeh" → "Aroob Alrawashdeh" (Titel ist "Ärztin in Weiterbildung", nicht "Dr.")
- "Praxis-Chef" / "Chefarzt" → "Prof. Dr. med. Stefan Rohde, Direktor der Klinik für Radiologie und Neuroradiologie"
- Alle "M1", "M2", "M3", "M4", "M5" → durch "P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7" ersetzen (siehe Phasen-Mapping unten)
- Datumsangaben auf 2026-04-30 aktualisieren

PHASEN-MAPPING (altes M-System → neues P-System):
- Alt "M1–M2" → neu "P1 (Ethikantrag + Datenvertrag + DSGVO-Setup)"
- Alt "M3–M5" → neu "P2 (Datenakquise retrospektiv n≥500) + P3 (Modell-Training MFSD-UNet + ONNX-Export)"
- Alt "M6–M9" → neu "P3 (Training) + P4 (Edge-Server-Integration + UI + Decision-Tree-Capture)"
- Alt "M10–M15" → neu "P4 (Integration) + P5 (Klinische Validierung DE + JO, Daily-Learning-Loop)"
- Alt "M16–M21" → neu "P5 (Validierung)"
- Alt "M22–M24" → neu "P6 (Manuskript + Disputation)"
- Neu hinzufügen: P7 (MDR-Class-IIa-Zertifizierung + Skalierung an weitere Kliniken)
- Neu hinzufügen: P0 (Stakeholder-Approval + Office-Docs aktualisiert + Floy-Recherche) — aktuelle Phase

NEUER ABSCHNITT: "ENGINEERING HARNESSING FRAMEWORK"
Füge nach der Einleitung und VOR der bisherigen Methodik einen neuen Abschnitt (ca. 1,5 Seiten) ein:

Titel: "Engineering Harnessing — Eine systematische Methodik für Medical AI"

Inhalt (als Fließtext mit Zwischenüberschriften):

1. PROBLEMSTELLUNG:
Traditionelle Medizinsoftware-Entwicklung dauert 3–5 Jahre von der Idee bis zur regulatorischen Zulassung. Unser Engineering-Harnessing-Framework reduziert diese Zeit auf 24 Monate, ohne Qualitätskompromiss, durch systematische Wissensaggregation aus Medizin, Engineering und KI.

2. DREI LAYER DER ARCHITEKTUR:

Layer 1 — PIXEL-MODELL (State-of-the-Art):
MFSD-UNet-Architektur (U-Net + Swin Transformer + Deep Supervision) mit Dice-Coefficient ≥ 0,90 und Sensitivity ≥ 0,99 für die Carotis-Vessel-Segmentierung. Aktueller Benchmark nach Xie et al. (Quantitative Imaging in Medicine and Surgery, 2024).

Layer 2 — DECISION-TREE-HARVESTING (Innovation):
Nach jeder Befundung wird in einer 30-Sekunden-Mini-UI strukturiert erfasst, welches Bild-Feature für den Befunder ausschlaggebend war, welche Differenzialdiagnosen erwogen und ausgeschlossen wurden, und mit welcher Konfidenz die Diagnose getroffen wurde. Diese Decision-Trees werden anonymisiert (DICOM PS 3.15) in einen lokalen Korpus geschrieben. Das Modell lernt nicht nur aus den Bildern — es lernt die ärztliche Begründung.

Layer 3 — DAILY-LEARNING-LOOP:
Ein nächtlicher Cron-Job trainiert das Modell inkrementell auf den neu hinzugekommenen Decision-Trees + Anomalien (Fälle mit AI-Mensch-Diskrepanz). Performance-Vergleich vor/nach jeder Iteration; Auto-Rollback bei Verschlechterung. Ergebnis: Das System wird mit jeder Befundung besser, ohne dass jemals Patientendaten das Klinikum verlassen.

3. MEMORY-HIERARCHIE:
Jeder AI-gestützte Entwicklungs-Run hinterlässt strukturierte Lehren in einer projekt-eigenen Memory-Bibliothek. Der nächste Run beginnt nicht bei Null — er beginnt mit dem konsolidierten Wissen aller vorherigen. Modell-Routing: Architekturentscheidungen mit hochwertigen Modellen (Claude Opus 4.7); Routine-Implementation mit kostengünstigeren Modellen (Sonnet 4.6, Haiku 4.5) — bei vollständiger Audit-Trail-Dokumentation.

4. REGULATORY-BY-DESIGN:
DIN EN 62304, EU AI Act (Art. 10/13/14/15) und DSGVO sind keine nachträglichen Hürden, sondern integrale Architektur-Prinzipien — dokumentiert von Phase P0 an.

5. PUBLIKATIONSPOTENZIAL:
Daraus ergeben sich zwei Publikationen mit Prof. Rohde als Senior-Author:
  • Klinisches Validierungs-Paper (Carotis-AI vs. Konsens-Ground-Truth, transnational DE/JO, n ≥ 300) — Zieljournal: Radiology / JNIS
  • Methodisches Paper (Decision-Tree-Harvesting als Trainings-Paradigma) — Zieljournal: Medical Image Analysis / NEJM AI

NEUER ABSCHNITT: "Decision-Tree-Harvesting — Die eigentliche Innovation"
Füge vor dem Abschnitt "Vergleich Floy vs. Carotis-AI" einen 1-seitigen Abschnitt ein:
- Beschreibe das Problem: Standard-KI lernt nur aus Pixeln, nicht aus ärztlicher Begründung.
- Beschreibe die Lösung: 30-Sek-Form nach jeder Befundung (Feature, Differenzialdiagnose, Konfidenz, Korrektur).
- Erkläre die Anonymisierung: DICOM PS 3.15 + k-Anonymity + Hash-Stamp — keine Re-Identifizierung möglich.
- Erkläre den Trainings-Pfad: reasoning_alignment_loss als zusätzliche Loss-Komponente.
- Erwähne den Daily-Learning-Loop: Nightly Retraining, Auto-Rollback, Performance-Tracking.
- Halte es verständlich für einen klinisch tätigen Radiologen — keine JSON-Snippets, keine Code-Blöcke. Prosa und maximal eine vereinfachte Tabelle.

AKTUALISIERUNG: "Vergleich Floy vs. Carotis-AI"
Wenn dieser Abschnitt existiert, aktualisiere ihn:
- Ersetze "Praxis" durch "Klinikum Dortmund".
- Füge die Zeile "Decision-Tree-Harvesting" hinzu (Carotis-AI: ja, Floy: nein).
- Füge die Zeile "Local-First Edge AI" hinzu (Carotis-AI: ja, Floy: nein).

AKTUALISIERUNG: "Nutzen für das Klinikum Dortmund"
Erweitere oder ersetze den Abschnitt "Nutzen für die Praxis" durch:
- Erste DSGVO-konforme KI-Implementation am Haus
- Drittmittelfähig (BMBF KI-in-der-Medizin-Programm)
- Methodik-Framework als wiederverwendbare Plattform für weitere KI-Promotionen am Haus
- Forschungs-Leadership: Klinikum Dortmund als führendes Zentrum für Local-First-KI in der Neuroradiologie
- Mögliche Co-Authorship von Prof. Rohde auf zwei Papers (klinisch + methodisch)
- Reputationsgewinn als technologisches und regulatorisches Vorbild für KI-Implementation in der deutschen Radiologie
- Aroob bleibt langfristig am Klinikum durch die Promotion gebunden
- Lou Alshdaifat als langfristiger technischer Ansprechpartner für KI-Projekte am Klinikum

AKTUALISIERUNG: Zeitplan
Ersetze den alten Zeitplan (M1–M5) durch den aktuellen 24-Monats-Plan mit Phasen P0–P7:

| Phase | Zeitraum | Ziel | Status |
|-------|----------|------|--------|
| P0 | Woche 1–2 | Stakeholder-Approval (Rohde) + Office-Docs + Floy-Recherche | 🔄 läuft |
| P1 | Monat 1–2 | Ethikantrag + Datenvertrag + DSGVO-Setup | 🔒 geplant |
| P2 | Monat 3–5 | Datenakquise retrospektiv (n≥500), Anonymisierung, Ground-Truth | 🔒 geplant |
| P3 | Monat 6–9 | Modell-Training MFSD-UNet + Plaque-Klassifikator + ONNX-Export | 🔒 geplant |
| P4 | Monat 10–15 | Edge-Server-Integration + UI + Decision-Tree-Capture im Workflow | 🔒 geplant |
| P5 | Monat 16–21 | Klinische Validierung DE (Klinikum Dortmund) + JO (Sarah Hospital), Daily-Learning-Loop | 🔒 geplant |
| P6 | Monat 22–24 | Manuskript Radiology / JNIS + Disputation | 🔒 geplant |
| P7 | nach M24 | MDR-Class-IIa-Zertifizierung + Skalierung an weitere Kliniken | 🔒 geplant |

Speichere als: Carotis_AI_Konzept_v2.docx
```

### 3. Erwartetes Output-Format

- Word-Dokument mit gleicher Formatierung wie das Original (Überschriften-Stile beibehalten)
- Neue Abschnitte als "Überschrift 1" / "Überschrift 2"
- Tabellen als echte Word-Tabellen
- Seitenumbrüche an sinnvollen Stellen
- Am Ende des Dokuments: eine Seite "Änderungsübersicht (Diff v1 → v2)" mit Bullet-Points

### 4. Verify-Schritte für Lou

Nachdem Stride das Dokument erstellt hat:

- [ ] Datei heißt `Carotis_AI_Konzept_v2.docx` und liegt im Projekt-Root.
- [ ] Das Wort "Praxis" kommt nirgendwo mehr vor (Suche mit Strg+F).
- [ ] Aroob wird durchgehend als "Ärztin in Weiterbildung für Radiologie" bezeichnet.
- [ ] Prof. Rohde wird als "Ziel-Betreuer" und "Direktor der Klinik für Radiologie und Neuroradiologie" geführt.
- [ ] Der Engineering-Harnessing-Abschnitt ist vorhanden und enthält Layer 1–3.
- [ ] Der Decision-Tree-Harvesting-Abschnitt ist verständlich geschrieben (keine Code-Blöcke, keine JSON-Snippets).
- [ ] Der Zeitplan zeigt P0–P7 (nicht M1–M5).
- [ ] P0 ist als "läuft", P1–P7 als "geplant" markiert.
- [ ] "Local-First Edge AI", "Decision-Tree Harvesting", "Engineering Harnessing" und "Klinikum Dortmund" kommen mindestens einmal vor.
- [ ] Die Diff-Liste am Ende ist vollständig und nachvollziehbar.
- [ ] Keine Übertreibungen wie "weltweit erste" oder "revolutionär".

---

**Letzte Aktualisierung:** 2026-04-30 · Stride-Prompts für Lou
