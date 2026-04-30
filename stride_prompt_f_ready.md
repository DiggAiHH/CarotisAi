# STRIDE PROMPT F — Kopieren & Einfügen

> **Vorher:** Öffne Stride. Lade `Carotis_Ai.pptx` hoch.
> **Danach:** Output speichern als `Carotis_Ai_Rohde_v2.pptx`

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

## SCHRITT 2: Prompt F einfügen

```
Aktualisiere die PowerPoint-Präsentation Carotis_Ai.pptx auf Prof. Dr. med. Stefan Rohde am Klinikum Dortmund.

GLOBALE ÄNDERUNGEN auf allen Folien:
- "Praxis" → "Klinikum Dortmund"
- "Dr. Aroob Alrawashdeh, Fachärztin" → "Aroob Alrawashdeh, Ärztin in Weiterbildung für Radiologie, Klinikum Dortmund"
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
Sprechernote: "Das ist der eigentliche Beitrag. Nicht das Bilderkennungsmodell — sondern die Methodik dahinter. Sie macht aus jeder ärztlichen Entscheidung ein wiederverwendbares Trainings-Asset, ohne dass jemals Patientendaten das Klinikum verlassen."

NEUE FOLIE 11.5 (zwischen "Das Investment" und "Nächste Schritte"):
Titel: "Warum das Klinikum Dortmund?"
Inhalt:
• Akademisches Lehrkrankenhaus mit Forschungstradition
• Aroob arbeitet bereits hier — natürliche Datenakquise und Validierung
• Etablierte Beziehung zu Prof. Rohde (freundliche Gespräche bereits geführt)
• Internationales Netzwerk: HAW Hamburg + Sarah Specialty Hospital (Jordanien)
• Positionierung als KI-Vorreiter in der Neuroradiologie
Sprechernote: "Wir hätten dieses Projekt theoretisch an jeder Klinik machen können. Wir wollen es hier machen, weil Aroob hier ist und weil Sie sie bereits kennen. Das ist kein Zufall, das ist eine Investition in eine bestehende Beziehung."

ZUSÄTZLICH:
- Folie 9 ("Der Nutzen für die Praxis") umbenennen zu "Der Nutzen für das Klinikum Dortmund". Inhaltliche Bullets ergänzen um:
  - Drittmittel-Fähigkeit (BMBF)
  - Erste DSGVO-konforme KI-Implementation am Haus
  - Wiederverwendbare Methodik für weitere Promotionen

Speichere als: Carotis_Ai_Rohde_v2.pptx
```

---

## SCHRITT 3: Review-Checkliste

- [ ] Datei heißt `Carotis_Ai_Rohde_v2.pptx`
- [ ] Mindestens 14 Folien (12 alte + 2 neue)
- [ ] Folie 2.5 Titel enthält "Engineering Harnessing"
- [ ] Folie 11.5 Titel enthält "Warum das Klinikum Dortmund"
- [ ] Aroob als "Ärztin in Weiterbildung"
- [ ] Diff-Liste am Ende
