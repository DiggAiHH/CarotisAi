# STRIDE PROMPT B — Kopieren & Einfügen

> **Vorher:** Öffne Stride. Lade `Anschreiben_Dr_Alrawashdeh_KI_Carotis_Diagnostik.docx` hoch.
> **Danach:** Output speichern als `Anschreiben_Aroob_an_Rohde_v2.docx`

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

## SCHRITT 2: Prompt B einfügen

```
Aktualisiere die Datei Anschreiben_Dr_Alrawashdeh_KI_Carotis_Diagnostik.docx auf das neue Setting "Klinikum Dortmund / Prof. Rohde / Aroob als Ärztin in Weiterbildung".

ÄNDERUNGEN:
- Empfänger: ändere ÜBERALL "Praxis-Chef" / "Praxisinhaber" / "Herr Dr. [Name]" zu "Prof. Dr. med. Stefan Rohde" / "Direktor der Klinik für Radiologie und Neuroradiologie, Klinikum Dortmund".
- Absender: ändere "Fachärztin" zu "Ärztin in Weiterbildung für Radiologie".
- Institution: ändere "Praxis" / "Praxisinhaber" zu "Klinikum Dortmund".
- Datum: 2026-04-27.

INHALTLICHE ERWEITERUNG:
Füge nach dem Absatz "Die technische Umsetzung erfolgt durch meinen Schwager…" einen neuen Absatz ein:

  "Wir nutzen dabei einen Engineering-Harnessing-Ansatz: systematische Wissensaggregation aus Medizin, Engineering und KI, kombiniert mit einer Mehrebenen-Architektur (Pixel-Modell + Decision-Tree-Harvesting + Daily-Learning-Loop). Das Modell lernt nicht nur aus den Bildern, sondern aus den anonymisierten Begründungs-Strukturen der Befunder — dadurch wird der eigentliche Wert der ärztlichen Expertise systematisch erfasst und trägt zur Verbesserung des Systems bei."

FÜGE EINEN NEUEN BULLET-POINT in die Vorteils-Liste ein:
- "Methodische Innovation mit Publikationspotenzial: Decision-Tree-Harvesting ist ein neuer Beitrag zur Medical-AI-Literatur (Zieljournal Medical Image Analysis oder NEJM AI)."

TON: respektvoll, Engineering-selbstbewusst. KEIN Bittstellertum.

Speichere als: Anschreiben_Aroob_an_Rohde_v2.docx
```

---

## SCHRITT 3: Review-Checkliste

- [ ] Datei heißt `Anschreiben_Aroob_an_Rohde_v2.docx`
- [ ] Empfänger "Prof. Dr. med. Stefan Rohde" + "Klinikum Dortmund"
- [ ] Engineering-Harnessing-Erläuterung im Anschreiben
- [ ] Aroob als "Ärztin in Weiterbildung"
- [ ] Diff-Liste am Ende
