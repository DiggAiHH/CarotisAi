# STRIDE PROMPT H — Kopieren & Einfügen

> **Vorher:** Öffne Stride. Lade `Carotis_Ai_Konzept.docx` hoch.
> **Danach:** Output speichern als `Carotis_AI_Konzept_v2.docx`

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

## SCHRITT 2: Prompt H einfügen

```
Aktualisiere das Konzeptpapier Carotis_Ai_Konzept.docx auf das neue Setting und ergänze den Decision-Tree-Harvesting-Abschnitt detaillierter.

ÄNDERUNGEN:
- Adressat: "Prof. Dr. med. Stefan Rohde, Klinikum Dortmund"
- Aroob's Titel: "Ärztin in Weiterbildung für Radiologie"
- Setting: "Klinikum Dortmund"
- Datum: 2026-04-27

NEUER ABSCHNITT "DECISION-TREE-HARVESTING — Die eigentliche Innovation" (2 Seiten, einfügen vor "Vergleich Floy vs. Carotis-AI"):

Decision-Tree-Harvesting ist ein neuartiges Trainings-Paradigma für medizinische KI-Systeme. Statt nur aus den Bildern zu lernen, erfasst das System nach jeder Befundung strukturiert die ärztliche Entscheidungs-Begründung.

WIE ES FUNKTIONIERT:
Nach jeder AI-gestützten Befundung erscheint eine 30-Sekunden-UI. Der Befunder markiert:
1. Welches Bild-Feature ausschlaggebend war (z.B. "dünne Kappe über LRNC")
2. Welche Differentialdiagnosen erwogen und ausgeschlossen wurden
3. Mit welcher Konfidenz die Diagnose getroffen wurde

Diese Informationen werden anonymisiert (DICOM PS 3.15 De-Identification Profile) in einen lokalen Korpus geschrieben. Ein nächtlicher Cron-Job trainiert das Modell inkrementell auf den neuen Decision-Trees. Performance-Vergleich vor/nach jedem Lern-Schritt; Auto-Rollback bei Verschlechterung.

DIE INNOVATION:
Der eigentliche Wert eines Radiologen liegt nicht in der Bilderkennung, sondern in der klinischen Beurteilung — der "Tacit Knowledge" aus 10 Jahren Facharztausbildung. Decision-Tree-Harvesting strukturiert dieses Wissen erstmals systematisch als Trainings-Information.

PUBLIKATIONS-POTENZIAL:
• Klinisches Validierungs-Paper (Carotis-AI vs. Konsens-Ground-Truth, transnational DE/JO, n ≥ 300) — Zieljournal Radiology / JNIS
• Methodisches Paper (Decision-Tree-Harvesting als Trainings-Paradigma) — Zieljournal Medical Image Analysis / NEJM AI

SCHEMA (vereinfacht, ohne JSON):
Jeder Decision-Tree enthält:
- Bild-Feature (z.B. "ThinCap")
- Differentialdiagnosen (erwogen / ausgeschlossen)
- Konfidenz (low/medium/high)
- Override-Flag (wenn Arzt AI widerspricht)
- Timestamp (anonymisiert)

ERWEITERE den Abschnitt "Nutzen für das Klinikum Dortmund" um:
• Methodik-Framework als wiederverwendbare Plattform für weitere KI-Promotionen am Haus
• Forschungs-Drittmittel-Fähigkeit (BMBF)
• Mögliche Co-Authorship von Prof. Rohde auf zwei Papers (klinisch + methodisch)
• Reputationsgewinn als technologisches und regulatorisches Vorbild für KI-Implementation in der deutschen Radiologie

Speichere als: Carotis_AI_Konzept_v2.docx
```

---

## SCHRITT 3: Review-Checkliste

- [ ] Datei heißt `Carotis_AI_Konzept_v2.docx`
- [ ] Decision-Tree-Harvesting-Abschnitt ist ~2 Seiten
- [ ] "Klinikum Dortmund" durchgehend (kein "Praxis")
- [ ] Aroob als "Ärztin in Weiterbildung"
- [ ] Diff-Liste am Ende
