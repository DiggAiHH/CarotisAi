---
name: capture-decision-tree
trigger_phrases: ["erfasse Arzt-Entscheidung", "save decision tree", "capture decision"]
required_tools: [filesystem, bash]
---
# Capture-Decision-Tree Skill

Action: Nimmt JSON-Input (das complete Decision-Tree-Schema),
validiert, schreibt in memory/decisions/, erzeugt Audit-Event.

Steps:
1. Parse JSON aus user input
2. Run: python ../scripts/validate_decision_tree.py <tmp.json>
3. Bei valid: write to ../memory/decisions/<datum>_<case_id_short>.json
4. Bei invalid: return Fehler-Liste, kein Write
5. POST /audit/event an localhost:8000 (Backend) mit event_type=
   decision_tree_captured, payload={case_id, audit_id}
