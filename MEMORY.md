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
- [ULTRAPLAN.md](ULTRAPLAN.md) — **Agent Pre-Flight Protocol v4 (2026-04-30)**: Workspace, Repo, Tool-Matrix, MCP-Server (5), 40+ Skills-Inventar, Windows PowerShell Quirks, Modellrouting, Verbote, Stop-Regeln, Anomalien-Register (A-01..A-18). Verbindlich fuer alle Agenten.
- [outputs/Aroob_Status_Briefing_v1.md](outputs/Aroob_Status_Briefing_v1.md) — Status-Briefing fuer Aroob: Was wurde gebaut, was Rohde sieht, was Aroob tut, FAQ-Spickzettel.
- [outputs/Rohde_Gesamtzusammenfassung_Massnahmen_2026-05-02.md](outputs/Rohde_Gesamtzusammenfassung_Massnahmen_2026-05-02.md) — Rohde-v4 Gesamtzusammenfassung, Massnahmen und Praesentationsstruktur mit NVIDIA-Rollenupdate und schlankem Promotionspfad.
- [outputs/Rohde_Anschreiben_v4_2026-05-02.md](outputs/Rohde_Anschreiben_v4_2026-05-02.md) — Neuer Rohde-Briefentwurf v4 mit Demo-Link, NVIDIA-Rolleninfo und Bitte um fachliche Einschaetzung.
- [outputs/Rohde_Roadmap_Cosima_Prompts_2026-05-02.md](outputs/Rohde_Roadmap_Cosima_Prompts_2026-05-02.md) — Roadmap ab P0f plus Cosima-Agent-Prompts fuer Praesentation, Brief, Massnahmen, Roadmap und QA.
- [outputs/Rohde_Testdaten_Demo_2026-05-02.md](outputs/Rohde_Testdaten_Demo_2026-05-02.md) — Online-Testdaten fuer Rohde/Nico: synthetische DICOM-Links, Testablauf, Sicherheitsnotiz, keine Patientendaten.
- [CLAUDE.md](CLAUDE.md) — Working Memory v1.1
- [tasks.jsonl](tasks.jsonl) — atomare Tasks für Sonnet/Haiku
- [RUNBOOK_TODAY.md](RUNBOOK_TODAY.md) — Was Lou jetzt tut (Schritt-für-Schritt P0)
- [dashboard.html](dashboard.html) — Live-Status (im Browser öffnen)

## Stakeholder-Materialien

- [Mail_Aroob_an_Rohde_DRAFT.txt](Mail_Aroob_an_Rohde_DRAFT.txt) — Plaintext-Mail-Backup (kein Stride nötig)

## Run-Logs

