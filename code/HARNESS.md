# code/HARNESS.md — Local AI Harness for Code Generation

> Defines how models are routed for engineering tasks **inside `code/`**.  
> For the project-wide harness see [`../01_HARNESS.md`](../01_HARNESS.md).

## Golden Rule

Three models collaborate inside this directory:

1. **Cloud-Claude** (Opus / Sonnet) — architecture, ADRs, heavy refactors
2. **Hermes via Ollama** — tool-use, memory, skill execution (local)
3. **Caveman via Ollama** — compression, boilerplate reduction (local)

GitHub Copilot (Sonnet 4.6 / Codex 5.3) is used for inline completion and small edits.

## Routing Matrix

| Task | Model | Endpoint / Tool |
|------|-------|-----------------|
| Architecture decisions, ADRs, stakeholder communication | Cloud-Claude Opus | anthropic API |
| Code review, heavy refactors | Cloud-Claude Sonnet | anthropic API |
| Code implementation, bug fixes | GitHub Copilot Sonnet 4.6 | Copilot Chat |
| Bulk generation, long files, boilerplate | **Kimi K2.6** | kimi-code CLI |
| Tool-use, memory retrieval, skill execution | Hermes Agent | `localhost:11434` |
| Compression, context reduction > 24k tokens | Caveman (qwen2.5-coder:7b) | `localhost:11434` |

## Hermes Setup

1. Install Ollama: <https://ollama.com>
2. Pull models:
   ```bash
   ollama pull nous-hermes-3-llama-3.1
   ollama pull qwen2.5-coder:7b
   ```
3. Install Hermes Agent:
   ```bash
   git clone https://github.com/NousResearch/hermes-agent.git
   cd hermes-agent && pip install -e .
   ```
4. Start Hermes (config in `code/hermes/config.toml`):
   ```bash
   hermes start --config code/hermes/config.toml
   ```

## Caveman Compression

When context exceeds 24k tokens, compress with Caveman before sending to Hermes:

```bash
hermes compress \
  --input ../CLAUDE.md \
  --output ../CLAUDE.compressed.md \
  --model qwen2.5-coder:7b \
  --target-tokens 1500
```

Use the compressed file as context for the next session.

## Workflow Inside Code Sessions (8 Steps)

1. **Pre-flight** — `scripts/preflight.sh`, `git status`, `pytest -q`
2. **Load context** — read `CLAUDE.md`, `MEMORY.md`, last 3 run-logs
3. **Select model** — use routing matrix above
4. **Generate / edit** — model produces code or docs
5. **Verify** — `pytest`, `npm run typecheck`, `docker compose build`
6. **Log** — write run-log to `memory/runs/`
7. **Update memory** — append lessons to `MEMORY.md`
8. **Commit** — `git commit` in English, imperative mood

## Reusability

The following items are **drop-in** for any other local-first OSS project:

- `code/HARNESS.md` (this file)
- `code/AGENTS.md`
- `code/hermes/` (config + skills)
- `code/scripts/install_local_stack.*`

Copy them, adjust the project name, and run.

## Sources

- Jake van Clief — *Interpretable Context Methodology / Model Workspace Protocol* (arXiv 2603.16021)
- Hermes Agent — <https://github.com/NousResearch/hermes-agent>
- Ollama — <https://ollama.com>

---

*Last updated: 2026-04-28*
