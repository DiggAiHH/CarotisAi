# MEMORY.md — Index

> Index der Carotis-AI Langzeit-Memorys + projekt-eigener Artefakte. Eine Zeile pro Eintrag. Wenn du eine Memory-Datei oder ein wichtiges Spec-Dokument anlegst, **trage hier eine Pointer-Zeile ein**, sonst findet es kein Modell.

---

## Harness-Files (im Workspace-Root)

- [00_INDEX.md](00_INDEX.md) — Single-Page-Einstieg, immer als Erstes lesen
- [01_HARNESS.md](01_HARNESS.md) — Modell-Routing-Matrix, Pre-Flight, DoD, Memory-Hierarchie
- [02_ROADMAP.md](02_ROADMAP.md) — Phasen P0–P7 (24 Monate)
- [03_PROMPT_TEMPLATES.md](03_PROMPT_TEMPLATES.md) — 9 Copy-Paste-Prompts
- [04_MASTER_PLAN.md](04_MASTER_PLAN.md) — v1.0-Plan mit Architektur + Stakeholder + Risiken
- [05_DECISION_TREE_HARVESTING.md](05_DECISION_TREE_HARVESTING.md) — Spec der Innovation
- [06_ROHDE_MEETING_KIT.md](06_ROHDE_MEETING_KIT.md) — Termin-Vorbereitung
- [07_OFFICE_AGENT_PROMPTS.md](07_OFFICE_AGENT_PROMPTS.md) — 8 Stride-Prompts (A–H)
- [08_RESEARCH_ATTENTION_2020-2026.md](08_RESEARCH_ATTENTION_2020-2026.md) — 27+ Paper-Inventar
- [09_COPILOT_PROMPT_SEQUENCE.md](09_COPILOT_PROMPT_SEQUENCE.md) — 29 Copilot-Prompts (Sonnet 4.6 / Codex 5.3 / GPT-4.1)
- [09b_KIMI_PROMPT_SEQUENCE.md](09b_KIMI_PROMPT_SEQUENCE.md) — 16 Kimi-K2.6-Prompts (K-01..K-16) + APPENDIX K-17..K-22 (P0a — Demo-Robustheit nach E2E-Verifikation)
- [kimi_prompt_p0f_pivot_ready.md](kimi_prompt_p0f_pivot_ready.md) — **P0f-PROMPTS v1**: 12 Wellen (W-01..W-12) — superseded by v2 nach Codex-Architektur-Korrektur.
- [kimi_codex_prompt_p0f_unblock_ready.md](kimi_codex_prompt_p0f_unblock_ready.md) — **P0f-PROMPTS v2 (AKTIV)**: Deploy-Unblock-Wellen U-01..U-08 nach Fly+Hetzner-Architektur. Lou erst Manual-Steps, dann Codex/Kimi parallel.
- [REPO_CLEANUP_AND_DEPLOY_HANDOFF.md](REPO_CLEANUP_AND_DEPLOY_HANDOFF.md) — Codex-Handoff: Repo-Cleanup, Deploy-Architektur Fly+Hetzner, GH-Secrets-Status, Manual-Stop-Points.
- [ULTRAPLAN.md](ULTRAPLAN.md) — **Agent Pre-Flight Protocol v2 (2026-04-30)**: Workspace, Repo, Tool-Matrix, 40+ Skills-Inventar, Windows PowerShell Quirks, Modellrouting, Verbote, Stop-Regeln, Anomalien-Register. Verbindlich fuer alle Agenten.
- [outputs/Aroob_Status_Briefing_v1.md](outputs/Aroob_Status_Briefing_v1.md) — Status-Briefing fuer Aroob: Was wurde gebaut, was Rohde sieht, was Aroob tut, FAQ-Spickzettel.
- [CLAUDE.md](CLAUDE.md) — Working Memory v1.1
- [tasks.jsonl](tasks.jsonl) — atomare Tasks für Sonnet/Haiku
- [RUNBOOK_TODAY.md](RUNBOOK_TODAY.md) — Was Lou jetzt tut (Schritt-für-Schritt P0)
- [dashboard.html](dashboard.html) — Live-Status (im Browser öffnen)