- [memory/runs/2026-05-12_codex_K-57_smoke_test.md](memory/runs/2026-05-12_codex_K-57_smoke_test.md) - Codex GPT-5.5: Docker Compose/CI full-stack smoke script, versioned health route, local 5/5 smoke green.
- [memory/runs/2026-05-11_codex_disclaimer_build.md](memory/runs/2026-05-11_codex_disclaimer_build.md) - Codex GPT-5.5: Disclaimer-Build Readiness, ResearchSplashGate + Watermark aktiv, CDS-Felder default aus public response entfernt, Splash-Confirmation auditierbar, Frontend/Backend verifiziert.
- [memory/runs/2026-04-29_codex_trust_simplicity_framework.md](memory/runs/2026-04-29_codex_trust_simplicity_framework.md) — Trust-/Simplicity-Evaluationsframework für klinikerorientierte KI mit Prozent-Tracking und 7-Pass-Loop.
- [memory/runs/2026-04-30_kimi_e2e-fix-final.md](memory/runs/2026-04-30_kimi_e2e-fix-final.md) — E2E Auth-Fix: ASGITransport, unique tokens, DecisionTreeRequest Schema, get_settings.cache_clear().
- [memory/runs/2026-04-30_Kimi_K26-Run02_ultraplan_harness_v3.md](memory/runs/2026-04-30_Kimi_K26-Run02_ultraplan_harness_v3.md) — ULTRAPLAN.md v3, AGENTS.md v2, Frontend-Tests 12 passed, CI-Hardening.
- [memory/runs/2026-04-30_Kimi_K26-Run03_solo_cleanup.md](memory/runs/2026-04-30_Kimi_K26-Run03_solo_cleanup.md) — Solo-Cleanup: ML-Duplikat entfernt, Frontend vereinheitlicht, pytest.ini fix.
- [memory/runs/2026-04-30_Kimi_K26-Run04_mcp_trio_b1_b5.md](memory/runs/2026-04-30_Kimi_K26-Run04_mcp_trio_b1_b5.md) — MCP-Trio B1-B5: Browser, Combined, Graphify Tags, Auto-Start, CI-Integration.
- [memory/runs/2026-04-30_Kimi_K26-Run05_ultraplan_v4_harness.md](memory/runs/2026-04-30_Kimi_K26-Run05_ultraplan_v4_harness.md) — ULTRAPLAN.md v4: MCP-Server Matrix, 8 neue Anti-Patterns, Anomalien A-13..A-18 FIXED.
- [memory/runs/2026-04-30_opus47_mcp_trio_integration.md](memory/runs/2026-04-30_opus47_mcp_trio_integration.md) — Opus 4.7: MCP-Trio Architektur, ADR-0007, Browser-Harness Skill.
- [memory/runs/2026-04-30_opus47_p0f_aligned.md](memory/runs/2026-04-30_opus47_p0f_aligned.md) — Opus 4.7: P0f Alignment, Deploy-Architektur Fly+Hetzner, Rohde-Meeting-Prep.
- [memory/runs/2026-05-01_opus47_p0f_plan_update.md](memory/runs/2026-05-01_opus47_p0f_plan_update.md) — Opus 4.7: P0f Plan Update, Codex-Handoff.
- [memory/runs/2026-05-01_Codex_GPT55-Run01_opus47_handoff.md](memory/runs/2026-05-01_Codex_GPT55-Run01_opus47_handoff.md) — Codex GPT-5.5: Opus47 Handoff, Repo-Cleanup.
- [memory/runs/2026-05-01_Codex_GPT55-Run02_mcp_conflict_cleanup.md](memory/runs/2026-05-01_Codex_GPT55-Run02_mcp_conflict_cleanup.md) — Codex GPT-5.5: MCP Conflict Cleanup.
- [memory/runs/2026-05-01_Codex_GPT55-Run03_ci_online_readiness.md](memory/runs/2026-05-01_Codex_GPT55-Run03_ci_online_readiness.md) — Codex GPT-5.5: PR #4 CI-Readiness gemerged; master CI gruen; Docker/Hetzner Demo-Deploy gehaertet; Live-Deploy blockiert nur noch an Hetzner-SSH, DNS und fehlendem `FLY_API_TOKEN`.
- [memory/runs/2026-05-01_Copilot_GPT53Codex-Run03_claude_design_prototype.md](memory/runs/2026-05-01_Copilot_GPT53Codex-Run03_claude_design_prototype.md) — GitHub Copilot Sonnet 4.6: Claude.ai/design Prototype-Session — vollstaendiges 3-Spalten Carotis AI Medical UI (DICOM Viewer + Grad-CAM + AI Panel + SHAP + Physician Override) gerendert. Verifier-Agent Auto-Fix. Alle 3 Tabs (Patients/Viewer/AI) verifiziert. ULTRAPLAN.md §4.12 Claude Design Browser Harness hinzugefuegt.
- **2026-05-02** — [SSH Fix + E2E + Demo Token](memory/runs/2026-05-02_Copilot_Sonnet46-Run01_ssh_fix_e2e_demo.md) — Agent: Copilot/Sonnet46 — Status: ✅ Done (Frontend ❌ Fly.io Trial abgelaufen)
- [ULTRAPLAN.md](ULTRAPLAN.md) — **Agent Pre-Flight Protocol v5 (2026-05-01)**: §4.12 Claude Design Browser Harness (claude.ai/design) hinzugefuegt — URL-Pattern, Chat Composer, Tweaks-Panel, iframe-Struktur, Generation-Complete-Signale, Verifier-Agent, Wait-Strategie, Anti-Patterns.
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

