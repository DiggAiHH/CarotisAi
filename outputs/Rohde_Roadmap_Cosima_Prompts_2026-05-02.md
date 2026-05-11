# Roadmap ab jetzt + Prompts fuer Cosima-Agent

Stand: 2026-05-02  
Ziel: Rohde-Kontakt sauber vorbereiten, danach P1 starten, ohne das Projekt kuenstlich auf zwei Jahre aufzublaehen.

## 1. Neuer Road Plan ab jetzt

### P0f - Versand- und Demo-Reife

Status: fast fertig.

Offen:

- Hauptdomain `carotis.diggai.de` reparieren: entweder Fly-Billing aktivieren oder INWX DNS auf Hetzner `204.168.230.127` drehen.
- Brief v4 final personalisieren.
- Praesentation v4 aus der neuen Struktur erzeugen.
- Demo-Link mit Screenshot/Smoke direkt vor Versand pruefen.
- Rolleninfo korrigieren: aktuell NVIDIA, Dortmund/Rohde historischer Bezug.

DoD:

- Rohde bekommt keinen losen Ideentext, sondern Brief + Demo + Kurzdeck + klaren naechsten Terminwunsch.

### P1 - Rohde-Gespraech und klinische Fragestellung

Zeitraum: 1-2 Wochen nach Rohde-Reaktion.

Ziele:

- Klinische Kernfrage festlegen.
- Endpunkte definieren: Stenosegrad, Plaque-Vulnerability, Workflow/Erklaerbarkeit.
- Datenbasis grob klaeren: retrospektiv, anonymisiert, CTA, Einschluss-/Ausschlusskriterien.
- Betreuungsmodell klaeren: Rohde als klinischer Betreuer/Senior-Advisor, HAW/technische Betreuung separat.

DoD:

- Eine 1-seitige Studienfrage + Scope-Abgrenzung.
- Entscheidung: "go", "go mit Anpassungen" oder "kein Klinikum-Dortmund-Pfad".

### P2 - Ethik, Datenschutz, Datenzugang

Zeitraum: 2-8 Wochen, je nach Klinikprozess.

Ziele:

- Ethikantrag vorbereiten.
- Datenschutz-Folgenabschaetzung und AVV/Datennutzungsvertrag.
- De-Identification-Prozess nach DICOM PS 3.15.
- Kein Cloud-Export von Patientendaten.

DoD:

- Freigegebener Datenpfad fuer anonymisierte retrospektive CTA-Daten.

### P3 - Retrospektive Validierung und Modellpfad

Zeitraum: 2-6 Monate nach Datenzugang.

Schlanker Promotionspfad:

- Fokus auf Machbarkeit, Reproduzierbarkeit, XAI und klinische Nutzbarkeit.
- Modell muss nicht produktreif sein.
- Ziel kann eine starke retrospektive Studie sein, nicht zwingend MDR-Produkt.

DoD:

- Validierungsdatensatz, Auswertung, Fehleranalyse, XAI-Beispiele.

### P4 - Manuskript / Dissertation

Zeitraum: parallel ab P3, nicht erst am Ende.

Moegliche Paper:

1. Klinisches Paper: CTA-Carotis-AI, Stenose/Plaque, Retrospektivvalidierung.
2. Methodisches Paper: Local-First XAI + Decision-Tree-Harvesting im neuroradiologischen Workflow.

DoD:

- Manuskriptentwurf + Dissertationsstruktur.

### P5 - Erweiterung nur wenn sinnvoll

Optionen:

- Jordanien/Sarah Hospital als zweite externe Validierung.
- Prospektive Mini-Workflow-Studie.
- MDR-/Produktpfad als Anschlussprojekt.

DoD:

- Nur starten, wenn P1-P4 robust sind.

## 2. Realistische Promotionsdauer

Nicht als "zwei Jahre Pflicht" darstellen.

Sinnvollere Aussage:

> "Der wissenschaftliche Kern kann schlank als retrospektive, anonymisierte Validierungs- und Machbarkeitsarbeit geplant werden. Je nach Datenzugang und Ethikprozess kann der Promotionskern deutlich kuerzer als zwei Jahre sein. Ein spaeterer Produkt- oder MDR-Pfad waere ein separates Anschlussprojekt."

Szenarien:

| Szenario | Dauer | Inhalt |
|---|---:|---|
| Minimal | 6-9 Monate | Retrospektive Machbarkeit + XAI-Fallserie + technischer Prototyp |
| Realistisch | 9-18 Monate | Retrospektive Validierung + Workflow-/Trust-Auswertung |
| Erweitert | 18-24 Monate | Multicenter/extern, prospektive Mini-Studie, Paper 2 |
| Produktpfad | >24 Monate | MDR, klinische Zulassung, Betrieb, Monitoring |

## 3. Prompt 1 fuer Cosima - Praesentation v4