## Stakeholder-Materialien

- [Mail_Aroob_an_Rohde_DRAFT.txt](Mail_Aroob_an_Rohde_DRAFT.txt) — Plaintext-Mail-Backup (kein Stride nötig)

## Run-Logs

- [memory/runs/2026-04-29_codex_trust_simplicity_framework.md](memory/runs/2026-04-29_codex_trust_simplicity_framework.md) — Trust-/Simplicity-Evaluationsframework für klinikerorientierte KI mit Prozent-Tracking und 7-Pass-Loop.
- [CV_Laith_Alshdaifat.md](CV_Laith_Alshdaifat.md) — Anlage 3 zur Mail (vor Versand zu PDF rendern)

## Schemas

- [schemas/decision_tree.schema.json](schemas/decision_tree.schema.json) — JSON Schema 2020-12 für Decision-Trees
- [schemas/decision_tree.sample.json](schemas/decision_tree.sample.json) — Synthetic-Sample für Tests/Doku

## Scripts (verifiziert: 78 passed — ML-Deps torch/mlflow in separater venv)

- [scripts/anonymize.py](scripts/anonymize.py) — DICOM PS 3.15 + k-Anonymity-Check (Skeleton + Tests)
- [scripts/test_anonymize.py](scripts/test_anonymize.py) — pytest-Tests (24 Tests)
- [scripts/validate_decision_tree.py](scripts/validate_decision_tree.py) — JSON-Schema-Validator
- [scripts/preflight.sh](scripts/preflight.sh) — Bash Pre-Flight-Check
- [scripts/preflight.ps1](scripts/preflight.ps1) — PowerShell Pre-Flight-Check
- [code/scripts/generate_demo_data.py](code/scripts/generate_demo_data.py) — 10 synthetische DICOMs + Decision-Trees
- [code/scripts/run_demo.sh](code/scripts/run_demo.sh) / [run_demo.ps1](code/scripts/run_demo.ps1) — 5-Min-Demo-Launcher
- [code/scripts/teardown_demo.sh](code/scripts/teardown_demo.sh) / [teardown_demo.ps1](code/scripts/teardown_demo.ps1) — Demo-Teardown
- [code/scripts/aggregate_free_text.py](code/scripts/aggregate_free_text.py) — Nightly Free-Text Aggregator (BERTopic/Hermes/Keyword)
- [scripts/README.md](scripts/README.md) — Skript-Dokumentation
- [code/mcp_servers/obsidian_mcp.py](code/mcp_servers/obsidian_mcp.py) — Vault CRUD + Backlinks + Search (FastMCP).
- [code/mcp_servers/graphify_mcp.py](code/mcp_servers/graphify_mcp.py) — Knowledge-Graph aus Wikilinks + Tags (FastMCP).
- [code/mcp_servers/hermes_mcp.py](code/mcp_servers/hermes_mcp.py) — Hermes :8200 Proxy + Self-Reflection + Ollama-Fallback (FastMCP).
- [code/mcp_servers/browser_mcp.py](code/mcp_servers/browser_mcp.py) — Playwright-Browser-Automation (FastMCP).
- [code/mcp_servers/combined_mcp.py](code/mcp_servers/combined_mcp.py) — All-in-one Server (RAM-sparend).
- [code/mcp_servers/run_loop.py](code/mcp_servers/run_loop.py) — Pre/Post-Hook + Auto-Start Hermes/Ollama.
- [code/mcp_servers/test_mcp_trio.py](code/mcp_servers/test_mcp_trio.py) — 12 Smoke-Tests + `--ignore-warn` CI-Flag.
- [deploy/MCP_SETUP.md](deploy/MCP_SETUP.md) — Setup-Guide fuer alle 4 MCPs + Browser-Harness.

