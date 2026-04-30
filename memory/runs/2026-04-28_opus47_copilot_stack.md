---
name: copilot_stack_v1
description: Copilot-Prompt-Sequence + Hermes/Ollama-Integration + Jake-van-Clief-MWP-Alignment + Carotis-AI v1.1
type: run
last_updated: 2026-04-28
---

# Session 2026-04-28 · Opus 4.7 (Cowork) · Copilot-Stack + Local-AI-Harness

## Goal

Lou hat noch 2 Tage und 97 % seiner GitHub-Copilot-Quota (€10/Monat). Wunsch:
1. Copilot-Prompt-Sequence wie für Elbtronika: einer-nach-dem-anderen, parallel-markiert, modell-zugewiesen, copy-paste-fertig
2. `code/`-Subprojekt von Lou's Sonnet+Copilot-Pre-Work integrieren — nicht überschreiben
3. `.github/copilot-instructions.md` + `code/CLAUDE.md` + `code/HARNESS.md` + `code/AGENTS.md` als Onboarding für jeden Copilot-Run
4. Hermes Agent (Nous Research) + Ollama (`localhost:11434`) + caveman als Local-AI-Stack — wiederverwendbar für jedes OSS-Projekt
5. Theoretische Basis: Jake van Clief — Interpretable Context Methodology / Model Workspace Protocol (arXiv 2603.16021). Numbered Folders + Markdown + Scripts statt Framework.

## Done

- `09_COPILOT_PROMPT_SEQUENCE.md` — 29 Prompts (P-01 bis P-29) in 8 Stages (A bis H), mit Sequential-/Parallel-Markern, Modell-Empfehlungen, Verify-Schritten, Quota-Schätzung
- Stage A (P-01): copilot-instructions.md als Onboarding — blockt alle weiteren
- Stage B (P-02 bis P-05): code-spezifische Memory-Files (CLAUDE, HARNESS, AGENTS, MEMORY)
- Stage C (P-06 bis P-09): Infrastruktur (docker-compose, .env, install_local_stack scripts)
- Stage D (P-10 bis P-14): Backend (config, db, services, api, factory)
- Stage E (P-15 bis P-18): Frontend (DicomViewer, AIPanel, DecisionTreeForm)
- Stage F (P-19 bis P-23): ML-Pipeline (dataset, model, losses, train, export)
- Stage G (P-24 bis P-26): Tests + CI
- Stage H (P-27 bis P-29): Hermes-Integration + Demo
- `CLAUDE.md` auf v1.1 — Multi-Model-Routing, Jake-van-Clief-Referenz, Hermes/Ollama-Stack
- `MEMORY.md` Index aktualisiert mit Pointer auf 09_COPILOT_PROMPT_SEQUENCE.md

## Surprised by

- Lou's `code/`-Subprojekt war bereits substanziell vorgebaut (FastAPI factory pattern, Cornerstone v2, MONAI + timm, demo-onnx-Generator). Mein Plan musste sich INTEGRIEREN, nicht bauen — die Prompts referenzieren existierende Files (`scripts/demo.sh`, `tests/test_smoke.py`, `frontend/package.json`) statt sie zu duplizieren.
- Jake van Clief's Methodologie ist genau das, was ich intuitiv schon mit `00_INDEX` … `08_RESEARCH` gebaut habe. Numbered Folders, Markdown-Prompts, Scripts für Mechanik. Kein Framework-Lock-In. Die Validierung kam erst nach dem Bauen — aber die Konvergenz auf MWP/ICM bestätigt den Pattern.
- Hermes Agent (Nous Research) hat eingebaute Cross-Session-Memory + Auto-Skill-Creation + Compression. Das ist 80 % unseres handgebauten Memory-Systems — wir können in P5 evaluieren, ob wir migrieren oder Hermes als zweite Schicht (für Code-Tasks) parallel laufen lassen.

## Avoided

- Nicht versucht, das `code/`-Verzeichnis selbst zu editieren oder neue Code-Files dort zu schreiben. Lou's Wunsch: Tokens für PLANEN sparen, Copilot-Quota für CODE nutzen. Strikt eingehalten.
- Nicht versucht, Hermes Agent direkt zu installieren oder zu konfigurieren — nur Spec geschrieben (P-27/P-28/P-29). Implementation läuft via Copilot.
- Nicht alle 29 Prompts mit individueller Validierung versehen — nur Verify-Befehle pro Stage. Sonst wäre die Datei > 2000 Zeilen.
- Nicht versucht, fast/slow-AI-Routing in Code zu implementieren. Routing ist eine HUMAN-Decision in der Routing-Matrix von `code/HARNESS.md` (P-03), nicht ein Auto-Switch.

## Next

**Lou's nächste 2 Tage:**

1. **Tag 1 vormittags:** P-01 (Sonnet 4.6) → dann P-02 bis P-09 in 5–8 parallelen Tabs
2. **Tag 1 nachmittags:** P-10 bis P-23 in 3 Tabs (Backend + Frontend + ML — verschiedene Sub-Verzeichnisse, kein Merge-Konflikt)
3. **Tag 2 vormittags:** P-24 bis P-29 (Tests + CI + Hermes-Integration)
4. **Tag 2 nachmittags:** Smoke-Test mit `bash code/scripts/demo.sh` + `bash scripts/preflight.sh`
5. **Pro Prompt:** 5-Zeilen-Eintrag in `memory/runs/2026-04-28_copilot_P-XX.md`

**Nach dem Code-Stack:**
- Zurück zum Stakeholder-Pfad: `RUNBOOK_TODAY.md`
- Mail an Prof. Rohde rausschicken (T-010 in tasks.jsonl)

**Wenn Rohde antwortet (kann jederzeit kommen):**
- Template 9 (Stakeholder) aus 03_PROMPT_TEMPLATES.md — eine Cloud-Claude-Session ist die Investment wert (politisch sensibel)

## Memory updates

- `CLAUDE.md` → v1.1 (Multi-Model-Routing, Jake-van-Clief-Foundation, Hermes/Ollama-Stack)
- `MEMORY.md` → Pointer auf 09_COPILOT_PROMPT_SEQUENCE.md
- Diese Datei (run-log) neu

## Hinweise an die nächste Session

1. **Wenn Lou sagt "ich bin durch mit den Copilot-Prompts":** Pre-Flight + Smoke-Test (`bash code/scripts/demo.sh`) ausführen, dann zurück zu RUNBOOK_TODAY.md (T-010 Mail an Rohde) — der eigentliche P0-Endpunkt.
2. **Wenn Hermes oder Ollama Probleme machen:** `code/HARNESS.md` Sektion "Hermes Setup" + Hermes-Agent-Doku konsultieren. Bekannte Stolpersteine: Modell-Pull-Timeout (Hermes raised stream-timeout auf 30 Min), Port-Konflikt 11434.
3. **Wenn die Decision-Tree-Capture-UI im Test live ist (P-18):** synthetisch ein paar Trees in `memory/decisions/` schreiben + `python scripts/validate_decision_tree.py memory/decisions/` laufen lassen. Sonst weiß keiner ob die Pipeline end-to-end funktioniert.
4. **Replicabilität:** wenn ein anderes lokales OSS-Projekt aufgesetzt wird (Lou-Roadmap nach P5), kopiere `code/HARNESS.md`, `code/AGENTS.md`, `code/hermes/`, `code/scripts/install_local_stack.*` — das ist der Drop-in-Stack für jedes Hermes+Ollama-Projekt. Carotis-spezifisch sind nur `app/services/inference_service.py`, `ml/models/mfsd_unet.py` und `schemas/decision_tree.schema.json`.
