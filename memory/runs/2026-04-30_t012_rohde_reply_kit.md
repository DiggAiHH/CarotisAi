---
date: 2026-04-30
model: Codex
task: T-012 Prep - Rohde Reply Kit
type: stakeholder-prep
---

# T-012 Reply-Kit fuer Prof. Rohde

## Ziel
Wenn Prof. Rohde antwortet, soll Aroob innerhalb von 24 Stunden eine saubere, passende Antwort senden koennen. Dieses Kit ersetzt nicht die echte Antwort auf seine Originalmail. Es liefert Szenarien, Textbausteine und Checks, damit Template 9 aus `03_PROMPT_TEMPLATES.md` schnell und ohne Tonfehler genutzt werden kann.

## Grundregeln
- Absender ist Aroob aus dem Klinikum-Kontext, nicht Lou.
- Ton: ruhig, respektvoll, konkret, kein Bittsteller-Ton, keine Uebertreibungen.
- Bei Zusage sofort den naechsten Schritt operationalisieren: Termin, Ethikantrag, Datenvertrag, Materialliste.
- Bei Bedenkzeit Sichtbarkeit halten, aber keinen Druck erzeugen.
- Bei Nein offen danken, nach Empfehlung fragen, Plan B aktivieren.
- Keine Patientendaten, keine internen Klinikdetails, keine ungeprueften medizinischen Behauptungen in die Mail.

## Inputs fuer Template 9
```text
KONTEXT-FILES:
1. CLAUDE.md
2. 06_ROHDE_MEETING_KIT.md
3. memory/runs/2026-04-30_t012_rohde_reply_kit.md
4. Original-Mail von Prof. Rohde vollstaendig

EMPFANGER:
Prof. Dr. med. Stefan Rohde, Direktor der Klinik fuer Radiologie und Neuroradiologie, Klinikum Dortmund

ABSENDER:
Aroob Alrawashdeh, Aerztin in Weiterbildung fuer Radiologie, Klinikum Dortmund

GOAL:
Passende Antwort auf Rohdes Rueckmeldung formulieren, naechsten Schritt konkret machen, Ton fachlich ruhig halten.
```

## Szenario A - Rohde sagt Ja / grundsaetzliches Interesse
```text
Betreff: Re: Carotis-AI - naechste Schritte

Sehr geehrter Herr Prof. Rohde,

vielen Dank fuer Ihre positive Rueckmeldung. Ich freue mich sehr, dass Sie das Thema grundsaetzlich weiterverfolgen moechten.

Als naechsten Schritt wuerde ich gerne ein kurzes Abstimmungsgespraech mit Ihnen und Laith vorbereiten. Ziel waere, den klinischen Rahmen, die Rolle des Klinikums Dortmund und die ersten P1-Unterlagen sauber festzulegen: Ethikantrag, Datenvertrag/AVV, Datenschutz-Folgenabschaetzung und Hardware-/Betriebskonzept.

Wenn es fuer Sie passt, wuerden wir fuer das Gespraech 30 Minuten einplanen. Ich richte mich gerne nach Ihrer Verfuegbarkeit.

Mit freundlichen Gruessen
Aroob Alrawashdeh
Aerztin in Weiterbildung fuer Radiologie
Klinikum Dortmund
```

Direkt danach: `memory/runs/<datum>_rohde_reply.md` schreiben, T-013 vorbereiten, P1-Materialliste aus `ethics/` und `regulatory/` verdichten.

## Szenario B - Rohde sagt Ja, aber verlangt zuerst X
```text
Betreff: Re: Carotis-AI - gewuenschte Unterlagen

Sehr geehrter Herr Prof. Rohde,

vielen Dank fuer Ihre Rueckmeldung und die klare Einordnung. Wir bereiten die von Ihnen genannten Unterlagen gerne strukturiert vor.

Wenn ich Sie richtig verstanden habe, wuenschen Sie zunaechst:

1. <Punkt 1 aus seiner Mail>
2. <Punkt 2 aus seiner Mail>
3. <Punkt 3 aus seiner Mail>

Ich wuerde diese Punkte mit Laith ausarbeiten und Ihnen bis <Datum> als kompaktes Paket zukommen lassen. Danach koennen wir in einem kurzen Gespraech klaeren, ob der Rahmen fuer eine Promotionsarbeit am Klinikum Dortmund aus Ihrer Sicht tragfaehig ist.

Mit freundlichen Gruessen
Aroob Alrawashdeh
Aerztin in Weiterbildung fuer Radiologie
Klinikum Dortmund
```

Agenten-Arbeit nach Freigabe: Literaturpaket, Studienprotokoll, Datenschutzpaket oder Risk-File je nach Rohdes konkreter Forderung.

## Szenario C - Rohde braucht Bedenkzeit
```text
Betreff: Re: Carotis-AI

Sehr geehrter Herr Prof. Rohde,

vielen Dank fuer Ihre Rueckmeldung. Selbstverstaendlich kann ich gut nachvollziehen, dass Sie das Thema erst in Ruhe pruefen moechten.

Falls es fuer Sie in Ordnung ist, wuerde ich Ihnen in etwa zwei Wochen ein kurzes Status-Update schicken. Bis dahin bereiten wir die Unterlagen weiter so auf, dass der klinische Nutzen, der Datenschutzpfad und der realistische Promotionsumfang klar nachvollziehbar sind.

Mit freundlichen Gruessen
Aroob Alrawashdeh
Aerztin in Weiterbildung fuer Radiologie
Klinikum Dortmund
```