- [memory/domain/zweckbestimmung_master_2026-05-06.md](memory/domain/zweckbestimmung_master_2026-05-06.md) — **KANONISCHE ZWECKBESTIMMUNG v1.0**: Forschungsprototyp-Frame statt MDR Class IIa. Master-Block A–G für alle Stride/README/Splash/Ethik/Mail-Stellen + Modul-Dekomposition A–E + Anwendungs-Checklist. Pivot-Begründung: Class IIa nicht durchführbar als Solo-Dev, Forschungs-Frame nutzt MDR Art. 1(2) + § 11 MPDG.
- [outputs/dissertation_hypotheses_v1_2026-05-06.md](outputs/dissertation_hypotheses_v1_2026-05-06.md) — **7 Dissertations-Hypothesen v1**: H1..H7 voll spezifiziert (Methode, Daten, Statistik, Aroob/Lou-h, T2P, Target-Journal, MDR-Frame). Pflicht-Stack H3+H1+H5 für kumulative Promotion + H6 als Quick-Win + H7 als Drittmittel-Hebel. Reserve H8..H10 skizziert. 36-Monats-Plan + Notion-Import-Instructions.
- [outputs/dissertation_hypotheses_v1_2026-05-06.html](outputs/dissertation_hypotheses_v1_2026-05-06.html) — Interaktiver Single-File-HTML-Artefakt mit Cards, Sort/Filter, 36-Monats-Timeline. Lokal im Browser öffnen.
- [outputs/dissertation_hypotheses_v1_2026-05-06.csv](outputs/dissertation_hypotheses_v1_2026-05-06.csv) — Notion-Import-CSV (7 Zeilen, 13 Properties) für Database-Setup.
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

