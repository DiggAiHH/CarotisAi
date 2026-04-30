---
name: fb_office_docs
description: Office-Dokumente (.docx, .pptx) werden NICHT von Modellen direkt editiert. Modelle erzeugen Stride-Prompts, Lou pastet sie in MS 365 Copilot. Grund: docx/pptx-XML-Diff ist menschlich nicht reviewbar, und ein falscher Edit kann ein 12-Folien-Deck zerlegen.
type: feedback
last_updated: 2026-04-27
---

# Office-Dokumente: Modelle generieren Prompts, nicht Diffs

**Regel:** Wenn die Aufgabe ist, eine `.docx`, `.pptx` oder `.xlsx` Datei zu ändern, schreibt das Modell **keinen Diff direkt in die Datei**. Stattdessen:

1. Modell schreibt einen **Stride-/Office-Agent-Prompt** in eine .md Datei (z.B. `07_OFFICE_AGENT_PROMPTS.md`)
2. Lou kopiert den Prompt in **Microsoft 365 Copilot / Stride**
3. Lou speichert den Output als `<originalname>_v2.<ext>` (NICHT überschreiben)
4. Aroob reviewt die Datei visuell, bevor sie versendet wird

## Why

Frühere Versuche (vor 2026-04), .docx/.pptx direkt mit `python-docx` / `python-pptx` zu editieren, haben:
- Layouts zerlegt (Spalten, Tabellen, eingebettete Bilder)
- Schriftarten verloren
- Folien-Reihenfolge durcheinander gebracht
- ein Powerpoint-Master-Slide überschrieben (alle 12 Folien sahen plötzlich identisch aus)

Stride hat das Format-Verständnis, das ein bash-/Python-Edit nie haben wird. Plus: Lou kann visuell prüfen, was Stride generiert hat, bevor es zu Aroob geht. Diese Visual-Review ist die letzte Verteidigungslinie gegen Halluzination in einem politisch-sensiblen Stakeholder-Dokument.

## How to apply

- **Trigger:** User-Frage enthält "Update das Word-Dokument", "Ändere die PowerPoint", "Pass das .docx an"
- **Reaktion:** Niemals direkten Edit. Immer Prompt schreiben + in `07_OFFICE_AGENT_PROMPTS.md` ablegen + Lou per Antwort sagen *„Der Prompt liegt in Sektion X. Kopier ihn in Stride und sag mir, wenn das Output erstellt ist."*
- **Ausnahme:** Wenn der User explizit sagt *„Edit die Datei direkt mit python-docx"* — dann tun, aber Disclaimer: *„Layout-Risiko. Backup machen."*

## Edge case

Markdown- und HTML-Dateien dürfen direkt editiert werden — die sind als Plain-Text reviewbar.
