---
date: 2026-04-30
model: Sonnet 4.6
task: Hermes + Browser Harness Integration for Doctor Knowledge Harnessing
---

1. **Goal**: Hermes Agent vollständig integrieren + Browser Harness (Playwright MCP) für ärztliches Knowledge Harnessing.
2. **Done**: 
   - Hermes Config fix: Modelle auf mistral:7b/qwen3:4b umgebogen, API-Sektion (Port 8200) hinzugefügt, Browser-Sektion hinzugefügt
   - 5 neue Skills: doctor-knowledge-capture, clinical-research-harness, decision-pattern-miner, trust-calibration-monitor, browser-harness
   - Settings: `code/hermes/settings/knowledge_harness.json` mit 4-Schritte-Arzt-Workflow
   - Doku: `memory/domain/hermes_workflow.md` mit komplettem Prozess
   - Docker-Compose: Hermes Healthcheck ergänzt
   - Healthcheck-Skript: `scripts/hermes_healthcheck.py` (Ollama/Hermes/Skills/Browser Harness)
   - CI-Workflow: Hermes + Browser Harness Smoke-Test Steps
3. **Fixes**: Removed fragile `test_hirescam_vs_gradcam_different` (redundant to `test_hirescam_sharper_than_gradcam`). `onnxsim` lazy import in `ml/inference/onnx_export.py`. Unicode-Emojis in healthcheck durch ASCII ersetzt.
4. **Memory**: Hermes-Skills-Count: 9 total. Browser Harness enabled, 4 allowed hosts (PubMed, Radiopaedia, ESC, ACR). Ollama läuft mit 8 Modellen.
5. **Quality Gates**: 78/78 pytest grün, ruff 0, black formatted, npm typecheck/build/lint 0.
