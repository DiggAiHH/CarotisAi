# Opus 4.7 Status-Briefing — Carotis-AI

## Wie du arbeitest (Kontext)
- **Modell**: claude-opus-4-7, 200K Kontext (1M Beta verfuegbar), 128K Output
- **Tokenizer v2**: 1.0-1.35x mehr Tokens als v2 — gleicher Text kostet mehr
- **Adaptive Thinking**: 5 Levels (low/medium/high/xhigh/max). xhigh = Default fuer Claude Code
- **Task Budgets**: Beta-Header `task-budgets-2026-03-13` fuer kostenkontrollierte Agent-Loops
- **Agent Teams**: Multi-Agent-Orchestrierung parallel moeglich
- **Compaction API**: Server-seitige Kontext-Zusammenfassung bei Langlaufenden Sessions

**Fuer dieses Projekt optimal:**
- xhigh fuer Architektur-Entscheidungen, ADRs, regulatorische Texte
- high fuer Code-Review und Planung
- medium fuer atomare Edits und Verify
- Task Budgets aktivieren bei langen Agent-Loops (z.B. 50K Token Ceiling)

---

## Projekt-Status (Stand 2026-04-30)

### Was fertig ist (88 Tests, 0 Regressions)

| Phase | Tasks | Status |
|-------|-------|--------|
| K-01..K-16 | Code-Stack Basis | Done |
| K-17..K-22 | Demo-Robustheit | Done |
| K-23..K-28 | Schema v0.3 + PII-Detection + Override-Capture | Done |
| K-29 | Transformers-PII-Layer (OpenMed-German-ClinicalLongformer) | Done |
| K-30 | HiResCAM Evaluation + ADR-005 | Done |
| K-31..K-32 | P1-Prep: Hardware-Spec + AVV-Vorlage | Done |
| K-33..K-34 | Codex-NN: Confidence Calibration + Trust Score + Frontend-Sync | Done |
| Hermes+Browser | 9 Skills, Config, Settings, Workflow-Doku | Done |
| Stride-Prompts G-H | Fuer Lou vorbereitet | Done |
| T-016 | Modell-Signing-Pipeline (Sigstore/GPG/SHA-256) | Done |

### Was blockiert ist

| Task | Blocker | Status |
|------|---------|--------|
| T-001..T-010 | Office-Dokumente — Lou muss Stride-Prompts ausfuehren | In Progress |
| T-010 | Mail an Prof. Rohde — wartet auf T-009 (Aroob-Review) | Pending |
| T-012..T-013 | Rohde-Reply + Termin-Prep — wartet auf Rohde-Antwort | Pending |
| P1..P7 | Alle Phasen blockiert bis Rohde-Approval | Blocked |

### Technischer Stack (verifiziert)

```
Backend:  Python 3.13.12, FastAPI, Pydantic v2, SQLAlchemy 2.0 async, SQLite
Frontend: React 19, Vite, TypeScript, Tailwind CSS v4, Cornerstone3D 2.19.16
ML:       PyTorch 2.5+ (optional), ONNX Runtime, MFSD-UNet
XAI:      HiResCAM (ADR-005), Grad-CAM Fallback
Local AI: Ollama (mistral:7b, qwen3:4b), Hermes Agent (Port 8200)
Tests:    pytest 78 core + 10 model-signing = 88 total
Quality:  ruff 0, black formatted, npm typecheck/build/lint 0
```

### Key Metrics

| Metric | Wert |
|--------|------|
| Tests passing | 88/88 |
| ruff errors | 0 |
| Frontend build | SUCCESS |
| Frontend typecheck | 0 errors |
| Hermes Skills | 9 |
| ADRs geschrieben | 6 (0001-0004, 005, 006) |
| Decision-Tree-Schema | v0.3 (CDSiC-Taxonomie) |

---

## Neue Features seit letztem Opus-Check-in

### 1. Confidence Calibration + Trust Score
- `ConfidenceCalibrationService`: Platt/Isotonic Scaling, ECE/MCE/Brier
- `TrustScoreService`: Composite Score (confidence 0.5, calibration 0.3, transparency 0.2)
- `PredictionResponse` erweitert: `trust_score`, `confidence_bucket`, `calibrated`
- Frontend: 5-Segment Trust-Balken + Kalibriert-Badge + Confidence-Bucket-Badge

