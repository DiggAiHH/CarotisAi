---
name: doctor-knowledge-capture
trigger_phrases: ["erfasse Begründung", "doctor reasoning", "capture knowledge", "warum dieser Befund"]
required_tools: [filesystem, http]
---
# Doctor Knowledge Capture Skill

Zweck: Erfasst ärztliche Begründungen in Echtzeit und bereichert sie mit kontextueller Information.

## Workflow
1. Arzt gibt Begründung ein (free_text oder structured)
2. Skill validiert gegen Decision-Tree-Schema
3. Skill reichert an mit:
   - Automatischer Stenose-Verdict-Ableitung (normal/mild/moderate/severe/critical)
   - Marker-Validierung (intraplaque_hemorrhage, thin_fibrous_cap, etc.)
4. Speichert in memory/decisions/ als JSON
5. Erzeugt Audit-Event via POST localhost:8000/audit/event

## Browser-Harness Integration
Wenn Arzt "recherchiere [Thema]" sagt:
- Skill ruft Browser-Harness auf (PubMed, Radiopaedia, ESC-Leitlinien)
- Fügt gefundene Evidenz als `supporting_literature` Feld hinzu
