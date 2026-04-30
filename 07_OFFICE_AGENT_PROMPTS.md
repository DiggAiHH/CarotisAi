# 07_OFFICE_AGENT_PROMPTS — Stride-Prompts für Microsoft 365

> Lou kopiert die Prompts unten in **Microsoft 365 Copilot / Stride / Office Agent** und bekommt die fertig aktualisierten Dokumente. Reihenfolge nicht ändern — die späteren Prompts bauen auf den Outputs der früheren auf.
>
> **Konvention:** Bestehende Datei wird durch eine `_v2.docx`-Variante ersetzt, niemals überschrieben (sonst geht der ältere Office-Agent-Output verloren).

---

## Vorbereitung — was Lou auf den Tisch legt

In Stride / Copilot diese Files vorher hochladen / im Workspace haben:

1. `Anschreiben_Dr_Alrawashdeh_KI_Carotis_Diagnostik.docx` (alte Praxis-Version)
2. `Ki_Carotis_Expose.docx`
3. `Ki_Carotis_Diagnostik.docx` (technische Beschreibung)
4. `Value_Proposition_Ki_Carotis.docx`
5. `Carotis_Ai.pptx`
6. `Ki_Tools_Marktanalyse.docx` (Floy-Recherche — wird kaum geändert, nur aufgehübscht)
7. `Carotis_Ai_Konzept.docx` (das eigene Konzept — wird leicht geupdated)

Außerdem: dieses Dokument-Set (`04_MASTER_PLAN.md` und `05_DECISION_TREE_HARVESTING.md`) als Kontext beilegen — der Office-Agent darf daraus zitieren.

---

## Globaler Kontext (am Anfang jeder neuen Session in Stride einfügen)

```
SETTING-UPDATE:
- Empfänger: Prof. Dr. med. Stefan Rohde, Klinikum Dortmund (Direktor / Klinik für Radiologie und Neuroradiologie)
- Absender: Aroob Alrawashdeh, Ärztin in Weiterbildung für Radiologie, Klinikum Dortmund
- Institution: durchgehend "Klinikum Dortmund" (NIE "Praxis")
- Aroob's Titel: "Ärztin in Weiterbildung für Radiologie" (NIE "Fachärztin")
- Bestehende Beziehung: Aroob war 01.01.2023 – 30.06.2023 schon einmal bei Prof. Rohde tätig. Er hat freundliche Gespräche geführt, eine Floy-Recherche als Hausaufgabe gegeben, und prüft, ob die Idee zur Promotion taugt.
- Heute ist der 27. April 2026.
- Sprache: Deutsch, formell, akademisch-präzise. Engineering-Begriffe korrekt.
- Tonalität: respektvoll und Engineering-selbstbewusst. KEIN Bittstellertum. KEINE Übertreibungen ("revolutionär", "weltweit erste", etc.). Konkrete Fakten.

KEYWORDS, die in jedem Dokument vorkommen müssen:
- "Engineering Harnessing" als Methodik
- "Local-First Edge AI"
- "Decision-Tree Harvesting"
- "Daily Learning Loop"
- "MFSD-UNet" (Modell-Architektur)
- "Klinikum Dortmund"
- "Human in the Loop"
- "DSGVO-konform by Design"
- "EU AI Act, Art. 10/13/14/15"
- "MDR Class IIa"
- "DIN EN 62304"
- "Plaque-Vulnerability-Marker (IPH, ThinCap, LRNC)"

Output für jedes Dokument:
1. Vollständiger aktualisierter Text in Word-importierbarem Format
2. Eine Diff-Liste am Ende (was wurde geändert vs. v1)
3. Speichern als <originalname>_v2.docx (NICHT überschreiben)
```

---

## PROMPT A — Mail an Prof. Rohde (NEU, ersetzt das alte Anschreiben)

