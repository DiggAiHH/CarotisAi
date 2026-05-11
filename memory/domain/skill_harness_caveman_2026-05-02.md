# Caveman Skill Harness Input - Carotis-AI

## Zweck

Operative Eingabe fuer den `caveman`-Skill im Carotis-AI Workspace. Ziel: kurze, dichte Agent-Kommunikation ohne Verlust technischer Substanz. Gilt fuer Status, Run-Logs, Handoffs, Deploy-Blocker, Error-Triage, DoD und Memory-Verdichtung. Keine Patientendaten, keine Secrets.

## Aufgaben

| # | Aufgabe | Status | Ergebnis / Artefakt |
|---|---|---|---|
| 1 | Agent-Status auf 3 Zeilen verdichten. | `executed-as-plan` | Artefakt: `Stand / Blocker / Next` fuer laufende Worker-Updates. |
| 2 | Run-Log-Kurzform erzeugen. | `executed-as-plan` | Artefakt: 5-Zeilen-Log mit `Goal`, `Done`, `Surprised by`, `Avoided`, `Next`. |
| 3 | Deploy-Blocker knapp melden. | `executed-as-plan` | Artefakt: `Blocker: <system>. Owner: <human/agent>. Next: <safe action>`. |
| 4 | Error-Triage komprimieren. | `executed-as-plan` | Artefakt: `Symptom / Cause / Fix / Verify`, keine Log-Rohdaten mit PII. |
| 5 | Task-DoD formulieren. | `executed-as-plan` | Artefakt: kurze DoD-Liste mit Files, Tests, Security-Check, Handoff. |
| 6 | Memory-Dichte erhoehen. | `executed-as-plan` | Artefakt: Memory-Notiz mit maximal 5 Bullets, nur stabile Fakten. |
| 7 | Handoff fuer Parallel-Worker schreiben. | `executed-as-plan` | Artefakt: `Touched / Not touched / Risk / Next owner`, verhindert fremde Reverts. |
| 8 | Test-Failure-Update schreiben. | `executed-as-plan` | Artefakt: `Failing test -> suspected area -> next command -> stop condition`. |
| 9 | Security-Hinweis entkomprimieren. | `executed-as-plan` | Artefakt: klare Vollsatz-Warnung fuer Secrets, Patientendaten, irreversible Aktionen. |
| 10 | User-Update im Arbeitsfluss kuerzen. | `executed-as-plan` | Artefakt: 1-2 Saetze, was gelesen/gelernt/als naechstes getan wird. |

## Preflight-Integration

- Caveman aktiv, wenn User `caveman`, `/caveman`, `be brief`, `less tokens` oder Token-Sparen verlangt.
- Caveman aktiv fuer Statusupdates, Run-Logs, Handoffs, Triage, DoD, Memory- und Harness-Dateien.
- Caveman nicht aktiv fuer Code, Commands, Commits, PR-Texte; diese bleiben normal und exakt.
- Caveman nicht aktiv, wenn Security-Warnung, irreversible Aktion, Patientendaten- oder Secret-Risiko erklaert wird.
- Caveman pausieren, wenn Kompression Reihenfolge, Verantwortung oder medizinisch/regulatorische Aussage verunklart.

## Anti-Patterns

- Keine entfernten Artikel, wenn dadurch ein Befehl oder eine Reihenfolge mehrdeutig wird.
- Keine Abkuerzung von Funktionsnamen, API-Pfaden, Fehlerstrings, Datei- oder Modellnamen.
- Keine Caveman-Ausgabe als Ersatz fuer Verifikation; Tests/Reads bleiben Pflicht.
- Keine Patientendaten, Tokenwerte, Roh-DICOM-Details oder private Kontakte in komprimierte Beispiele.
- Keine aggressive Kuerzung bei Legal-, MDR-, DSGVO-, Ethik- oder Clinical-Safety-Entscheidungen.

## Mini-Beispiel

Normal:

> Der aktuelle Deploy ist nicht durch Code blockiert, sondern durch ausstehende manuelle DNS- und SSH-Schritte; danach kann der Rohde-Demo-Link erneut verifiziert werden.

Caveman:

> Code nicht Blocker. DNS + SSH noch human. Danach Rohde-Demo-Link verify.
