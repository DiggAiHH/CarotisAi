# STRIDE PROMPT A — Kopieren & Einfügen

> **Vorher:** Öffne Stride. Kein Upload nötig (komplett neuer Text).
> **Danach:** Output speichern als `Mail_Aroob_an_Rohde_v2.docx`
> **Auch:** Plaintext-Variante existiert bereits als `Mail_Aroob_an_Rohde_DRAFT.txt`

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

## SCHRITT 2: Prompt A einfügen

```
Schreibe eine professionelle E-Mail von Aroob Alrawashdeh (Ärztin in Weiterbildung für Radiologie, Klinikum Dortmund) an Prof. Dr. med. Stefan Rohde (Direktor, Klinik für Radiologie und Neuroradiologie, Klinikum Dortmund).

KONTEXT:
- Aroob hat von Prof. Rohde eine Aufgabenstellung bekommen: Recherche zu KI-Tools in der Radiologie, speziell Floy-Software.
- Sie liefert die Recherche jetzt ab UND zusätzlich ein eigenes Konzept ("Carotis-AI"), das sie gemeinsam mit ihrem Schwager Laith Alshdaifat (Medizintechniker, HAW Hamburg) und unter Beratung von HAW-Professoren (Margaritoff, Tolg) entwickelt hat.
- Sie bittet um ein 30-minütiges Gespräch mit Prof. Rohde — zusammen mit Laith — um beides vorzustellen.

DIE 5 KERN-PUNKTE in der Mail:
1. Floy ist cloud-basiert mit CT-Thorax-Schwerpunkt — für Carotis nur bedingt geeignet, und unter DSGVO/EU AI Act in einem deutschen Klinikum problematisch.
2. Eine Local-First, DSGVO-konforme, erklärbare Lösung für die Carotis-Diagnostik existiert bisher nicht.
3. Aroob hat mit Lou ein eigenes Konzept entwickelt: Carotis-AI, MFSD-UNet-basiert, lokal lauffähig, mit Decision-Tree-Harvesting (lernt die ärztliche Begründung, nicht nur das Bild).
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
- Aroob als Mensch hinter dem Text spürbar — sie ist die, die die Promotion will, nicht eine Engineering-Marketing-Maschine.
- Keine Übertreibungen.
- Termin-Vorschlag konkret: "in der kommenden Woche, 30 Minuten" + Angebot, sich nach seinem Kalender zu richten.

Speichere als: Mail_Aroob_an_Rohde_v2.docx
```

---

## SCHRITT 3: Review-Checkliste

- [ ] Datei heißt `Mail_Aroob_an_Rohde_v2.docx`
- [ ] Mail-Text < 30 Zeilen
- [ ] 3 Anlagen explizit gelistet
- [ ] 30-Min-Termin-Bitte konkret
- [ ] Aroob als Mensch spürbar (nicht Marketing-Maschine)
- [ ] Diff-Liste am Ende