```
Schreibe eine professionelle E-Mail von Aroob Alrawashdeh (Ärztin in 
Weiterbildung für Radiologie, Klinikum Dortmund) an Prof. Dr. med. Stefan Rohde
(Direktor, Klinik für Radiologie und Neuroradiologie, Klinikum Dortmund).

KONTEXT:
- Aroob hat von Prof. Rohde eine Aufgabenstellung bekommen: Recherche zu KI-Tools 
  in der Radiologie, speziell Floy-Software.
- Sie liefert die Recherche jetzt ab UND zusätzlich ein eigenes Konzept ("Carotis-AI"), 
  das sie gemeinsam mit ihrem Schwager Laith Alshdaifat (Medizintechniker, HAW Hamburg) 
  und unter Beratung von HAW-Professoren (Margaritoff, Tolg) entwickelt hat.
- Sie bittet um ein 30-minütiges Gespräch mit Prof. Rohde — zusammen mit Laith — 
  um beides vorzustellen.

DIE 5 KERN-PUNKTE in der Mail:
1. Floy ist cloud-basiert mit CT-Thorax-Schwerpunkt — für Carotis nur bedingt geeignet, 
   und unter DSGVO/EU AI Act in einem deutschen Klinikum problematisch.
2. Eine Local-First, DSGVO-konforme, erklärbare Lösung für die Carotis-Diagnostik 
   existiert bisher nicht.
3. Aroob hat mit Lou ein eigenes Konzept entwickelt: Carotis-AI, MFSD-UNet-basiert, 
   lokal lauffähig, mit Decision-Tree-Harvesting (lernt die ärztliche Begründung, 
   nicht nur das Bild).
4. Daraus könnten zwei Publikationen entstehen mit Prof. Rohde als Senior-Author:
   - Klinisches Validierungs-Paper (Radiology / JNIS)
   - Methodisches Paper (Medical Image Analysis / NEJM AI)
5. Sie bittet um einen 30-Minuten-Termin in der kommenden Woche.

ANLAGEN:
1. Recherche-Dokumentation: KI-Tools in der Radiologie & Floy-Software
2. Konzeptpapier: Carotis-AI — Local-First KI für die Carotis-Diagnostik
3. Kurz-CV Laith Alshdaifat

REGELN:
- Maximal 25 Zeilen Fließtext, kein Bullet-Marathon.
- Format: standard formelle Mail.
- Betreff prominent.
- Aroob als Mensch hinter dem Text spürbar — sie ist die, die die Promotion will, 
  nicht eine Engineering-Marketing-Maschine.
- Keine Übertreibungen.
- Termin-Vorschlag konkret: "in der kommenden Woche, 30 Minuten" + Angebot, sich 
  nach seinem Kalender zu richten.

Speichere als: Mail_Aroob_an_Rohde_v2.docx
```

---

## PROMPT B — Aktualisiere Anschreiben_Dr_Alrawashdeh_KI_Carotis_Diagnostik.docx → v2

```
Aktualisiere die Datei Anschreiben_Dr_Alrawashdeh_KI_Carotis_Diagnostik.docx auf 
das neue Setting "Klinikum Dortmund / Prof. Rohde / Aroob als Ärztin in Weiterbildung".

ÄNDERUNGEN:
- Empfänger: ändere ÜBERALL "Praxis-Chef" / "Praxisinhaber" / "Herr Dr. [Name]" zu 
  "Prof. Dr. med. Stefan Rohde" / "Direktor der Klinik für Radiologie und 
  Neuroradiologie, Klinikum Dortmund".
- Absender: ändere "Fachärztin" zu "Ärztin in Weiterbildung für Radiologie".
- Institution: ändere "Praxis" / "Praxisinhaber" zu "Klinikum Dortmund".
- Datum: 2026-04-27.

INHALTLICHE ERWEITERUNG:
Füge nach dem Absatz "Die technische Umsetzung erfolgt durch meinen Schwager…" 
einen neuen Absatz ein:

  "Wir nutzen dabei einen Engineering-Harnessing-Ansatz: systematische 
  Wissensaggregation aus Medizin, Engineering und KI, kombiniert mit 
  einer Mehrebenen-Architektur (Pixel-Modell + Decision-Tree-Harvesting + 
  Daily-Learning-Loop). Das Modell lernt nicht nur aus den Bildern, sondern 
  aus den anonymisierten Begründungs-Strukturen der Befunder — dadurch wird 
  der eigentliche Wert der ärztlichen Expertise systematisch erfasst und 
  trägt zur Verbesserung des Systems bei."

FÜGE EINEN NEUEN BULLET-POINT in die Vorteils-Liste ein:
- "Methodische Innovation mit Publikationspotenzial: Decision-Tree-Harvesting ist 
  ein neuer Beitrag zur Medical-AI-Literatur (Zieljournal Medical Image Analysis 
  oder NEJM AI)."

TON: respektvoll, Engineering-selbstbewusst. KEIN Bittstellertum.

Speichere als: Anschreiben_Aroob_an_Rohde_v2.docx
```

