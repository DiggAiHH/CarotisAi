# STRIDE PROMPT C — Kopieren & Einfügen

> **Vorher:** Öffne Stride. Lade `Ki_Carotis_Expose.docx` hoch.
> **Danach:** Output speichern als `Expose_Carotis_AI_Rohde_v2.docx`

---

## SCHRITT 1: Globalen Kontext einfügen

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

## SCHRITT 2: Prompt C einfügen

```
Aktualisiere das Exposé Ki_Carotis_Expose.docx.

ÄNDERUNGEN:
- Kandidatin: "Aroob Alrawashdeh, Ärztin in Weiterbildung für Radiologie, Klinikum Dortmund"
- Betreuer: "Prof. Dr. med. Stefan Rohde, Direktor der Klinik für Radiologie und Neuroradiologie, Klinikum Dortmund"
- Institution durchgehend: "Klinikum Dortmund"
- Datum: 2026-04-27

NEUER ABSCHNITT (einfügen nach "Zielsetzung", VOR "Methodik"):

═══════════════════════════════════════════════════════
ENGINEERING HARNESSING FRAMEWORK

Die Promotionsarbeit nutzt einen neuartigen, systematischen Ansatz für die Entwicklung medizinischer KI-Systeme. Das Framework hat drei Layer:

1. PIXEL-MODELL (State-of-the-Art): MFSD-UNet-Architektur (U-Net + Swin Transformer + Deep Supervision) mit Dice-Coefficient ≥ 0,90 und Sensitivity ≥ 0,99 für die Carotis-Vessel-Segmentierung. Aktueller Benchmark nach Xie et al. (Quantitative Imaging in Medicine and Surgery, 2024).

2. DECISION-TREE-HARVESTING (Innovation): Nach jeder Befundung wird in einer 30-Sekunden-Mini-UI strukturiert erfasst, welches Bild-Feature für den Befunder ausschlaggebend war, welche Differentialdiagnosen erwogen und ausgeschlossen wurden, und mit welcher Konfidenz die Diagnose getroffen wurde. Diese Decision-Trees werden anonymisiert (DICOM PS 3.15) in einen lokalen Korpus geschrieben.

3. DAILY-LEARNING-LOOP: Ein nächtlicher Cron-Job trainiert das Modell inkrementell auf den neu hinzugekommenen Decision-Trees + Anomalien (Fälle mit AI-Mensch-Diskrepanz). Performance-Vergleich vor/nach jeder Iteration; Auto-Rollback bei Verschlechterung.

Die Innovation liegt nicht im Bilderkennungs-Modell selbst, sondern in der systematischen Erfassung und Nutzung der ärztlichen Entscheidungs-Begründung als zusätzliche Trainings-Information. Damit wird Tacit Knowledge — der eigentliche Wert von 10 Jahren Facharztausbildung — erstmals strukturiert in die KI-Trainingspipeline eingespeist.

Daraus ergeben sich zwei Publikationen:
  • Klinisches Validierungs-Paper (Carotis-AI vs. Konsens-Ground-Truth, transnational DE/JO, n ≥ 300) — Zieljournal Radiology / JNIS
  • Methodisches Paper (Decision-Tree-Harvesting als Trainings-Paradigma) — Zieljournal Medical Image Analysis / NEJM AI
═══════════════════════════════════════════════════════

ÄNDERE die Methodik-Tabelle entsprechend:
Phase P0: Stakeholder-Alignment + Code-Stack (done)
Phase P1: Ethikantrag + Datenvertrag + DSGVO-Setup
Phase P2: Datenakquise retrospektiv n≥500, Anonymisierung
Phase P3: Modell-Training MFSD-UNet, ONNX-Export, Decision-Tree-Loss
Phase P4: Edge-Server-Integration, UI, Decision-Tree-Capture
Phase P5: Klinische Validierung DE + Jordanien
Phase P6: Manuskript Radiology / JNIS, Disputation
Phase P7: MDR-Zertifizierung, Skalierung

ERGÄNZE im Abschnitt "Praktischer Nutzen für das Klinikum Dortmund":
- Erste DSGVO-konforme KI-Implementation am Haus
- Drittmittelfähig (BMBF KI-in-der-Medizin-Programm)
- Methodik-Framework wiederverwendbar für weitere Promotionen am Klinikum
- Reputationsgewinn als KI-Vorreiter in der Neuroradiologie

Speichere als: Expose_Carotis_AI_Rohde_v2.docx
```

---

## SCHRITT 3: Review-Checkliste

- [ ] Datei heißt `Expose_Carotis_AI_Rohde_v2.docx`
- [ ] Engineering-Harnessing-Block vorhanden
- [ ] Methodik-Tabelle zeigt P0-P7 (nicht M1-M5)
- [ ] Aroob als "Ärztin in Weiterbildung"
- [ ] "Klinikum Dortmund" durchgehend
- [ ] Diff-Liste am Ende