- [skill_team_harness_2026-05-02.md](memory/domain/skill_team_harness_2026-05-02.md) - Skill-Team Harness: 5 neue Codex-Skills, 50 operative Aufgaben, Preflight-/Stop-Regeln.
- [skill_team_harness_compact_2026-05-02.md](memory/domain/skill_team_harness_compact_2026-05-02.md) - Kompaktfassung fuer Preflight bei Skill-/Connector-Arbeit.

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
- [runs/2026-05-01_Kimi_K26-Run06_deep_audit_ml_optimization.md](memory/runs/2026-05-01_Kimi_K26-Run06_deep_audit_ml_optimization.md) — **Deep Audit + ML Optimization**: 105/105 Tests gruen. Timing-Attack-Fix, ONNX-Export-Bugfix, AMP+Warmup+Gradient-Clip, Frontend Signal+Retry+State-Sync Fixes, Lazy Schema Loading, 59 Frontend-Issues dokumentiert.
- [runs/2026-05-01_kimi_post_audit_test_fixes.md](memory/runs/2026-05-01_kimi_post_audit_test_fixes.md) — **Post-Audit Test-Fix Sprint**: 8 Backend + 17 Frontend Failures behoben. Baseline: 120 passed / 29 passed / 0 TS errors / Build green.
- [runs/2026-05-01_handoff_opus47_post_audit_fixes.md](memory/runs/2026-05-01_handoff_opus47_post_audit_fixes.md) — **Opus 4.7 Handoff**: Vollstaendige Failure/Fix-Matrix, Accessibility-Verbesserungen, aktualisierte Test-Baselines.
- [runs/2026-05-01_Codex_GPT55-Run04_post_audit_ml_harness.md](memory/runs/2026-05-01_Codex_GPT55-Run04_post_audit_ml_harness.md) — **Codex Post-Audit ML/Harness**: Dynamic INT8 opt-in, default-off W/L-TTA Hook, `sympy` ML-Requirement, Harness Lessons in MCP_SETUP, Backend 123 passed/11 skipped.
- [runs/2026-05-01_Codex_GPT55-Run05_memory_task_cleanup.md](memory/runs/2026-05-01_Codex_GPT55-Run05_memory_task_cleanup.md) — **Memory/Task Cleanup**: stale Stride-Pending-Status korrigiert, W-11 Runbook erstellt, Rohde-E2E 7/7 gruen, offene Tasks auf echte Blocker reduziert.
- [runs/2026-05-01_Codex_GPT55-Run06_browser_design_prompt.md](memory/runs/2026-05-01_Codex_GPT55-Run06_browser_design_prompt.md) — **Browser-Smoke + Claude Design Prompt**: Frontend-Blank-Screen durch lazy Cornerstone-Imports + CJS-Shims behoben; Lint/Typecheck/Build/Vitest gruen; Chromium-Smoke mit synthetischem Demo-Token; Claude-Design-Prompt vorbereitet.
- [runs/2026-05-01_Copilot_GPT53Codex-Run01_ultraplan_preflight_protocol.md](memory/runs/2026-05-01_Copilot_GPT53Codex-Run01_ultraplan_preflight_protocol.md) — **ULTRAPLAN v5 Protocol Hardening**: Tool-Call-Reihenfolge, Connector/Skill-Aktivierungsstrategie, Prompt-by-Prompt 5-Zeilen-Run-Log Pflicht verbindlich gemacht.
- [runs/2026-05-01_Copilot_GPT53Codex-Run02_chromium_test_and_preflight.md](memory/runs/2026-05-01_Copilot_GPT53Codex-Run02_chromium_test_and_preflight.md) — **Chromium Playwright + copilot-instructions**: copilot-instructions.md ULTRAPLAN-Patch bestätigt; Chromium visual smoke test 1 passed (18.5s) + screenshot; AuthGate benötigt Backend → Auth-bypass via VITE_SKIP_AUTH für E2E (P1-Readiness).
- [runs/2026-05-01_Kimi_K26-Run01_ultraplan_v6_harness.md](memory/runs/2026-05-01_Kimi_K26-Run01_ultraplan_v6_harness.md) — **Kimi K2.6 ULTRAPLAN v6 + Design Bridge**: ULTRAPLAN.md v6 (Claude Design Harness §4.12, Playwright E2E §4.13, Anomalien A-19..A-21), copilot-instructions.md aktualisiert, `demo_walkthrough_visual.spec.ts` mit 11 Screenshots, Claude Design reconnect + Screenshot. Status: Prototyp aktiv (M. Müller + Grad-CAM).
- [runs/2026-05-01_Kimi_K26-Run02_deploy_unblock_browser.md](memory/runs/2026-05-01_Kimi_K26-Run02_deploy_unblock_browser.md) — **Kimi K2.6 Deploy-Unblock via Browser**: FLY_API_TOKEN erstellt + GitHub Secret gesetzt, Hetzner Web-Konsole SSH-Key eingegeben, INWX DNS geprueft (api.diggai.de korrekt, carotis + api.carotis fehlen). ULTRAPLAN.md Stop-Regeln aktualisiert. Anomalien A-22, A-23.
- [runs/2026-05-01_Codex_GPT55-Run07_aroob_agent_summary.md](memory/runs/2026-05-01_Codex_GPT55-Run07_aroob_agent_summary.md) — **Aroob Agenten-Briefing**: `outputs/Aroob_Run_Agenten_Briefing_v1.md` erstellt mit Run-/Agenten-Zusammenfassung, Mermaid/GraphGen-Graph, menschlicher Stunden-Schaetzung und visueller Statusdarstellung.
- [runs/2026-05-02_Codex_GPT55-Run08_skill_sources.md](memory/runs/2026-05-02_Codex_GPT55-Run08_skill_sources.md) — **Skill-Installation**: browser-harness, caveman, compress, obsidian und remotion-best-practices nach `.codex/skills` installiert; nicht installierbare Quellen dokumentiert.
- [runs/2026-05-02_Codex_GPT55-Run09_skill_team_harness.md](memory/runs/2026-05-02_Codex_GPT55-Run09_skill_team_harness.md) — **Skill-Team Harness**: 5 Subagenten nutzten neue Skills, 50 Aufgaben dokumentiert, Preflight/Skill-Inventar in ULTRAPLAN/AGENTS/CLAUDE/MEMORY integriert.
- [runs/2026-05-02_Codex_GPT55-Run10_skill_operating_board.md](memory/runs/2026-05-02_Codex_GPT55-Run10_skill_operating_board.md) — **Skill Operating Board**: naechste Skill-Runs priorisiert, `scripts/check_codex_skills.ps1` erstellt, 5/5 Skill-Dateien verifiziert, `browser-harness` PATH-Warnung dokumentiert.
- [runs/2026-05-02_Codex_GPT55-Run11_memory_deploy_smoke.md](memory/runs/2026-05-02_Codex_GPT55-Run11_memory_deploy_smoke.md) — **Memory + Deploy + Smoke**: Memory summary-first verdichtet, Frontend Fly online + Playwright visual smoke gruen, Backend-Code lokal 6/6 smoke gruen, Backend online durch Hetzner SSH-Auth blockiert.
- [runs/2026-05-02_Codex_GPT55-Run12_hetzner_frontend_fallback.md](memory/runs/2026-05-02_Codex_GPT55-Run12_hetzner_frontend_fallback.md) — **Hetzner Frontend Fallback**: Fly durch Trial/Billing 502, React-Frontend als Hetzner-Container unter `https://api.carotis.diggai.de/` online, Backend-Health + Playwright visual smoke gruen; Hauptdomain bleibt DNS/Fly-blockiert.
- [runs/2026-05-02_Codex_GPT55-Run13_rohde_v4_docs.md](memory/runs/2026-05-02_Codex_GPT55-Run13_rohde_v4_docs.md) — **Rohde v4 Docs**: drei Rohde-Artefakte erstellt, NVIDIA-Rollenupdate aufgenommen, Promotion modular statt starr zweijaehrig formuliert, Cosima-Prompts vorbereitet.
- [runs/2026-05-02_Codex_GPT55-Run14_design_demo_testdata.md](memory/runs/2026-05-02_Codex_GPT55-Run14_design_demo_testdata.md) — **Design Demo + Testdaten**: Claude-Design-nahe 3-Spalten-Demo ins Online-Frontend integriert, synthetische DICOMs downloadbar gemacht, Backend-Upload/Grad-CAM-Fallback repariert und online mit Playwright verifiziert.
- [runs/2026-05-04_Codex_GPT55-Run15_dns_hetzner_proxy.md](memory/runs/2026-05-04_Codex_GPT55-Run15_dns_hetzner_proxy.md) — **DNS + Hetzner Proxy**: INWX final auf Hetzner-A umgestellt; Caddy bedient `carotis.diggai.de` und `api.carotis.diggai.de`, beide liefern 200; Fly.io bleibt wegen Trial/Billing blockiert und ist kein DNS-Ziel.
- [runs/2026-05-04_Codex_GPT55-Run16_master_demo_token.md](memory/runs/2026-05-04_Codex_GPT55-Run16_master_demo_token.md) — **Master Demo Token**: Dauerhafter `master-admin-demo` Zugang via gehashtem Master-Demo-Token im Backend aktiviert und live verifiziert; Rohwert nicht in Memory/Docs wiederholt.
- [runs/2026-05-04_Codex_GPT55-Run17_live_browser_ui_fix.md](memory/runs/2026-05-04_Codex_GPT55-Run17_live_browser_ui_fix.md) — **Live Browser UI Fix**: Playwright-Live-Test gegen `carotis.diggai.de`; Master-Demo-Token im Frontend verifiziert; CSP `connect-src`, `/health/` Redirect-Bug und Walkthrough-Mobile/Overlay verbessert; Live-Smoke gruen.

