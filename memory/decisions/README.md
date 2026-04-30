# memory/decisions/ — Anonymisierte Arzt-Entscheidungs-Trees

> **Ab P5 aktiv.** Bis dahin leer.

Pro JSON-File: ein anonymisierter Decision-Tree nach dem Schema in `schemas/decision_tree.schema.json`. Validierung mit `scripts/validate_decision_tree.py`.

## Dateinamens-Konvention

`<YYYY-MM-DD>_<case_id_short_8chars>.json`

Beispiel: `2026-08-15_a3f4e8c9.json`

## Pflicht vor jedem Commit / Export

1. Validate gegen Schema: `python scripts/validate_decision_tree.py memory/decisions/`
2. Re-Identification-Check: case_id darf NICHT der echte study_uid sein
3. k-Anonymity ≥ 5 in jeder Datei

Diese Files sind Trainings-Daten — sie unterliegen dem `.gitignore`. Im Repo sichtbar ist NUR diese README.
