# STRIDE PROMPT E — Kopieren & Einfügen

> **Vorher:** Öffne Stride. Lade `Value_Proposition_Ki_Carotis.docx` hoch.
> **Danach:** Output speichern als `Value_Proposition_Klinikum_v2.docx`

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

## SCHRITT 2: Prompt E einfügen

```
Aktualisiere die Value Proposition Value_Proposition_Ki_Carotis.docx auf Prof. Dr. med. Stefan Rohde / Klinikum Dortmund.

ÄNDERUNGEN:
- Zielgruppe: "Prof. Dr. med. Stefan Rohde und das Klinikum Dortmund"
- Setting durchgehend: "Klinikum Dortmund"

NEUE BULLET-POINTS in die Sektion "Wissenschaftlicher Ruhm":
• Forschungs-Leadership: Klinikum Dortmund als führendes Zentrum für Local-First-KI in der Neuroradiologie
• Engineering-Harnessing-Methodik publizierbar als eigenes Paper — Lou als Erst-Autor, Rohde als Senior-Author
• Drittmittel-Fähigkeit: BMBF KI-in-der-Medizin-Förderprogramm

NEUE BULLET-POINTS in die Sektion "Personalbindung":
• Aroob bleibt langfristig am Klinikum durch die Promotion gebunden
• Zugang zum HAW-Hamburg-Netzwerk (Margaritoff, Tolg, van Stevendaal) für weitere kooperative Promotionen
• Lou Alshdaifat als langfristiger technischer Ansprechpartner für KI-Projekte am Klinikum

Speichere als: Value_Proposition_Klinikum_v2.docx
```

---

## SCHRITT 3: Review-Checkliste

- [ ] Datei heißt `Value_Proposition_Klinikum_v2.docx`
- [ ] BMBF-Drittmittel erwähnt
- [ ] HAW-Netzwerk erwähnt
- [ ] Lou als langfristiger Ansprechpartner
- [ ] Diff-Liste am Ende