## Regulatory

- [regulatory/risk_register.md](regulatory/risk_register.md) — ISO-14971-Stil Risk Register (11 Hazards inkl. H-011 Freitext-PII)
- [regulatory/adr/ADR_TEMPLATE.md](regulatory/adr/ADR_TEMPLATE.md) — Template für neue ADRs
- [regulatory/adr/ADR-0001-local-first.md](regulatory/adr/ADR-0001-local-first.md) — Local-First-Architektur (Accepted)
- [regulatory/adr/ADR-0002-decision-tree-harvesting.md](regulatory/adr/ADR-0002-decision-tree-harvesting.md) — Decision-Tree-Loss (Accepted)
- [regulatory/adr/ADR-0003-api-versioning-router-prefix.md](regulatory/adr/ADR-0003-api-versioning-router-prefix.md) — API-Versionierung via `/api/v1` (Accepted, P0a)
- [regulatory/adr/ADR-0004-lazy-db-engine-init.md](regulatory/adr/ADR-0004-lazy-db-engine-init.md) — Lazy DB-Engine Init für Test-Isolierung (Accepted, P0a)
- [regulatory/adr/ADR-0007-mcp-trio.md](regulatory/adr/ADR-0007-mcp-trio.md) — Obsidian + Graphify + Hermes MCP-Trio + Browser-Harness (Proposed, P0f)
- [regulatory/avv_local_first_template.md](regulatory/avv_local_first_template.md) — AVV-Skelett Klinikum ↔ Lou (P1-Ready)

## Ethik & Datenschutz (P1-ready)

- [ethics/README.md](ethics/README.md) — Reihenfolge + Wer-tut-was
- [ethics/ethikantrag_skelett.md](ethics/ethikantrag_skelett.md) — Antrag Ärztekammer Westfalen-Lippe
- [ethics/patienteninformation.md](ethics/patienteninformation.md) — für prospektive Teilnehmer
- [ethics/einwilligungserklaerung.md](ethics/einwilligungserklaerung.md) — Unterschriften-Vorlage
- [ethics/dpia_skelett.md](ethics/dpia_skelett.md) — Datenschutz-Folgenabschätzung (DSGVO Art. 35)

---

## User-Memorys

- [user_role.md](memory/domain/user_role.md) — Lou: Solo-Builder + Medizintechniker, baut für Schwägerin Aroob; Engineering-Harness-Stil; deutsch primär.

## Project-Memorys

- [project_carotis.md](memory/domain/project_carotis.md) — Carotis-AI Promotionsprojekt; Klinikum Dortmund; Prof. Rohde Ziel-Betreuer; 24-Monate-Plan.
- [project_status_p0.md](memory/domain/project_status_p0.md) — P0 läuft: Rohde-Meeting + Floy-Recherche + Office-Doc-Update.

## Reference-Memorys

- [refs_repos.md](memory/domain/refs_repos.md) — GitHub-Repos und Hosting-Pointer.
- [refs_papers.md](memory/domain/refs_papers.md) — Pointer auf 08_RESEARCH (Top-3 Must-Reads).
- [refs_regulatory.md](memory/domain/refs_regulatory.md) — EU AI Act, MDR, DSGVO, DIN EN 62304, ISO 14971, BSI.

## Feedback-Memorys

- [fb_office_docs.md](memory/domain/fb_office_docs.md) — Office-Dokumente werden NICHT von Modellen direkt editiert; Stride-Prompts statt Diff.
- [fb_local_first.md](memory/domain/fb_local_first.md) — Local-First ist nicht-verhandelbar; kein Cloud-API für Patientendaten.

## Run-Memorys (per Session)