```text
Du bist Cosima, Office-/Praesentations-Agentin. Erstelle aus dem folgenden Kontext eine professionelle PowerPoint-Praesentation fuer Prof. Dr. med. Stefan Rohde.

Ziel: 8-10 Folien, ruhig, klinisch, nicht werblich.

Wichtige Korrektur:
- Aroob/Apo wird NICHT als aktuell am Klinikum Dortmund angestellt dargestellt.
- Aktuelle Rolleninformation: arbeitet bei NVIDIA.
- Dortmund/Rohde-Bezug historisch formulieren: fruehere Taetigkeit im Umfeld des Klinikums Dortmund / Rohde, daraus klinische Fragestellung entstanden.

Kernbotschaft:
Carotis-AI ist ein local-first Promotionsprototyp fuer CTA-basierte Carotis-Stenose, Plaque-Vulnerability, XAI und Decision-Tree-Harvesting. Es ist keine fertige Medizinsoftware und nutzt in der Demo keine echten Patientendaten.

Folienstruktur:
1. Titel
2. Klinisches Problem
3. Warum bestehende KI-Loesungen nicht reichen
4. Carotis-AI Ansatz
5. Was bereits gebaut wurde
6. Live-Demo / Screenshot-Platzhalter
7. Wissenschaftliche Fragestellung
8. Schlanker Promotionsumfang: nicht zwingend zwei Jahre
9. Rolle von Prof. Rohde
10. Naechste Schritte / 30-Minuten-Gespraech

Ton:
Praezise, professorentauglich, keine Startup-Sprache, keine Uebertreibung.
```

## 4. Prompt 2 fuer Cosima - Rohde-Brief finalisieren

```text
Du bist Cosima, Schreibagentin fuer ein medizinisch-akademisches Anschreiben. Ueberarbeite den Brief an Prof. Dr. med. Stefan Rohde.

Ziel:
Eine kurze, serioese Mail mit maximal 250-350 Woertern.

Pflichtinhalte:
- Aroob/Apo arbeitet aktuell bei NVIDIA.
- Klinikum Dortmund/Rohde-Bezug ist historisch, nicht aktuelle Anstellung.
- Bitte um fachliche Einschaetzung, nicht sofortige Zusage.
- Demo-Link als technischer Prototyp: https://api.carotis.diggai.de/
- Keine echten Patientendaten in der Demo.
- Local-first Architektur, keine Cloud-Inferenz fuer Patientendaten.
- Promotion muss nicht zwingend zwei Jahre dauern; schlanker, fokussierter Scope moeglich.
- Bitte um 30-Minuten-Termin.

Nicht schreiben:
- Keine Behauptung "fertiges Medizinprodukt".
- Keine aktuelle Klinikum-Dortmund-Anstellung.
- Keine aggressive Verkaufsrhetorik.
```

## 5. Prompt 3 fuer Cosima - Massnahmenliste

```text
Erstelle eine einseitige Massnahmenliste fuer Lou vor Versand an Prof. Rohde.

Format:
Tabelle mit Prioritaet, Aufgabe, Owner, Status, naechster Schritt.

Aufgaben:
1. Rolleninfo korrigieren: NVIDIA aktuell, Dortmund historisch.
2. Demo-Link testen.
3. Hauptdomain reparieren oder Fallback-Link bewusst nutzen.
4. Brief finalisieren.
5. Praesentation finalisieren.
6. Drei Terminvorschlaege sammeln.
7. Nach Versand Follow-up in 7 Tagen setzen.

Ton:
Kurz, operativ, keine langen Erklaerungen.
```

## 6. Prompt 4 fuer Cosima - Roadmap als One-Pager

```text
Erstelle einen Roadmap-One-Pager fuer Prof. Rohde.

Die Roadmap darf nicht wie ein starres 2-Jahres-Projekt wirken. Stelle sie modular dar:

P0: Demo und fachliche Einschaetzung
P1: Fragestellung, Ethik, Datenschutz
P2: Retrospektive anonymisierte Datenbasis
P3: Modell-/XAI-Auswertung
P4: Manuskript/Dissertation
P5 optional: externe Validierung oder prospektive Erweiterung

Wichtige Aussage:
Der Promotionskern kann schlank sein und je nach Datenzugang deutlich kuerzer als zwei Jahre. Produktzulassung/MDR ist optionaler Anschluss, nicht Kernversprechen.
```

## 7. Prompt 5 fuer Cosima - Qualitaetscheck

```text
Pruefe die finalen Rohde-Unterlagen auf folgende Risiken:

1. Wird Aroob/Apo irgendwo faelschlich als aktuell am Klinikum Dortmund angestellt dargestellt?
2. Wird NVIDIA korrekt und nicht uebertrieben genannt?
3. Wird die Demo als synthetisch/anonymisiert und nicht als Patientendaten-System dargestellt?
4. Wird die Promotion zu gross oder zu lang verkauft?
5. Wird Prof. Rohde klar um fachliche Einschaetzung gebeten statt unter Druck gesetzt?
6. Ist die Sprache akademisch, ruhig und medizinisch serioes?

Gib eine Liste mit Fundstelle, Risiko, Korrekturvorschlag.
```

## 8. Direkter naechster Schritt

1. Lou prueft die Rolleninfo final.
2. Cosima erzeugt Praesentation v4 aus Prompt 1.
3. Brief v4 wird auf echte Signatur gekuerzt.
4. Demo-Link wird unmittelbar vor Versand noch einmal getestet.
5. Versand an Prof. Rohde mit Bitte um 30-Minuten-Termin.