---

## PROMPT C — Aktualisiere Ki_Carotis_Expose.docx → v2

```
Aktualisiere das Exposé Ki_Carotis_Expose.docx.

ÄNDERUNGEN:
- Kandidatin: "Aroob Alrawashdeh, Ärztin in Weiterbildung für Radiologie, 
  Klinikum Dortmund"
- Betreuer: "Prof. Dr. med. Stefan Rohde, Direktor der Klinik für Radiologie 
  und Neuroradiologie, Klinikum Dortmund"
- Institution durchgehend: "Klinikum Dortmund"
- Datum: 2026-04-27

NEUER ABSCHNITT (einfügen nach "Zielsetzung", VOR "Methodik"):

═══════════════════════════════════════════════════════
ENGINEERING HARNESSING FRAMEWORK

Die Promotionsarbeit nutzt einen neuartigen, systematischen Ansatz für die 
Entwicklung medizinischer KI-Systeme. Das Framework hat drei Layer:

1. PIXEL-MODELL (State-of-the-Art): MFSD-UNet-Architektur (U-Net + Swin 
   Transformer + Deep Supervision) mit Dice-Coefficient ≥ 0,90 und 
   Sensitivity ≥ 0,99 für die Carotis-Vessel-Segmentierung. Aktueller 
   Benchmark nach Xie et al. (Quantitative Imaging in Medicine and Surgery, 
   2024).

2. DECISION-TREE-HARVESTING (Innovation): Nach jeder Befundung wird in 
   einer 30-Sekunden-Mini-UI strukturiert erfasst, welches Bild-Feature 
   für den Befunder ausschlaggebend war, welche Differenzialdiagnosen 
   erwogen und ausgeschlossen wurden, und mit welcher Konfidenz die 
   Diagnose getroffen wurde. Diese Decision-Trees werden anonymisiert 
   (DICOM PS 3.15) in einen lokalen Korpus geschrieben.

3. DAILY-LEARNING-LOOP: Ein nächtlicher Cron-Job trainiert das Modell 
   inkrementell auf den neu hinzugekommenen Decision-Trees + Anomalien 
   (Fälle mit AI-Mensch-Diskrepanz). Performance-Vergleich vor/nach jeder 
   Iteration; Auto-Rollback bei Verschlechterung.

Die Innovation liegt nicht im Bilderkennungs-Modell selbst, sondern in der 
systematischen Erfassung und Nutzung der ärztlichen Entscheidungs-Begründung 
als zusätzliche Trainings-Information. Damit wird Tacit Knowledge — der 
eigentliche Wert von 10 Jahren Facharztausbildung — erstmals strukturiert in 
die KI-Trainingspipeline eingespeist.

Daraus ergeben sich zwei Publikationen:
  • Klinisches Validierungs-Paper (Carotis-AI vs. Konsens-Ground-Truth, 
    transnational DE/JO, n ≥ 300) — Zieljournal Radiology / JNIS
  • Methodisches Paper (Decision-Tree-Harvesting als Trainings-Paradigma) 
    — Zieljournal Medical Image Analysis / NEJM AI
═══════════════════════════════════════════════════════

ÄNDERE die Methodik-Tabelle entsprechend (siehe 02_ROADMAP.md im Workspace 
für die 8 Phasen P0–P7).

ERGÄNZE im Abschnitt "Praktischer Nutzen für die Praxis" (umbenennen zu 
"Praktischer Nutzen für das Klinikum Dortmund"):
- Erste DSGVO-konforme KI-Implementation am Haus
- Drittmittelfähig (BMBF KI-in-der-Medizin-Programm)
- Methodik-Framework wiederverwendbar für weitere Promotionen am Klinikum
- Reputationsgewinn als KI-Vorreiter in der Neuroradiologie

Speichere als: Expose_Carotis_AI_Rohde_v2.docx
```

---

## PROMPT D — Aktualisiere Ki_Carotis_Diagnostik.docx (Tech-Beschreibung) → v2

