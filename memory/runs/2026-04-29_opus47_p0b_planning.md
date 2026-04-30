---
name: p0b_planning
description: P0b — Tacit-Knowledge-Capture geplant. K-23..K-27 Kimi-Prompts geschrieben. Schema v0.2 mit free_text_notes. Risk Register H-011 hinzugefügt. Spec-Update in 05_DECISION_TREE_HARVESTING.md Sektion 3.1 + 4.
type: run
last_updated: 2026-04-29
---

# Session 2026-04-29 (afternoon) · Opus 4.7 (Cowork) · P0b Tacit-Knowledge-Capture Planning

## Goal

Lou's Request: UI-Erweiterung mit Freitext-Feld am Ende der Decision-Tree-Form. Arzt schreibt frei was er entschieden, nicht entschieden, oder offen gelassen hat. Diese Notizen sollen täglich aggregiert werden und Tag-für-Tag den strukturierten Entscheidungsbaum erweitern.

Aufgabe von Opus: Spec erweitern, Risk-Register erweitern (Freitext = neues PII-Risiko), 5 Kimi-Prompts (K-23..K-27) für die Implementierung schreiben.

## Done

**Spec-Erweiterungen:**
- `05_DECISION_TREE_HARVESTING.md` Sektion 3.1 (Schema v0.2 mit `free_text_notes`) + Sektion 4 (UI-Spec mit Textarea, Live-Validation, PII-Highlights)
- `regulatory/risk_register.md` H-011 (Freitext-PII-Leak, Score 15, RCM aktiv)

**5 Kimi-Prompts in `09b_KIMI_PROMPT_SEQUENCE.md` als APPENDIX P0b:**
- K-23: Schema v0.2 + Spec-Update + Validate-Test (BLOCKS K-24..K-27)
- K-24: Backend PII-Detection-Service (Spacy DE-NER + Regex) + `/check-text` Endpoint [PARALLEL zu K-25]
- K-25: Frontend FreeTextField-Component + DecisionTreeForm-Integration [PARALLEL zu K-24]
- K-26: Backend `decision_tree_service.capture()` PII-Check Pflicht [SEQUENTIAL nach K-24]
- K-27: Nightly Free-Text-Aggregator (BERTopic + Hermes-Fallback) + Hermes-Skill [SEPARATE]

**Neue Anti-Patterns dokumentiert (B-14, B-15, B-16):**
- B-14: PII-Check NUR backend-autoritativ; Frontend ist UX-Hint
- B-15: free_text_notes NIE in Logs; Audit-Events nur Span-Count + Labels
- B-16: Spacy DE-Modell (~500 MB) lazy-load mit `@lru_cache`, nicht im Container-Boot

**Tasks.jsonl:** K-22 als `done` markiert, K-23..K-27 als `pending` hinzugefügt.

## Surprised by

- Lou's Request für Freitext kam genau richtig — die Diskussion über strukturiertes vs. tacit knowledge in der Decision-Tree-Spec war seit Sektion 1 präsent ("Tacit Knowledge, der eigentliche Wert von 10 Jahren Facharztausbildung"). Aber wir hatten nur eine strukturierte UI. Die Freitext-Erweiterung füllt eine konkrete Lücke.
- Der Daily-Aggregator-Pattern (BERTopic-Cluster → Schema-Erweiterungs-Vorschläge → Lou approved wöchentlich) ist eigentlich eine Self-Improving-Loop für das Schema selbst. Das ist sehr cool: der Entscheidungsbaum wächst aus dem Korpus heraus, nicht von oben definiert.
- PII-Risiko bei Freitext ist nicht trivial — Spacy DE-Modell (~500 MB) muss lazy-loaded werden, sonst sprengt es das Backend-Image. Lou's Maschine kann das aber easy verkraften.

## Avoided

