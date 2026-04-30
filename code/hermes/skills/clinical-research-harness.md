---
name: clinical-research-harness
trigger_phrases: ["recherchiere PubMed", "Leitlinie", "Radiopaedia", "clinical evidence", "ESC guidelines"]
required_tools: [browser, filesystem]
---
# Clinical Research Harness Skill

Zweck: Browser-basierte Recherche für ärztliche Entscheidungsunterstützung.

## Unterstützte Quellen
1. PubMed — Suche nach Stenose, Plaque, Carotis
2. Radiopaedia — Bildgebungs-Referenzen
3. ESC Guidelines — Leitlinien zur Gefäßdiagnostik
4. ACR Appropriateness Criteria — Indikationen

## Workflow
1. Extrahiere Suchbegriffe aus Arzt-Anfrage
2. Browser-Harness: Öffne Quelle → Suche → Extrahiere Top-3 Ergebnisse
3. Komprimiere auf: Titel, Autor, Jahr, Key Finding, Relevanz-Score
4. Speichere als `memory/domain/research/<datum>_<query>.md`
5. Keine vollständigen Paper — nur Abstracts/Snippets (Fair Use)