```
Aktualisiere die technische Projektbeschreibung Ki_Carotis_Diagnostik.docx 
für Prof. Dr. med. Stefan Rohde am Klinikum Dortmund.

ÄNDERUNGEN:
- Setting: durchgehend "Klinikum Dortmund" statt "Praxis"
- Nutzer: "Radiologen und Ärzte in Weiterbildung am Klinikum"
- Datum: 2026-04-27

NEUER ABSCHNITT (am Ende, vor dem Zeitplan):

═══════════════════════════════════════════════════════
ENGINEERING HARNESSING IN DER MEDIZINTECHNIK

Traditionelle Medizinsoftware-Entwicklung dauert 3–5 Jahre von der Idee bis 
zur regulatorischen Zulassung. Unser Engineering-Harnessing-Framework 
reduziert diese Zeit auf 24 Monate, ohne Qualitätskompromiss, durch:

• Modell-Routing: Architekturentscheidungen werden einmal mit hochwertigen 
  AI-Modellen (Anthropic Claude Opus 4.7) getroffen; Routine-Implementation 
  läuft mit kostengünstigeren Modellen (Sonnet 4.6, Haiku 4.5) — bei 
  vollständiger Audit-Trail-Dokumentation.

• Memory-Hierarchie: Jeder AI-gestützte Entwicklungs-Run hinterlässt 
  strukturierte Lehren in einer projekt-eigenen Memory-Bibliothek. Der 
  nächste Run beginnt nicht bei Null — er beginnt mit dem konsolidierten 
  Wissen aller vorherigen.

• Regulatory-by-Design: DIN EN 62304, EU AI Act und DSGVO sind keine 
  nachträglichen Hürden, sondern integrale Architektur-Prinzipien — 
  dokumentiert von Phase 0 an.

• Decision-Tree-Harvesting in der klinischen Validierung: ab Phase 5 lernt 
  das System täglich aus den anonymisierten Entscheidungs-Begründungen der 
  Befunder. Performance-Vergleich vor/nach jedem Lern-Schritt; Auto-Rollback 
  bei Verlust.

Diese Methodik ist nicht Carotis-spezifisch. Nach erfolgreicher Validierung 
in der Carotis-Diagnostik kann sie auf andere radiologische Fragestellungen 
übertragen werden — was dem Klinikum Dortmund eine reproduzierbare 
Plattform für weitere KI-Promotionen bietet.
═══════════════════════════════════════════════════════

Speichere als: Tech_Description_Klinikum_v2.docx
```

---

## PROMPT E — Aktualisiere Value_Proposition_Ki_Carotis.docx → v2

```
Aktualisiere die Value Proposition Value_Proposition_Ki_Carotis.docx 
auf Prof. Dr. med. Stefan Rohde / Klinikum Dortmund.

ÄNDERUNGEN:
- Zielgruppe: "Prof. Dr. med. Stefan Rohde und das Klinikum Dortmund"
- Setting durchgehend "Klinikum Dortmund"

NEUE BULLET-POINTS in die Sektion "Wissenschaftlicher Ruhm":
• Forschungs-Leadership: Klinikum Dortmund als führendes Zentrum für 
  Local-First-KI in der Neuroradiologie
• Engineering-Harnessing-Methodik publizierbar als eigenes Paper — Lou 
  als Erst-Autor, Rohde als Senior-Author
• Drittmittel-Fähigkeit: BMBF KI-in-der-Medizin-Förderprogramm

NEUE BULLET-POINTS in die Sektion "Personalbindung":
• Aroob bleibt langfristig am Klinikum durch die Promotion gebunden
• Zugang zum HAW-Hamburg-Netzwerk (Margaritoff, Tolg, van Stevendaal) für 
  weitere kooperative Promotionen
• Lou Alshdaifat als langfristiger technischer Ansprechpartner für KI-Projekte 
  am Klinikum

Speichere als: Value_Proposition_Klinikum_v2.docx
```

---

## PROMPT F — Aktualisiere Carotis_Ai.pptx → v2

