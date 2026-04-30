---
name: 2026-04-29_codex_trust_simplicity_framework
type: run
---
## Goal
Ein messbares Framework für "Trust" und "Simplicity" in einer klinikerorientierten Carotis-AI entwerfen, inklusive Prozent-Tracking, 7-Pass-Loop und Evidenzmarkierung.

## Done
- Projekt-Pre-Flight durchgeführt: `CLAUDE.md`, Root-`MEMORY.md`, letzte Run-Logs und Anomalie-Datei gelesen.
- Ad-hoc-Research-Task `T-025` in `tasks.jsonl` angelegt und für diese Session verfolgt.
- Externe Evidenz aus NIST AI RMF, ISO 9241-11, FDA Human Factors Guidance, Brooke SUS, NASA TLX sowie aktuellen Studien zu Trust Calibration und XAI in der Medizin gesichtet.
- Kompaktes Metrikset mit operationalen Definitionen, Formeln und Composite-Indizes abgeleitet.
- 7-Pass-Verbesserungs- und Verifikationsloop für wiederholte Qualitätssteigerung formuliert.
- Reporting-Template für prozentuale Verbesserungen pro Pass vorbereitet.

## Surprised by
- Im bestehenden `tasks.jsonl` gab es keinen passenden Research-/Human-Factors-Task für Trust/Simplicity, obwohl das Thema für P0-Kommunikation und spätere klinische Adoption zentral ist.
- Die Quellenlage stützt stark "appropriate reliance" und Usability Engineering, aber weniger ein einheitliches Standard-Set speziell für klinische XAI-Produkte; der konkrete Metrikmix musste daher synthetisiert werden.

## Avoided
- Keine unbelegten Behauptungen zu regulatorischen Pflichtmetriken.
- Keine Vermischung von "viel Vertrauen" mit "gut kalibriertem Vertrauen".
- Keine Code-Änderungen im Produktstack.

## Next
- Framework in einen projektinternen Evaluationsplan oder eine ADR überführen.
- Für Carotis-AI konkrete Schwellenwerte pro Kernworkflow definieren, z. B. CTA laden, Läsion prüfen, Erklärung prüfen, Entscheidung dokumentieren.
- Später in P4/P5 mit echten Radiologie-Tasks, Holdout-Cases und mehreren Befundergruppen operationalisieren.

## Memory updates
- `T-025` ergänzt.
- Pointer in Root-`MEMORY.md` auf dieses Run-Log ergänzt.
