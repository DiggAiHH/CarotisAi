# Stride Prompts — Ausführungsplan

## Ziel
Alle 8 Stride-Prompts (G, H, C, D, E, F, B, A) ausführen, um Office-Dokumente für Prof. Rohde / Klinikum Dortmund vorzubereiten.

## Reihenfolge (fix, nicht ändern)

| # | Prompt | Input-File | Output-File | Status |
|---|--------|-----------|-------------|--------|
| 1 | **G** | `Ki_Tools_Marktanalyse.docx` | `KI_Tools_Marktanalyse_v2.docx` | ✅ Ready |
| 2 | **H** | `Carotis_Ai_Konzept.docx` | `Carotis_AI_Konzept_v2.docx` | ✅ Ready |
| 3 | **C** | `Ki_Carotis_Expose.docx` | `Expose_Carotis_AI_Rohde_v2.docx` | ✅ Ready |
| 4 | **D** | `Ki_Carotis_Diagnostik.docx` | `Tech_Description_Klinikum_v2.docx` | ✅ Ready |
| 5 | **E** | `Value_Proposition_Ki_Carotis.docx` | `Value_Proposition_Klinikum_v2.docx` | ✅ Ready |
| 6 | **F** | `Carotis_Ai.pptx` | `Carotis_Ai_Rohde_v2.pptx` | ✅ Ready |
| 7 | **B** | `Anschreiben_Dr_Alrawashdeh_KI_Carotis_Diagnostik.docx` | `Anschreiben_Aroob_an_Rohde_v2.docx` | ✅ Ready |
| 8 | **A** | (neu) | `Mail_Aroob_an_Rohde_v2.docx` | ✅ Ready |

## Vorgehen pro Prompt

### Schritt 1: Vorbereitung (durch KI)
- `stride_prompt_<X>_ready.md` liegt bereit im Workspace-Root
- Globaler Kontext + Prompt-Text sind Copy-Paste-fertig

### Schritt 2: Ausführung (durch Lou in Stride)
1. Stride öffnen
2. Input-File hochladen (außer Prompt A — der ist neu)
3. Globaler Kontext einfügen → Enter
4. Auf Bestätigung warten
5. Prompt-Text einfügen → Enter
6. Output reviewen
7. Als `<name>_v2.docx` speichern (NICHT überschreiben)

### Schritt 3: Verification (durch Lou)
- Checkliste in `stride_prompt_<X>_ready.md` abhaken
- Diff-Liste prüfen
- Dateiname korrekt?

### Schritt 4: Memory-Disziplin (durch KI nach jedem Prompt)
- `memory/runs/2026-04-30_stride_prompt_<X>.md` schreiben (5 Zeilen)
- `tasks.jsonl` Status auf "done" setzen
- `MEMORY.md` aktualisieren falls nötig

## Gesamt-DoD

- [ ] G: `KI_Tools_Marktanalyse_v2.docx` existiert + Gap-Analyse-Kapitel
- [ ] H: `Carotis_AI_Konzept_v2.docx` existiert + DTH-Abschnitt
- [ ] C: `Expose_Carotis_AI_Rohde_v2.docx` existiert + Engineering-Harnessing-Block
- [ ] D: `Tech_Description_Klinikum_v2.docx` existiert + EH-Abschnitt
- [ ] E: `Value_Proposition_Klinikum_v2.docx` existiert + BMBF/HAW-Bullets
- [ ] F: `Carotis_Ai_Rohde_v2.pptx` existiert + 14 Folien
- [ ] B: `Anschreiben_Aroob_an_Rohde_v2.docx` existiert + Rohde-Setting
- [ ] A: `Mail_Aroob_an_Rohde_v2.docx` existiert + <30 Zeilen
- [ ] 8 Run-Logs in `memory/runs/`
- [ ] `tasks.jsonl` T-001..T-008 auf "done"

## Nächster Schritt nach allen 8 Prompts

**T-009:** Lou + Aroob gemeinsamer Review aller v2-Dokumente
**T-010:** Aroob schickt Mail an Prof. Rohde raus
