# Carotis-AI — Status für Aroob

**Stand:** 30. April 2026 · **Verfasst von:** Lou · **Vertraulich**

> Liebe Aroob, dieses Dokument ist dein 5-Minuten-Update. Es erklärt **was wir gebaut haben**, **wie es Prof. Rohde demonstriert wird**, **was du tust** und liefert dir einen **FAQ-Spickzettel**, falls Prof. Rohde dich vor Mail-Versand anruft. Lass uns das gemeinsam durchgehen, bevor die Mail rausgeht.

---

## Zusammenfassung in 3 Sätzen

1. Das technische System (Backend + Frontend + KI-Modell + Erklärbarkeitsschicht + Audit-Trail) ist **fertig und automatisiert getestet** (107 Tests grün).
2. Wir haben **die Strategie geändert**: statt Prof. Rohde nur ein Konzept zu mailen, schicken wir ihm **einen persönlichen Zugang zu einer Live-Demo**, die er selbst ausprobieren kann.
3. **Drei letzte technische Schritte** sind noch offen (Fly.io-Token, Hetzner-SSH, DNS-Eintrag bei INWX), die Lou diese Woche erledigt — **dann geht die Mail raus**, frühestens Anfang nächster Woche.

---

## Was wir gebaut haben (in deinen Worten erklärbar)

### 1. Das KI-Modell
Eine neuronale Architektur namens **MFSD-UNet** (U-Net mit Swin-Transformer-Backbone), die in der Literatur (Xie 2024) für Carotis-Segmentierung Dice 0.91 erreicht. Sie segmentiert das Lumen, klassifiziert Plaque-Vulnerabilität (IPH, ThinCap, LRNC, Calcified) und schätzt den Stenosegrad nach NASCET. **Lokal lauffähig**, kein Cloud-Aufruf, kein Patientendaten-Export.

### 2. Erklärbarkeit (XAI)
**HiResCAM-Heatmaps** (höher aufgelöst als klassisches Grad-CAM) zeigen dir farblich, **wo das Modell hingeschaut hat**, als es den Stenosegrad berechnet hat. Wenn die Heatmap nicht auf der Stenose liegt, weißt du, dass das Ergebnis nicht vertrauenswürdig ist. Das ist genau der Punkt, an dem EU AI Act Art. 13 (Transparenz) und Art. 14 (Human Oversight) reinspielen.

### 3. Trust-Score
Eine zusätzliche Zahl pro Vorhersage: kombiniert Modell-Konfidenz, Kalibrierungsstatus und Erklärbarkeitsabdeckung zu einem 5-Segment-Indikator von "wenig vertrauen" bis "viel vertrauen". Konkret: wenn das Modell 65% Stenose mit Trust-Score 5 sagt, kannst du dem mehr glauben als 65% mit Trust-Score 2. Das ist neu in der Literatur und unser methodischer Beitrag.

### 4. Decision-Tree-Capture
Nach jedem AI-Vorschlag siehst du eine **30-Sekunden-Form**: Stenose-Slider, Plaque-Checkboxen, Trust-Stern, optional Freitext warum du anders entschieden hast. Diese anonymisierten Begründungen fließen ins **Daily-Learning** ein — das Modell lernt nicht nur aus den Bildern, sondern aus der Reasoning-Struktur deiner Befundungen. Das ist der **Wow-Moment für Prof. Rohde**.

### 5. Anonymisierung + Audit-Trail
Alle DICOM-Dateien werden **vor Verarbeitung** nach DICOM PS 3.15 (33 PII-Tags) anonymisiert. Jede Inferenz und jede Entscheidung landet in einem **append-only-Audit-Log** (kann nicht nachträglich gelöscht oder verändert werden). DSGVO-konform by Design.

### 6. Webseite + App (jetzt im Aufbau)
- **`carotis.diggai.de`** — öffentliche Webseite mit Konzept, Team und CTA "Demo testen"
- **`api.carotis.diggai.de`** — die App selbst, **per persönlichem Token gesichert**

---

## Was Prof. Rohde sehen wird

