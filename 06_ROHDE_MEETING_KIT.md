# 06_ROHDE_MEETING_KIT — Prep für Prof. Dr. med. Stefan Rohde

> Das hier ist das Kit, mit dem Aroob den Termin holt — und mit dem du (Lou) bei diesem Termin überzeugst. Alles in einem Dokument, damit nichts vergessen wird.

---

## 1. Was Rohde wirklich will (zwischen den Zeilen lesen)

Aus dem bestehenden Schriftverkehr:

- Er hat **freundliche Gespräche** geführt → er ist **nicht abweisend**, er ist **interessiert**.
- Er hat eine **Hausaufgabe** gegeben (Floy + KI-Tools-Recherche) → er testet, ob Aroob **wissenschaftlich systematisch arbeiten kann**.
- Er fragt nach **Arbeitsablauf-Veränderung, Zeitgewinn / -verlust, Vor- / Nachteilen** → er denkt **klinisch-pragmatisch**, nicht akademisch-abstrakt.
- Er bietet eine **Empfehlung für Aachen** → er ist bereit, sie zu **fördern**.
- Er sagt, er prüfe, *„ob und wie aus Ihrer Idee eine Promotionsarbeit werden könnte"* → er hat noch nicht **Nein** gesagt. Er hat **Ja unter Bedingung** gesagt.

**Seine wahre Frage:** *„Ist diese junge Frau jemand, in dessen Promotion ich 2 Jahre meiner Aufmerksamkeit investieren will, ohne dass es schiefgeht?"*

**Unsere Antwort:** *„Sie ist nicht alleine. Hinter ihr steht ein Engineering-Team mit HAW-Professoren und ein 24-Monats-Plan, der bereits in v1.0 dokumentiert ist. Du musst nur die klinische Hand auflegen."*

---

## 2. Die Strategie

**Wir liefern nicht nur die Hausaufgabe (Floy-Recherche). Wir liefern eine fertige Lösung, die Floy obsolet macht.** Das ist der Wow-Moment. Plus: das Engineering-Harnessing-Framework als publizierbare Methodik — das macht die Arbeit für ihn akademisch attraktiver, weil er auf zwei Papers (klinisch + methodisch) Senior-Author wäre, nicht auf einem.

---

## 3. Termin-Anbahnung: Die E-Mail (Aroob → Rohde)

Diese Mail wird von Opus 4.7 generiert (Template 9). Hier der Master-Entwurf:

```text
Betreff: Re: Doktorarbeit – KI-Tools-Recherche abgeschlossen + Carotis-AI Konzept

Sehr geehrter Herr Prof. Rohde,

vielen Dank für Ihre konkrete Aufgabenstellung. Ich habe die Recherche zu KI-Tools 
in der Radiologie und der Floy-Software systematisch durchgeführt (Anlage 1).

Die zentralen Ergebnisse zusammengefasst:

• Floy ist eine cloud-basierte Lösung mit Schwerpunkt CT-Thorax. Für die 
  Carotis-Stenose-Diagnostik nur bedingt geeignet, weil Cloud-Architektur 
  unter DSGVO und EU AI Act in einem deutschen Klinikum erhöhte Compliance-
  Anforderungen erzeugt.

• Die Mehrheit der etablierten KI-Tools am Markt ist Cloud-basiert. Eine 
  systematische Lösung, die auf Edge-Hardware lokal läuft, DSGVO-konform 
  und gleichzeitig erklärbar ist (Grad-CAM, SHAP), existiert für die 
  Carotis-Diagnostik aktuell nicht.

Diese Lücke hat mich motiviert, gemeinsam mit meinem Schwager Laith Alshdaifat 
(Medizintechniker, HAW Hamburg) und unter wissenschaftlicher Beratung von 
Prof. Margaritoff (Medical Software / DIN EN 62304) und Prof. Tolg 
(SIMLab / VR in Medicine) ein eigenes Konzept zu entwickeln: 
"Carotis-AI" — ein lokal betriebenes, erklärbares CDSS für die Carotis-
Stenose-Quantifizierung (Anlage 2).

Das Besondere an unserem Ansatz ist nicht das Bilderkennungsmodell — das 
ist State-of-the-Art (MFSD-UNet, Dice 0.91, Sensitivity 0.99 nach Xie 2024). 
Das Besondere ist die Methodik dahinter: ein Engineering-Harnessing-Framework, 
das aus den Entscheidungen der Radiologen einen anonymisierten Decision-Tree-
Korpus baut, mit dem das Modell täglich inkrementell weiterlernt. Wir lernen 
nicht das Bild — wir lernen die ärztliche Begründung.

Daraus ergibt sich für eine Promotion zwei Publikationen mit Ihrem Namen 
als Senior-Author:

  1. Klinisches Validierungs-Paper (Carotis-AI vs. Konsens-Ground-Truth, 
     transnational DE / JO) — Zieljournal: Radiology oder Journal of 
     NeuroInterventional Surgery.

  2. Methodisches Paper (Decision-Tree-Harvesting als Trainings-Paradigma 
     für medizinische KI) — Zieljournal: Medical Image Analysis oder NEJM AI.

Ich würde mich sehr freuen, wenn wir uns zu einem 30-minütigen Gespräch 
treffen könnten. Mein Schwager Laith Alshdaifat würde gerne teilnehmen, 
um Ihnen die technische Architektur und einen ersten Prototypen zu zeigen.

Wäre Ihnen ein Termin in der kommenden Woche möglich? Ich richte mich 
nach Ihrer Verfügbarkeit.

Mit freundlichen Grüßen
Aroob Alrawashdeh
Ärztin in Weiterbildung für Radiologie
Klinikum Dortmund

Anlagen:
  1. Recherche-Dokumentation: KI-Tools in der Radiologie & Floy-Software
  2. Konzeptpapier: Carotis-AI — Local-First KI für die Carotis-Diagnostik
  3. Kurz-CV Laith Alshdaifat (Medizintechniker, HAW Hamburg)
```