- [runs/2026-04-27_opus47_harness_v1.md](memory/runs/2026-04-27_opus47_harness_v1.md) — Initial-Harness erstellt; Office-Prompts geschrieben; Paper-Recherche; Schemas; Anonymisierung; ADRs; Risk-Register; Ethik-Skelette; Dashboard.
- [runs/2026-04-28_opus47_copilot_stack.md](memory/runs/2026-04-28_opus47_copilot_stack.md) — Copilot-Prompt-Sequence (29 Prompts) + Hermes/Ollama-Integration + Jake-van-Clief-Alignment.
- [runs/2026-04-28_opus47_kimi_adaptation.md](memory/runs/2026-04-28_opus47_kimi_adaptation.md) — Kimi-K2.6-Adaptation (16 gebündelte Prompts) für Quota-Schonung.
- [runs/2026-04-29_kimi_e2e_verification.md](memory/runs/2026-04-29_kimi_e2e_verification.md) — K-01..K-16 abgeschlossen; 22/24 pytest grün; 13 Bugs gefixt; Schema-Lockerung B-12.
- [runs/2026-04-29_kimi_K-17.md](memory/runs/2026-04-29_kimi_K-17.md) — Router-Prefix `/api/v1` + pytest-asyncio config.
- [runs/2026-04-29_kimi_K-18.md](memory/runs/2026-04-29_kimi_K-18.md) — DB-Engine lazy init via `@lru_cache`.
- [runs/2026-04-29_kimi_K-19.md](memory/runs/2026-04-29_kimi_K-19.md) — Cornerstone3D WASM-Init + DICOM-Rendering.
- [runs/2026-04-29_kimi_K-20.md](memory/runs/2026-04-29_kimi_K-20.md) — 10 Synthetic DICOMs + Decision-Trees.
- [runs/2026-04-29_kimi_K-21.md](memory/runs/2026-04-29_kimi_K-21.md) — 5-Min-Demo-Walkthrough + run_demo.sh/ps1.
- [runs/2026-04-29_kimi_K-22.md](memory/runs/2026-04-29_kimi_K-22.md) — Dashboard-Update mit P0a-Status.
- [runs/2026-04-29_handoff_opus47_p0a_complete.md](memory/runs/2026-04-29_handoff_opus47_p0a_complete.md) — Handoff Opus 4.7: P0a komplett, Blocker T-010.