```
Aktualisiere die PowerPoint-Präsentation Carotis_Ai.pptx auf Prof. Dr. med. 
Stefan Rohde am Klinikum Dortmund.

GLOBALE ÄNDERUNGEN auf allen Folien:
- "Praxis" → "Klinikum Dortmund"
- "Dr. Aroob Alrawashdeh, Fachärztin" → "Aroob Alrawashdeh, Ärztin in 
  Weiterbildung für Radiologie, Klinikum Dortmund"
- "Praxis-Chef" → "Prof. Dr. med. Stefan Rohde"
- Datumsangaben: 2026-04-27

ZWEI NEUE FOLIEN:

NEUE FOLIE 2.5 (zwischen "Das Problem" und "Die Lösung"):
Titel: "Engineering Harnessing — Eine neue Methodik für Medical AI"
Inhalt (Bullet-Points):
• Pixel-Modell (Layer 1) — MFSD-UNet, State-of-the-Art
• Decision-Tree-Harvesting (Layer 2) — Lerne, WIE der Arzt denkt
• Daily-Learning-Loop (Layer 3) — Modell verbessert sich jede Nacht
• Memory-Hierarchie für Entwicklungs-AI: Jeder Run macht den nächsten klüger
• Resultat: 24 Monate von der Idee zum zertifizierten System (statt 5 Jahre)
Sprechernote: "Das ist der eigentliche Beitrag. Nicht das Bilderkennungsmodell 
— sondern die Methodik dahinter. Sie macht aus jeder ärztlichen Entscheidung 
ein wiederverwendbares Trainings-Asset, ohne dass jemals Patientendaten das 
Klinikum verlassen."

NEUE FOLIE 11.5 (zwischen "Das Investment" und "Nächste Schritte"):
Titel: "Warum das Klinikum Dortmund?"
Inhalt:
• Akademisches Lehrkrankenhaus mit Forschungstradition
• Aroob arbeitet bereits hier — natürliche Datenakquise und Validierung
• Etablierte Beziehung zu Prof. Rohde (freundliche Gespräche bereits geführt)
• Internationales Netzwerk: HAW Hamburg + Sarah Specialty Hospital (Jordanien)
• Positionierung als KI-Vorreiter in der Neuroradiologie
Sprechernote: "Wir hätten dieses Projekt theoretisch an jeder Klinik machen 
können. Wir wollen es hier machen, weil Aroob hier ist und weil Sie sie 
bereits kennen. Das ist kein Zufall, das ist eine Investition in eine 
bestehende Beziehung."

ZUSÄTZLICH:
- Folie 9 ("Der Nutzen für die Praxis") umbenennen zu "Der Nutzen für das 
  Klinikum Dortmund". Inhaltliche Bullets ergänzen um:
  - Drittmittel-Fähigkeit (BMBF)
  - Erste DSGVO-konforme KI-Implementation am Haus
  - Wiederverwendbare Methodik für weitere Promotionen

Speichere als: Carotis_Ai_Rohde_v2.pptx
```

---

## PROMPT G — Erweitere Ki_Tools_Marktanalyse.docx → v2 (Floy-Recherche)

```
Erweitere die Floy-Recherche Ki_Tools_Marktanalyse.docx um ein abschließendes 
Kapitel "Gap-Analyse: Warum Floy für die Carotis-Diagnostik nicht reicht".

INHALT des neuen Kapitels:

1. Floy-Schwerpunkt: CT-Thorax (Lungennoduli, Pneumonie). Carotis-Diagnostik 
   ist KEIN dokumentierter Use-Case in der Floy-Produktdokumentation.

2. Architektur: Floy ist cloud-basiert (laut Produktdokumentation und Blog). 
   Damit problematisch unter:
   • DSGVO Art. 9 (Gesundheitsdaten — strenge Cloud-Anforderungen)
   • EU AI Act Art. 10 (Data Governance bei High-Risk AI)
   • BSI-Empfehlungen für Krankenhausinformations-Systeme

3. Erklärbarkeit: Floy bietet primär Bounding-Boxes und Konfidenz-Werte. 
   Keine Grad-CAM-Heatmaps, keine SHAP-Analyse, kein expliziter 
   Reasoning-Capture. Damit nur teilweise EU-AI-Act-Art-13-konform.

4. Multi-Center / Transnational: Floy hat keinen dokumentierten Use-Case 
   für Multi-Center-Studien mit Differenz zwischen DE und MENA-Region 
   (relevant für die geplante Sarah-Hospital-Kooperation).

5. Lock-In: Floy-Lizenzmodell ist proprietär; bei Anbieter-Wechsel sind 
   Trainings-Investitionen und Workflow-Anpassungen verloren.

6. Tabelle (Floy vs. Carotis-AI):
   | Kriterium | Floy | Carotis-AI |
   |-----------|------|------------|
   | Architektur | Cloud | Local-First Edge |
   | DSGVO | erhöhte Anforderungen | by Design konform |
   | Carotis-Spezialisierung | nicht dokumentiert | Kern-Use-Case |
   | Erklärbarkeit (XAI) | Bounding-Box + Konfidenz | Grad-CAM + SHAP + Reasoning-Capture |
   | EU AI Act | teilweise konform | proaktiv konform |
   | Decision-Tree-Harvesting | nein | ja, als Trainings-Loss |
   | Multi-Center-DE/JO | nein | ja, transnational designed |
   | Lock-In | hoch | null (Open-Source-Stack + ONNX) |
   | Lizenzkosten | wiederkehrend | einmalig (HAW-Förderung) |

FAZIT: Floy ist eine valide Lösung für die Anwendungsfälle, für die sie 
gebaut wurde (CT-Thorax). Für die Carotis-Diagnostik im Klinikum Dortmund 
unter Berücksichtigung von DSGVO und EU AI Act ist eine maßgeschneiderte 
Lösung sowohl regulatorisch sauberer als auch wissenschaftlich publikations-
stärker.

Speichere als: KI_Tools_Marktanalyse_v2.docx
```

