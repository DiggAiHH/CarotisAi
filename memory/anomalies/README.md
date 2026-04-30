# memory/anomalies/ — KI-Mensch-Diskrepanzen

> **Ab P5 aktiv.** Bis dahin leer.

Jeder Eintrag: ein Fall, in dem die AI-Vorhersage und die Arzt-Entscheidung sich substanziell unterscheiden. Plus wöchentliche Triage-Reports von Opus 4.7.

## Dateinamens-Konvention

- Einzelfälle: `<YYYY-MM-DD>_<case_id_short>_disagreement.json` (Schema wie `decision_tree.schema.json`, Filter `agreement_with_ai.verdict == "disagreement"`)
- Wochen-Triage: `<YYYY-MM-DD>_triage_week<N>.md` — Synthese aller Disagreements der Woche, mit Patterns + Folge-Tasks

## Wer schreibt hier?

- Edge-Server schreibt automatisch JSON-Disagreements (wenn `verdict == "disagreement"`)
- Opus 4.7 schreibt wöchentlich die Triage-Reports basierend auf den JSONs

## Wer liest hier?

- Pre-Flight-Check JEDES Modells (siehe `01_HARNESS.md`)
- Lou bei Roadmap-Updates (Template 7)
- Aroob bei der Bias-Analyse (P5)
- Reviewer der wissenschaftlichen Manuskripte (Anhang)

JSON-Disagreements unterliegen dem `.gitignore`. Triage-Reports (`.md`) dürfen committed werden — sie enthalten nur aggregierte, nicht-personen­bezogene Patterns.
