# Stride V3 Prompt W-07: Rohde-Anleitung 2-Seiten-PDF

## Ziel
Erstelle eine 2-seitige Anleitung fuer Prof. Dr. Rohde, die ihm Schritt-fuer-Schritt erklaert, wie er die Carotis-AI Demo nutzt. Die Anleitung wird von Aroob zusammen mit dem Token und dem Link uebergeben.

## Kontext
- Demo-URL: `https://carotis.diggai.de`
- API-URL: `https://api.carotis.diggai.de`
- Token: Wird separat uebergeben (Rohde-spezifischer Demo-Token, 30 Tage gueltig, 50 Requests)
- Die Anleitung muss fuer einen Mediziner verstaendlich sein, nicht fuer einen Informatiker
- Sprache: Deutsch

## Inhalt (2 Seiten A4)

### Seite 1: Schnellstart (60 Sekunden zur ersten Analyse)

1. **Oeffnen Sie** `https://carotis.diggai.de` in Ihrem Browser (Chrome, Firefox, Edge — alle aktuellen Versionen)
2. **Geben Sie Ihren Token ein**, wenn Sie danach gefragt werden. Der Token ist Ihr persoenlicher Zugang — bitte nicht weitergeben.
3. **Ziehen Sie eine DICOM-Datei** in den grauen Bereich oder klicken Sie auf "Datei auswaehlen". Sie koennen die Demo-Daten verwenden (Link auf der Seite) oder eine eigene anonymisierte CTA-Datei.
4. **Warten Sie 3-5 Sekunden.** Das System analysiert das Bild lokal auf dem Server.
5. **Sehen Sie das Ergebnis:**
   - Stenosegrad (0-100%)
   - Plaque-Vulnerability-Score (niedrig / mittel / hoch)
   - Grad-CAM Heatmap (rote Bereiche = Modell-Attention)
   - Confidence-Badge (kalibriert, nicht roh)

### Seite 2: Decision-Tree-Capture (die Innovation)

6. **Bewerten Sie das Ergebnis.** Stimmt es mit Ihrer klinischen Einschaetzung ueberein?
7. **Oeffnen Sie das Decision-Formular** rechts unten. Hier koennen Sie:
   - Ihre klinische Bewertung eingeben (Stenosegrad, Plaque-Typ)
   - Den entscheidenden Befund merkmal angeben (z.B. "kalcifizierte Plaque im Bulbus")
   - Ihr Vertrauen in die KI-Unterstuetzung angeben (1-5)
   - Optional: Freitext (wird auf PII geprueft)
8. **Senden Sie den Decision-Tree.** Das System speichert nur anonymisierte Daten.
9. **Wiederholen Sie mit weiteren Faellen.** Jeder Fall verbessert das Modell.

### FAQ (kurz)

- **Q: Was passiert mit meinen Daten?**
  A: Nichts. Die DICOM-Datei wird im Browser geoeffnet, analysiert und verworfen. Kein Cloud-Upload.

- **Q: Was ist der Unterschied zu Floy?**
  A: Carotis-AI laeuft lokal (DSGVO-konform), ist spezialisiert auf Carotis, und lernt aus Ihren Entscheidungen.

- **Q: Wie lange ist der Token gueltig?**
  A: 30 Tage. Bei Bedarf verlaengern wir ihn.

- **Q: Funktioniert das auf dem Klinikum-Rechner?**
  A: Ja, nur ein moderner Browser noetig. Keine Installation.

- **Q: Wer sieht meine Decision-Trees?**
  A: Nur das anonymisierte Aggregat. Keine Rueckschluesse auf einzelne Personen moeglich.

## Format
- Word-Dokument (.docx)
- Seite 1: Screenshots der UI (wenn verfuegbar) oder Platzhalter [Screenshot: Login] [Screenshot: Upload] [Screenshot: Ergebnis]
- Seite 2: Screenshots des Decision-Forms
- Fusszeile: "Carotis-AI Demo | carotis.diggai.de | Fragen: aroob.alrawashdeh@klinikum-dortmund.de"

## Output
Speichere als `Stride V3/Rohde_Anleitung_v1.docx`