---

## PROMPT H — Aktualisiere Carotis_Ai_Konzept.docx → v2

```
Aktualisiere das Konzeptpapier Carotis_Ai_Konzept.docx auf das neue Setting 
und ergänze den Decision-Tree-Harvesting-Abschnitt detaillierter.

ÄNDERUNGEN:
- Adressat: "Prof. Dr. med. Stefan Rohde, Klinikum Dortmund"
- Aroob's Titel: "Ärztin in Weiterbildung für Radiologie"
- Setting: "Klinikum Dortmund"
- Datum: 2026-04-27

NEUER ABSCHNITT "DECISION-TREE-HARVESTING — Die eigentliche Innovation" 
(2 Seiten, einfügen vor "Vergleich Floy vs. Carotis-AI"):

[Hier das gesamte Konzept aus 05_DECISION_TREE_HARVESTING.md zusammenfassen 
in 2 Seiten — Schema kurz, UI-Spec kurz, Trainings-Pfad kurz, Anonymisierungs-
Pipeline kurz, geplante Publikation. Akademisch-präzise, aber für einen 
klinisch-tätigen Arzt verständlich. Keine JSON-Snippets — Prosa und Tabellen.]

ERWEITERE den Abschnitt "Nutzen für das Klinikum Dortmund" um:
• Methodik-Framework als wiederverwendbare Plattform für weitere KI-
  Promotionen am Haus
• Forschungs-Drittmittel-Fähigkeit (BMBF)
• Mögliche Co-Authorship von Prof. Rohde auf zwei Papers (klinisch + 
  methodisch)
• Reputationsgewinn als technologisches und regulatorisches Vorbild für 
  KI-Implementation in der deutschen Radiologie

Speichere als: Carotis_AI_Konzept_v2.docx
```

---

## Reihenfolge der Ausführung

1. **PROMPT G** zuerst (Floy-Recherche) — die ist die Voraussetzung für die Mail
2. **PROMPT H** (Konzeptpapier) — zweite Anlage für die Mail
3. **PROMPT C** (Exposé) — dritte zentrale Anlage
4. **PROMPT D** (Tech-Beschreibung) — zusätzliche Anlage
5. **PROMPT E** (Value Proposition) — Mit-Dokument für Lou's Demo
6. **PROMPT F** (PowerPoint) — für den Termin selbst
7. **PROMPT B** (altes Anschreiben → v2) — Backup-Variante
8. **PROMPT A** (Mail-Text) — ZULETZT, weil sie auf alle anderen Dokumente referenziert

---

## Nach jedem Stride-Run

In `memory/runs/` einen Eintrag schreiben:

```markdown
# 2026-04-27 · Stride · <Prompt-Name>

**Goal:** Update <docname> auf Klinikum Dortmund / Rohde-Setting
**Done:** <docname>_v2.docx erstellt
**Surprised by:** <was hat Stride anders gemacht als erwartet?>
**Avoided:** <welche Halluzination musstest du korrigieren?>
**Next:** Review durch Aroob, dann nächster Prompt in der Liste
**Memory updates:** keine (bestehende Dokumente)
```

So bleibt das System lernfähig — wir wissen beim nächsten Mal, welche Prompts schon mal Probleme bereitet haben.

---

**Letzte Aktualisierung:** 2026-04-27 · Opus 4.7