### 2. Hermes + Browser Harness
- Hermes Config: mistral:7b Default, qwen3:4b Fallback, API-Port 8200
- 5 neue Skills: doctor-knowledge-capture, clinical-research-harness, decision-pattern-miner, trust-calibration-monitor, browser-harness
- Browser-Harness: Playwright MCP, erlaubte Hosts (PubMed, Radiopaedia, ESC, ACR)
- Arzt-Workflow: 4 Schritte (DICOM -> AI-Review -> Knowledge Capture -> Pattern Mining)

### 3. Modell-Signing-Pipeline
- `scripts/sign_model.py`: Cosign -> GPG -> SHA-256 Fallback
- `scripts/verify_model.py`: Bundle-Verify mit Integrity + Timestamp-Expiry
- 10 Tests fuer Sign/Verify Roundtrip, Tamper-Detection, Missing-Files

### 4. ONNX Calibration Export
- `ml/inference/onnx_export.py`: `--calibration-pkl` Parameter
- Platt-Scaling als ONNX-Graph (Mul -> Add -> Sigmoid)
- Roundtrip-Test: ONNX-Output vs sklearn predict_proba < 1e-5 diff

---

## Offene Entscheidungen (brauchen Opus 4.7)

### 1. Modell-Update-Verfahren (T-017)
- **Option A**: USB-Lieferung mit signiertem Bundle + manuellem Verify
- **Option B**: Gesicherter Klinikum-Netzwerk-Pfad (FHIR-Bridge) + auto-Verify
- **Frage**: Welche Option empfehlen? Oder beide dokumentieren?

### 2. P3-Architektur-Entscheidungen
- Reasoning-Alignment-Loss: `cosine_similarity(gradcam_heatmap, annotated_mask)`?
- Multi-Task-Head fuer `deciding_feature`: 12-Klassen-Klassifikation?
- Hyperparam-Search: Optuna mit 50+ Trials — lokal oder auf HAW-Cluster?

### 3. Frontend-Next
- Trust-Score-Panel ist visuell verbessert, aber noch keine Echtzeit-Graph
- Heatmap-Annotation (Arzt malt Region auf DICOM) — P3 oder P4?
- Settings-Seite fuer XAI-Default-Methoden — P0a oder P4?

---

## Memory-Updates fuer dich

### Was du wissen musst
- `types/api.ts` ist VERALTET — immer `types/index.ts` als Source of Truth verwenden
- `case_hash` wurde zu `case_id` migriert (Frontend + Backend sync)
- B-14/B-15 Compliance: Keine PII in Logs/Responses, Audit Events metadata-only
- `onnxsim` ist optional (lazy import) — nicht in requirements.txt
- Hermes laeuft als Docker-Service, Port 8200 — noch nicht gestartet auf Dev-Maschine

### Was du NICHT tun sollst
- Keine Office-Dokumente direkt editieren — nur Stride-Prompts generieren
- Kein Modell-Training auf nicht-anonymisierten Daten
- Keine Cloud-Inferenz fuer Patientenbilder

---

## Naechster Plan (Vorschlag)

Wenn du dieses Briefing liest, sind die verbleibenden P0-Tasks:
1. **T-017**: Modell-Update-Verfahren dokumentieren (`regulatory/model_update_procedure.md`)
2. **P3-Architektur-ADR**: ADR-007 fuer Reasoning-Alignment-Loss + Multi-Task-Head
3. **Frontend Settings-Seite**: P0a-Abschluss oder P4-Vorbereitung?

**Lou's naechste menschliche Aktion:** T-001 (Stride-Prompt G) ausfuehren, dann T-002..T-008.

---

## Codex-Update 2026-04-30

- Stride-Artefakte werden gemaess Nutzeranweisung uebersprungen.
- **T-012 Prep abgeschlossen**: `memory/runs/2026-04-30_t012_rohde_reply_kit.md` enthaelt Antwort-Szenarien fuer Ja, Ja-mit-Auflagen, Bedenkzeit, Nein, Aufwand/Kosten/Risiko und Aachen/externer Mentor.
- **T-012 bleibt fachlich blockiert** bis Prof. Rohdes echte Antwort vorliegt. Die finale Mail muss dann aus seiner Originalantwort mit Template 9 erstellt werden.
- Naechster voll agentisch ausfuehrbarer Task: **T-017 Modell-Update-Verfahren** oder **ADR-007 P3-Architektur**, je nach Priorisierung.

---

*Briefing erstellt: 2026-04-30 | Modell: Sonnet 4.6 (Recherche + Aggregation) | 88/88 Tests passing*
*Fuer Opus 4.7: Task Budget empfohlen bei ADR-Schreiben (30K Token Ceiling)*