- Nicht gerushed das Feature ohne Risk-Assessment durchgepusht. H-011 mit Score 15 (Brutto) → 5 (nach RCM) ist substanziell — das musste erst dokumentiert werden, sonst rutscht uns ein PII-Leak später in die Studien-Daten.
- Nicht versucht das Schema selbst auf-the-fly zu mutieren (z.B. Aggregator schreibt automatisch neue Enums). Schema-Änderung bleibt Lou-Decision, mit wöchentlichem Approval-Loop.
- Nicht versucht eine LLM-basierte Free-Text-NER nur via Hermes/Ollama zu bauen. Spacy ist bewährt, schnell, deterministisch — LLM nur als Sanity-Check oder Cluster-Tool.
- Nicht in Patienteninformation/Einwilligungserklärung den Freitext-Hinweis ergänzt — das wird in einem separaten Edit gemacht (P1, sobald Ethik-Antrag final geprüft wird), weil Aroob das eh mit Anwalt abstimmen muss.

## Next

**Lou's nächste Schritte:**
1. K-23 in Kimi pasten (mit DELTA-UPDATE aus 09b APPENDIX P0b SETUP-DELTA als Erstes, falls Kimi-Session noch nicht das P0b-Wissen hat)
2. Wenn K-23 grün: K-24 + K-25 in 2 parallelen Tabs
3. K-26 nach K-24 fertig
4. K-27 separat (kann auch später)
5. End-to-End-Verifikation laut "End-of-K-27" am Ende des APPENDIX

**Wann ist P0 / P0a / P0b done?** Wenn:
- Code-Stack läuft mit Freitext-Capture + PII-Filter
- Bash `scripts/run_demo.sh` zeigt im Frontend die Textarea mit Live-PII-Check
- Triage-Report läuft (mind. 1× erfolgreich)
→ dann zurück zu **RUNBOOK_TODAY.md Schritt 8** (Aroob-Review der Office-Docs) und Schritt 9 (Mail an Rohde rausschicken). **Das ist der echte P0-Endpunkt.**

**P1 (Ethik + DSGVO + Datenvertrag) bleibt blocked** bis Rohde-Approval. Patienteninformation muss dann den Freitext-PII-Filter explizit erwähnen (Add-on für `ethics/patienteninformation.md`, gehört in P1-Sprint).

## Memory updates

- `05_DECISION_TREE_HARVESTING.md` Sektion 3.1 + 4 erweitert
- `regulatory/risk_register.md` H-011 hinzugefügt
- `09b_KIMI_PROMPT_SEQUENCE.md` APPENDIX P0b (K-23..K-27)
- `tasks.jsonl` K-22 done, K-23..K-27 pending
- `memory/runs/2026-04-29_opus47_p0b_planning.md` neu (diese Datei)

## Hinweise an die nächste Session

1. **Wenn Kimi K-23 nicht versteht:** Setup-Block (oben in 09b) komplett pasten + DELTA-UPDATE nochmal. Kimi vergisst Kontext zwischen Sessions, also Cold-Start braucht Re-Priming.
2. **Wenn Spacy DE-Modell zu groß für Lou's Setup:** B-16 erlaubt Regex-only-Fallback (PIIDetectionService funktioniert auch ohne Spacy, mit reduzierter Recall — primär PERSON-Erkennung schwächer). Für Demo-Zwecke akzeptabel; für Produktion in P5 muss Spacy laufen.
3. **Wenn Patient/Einwilligungserklärung-Update angefragt wird:** das gehört in P1, nicht P0b. Anwalt-Review erforderlich. Kein Kimi-Prompt — Opus + Anwalt-Konsultation.
4. **Wenn der Aggregator beim Wochen-Triage vorschlägt, einen neuen `deciding_feature`-Wert ins Schema aufzunehmen:** das ist ein **manueller** Schema-Update-Lauf — Opus schreibt einen K-Prompt für die Schema-Erweiterung, Kimi führt aus. Niemals automatisch.
5. **Replicabilität:** Das P0b-Pattern (Freitext + PII-Filter + Daily-Topic-Cluster + Schema-Wachstum) ist **wiederverwendbar für jedes andere Projekt** wo strukturiertes Capture an seine Grenzen stößt. Bei künftigen Projekten: kopiere `pii_detection_service.py`, `FreeTextField.tsx`, `aggregate_free_text.py` als Drop-in.