## Stride-Prompts (P0 — v2 erledigt / v3 vorbereitet)

| Prompt | Status | Ready-File |
|--------|--------|-----------|
| G | ✅ Done | `Stride V2/KI_Tools_Marktanalyse_v2.pdf` |
| H | ✅ Done | `Stride V2/Carotis_AI_Konzept_v2.docx` |
| C | ✅ Done | `Stride V2/Expose_Carotis_AI_Rohde_v2.docx` |
| D | ✅ Done | `Stride V2/Tech_Description_Klinikum_v2.docx` |
| E | ✅ Done | `Stride V2/Value_Proposition_Klinikum_v2.docx` |
| F | ✅ Done | `Stride V2/Carotis_Ai_Rohde_v2.docx` |
| B | ✅ Done | `Stride V2/Anschreiben_Aroob_an_Rohde_v2.docx` |
| A | ✅ Superseded | Plaintext backup: `Mail_Aroob_an_Rohde_DRAFT.txt`; v3 prompt: `Stride V3/Anschreiben_Aroob_an_Rohde_v3_PROMPT.md` |

**Plan:** `stride_execution_plan.md`. V3-Master-Prompt liegt in `Stride V3/Office_Docs_v3_MASTER_PROMPT.md`.

## Offene Tasks (Stand 2026-05-01)