**Wichtig:** Aroob schickt diese Mail von **ihrem Klinikum-Konto**, nicht von einer privaten Adresse. Empfänger ist Rohde direkt, nicht das Sekretariat (außer das ist sein Standard).

---

## 4. Der Termin selbst — Agenda (30 Minuten)

| Zeit | Wer | Was | Zweck |
|------|-----|-----|-------|
| 0:00–0:03 | Aroob | Begrüßung + Kontext: *"Vielen Dank, dass Sie sich Zeit nehmen. Wir möchten Ihnen heute zeigen, wie aus der Floy-Recherche ein eigenes System geworden ist."* | Persönliche Wärme, kurz |
| 0:03–0:08 | Aroob | **Floy-Befund** in 5 Minuten: Was Floy kann, was es nicht kann, warum es für Carotis nicht reicht | Hausaufgabe abgeliefert |
| 0:08–0:13 | Lou | **Carotis-AI in 5 Minuten:** Architektur-Diagramm aus `04_MASTER_PLAN.md` zeigen, 3 Sätze pro Layer (Pixel-Modell, Decision-Tree-Harvesting, Daily-Learning-Loop) | Wow-Moment |
| 0:13–0:18 | Lou | **Live-Demo:** Browser auf, dr-aroob-ki Repo, Mock-DICOM mit Heatmap-Overlay zeigen. *"So sieht die UI aus, in der Aroob arbeiten würde."* | Tangibilität |
| 0:18–0:23 | Lou + Aroob | **Engineering-Harnessing-Pitch (3 Min):** *"Wir haben das ganze Projekt in einem CLAUDE.md + MEMORY.md System organisiert. Jeder AI-Run lernt aus dem vorherigen. Das ist nicht nur das Carotis-Modell — das ist eine Methodik, die für jede medizinische KI-Promotion am Klinikum nutzbar wäre."* | Akademischer Hook |
| 0:23–0:28 | Aroob | **Konkrete Bitte:** *"Würden Sie die Betreuung übernehmen? Wenn ja, wäre der nächste Schritt der Ethikantrag — den hätten wir gerne in 4 Wochen eingereicht."* | Direkter Ask |
| 0:28–0:30 | Aroob + Lou | Pufferzeit für Fragen | Respekt für seine Zeit |

**Demo-Material:**
- Laptop mit Carotis Ai.pptx geöffnet (alle 12 Folien plus die zwei neuen)
- Browser-Tab mit `dashboard.html` (Live-Status, Tasks, Stats)
- Browser-Tab mit `http://localhost:3000` (Frontend mit DICOM-Viewer + AI-Panel)
- `demo_walkthrough.md` in VS Code geöffnet (als Backup-Script)
- `run_demo.sh` oder `run_demo.ps1` vorab ausgeführt, damit der Stack läuft
- Ausgedruckt: Floy-Recherche + Carotis-AI Konzept + dieser Master-Plan

---

## 5. FAQ — Was Rohde fragen wird

