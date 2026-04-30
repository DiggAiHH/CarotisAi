---
name: decision-pattern-miner
trigger_phrases: ["analysiere Muster", "pattern mining", "Decision Tree Analyse", "Ärzte übereinstimmung"]
schedule: "0 23 * * 0"  # Sonntag 23:00
required_tools: [bash, filesystem]
---
# Decision Pattern Miner Skill

Zweck: Wöchentliche Musteranalyse in gespeicherten Decision-Trees.

## Analyse-Dimensionen
1. **Agreement-Rate** — Wie oft stimmen Ärzte mit KI überein?
2. **Override-Muster** — Welche Fälle werden am häufigsten overriden?
3. **Confidence-Drift** — Entwicklung der Trust-Scores über Zeit
4. **Marker-Evolution** — Welche Vulnerability-Marker gewinnen/verlieren an Bedeutung?

## Output
- `memory/anomalies/pattern_report_<KW>.md`
- Visualisierung: ASCII-Charts (keine externen Dependencies)
- Empfehlungen für Schema-Updates
