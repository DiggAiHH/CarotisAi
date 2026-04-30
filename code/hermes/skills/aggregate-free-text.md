---
name: aggregate-free-text
trigger_phrases: ["aggregiere Freitext-Notes", "wöchentliche Triage",
                  "topic-cluster decision-trees"]
schedule: "30 22 * * 0"  # Sonntag 22:30
required_tools: [bash, filesystem]
---

# Skill: Wöchentliche Free-Text Aggregation

## Zweck
Liest alle gespeicherten Decision-Trees der letzten 7 Tage, extrahiert die
`free_text_notes`, clustert sie nach Topics (BERTopic → Hermes/Ollama →
Keyword-Fallback) und schreibt einen Triage-Report nach
`memory/anomalies/triage_<KW>.md`.

## Ausführung

```bash
cd code
python scripts/aggregate_free_text.py --since-days 7
```

## Output
- `memory/anomalies/triage_2026-W17.md` (Beispiel)
- Enthält: Topic-Labels, Keywords, Cluster-Size
- Enthält KEINE einzelnen Note-Snippets (Compliance — B-15)

## Lou-Review
Wöchentlich (Montag morgen): Lou liest den Report, approved/rejected pro
Topic. Bei Approval: neuer `deciding_feature`-Wert wird ins Schema
aufgenommen (separater K-Prompt für Schema-Update).

## Fallback
Wenn BERTopic nicht installiert: Hermes/Ollama LLM-Cluster.
Wenn Ollama nicht erreichbar: Keyword-Fallback (einfache Häufigkeitsanalyse).