- [runs/2026-04-29_codex_init.md](memory/runs/2026-04-29_codex_init.md) - Codex-Init: Pre-Flight geladen, offene Tasks und bekannte Anomalien geprueft.
- [runs/2026-04-29_codex_ui_cds_research.md](memory/runs/2026-04-29_codex_ui_cds_research.md) - Externe Evidenz zu Low-Friction-UI, CDS-Usability, kognitiver Last und Structured Reporting fuer Carotis-AI.
- [runs/2026-04-29_codex_repo_audit.md](memory/runs/2026-04-29_codex_repo_audit.md) - Repo-Audit: verbleibende Luecken in UX, Robustheit, Tests, CI, Deployment, Security und Doku gegen den tatsaechlichen Ist-Stand abgeglichen.
- [runs/2026-04-29_Codex-NN_Alpha-Beta-Gamma.md](memory/runs/2026-04-29_Codex-NN_Alpha-Beta-Gamma.md) — Codex-NN Plan: ConfidenceCalibrationService + TrustScoreService + Frontend-Sync + HiResCAM-Doku. 78/78 Tests grün.
- [runs/2026-04-29_K-NN-final.md](memory/runs/2026-04-29_K-NN-final.md) — P0d Abschluss: ADR-006 + Trust-Score-UI + ONNX Calibration Export. 79/79 Tests grün.
- [runs/2026-04-30_hermes_browser_harness.md](memory/runs/2026-04-30_hermes_browser_harness.md) — Hermes + Browser Harness Integration. 78/78 Tests grün.
- [runs/2026-04-30_next_phase_closure.md](memory/runs/2026-04-30_next_phase_closure.md) — P0-Closure + P3-Prep: Stride-Prompts + Model-Signing + Frontend Trust-Panel. 88/88 Tests grün.
- [runs/2026-04-30_opus47_status_briefing.md](memory/runs/2026-04-30_opus47_status_briefing.md) — Opus 4.7 Status-Briefing: Token-optimierter Handoff mit Modell-Specs (200K/1M Kontext, Adaptive Thinking xhigh, Task Budgets), technischer Status, offene Entscheidungen.
- [runs/2026-04-30_t012_rohde_reply_kit.md](memory/runs/2026-04-30_t012_rohde_reply_kit.md) - T-012 Prep: Rohde Reply-Kit fuer Ja/Bedenkzeit/Nein/Rueckfragen; finaler Versand bleibt bis Rohdes Originalantwort blockiert.
- [runs/2026-04-30_opus47_research_briefing.md](memory/runs/2026-04-30_opus47_research_briefing.md) — Opus 4.7 Recherche + Status-Briefing + Memory-Update (dieser Log).
- [runs/2026-04-30_stride_prompt_g.md](memory/runs/2026-04-30_stride_prompt_g.md) — Stride Prompt G: Floy-Recherche v2 (Lou in Stride).
- [runs/2026-04-30_handoff_opus47_p0e.md](memory/runs/2026-04-30_handoff_opus47_p0e.md) — **HANDOFF Opus 4.7**: P0e DONE, 101/101 Tests grün, 6/6 Anomalien FIXED, T-017 done. Routing + next guidance für Opus.
- [runs/2026-04-30_codex_today_parallel_plan.md](memory/runs/2026-04-30_codex_today_parallel_plan.md) — Codex-Plan: heutige P0e/P1-Readiness-Implementierung mit maximaler konfliktfreier Subagenten-Parallelität + Kimi-2.6-Prompt.
- [runs/2026-04-30_kimi_K-35_to_K-42.md](memory/runs/2026-04-30_kimi_K-35_to_K-42.md) — K-35..K-42: Model-Update-Procedure, Reasoning-Alignment-Loss ADR, Audit-Service-Rewrite, Frontend-Contract-Cleanup, Vitest-Baseline, Security-Hardening, E2E-Verification-Scripts. 101/101 Tests grün.
- [runs/2026-04-30_kimi_K-43_to_K-46.md](memory/runs/2026-04-30_kimi_K-43_to_K-46.md) — K-43..K-46: Dead-Code-Removal (orphaned router, duplicate export_onnx, stale frontend components). Alle Tests grün, ruff 0, black 0.
- [runs/2026-04-30_opus47_p0f_pivot_plan.md](memory/runs/2026-04-30_opus47_p0f_pivot_plan.md) — **P0f-Pivot**: Production-Demo-Pivot Plan W-01..W-12 (Webseite + Demo-Deploy + Auth + Walkthrough + Rohde-Kit + Stride V3 + Mail v3). Strategie-Shift: Mail mit Live-Link statt Konzept.
- [runs/2026-04-30_codex_clean_repo_handoff.md](memory/runs/2026-04-30_codex_clean_repo_handoff.md) — **Codex Repo-Cleanup**: Token-Leak in Remote entfernt, sauberes `DiggAiHH/CarotisAi` master, Deploy-Files Fly+Hetzner, 6 GH-Secrets gesetzt, ULTRAPLAN als Pre-Flight-Protokoll geschrieben.
- [runs/2026-04-30_opus47_p0f_aligned.md](memory/runs/2026-04-30_opus47_p0f_aligned.md) — **P0f-Alignment**: Plan an Codex-Architektur (Fly+Hetzner) angeglichen. Aroob-Briefing erstellt. Next-Run-Prompt fuer Deploy-Unblock.
- [runs/2026-04-30_kimi_ULTRAPLAN-v2.md](memory/runs/2026-04-30_kimi_ULTRAPLAN-v2.md) — **ULTRAPLAN v2**: Erweitertes Agent Pre-Flight Protocol mit 40+ Skills, Windows Quirks, Agent Quickstart, Anomalien-Register A-01..A-10.
- [runs/2026-04-30_kimi_W-07_to_W-10.md](memory/runs/2026-04-30_kimi_W-07_to_W-10.md) — **W-07..W-10 DONE**: Rohde-Anleitung, Video-Skript, Mail v3 Prompt, Office-Docs v3 Master-Prompt. Deploy-Blocker weiterhin aktiv (FLY_TOKEN, SSH, DNS).
- [runs/2026-04-30_kimi_17-step-optimizations.md](memory/runs/2026-04-30_kimi_17-step-optimizations.md) — **17 Pre-Deploy Optimierungen DONE**: CI/CD, Frontend-Resilienz (ErrorBoundary, Timeout, Retry), Backend-Sicherheit (CORS, Security Headers, Config-Haertung, Metrics-Auth, Graceful Shutdown), DevOps (Resource Limits, Healthchecks, Gzip), Testing (E2E-Stresstest, Bundle Analysis, Pre-Deploy Checkliste).
- [runs/2026-04-30_opus47_mcp_trio_integration.md](memory/runs/2026-04-30_opus47_mcp_trio_integration.md) — **MCP-Trio Integration**: ADR-0007 + obsidian/graphify/hermes-mcp + run_loop.py + 11/11 Smoke-Tests gruen. Pro-Run Memory-Sync + Graph-Build + Hermes-Reflection + Browser-Harness verbunden.
- [runs/2026-05-01_opus47_p0f_plan_update.md](memory/runs/2026-05-01_opus47_p0f_plan_update.md) — **P0f-Plan-Update**: Codex GPT-5.5 Handoff Ack + Agent-Harness Verifikation. Kritischer Pfad jetzt extern (FLY_API_TOKEN/SSH/DNS/Fly-App), Code GREEN. 6 MCP-Module 1405 LOC, 11/11 Smoke-Tests.
- [runs/2026-05-01_Codex_GPT55-Run01_opus47_handoff.md](memory/runs/2026-05-01_Codex_GPT55-Run01_opus47_handoff.md) — **Codex Deploy-Audit**: Hetzner/Fly Workflow-Holes geprueft, `ANONYMIZATION_SALT` gesetzt, `OPUS47_HANDOFF_2026-05-01.md` geschrieben; externe Blocker bleiben FLY_API_TOKEN, SSH-Key, DNS.