Direkt danach: Follow-up-Datum notieren, Eingang der Rohde-Mail + 14 Tage. Keine zweite lange Mail ohne neues Material.

## Szenario D - Rohde sagt Nein
```text
Betreff: Re: Carotis-AI

Sehr geehrter Herr Prof. Rohde,

vielen Dank fuer Ihre offene Rueckmeldung und dafuer, dass Sie sich die Zeit genommen haben, das Thema zu pruefen.

Ich bedaure Ihre Entscheidung, kann sie aber respektieren. Falls Sie eine Person oder einen Lehrstuhl empfehlen koennten, bei dem die Kombination aus Neuroradiologie, lokaler KI-Entwicklung und medizinischer Software besser aufgehoben waere, waere ich Ihnen sehr dankbar.

Unabhaengig davon danke ich Ihnen fuer die bisherigen Gespraeche und die konkrete Aufgabenstellung zur KI- und Floy-Recherche. Sie hat uns sehr geholfen, das Projekt fachlich zu schaerfen.

Mit freundlichen Gruessen
Aroob Alrawashdeh
Aerztin in Weiterbildung fuer Radiologie
Klinikum Dortmund
```

Direkt danach: Plan B vorbereiten: Tolg / van Stevendaal / Margaritoff. Kein Verteidigungsschreiben senden.

## Szenario E - Rohde fragt nach Aufwand/Kosten/Risiko
```text
Kosten fuer das Klinikum:
In P0-P5 entstehen dem Klinikum keine Produkt- oder Lizenzkosten. Die Entwicklung erfolgt ueber Lou/HAW/Familienmittel; das Klinikum stellt nur den klinischen Rahmen, die Betreuung und spaeter nach Ethikfreigabe die Datenzugangsstruktur.

Zeitaufwand fuer die Radiologie:
Der geplante Decision-Tree-Capture ist als 30-Sekunden-Mini-UI nach der Befundung konzipiert. Pflicht wird nur der minimale Kern: Stenosegrad, Agreement, Trust/Confidence. Freitext und Detail-Reasoning bleiben optional.

Datenschutz:
Die Architektur ist local-first. Patientendaten verlassen das Klinikum nicht. Verarbeitung, Audit-Trail und Inferenz laufen lokal; externe Modell- oder Cloud-Inferenz ist ausgeschlossen.

Haftung:
Carotis-AI ist als Clinical Decision Support geplant. Das System macht Vorschlaege; die aerztliche Entscheidung bleibt bei den Radiologen. Jede Inferenz und jede menschliche Entscheidung wird auditierbar dokumentiert.
```

## Szenario F - Rohde schlaegt Aachen oder externen Mentor vor
```text
Sehr geehrter Herr Prof. Rohde,

vielen Dank fuer den Hinweis. Wenn Sie den Weg ueber Aachen fachlich fuer sinnvoll halten, nehme ich diese Empfehlung sehr gerne ernst.

Mir waere wichtig, dass das Klinikum Dortmund weiterhin als klinischer Kern des Projekts erhalten bleibt, weil hier der konkrete radiologische Workflow, die Betreuung und spaeter die Validierung verankert sind. Wenn Sie eine Vorstellung haben, wie sich Aachen und das Klinikum Dortmund in diesem Rahmen sinnvoll ergaenzen koennten, wuerde ich das gerne in die weitere Planung aufnehmen.
```

## Antwort-Check vor Versand
- Stimmt die Anrede exakt?
- Ist Aroob als Aerztin in Weiterbildung benannt, nicht als Fachaerztin?
- Ist der naechste Schritt konkret?
- Sind Anlagen nur erwaehnt, wenn sie wirklich beigelegt werden?
- Keine "weltweit erste", "revolutionaer", "bahnbrechend".
- Keine Patientendaten oder interne Klinikdetails.
- Mail ist kurz genug: ideal 10-18 Zeilen.

## Status
T-012 ist vorbereitet, aber nicht erledigt. Erledigt ist T-012 erst, wenn Rohdes Originalantwort vorliegt, eine konkrete Reply daraus erstellt wurde und Aroob sie gesendet hat.

## Session Run-Log
## Goal
Stride ueberspringen und Punkt 2 aus dem naechsten Plan abschliessen: T-012 Reply-Vorbereitung fuer Rohdes Antwort.
## Done
Reply-Kit erstellt, Status-Briefing aktualisiert, Memory-Index verlinkt.
## Surprised by
T-012 kann nur vorbereitet werden; echte Erledigung haengt zwingend von Rohdes Originalantwort ab.
## Avoided
Keine direkte Office-Bearbeitung, kein Versand, keine Spekulation ueber Rohdes konkrete Antwort.
## Next
Wenn Rohdes Antwort vorliegt: Template 9 mit Originalmail nutzen. Bis dahin ist T-017 das naechste voll agentisch ausfuehrbare Arbeitspaket.
## Memory updates
`MEMORY.md` zeigt auf dieses Kit; `2026-04-30_opus47_status_briefing.md` enthaelt den Codex-Update-Block.
