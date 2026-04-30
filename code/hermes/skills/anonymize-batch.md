---
name: anonymize-batch
trigger_phrases: ["anonymisiere DICOM", "anonymize batch", "DICOM batch anonym"]
required_tools: [bash]
---
# Anonymize-Batch Skill

Action: Ruft scripts/anonymize.py mit dem geforderten Pfad auf, parsed
das Manifest, gibt eine Zusammenfassung als Markdown.

Steps:
1. Parse user input: extract input_dir und output_dir
2. Run: bash -c "python ../scripts/anonymize.py --input <in>
   --output <out> --salt $ANONYMIZATION_SALT"
3. Read das output/<batch>.manifest.json
4. Return Markdown mit:
   - Anzahl files: ok / rejected_low_k / rejected_pii_leak
   - Liste der rejected mit Reason
   - SHA-256 des Manifest fuer Audit-Trail
