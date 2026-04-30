# Stride V3 Prompt W-09: Anschreiben Aroob an Rohde (Mail v3)

## Ziel
Erstelle das Anschreiben von Aroob an Prof. Rohde — Version 3. Der wesentliche Unterschied zu v2: wir liefern nicht nur Konzept-Papiere, sondern eine **live lauffaehige Demo** mit persoenlichem Token.

## Strategie-Shift v2 -> v3
- v2: "Hier ist unser Konzept, wollen Sie es sich ansehen?"
- v3: "Hier ist unsere Demo — sie laeuft bereits. Ihr persoenlicher Token ist gueltig fuer 30 Tage."
- Der Wow-Moment verschiebt sich vom Termin in die Mail selbst.
- Rohde kann vor dem Termin bereits selbst testen.

## Anschreiben-Struktur (1 Seite, kein Wall-of-Text)

### Betreff
`Re: Doktorarbeit – Live-Demo verfuegbar + Carotis-AI Update`

### Absatz 1: Dank + Kontext (3 Saetze)
- Dank fuer die Gespraechsbreitschaft
- Kurze Erinnerung: Floy-Recherche erledigt, eigenes System entwickelt
- **Neu:** Live-Demo steht bereit

### Absatz 2: Die Demo in 4 Bullet Points
- **URL:** `https://carotis.diggai.de`
- **Token:** [WIRD VON LOU EINGEFUEGT — siehe generate_rohde_token.py Output]
- **Was:** DICOM-Upload, KI-Analyse mit Heatmap, Decision-Tree-Capture
- **Dauer:** 5 Minuten fuer den ersten Fall

### Absatz 3: Was anders ist als Floy (3 Saetze)
- Local-First (kein Cloud-Upload)
- Carotis-spezifisch (nicht Thorax-generisch)
- Lernfaehig (jeder Decision-Tree verbessert das Modell)

### Absatz 4: Der akademische Mehrwert (2 Saetze)
- Zwei Papers moeglich (klinisch + methodisch)
- Engineering-Harnessing als publizierbare Methodik

### Absatz 5: Der Ask (2 Saetze)
- Terminwunsch: 30 Minuten
- Lou zeigt technische Architektur + Live-Demo
- Alternative: Rohde testet selbst vorab mit dem Token

### Signatur
Aroob Alrawashdeh, AErtzin in Weiterbildung fuer Radiologie, Klinikum Dortmund

### Anlagen (4 Statt 3)
1. KI-Tools-Marktanalyse (PDF)
2. Carotis-AI Konzept (DOCX)
3. **NEU:** Rohde-Anleitung 2-Seiten-PDF (W-07)
4. **NEU:** 3-Minuten-Demo-Video (W-08, optional wenn noch nicht gerendert)

## Ton
- Professionell, nicht ueberheblich
- Selbstbewusst ("wir haben gebaut" statt "wir haetten gern")
- Kurz (Rohde hat keine Zeit fuer Romane)
- Kein "Weltweit erste" — sachlich

## Output
Speichere als `Stride V3/Anschreiben_Aroob_an_Rohde_v3.docx`

## Pre-Send-Checklist (Lou muss vor Versand pruefen)
- [ ] Token ist gueltig und funktioniert (`curl -H "X-Demo-Token: ..." https://api.carotis.diggai.de/api/v1/demo/whoami`)
- [ ] Demo-URL ist erreichbar (`curl -I https://carotis.diggai.de`)
- [ ] Anleitung ist als PDF exportiert
- [ ] Video ist als MP4 exportiert (falls vorhanden)
- [ ] Von Aroobs Klinikum-Mail gesendet