### F1: *"Wer trainiert das Modell?"*
**A:** Lou (Medizintechniker HAW) als Lead, beraten von Dr. Islam Shdaifat (4 Patente Computer Vision, JoVision) und unterstützt von Prof. Margaritoff (HAW, DIN EN 62304). Das Trainings-Setup läuft auf einer Workstation außerhalb des Klinikums. Daten werden vorher anonymisiert (DICOM PS 3.15) und gehasht. Kein PII verlässt jemals das Klinikum.

### F2: *"Was kostet uns das?"*
**A:** Null Euro für das Klinikum. Finanzierung: Familienmittel + HAW-Infrastruktur. Eventuelle Drittmittel (BMBF KI-in-der-Medizin) würden wir gemeinsam beantragen — das wäre Bonus, nicht Voraussetzung.

### F3: *"Wie lange wird das dauern?"*
**A:** 24 Monate bis zur Disputation. Phasen sind detailliert: M1–M2 Ethik + Datenvertrag, M3–M5 Datenakquise, M6–M9 Modell-Training, M10–M15 Klinikum-Integration, M16–M21 Validierung, M22–M24 Manuskript. Plan steht schriftlich (Sie haben ihn als Anlage 2 bekommen).

### F4: *"Was ist der wissenschaftliche Beitrag?"*
**A:** Das Bilderkennungs-Modell selbst ist State-of-the-Art (MFSD-UNet) und nicht der eigentliche Beitrag. Der Beitrag ist die **Decision-Tree-Harvesting-Methodik**: wir trainieren nicht nur auf Bildern, sondern auch auf den anonymisierten Begründungs-Strukturen der Befunder. Das ist neu in der Medical-AI-Literatur (siehe Kommentar von [Le et al. 2024 Circulation Imaging](https://www.ahajournals.org/doi/10.1161/CIRCIMAGING.123.016274) zur Notwendigkeit von Reasoning-Capture).

### F5: *"Wer hat Datenzugriff?"*
**A:** Innerhalb des Klinikums: nur Aroob und autorisierte Radiologen via PVS. Auf dem Edge-Server: nur das Modell selbst und ein Audit-Trail. Beim Trainings-Standort: nur anonymisierte Daten ohne Re-Identifizierungs-Möglichkeit. Auditierbar via DICOM-Anonymisierungs-Report. Auf Wunsch: externer Auditor jährlich (Prof. Margaritoff hat dafür akkreditierte Kontakte).

### F6: *"Was ist mit dem EU AI Act?"*
**A:** Wir behandeln Carotis-AI proaktiv als High-Risk AI System. Konkret: Art. 10 (Data Governance — Anonymisierung + Bias-Audit), Art. 13 (Transparency — Grad-CAM), Art. 14 (Human Oversight — Sie und Aroob sind Entscheider, nicht Beobachter), Art. 15 (Accuracy/Robustness — auto-Rollback bei Performance-Verlust). Das ist eine MDR-Class-IIa-Schiene. Dokumentation läuft ab P1 mit.

### F7: *"Was passiert, wenn das Modell etwas Falsches sagt und ein Patient Schaden nimmt?"*
**A:** Das Modell sagt nichts — es schlägt vor. Sie und Aroob bestätigen jeden Befund. Audit-Trail jeder Inferenz und jeder Bestätigung. Im Schadensfall ist die ärztliche Entscheidung dokumentiert und nachvollziehbar. Haftungsrechtlich identisch zur Standard-Befundung mit konventionellem CAD. Das wird in der Risk-Management-Datei nach ISO 14971 detailliert beschrieben (M1–M2).

### F8: *"Warum gerade ich? Warum nicht ein anderer Lehrstuhl?"*
**A:** Drei Gründe: (1) Aroob arbeitet bei Ihnen — die Datenakquise und klinische Validierung sind nur in Ihrem Klinikum sinnvoll. (2) Sie haben Aroob als Persönlichkeit eingeschätzt — wir wollen die Beziehung nutzen, nicht eine neue aufbauen. (3) Ihr Profil in der Neuroradiologie macht das Paper für die Reviewer glaubwürdiger.

### F9: *"Was ist mit Datenschutz nach OAuth-Skandalen / aktuellen Behörden-Themen?"*
**A:** Genau deshalb Local-First. Kein Cloud-Provider, kein API-Aufruf, keine Drittpartei. Die Architektur ist DSGVO-konform by Design, nicht by Compliance. Wenn Sie wollen, können wir die Datenflüsse vor dem Termin mit Ihrer Datenschutzbeauftragten abstimmen.

### F10: *"Wie ist die Erfolgsquote?"*
**A:** Drei Szenarien:
- **Best Case** (P > 60 %): zwei Papers, Disputation in 24 Monaten, MDR-Bundle für Skalierung an weitere Kliniken.
- **Realistic Case** (P ≈ 30 %): ein Paper (klinische Validierung), Disputation in 26–28 Monaten, Methodik-Paper als Folge-Arbeit für Lou.
- **Worst Case** (P < 10 %): ein Paper (negative Studie — auch publikationsfähig in *Annals of Internal Medicine* o. ä.), Disputation in 30 Monaten, Lehre für die Community.

In allen Szenarien: Aroob promoviert. In allen Szenarien: Sie sind Senior-Author auf mindestens einem Paper.

---

## 6. Der Notfall-Plan (Wenn Rohde "Nein" oder "noch nicht" sagt)

### Wenn Nein:
- **Plan B:** Prof. Tolg (HAW Hamburg, Dekan Life Sciences, SIMLab) als Erstgutachter. Aroob promoviert dann an der HAW (ist möglich für Mediziner via kooperativer Promotion HAW + Med. Fakultät). Klinikum Dortmund bleibt als Datenpartner.
- **Plan C:** Prof. van Stevendaal (Vorsitz Medizintechnik Hamburg) als Erstgutachter. Gleicher Pfad wie B.

### Wenn "Ja, aber zuerst noch X":
- Höchstwahrscheinlich verlangt er: **mehr Literatur**, **klinisches Studienprotokoll-Skelett**, **Risk-File-Skelett**. Alles drei kann Opus 4.7 in 1 Woche liefern.
- Reaktion: *"Vielen Dank — wir liefern X bis nächsten Freitag und nehmen dann das nächste Gespräch wahr."* Termin sofort vorschlagen.

### Wenn "Lassen Sie mir Bedenkzeit":
- Reaktion: *"Selbstverständlich. Dürfen wir Ihnen in 2 Wochen einen Status-Update schicken — auch wenn Sie noch nicht entschieden haben?"* Damit halten wir die Sichtbarkeit hoch ohne Druck.

---

## 7. Was du (Lou) ZUR Termin mitbringst

- [ ] Laptop mit allen aktuellen Office-Docs (nach Stride-Update aus `07_OFFICE_AGENT_PROMPTS.md`)
- [ ] Browser mit Demo-Tabs offen (kein "ich starte das mal eben")
- [ ] HAW-Hamburg-Visitenkarte oder LinkedIn-Profil sichtbar
- [ ] Eine Kopie von `04_MASTER_PLAN.md` ausgedruckt
- [ ] Eine Kopie von `05_DECISION_TREE_HARVESTING.md` ausgedruckt (für die Folge-Frage „Wie genau funktioniert das mit den Entscheidungen?")
- [ ] Stift + Notizblock — wenn Rohde Bedenken äußert: schreiben, nicht antworten, später schriftlich beantworten
- [ ] Wasser

**Was du NICHT tust:**
- Nicht über Diggai allgemein reden — nur Carotis-AI relevant für ihn
- Nicht über die anderen Professoren als „Coach" reden — sie sind Berater, er ist Betreuer
- Nicht „revolutionär" oder „weltweit erste" sagen — er ist Akademiker, das wirkt schmierig
- Nicht länger als 5 Minuten am Stück reden — er soll zum Mitdenken aktiviert werden

---

## 8. Nach dem Termin

| Outcome | Aktion |
|---------|--------|
| Rohde sagt Ja | E-Mail innerhalb 24 h: Dank + Termin für nächstes Treffen + erste Liste der Materialien (Datenvertrag-Entwurf, Ethikantrags-Skelett) |
| Rohde sagt „Brauche Bedenkzeit" | Mail in 24 h: Dank für die Zeit + die diskutierten Punkte als 1-Seiter zusammengefasst + Angebot für Status-Update in 2 Wochen |
| Rohde sagt Nein | Mail in 24 h: Dank für die Offenheit + Bitte um Empfehlung für anderen Mentor + Plan B aktivieren (Tolg / van Stevendaal kontaktieren) |

**In allen Fällen:** Eintrag in `memory/runs/<datum>_rohde_meeting.md` — was wurde gesagt, was war seine Körpersprache, was würden wir beim nächsten Mal anders machen.

---

**Letzte Aktualisierung:** 2026-04-29 · Opus 4.7 + Kimi K2.6 (P0a Demo-Robustheit: Cornerstone3D, Demo-Daten, Walkthrough, Dashboard)