Wenn die Mail rausgeht, bekommt Prof. Rohde:

1. **Eine kurze Mail** (max 25 Zeilen, formell, Sie-Form) mit deinem Namen als Absenderin.
2. **4 Anlagen:**
   - KI-Tools-Marktanalyse v2 (seine Hausaufgabe — die Floy-Recherche)
   - Carotis-AI-Konzeptpapier v2
   - 2-Seiten-Demo-Anleitung (mit seinem persönlichen Token)
   - Dein CV (Lou's CV ist erwähnt)
3. **Zwei Links:**
   - Webseite (öffentlich)
   - Demo-App (mit seinem Token)
4. **Optional:** ein 3-Minuten-Walkthrough-Video, das Lou aufnimmt.

**Sein Erlebnis:**
- Klickt auf den Webseiten-Link → liest 2 Minuten
- Klickt auf "Demo testen" → kommt mit Token in die App
- Sieht eine **3-Minuten-Tour** (Walkthrough-Mode), die ihn durch DICOM-Viewer, AI-Panel, Decision-Form führt
- Kann selbst aus 30 synthetischen Fällen wählen
- Klickt eigene Befunde, sieht Heatmaps, gibt Decision-Tree ab
- Hat ein 500-Request-Limit über 30 Tage — mehr als genug zum Testen
- **Alles synthetisch, keine Patientendaten**

---

## Was du jetzt tust (3 Punkte)

### 1. Diese Markdown gemeinsam mit Lou durchgehen
20 Minuten. Wenn dir etwas unklar ist oder du etwas anders formuliert haben willst, sag es jetzt — bevor die Mail rausgeht.

### 2. Den Mail-Entwurf v3 absegnen
Lou erstellt einen Stride-Prompt für die Mail. Du bekommst die finale .docx-Version. **Du liest, du segnest ab, du klickst Senden.** Es ist deine Mail, von deinem Klinikum-Konto. Lou steht im CC.

### 3. Drei Termin-Optionen vorschlagen
Wir bieten Prof. Rohde **drei konkrete Slots** für ein 30-Min-Gespräch an. Such drei Optionen aus deinem Kalender raus, die nächste 2 Wochen abdecken (am liebsten Vor-Mittag, da ist er meistens entspannter).

---

## FAQ — Falls Prof. Rohde dich anruft, bevor die Mail rausgeht

### "Wer baut das eigentlich?"
*"Mein Schwager Laith Alshdaifat — er ist Medizintechniker an der HAW Hamburg, betreut von Prof. Margaritoff für Medical Embedded Systems. Er hat das System in den letzten Wochen aus eigener Initiative gebaut, nicht weil ich ihn beauftragt habe. Wir haben ein Repo, automatisierte Tests, eine Roadmap — alles dokumentiert."*

### "Was kostet das Klinikum?"
*"Null Euro. Finanzierung läuft über Familienmittel und HAW-Infrastruktur. Etwaige Drittmittel würden wir gemeinsam beantragen — das wäre Bonus, nicht Voraussetzung."*

### "Wie schützt ihr Patientendaten?"
*"Local-First-Architektur. Patientendaten verlassen das Klinikum nie. Alle DICOM werden nach DICOM PS 3.15 De-Identification anonymisiert, das Modell läuft auf Edge-Hardware vor Ort, der Audit-Trail ist append-only. Wir können den Datenfluss vor dem Termin gerne mit der Datenschutzbeauftragten des Klinikums abstimmen."*

### "Wie sicher seid ihr, dass das funktioniert?"
*"Das Bilderkennungs-Modell selbst ist State-of-the-Art (Xie 2024 zeigt Dice 0.91, Sensitivity 0.99). Der eigentliche Beitrag ist die **Decision-Tree-Harvesting-Methodik** — wir trainieren nicht nur auf Bildern, sondern auf den anonymisierten Begründungs-Strukturen. Das ist neu in der Literatur."*

### "Wann kann ich mir das ansehen?"
*"Nächste Woche schicke ich Ihnen eine Mail mit einem persönlichen Zugang. Sie können die Demo dann ohne Termin in zehn Minuten ausprobieren. Danach treffen wir uns 30 Minuten, um Ihre Einschätzung zu hören."*

### "Was wäre der wissenschaftliche Beitrag?"
*"Zwei Publikationen mit Ihnen als Senior-Author: ein klinisches Validierungs-Paper (Carotis-AI vs. Konsens-Ground-Truth, transnational DE/JO) und ein methodisches Paper (Decision-Tree-Harvesting als Trainings-Paradigma). Zieljournals: Radiology oder JNIS für Paper 1, Medical Image Analysis oder NEJM AI für Paper 2."*

### "Warum gerade ich als Doktorvater?"
*"Drei Gründe: (1) ich arbeite bei Ihnen — die Datenakquise und klinische Validierung sind nur in Ihrem Klinikum sinnvoll. (2) Sie haben mich als Persönlichkeit eingeschätzt — wir wollen die Beziehung nutzen, nicht eine neue aufbauen. (3) Ihr Profil in der Neuroradiologie macht das Paper für Reviewer glaubwürdiger."*

### "Was ist mit Haftung?"
*"Carotis-AI ist Clinical Decision Support, kein autonomer Diagnose-Roboter. Das System schlägt vor — Sie und ich entscheiden. Audit-Trail jeder Inferenz und jeder Bestätigung. Im Schadensfall ist die ärztliche Entscheidung dokumentiert und nachvollziehbar. Haftungsrechtlich identisch zur Standard-Befundung mit konventionellem CAD."*

### "Was passiert, wenn ich Nein sage?"
*"Dann respektiere ich das. Wir haben einen Plan B: Prof. Tolg an der HAW Hamburg als alternativer Erstgutachter, mit Ihnen als externer Berater wenn Sie wollen. Aber Sie sind unsere erste Wahl, weil das Projekt ohne Klinikum-Dortmund keinen klinischen Sinn macht."*

---

## Tonregeln für dich (wichtig!)

Wenn du mit Prof. Rohde sprichst — Telefon, Mail, Termin:

- **Du bist Ärztin in Weiterbildung**, nicht Fachärztin. Niemals umgekehrt.
- **Sie-Form** durchgehend.
- **Keine Werbe-Wörter:** kein "weltweit erste", "revolutionär", "bahnbrechend". Er ist Akademiker — das wirkt schmierig.
- **Konkrete Zahlen statt Adjektive.** "Dice 0.91" statt "sehr genau". "30 synthetische Fälle" statt "viele Beispiele".
- **Wenn er Bedenken äußert: schreiben, nicht sofort antworten.** Wir antworten schriftlich später, mit Material.
- **Kein Druck.** Wenn er Bedenkzeit will, gib sie ihm. Wir schicken dann ein höfliches Status-Update in 14 Tagen.

---

## Was Lou diese Woche noch macht

- Fly.io-Token rotieren + setzen
- Hetzner-SSH-Key auf den Server tragen
- DNS-Records bei INWX setzen (`api.carotis.diggai.de`, `carotis.diggai.de`)
- Webseite-Inhalt finalisieren und auf Fly deployen
- Walkthrough-Mode in der App final testen
- Persönlichen Token für Prof. Rohde generieren
- Mail v3 Stride-Prompt mit Lou's Zustimmung schreiben → Aroob → Aroob klickt Senden

**Realistische Mail-Versand-Woche:** 5.-9. Mai 2026.

---

## Drei Fragen an dich, Aroob

1. **Bist du mit der Strategie einverstanden, dass die Mail v3 explizit die Live-Demo-Links enthält?** (Alternative wäre: nur Konzept-Mail, Demo erst beim Termin live zeigen.)
2. **Welche drei Termin-Slots schlagen wir Prof. Rohde vor?** Bitte aus deinem Kalender 5.-23. Mai 2026.
3. **Soll Lou im Mail-CC stehen oder nur als "verfasst gemeinsam mit"-Hinweis erwähnt werden?**

---

*Bei Fragen zwischendurch: Lou, jederzeit. Ich erreiche dich auch übers Familien-WhatsApp.*

*— Lou*