- `T-018` — P5 Sarah Hospital Hardware: human/external, nicht agentisch jetzt.
- `T-020` — P3 Heatmap-Annotation-UI: wartet auf P3/echtes DICOM-Rendering.
- `T-022` — P3 Hyperparam-Search: wartet auf P3-Trainingsdaten/GPU.
- `T-023` — P5 Adoption-Monitoring: wartet auf klinische Nutzung.
- `T-024` — P6 Methodisches Paper: wartet auf Validierungsergebnisse.
- `W-12` — Mail rausschicken: human, wartet auf Deploy-Unblock/Versandentscheidung.

## Decisions (Arzt-Entscheidungs-Trees)

- [decisions/README.md](memory/decisions/README.md) — Format + Konventionen. Ab P5 gefüllt.

## Anomalies (KI-Mensch-Diskrepanzen + Code-Bugs)

- [anomalies/README.md](memory/anomalies/README.md) — Format + Triage-Workflow. Ab P5 für klinische Anomalien gefüllt.
- [anomalies/2026-04-29_kimi_e2e_13_bugs.md](memory/anomalies/2026-04-29_kimi_e2e_13_bugs.md) — 13 gefixte Bugs aus K-01..K-16 E2E-Verifikation. **Pflicht-Lese vor Code-Generation in `code/`.**

---

**Wartung:** Halte diese Datei < 200 Zeilen. Wenn ein Eintrag obsolet ist (z.B. P0 abgeschlossen → P1 läuft) → Datei in `memory/archive/` verschieben + Zeile hier streichen.
# MEMORY UPDATE 2026-05-11

- [outputs/Aroob_Today_Briefing_2026-05-11.md](outputs/Aroob_Today_Briefing_2026-05-11.md) - Aktuelles Tagesbriefing fuer Dr. Aroob: Forschungsprototyp-Pivot, Full Frontend/Backend Stack, Hetzner-Live-Stand, kritische Disclaimer-/CDS-Gaps und konkrete Gespraechspunkte fuer 2026-05-11.
- [runs/2026-05-11_Codex_GPT55-Run18_aroob_today_alignment.md](memory/runs/2026-05-11_Codex_GPT55-Run18_aroob_today_alignment.md) - Codex GPT-5.5: Aroob-Gespraechsstand, Plan-/Stack-Pivot, Index/Roadmap/Master-Update, K-55 done.
