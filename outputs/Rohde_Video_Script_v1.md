# Walkthrough-Video-Skript: Carotis-AI Demo fuer Prof. Rohde

**Laenge:** 3:00 Minuten (180 Sekunden)
**Format:** Bildschirmaufnahme + Sprecherstimme (Lou)
**Ziel:** Prof. Rohde sieht in 3 Minuten, was Carotis-AI kann, ohne selbst klicken zu muessen.

---

## Segment 1: Intro (0:00 - 0:20)
**[B-Roll: Fade-in von carotis.diggai.de Landing Page]**

**Sprecher (Lou):**
"Guten Tag, Herr Professor Rohde. In den naechsten drei Minuten zeige ich Ihnen, was aus der Floy-Recherche geworden ist: Carotis-AI. Ein lokal betriebenes, erklaerbares KI-System fuer die Carotis-Stenose-Diagnostik. Kein Cloud-Upload, keine Installation — nur ein Browser."

**[Cut zu: Browser-Tab mit Demo-Login]**

---

## Segment 2: Login + Upload (0:20 - 0:50)
**[B-Roll: Mauszeiger tippt Token ein, klickt Login]**

**Sprecher:**
"Mit dem Token, den Aroob Ihnen uebergeben hat, oeffnen wir die Demo. Der Token ist 30 Tage gueltig — genug Zeit, das System in Ihrem Tempo zu erkunden."

**[Cut zu: Upload-Bereich mit Drag-and-Drop]**

**Sprecher:**
"Wir ziehen eine CTA-DICOM-Datei in den Viewer. Das kann eine der 30 Demo-Faelle sein oder eine eigene anonymisierte Datei aus Ihrem Klinikum."

**[B-Roll: Datei wird hochgeladen, Ladeanimation]**

**Sprecher:**
"Die Datei wird im Browser analysiert — keine Daten verlassen Ihren Rechner."

---

## Segment 3: Ergebnis + Heatmap (0:50 - 1:30)
**[B-Roll: DICOM-Bild erscheint, Heatmap-Overlay fade-in]**

**Sprecher:**
"Nach drei Sekunden sehen wir das Ergebnis. Links das Original-CT, rechts die KI-Analyse. Der Stenosegrad: 67 Prozent. Der Plaque-Vulnerability-Score: mittel."

**[B-Roll: Mauszeiger gleitet ueber Heatmap-Overlay]**

**Sprecher:**
"Die roten Bereiche zeigen, wo das Modell hingeschaut hat — Grad-CAM heisst das. Nicht ein Black-Box-Score, sondern eine Begruendung, die Sie als Radiologe bewerten koennen."

**[B-Roll: Opacity-Slider wird bewegt, Heatmap wird transparenter]**

**Sprecher:**
"Der Slider erlaubt es, die Ueberlagerung anzupassen — je nachdem, was fuer die Befundung hilfreicher ist."

---

## Segment 4: Decision-Tree-Capture (1:30 - 2:10)
**[B-Roll: Scroll nach rechts unten zum Decision-Formular]**

**Sprecher:**
"Jetzt kommt der wichtigste Teil. Als Radiologe bewerte ich das Ergebnis — und das System lernt von meiner Bewertung."

**[B-Roll: Formular wird ausgefuellt — Stenosegrad 65%, Plaque-Typ kalcifiziert, deciding_feature "Bulbus-Stenose"]**

**Sprecher:**
"Ich gebe meine klinische Einschaetzung ein, markiere den entscheidenden Befund — und bewerte, wie sehr ich der KI-Unterstuetzung vertraue. Das ist keine Pflicht, aber jeder eingetragene Fall verbessert das Modell."

**[B-Roll: Submit-Button, gruene Bestaetigung]**

**Sprecher:**
"Die Daten werden anonymisiert gespeichert. Kein Name, keine Patienten-ID, kein Geburtsdatum. Nur die medizinische Entscheidung."

---

## Segment 5: Trust-Score + Kalibrierung (2:10 - 2:40)
**[B-Roll: AiPanel zoomt auf Confidence-Badge und Trust-Score]**

**Sprecher:**
"Ein Wort zur Zuverlaessigkeit. Was Sie hier sehen, ist kein roher Modell-Confidence. Der Trust-Score kombiniert drei Faktoren: die Modell-Sicherheit, die Kalibrierungs-Qualitaet und die Transparenz der Entscheidung."

**[B-Roll: Mouseover auf Trust-Score zeigt Breakdown]**

**Sprecher:**
"Das heisst: wenn das System unsicher ist, sagt es das auch. Kein false confidence. Das ist fuer die klinische Praxis entscheidend."

---

## Segment 6: Outro + Ask (2:40 - 3:00)
**[B-Roll: Langsamer Zoom-out auf die gesamte UI]**

**Sprecher:**
"Carotis-AI ist keine fertige Software — es ist ein Promotionsprojekt. Aber der Prototyp steht, die Architektur ist robust, und das Team ist bereit. Herr Professor Rohde, wir wuerden uns freuen, wenn Sie die wissenschaftliche Betreuung uebernehmen. Aroob und ich stehen fuer ein Gespraech jederzeit zur Verfuegung."

**[B-Roll: Fade-out auf carotis.diggai.de mit Kontakt-E-Mail]**

**[Text-Einblendung:]**
"Carotis-AI | carotis.diggai.de | Aroob Alrawashdeh | Laith Alshdaifat"

---

## Aufnahme-Hinweise fuer Lou

1. **Vor der Aufnahme:**
   - `run_demo.sh` starten (Backend + Frontend lokal)
   - Browser im Inkognito-Modus (keine Extensions, sauberes UI)
   - Aufloesung: 1920x1080, 60 FPS
   - Mauszeiger: deutlich sichtbar (macOS: Mouse Highlight, Windows: PowerToys)

2. **Waehrend der Aufnahme:**
   - Langsam klicken (nicht unter Druck)
   - Jede Aktion 1-2 Sekunden Pause danach
   - Bei Fehlern: stoppen, korrigieren, Segment neu aufnehmen
   - Stimme: ruhig, nicht ueberzeugend sondern sachlich

3. **Nach der Aufnahme:**
   - Schneiden mit CapCut oder Descript
   - Untertitel auf Deutsch (fuer Rohde wichtig)
   - Keine Musik (Prof. akademisch, nicht werblich)
   - Export: MP4, 1080p, max. 50 MB (Mail-Anhang)

4. **Dateiname:**
   `CarotisAI_Demo_Rohde_2026-04-30.mp4`