## Stride-Prompts (P0 — aktuell in Ausführung)

| Prompt | Status | Ready-File |
|--------|--------|-----------|
| G | 🔄 In Progress | `stride_prompt_g_ready.md` |
| H | ⏳ Pending | `stride_prompt_h_ready.md` |
| C | ⏳ Pending | `stride_prompt_c_ready.md` |
| D | ⏳ Pending | `stride_prompt_d_ready.md` |
| E | ⏳ Pending | `stride_prompt_e_ready.md` |
| F | ⏳ Pending | `stride_prompt_f_ready.md` |
| B | ⏳ Pending | `stride_prompt_b_ready.md` |
| A | ⏳ Pending | `stride_prompt_a_ready.md` |

**Plan:** `stride_execution_plan.md`

## Decisions (Arzt-Entscheidungs-Trees)

- [decisions/README.md](memory/decisions/README.md) — Format + Konventionen. Ab P5 gefüllt.

## Anomalies (KI-Mensch-Diskrepanzen + Code-Bugs)

- [anomalies/README.md](memory/anomalies/README.md) — Format + Triage-Workflow. Ab P5 für klinische Anomalien gefüllt.
- [anomalies/2026-04-29_kimi_e2e_13_bugs.md](memory/anomalies/2026-04-29_kimi_e2e_13_bugs.md) — 13 gefixte Bugs aus K-01..K-16 E2E-Verifikation. **Pflicht-Lese vor Code-Generation in `code/`.**

---

**Wartung:** Halte diese Datei < 200 Zeilen. Wenn ein Eintrag obsolet ist (z.B. P0 abgeschlossen → P1 läuft) → Datei in `memory/archive/` verschieben + Zeile hier streichen.
