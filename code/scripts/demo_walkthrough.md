# Carotis-AI Demo-Walkthrough — Rohde-Meeting (5 Minuten)

> **Ziel:** In 5 Minuten zeigen wir den kompletten Stack:
> Dashboard -> Architektur -> Live-Demo -> Audit-Trail -> Engineering-Harness.

---

## Min 0:00–1:00 — Dashboard-Tour

**Was Lou sagt:**
> "Das ist unser Projekt-Dashboard. Es zeigt den aktuellen Stand aller Arbeitspakete, den Modell-Status und die jüngsten Sessions. Alles offline-fähig — kein Cloud-Export von Patientendaten."

**Aktion auf dem Bildschirm:**
1. `dashboard.html` im Browser öffnen (Doppelklick).
2. Scroll zu "Phase-Status" — P0 (Code-Stack) ist 80 % done.
3. Kanban zeigt K-01..K-20 als done, K-21..K-22 pending.
4. Stat-Box: "22 Tests grün, 13 Bugs gefixt, 16 Round-Trips gespart".

**Erwartete visuelle Reaktion:**
- Dashboard ist dunkles Theme (slate-900), professionell, responsiv.

---

## Min 1:00–2:00 — Architektur-Überblick

**Was Lou sagt:**
> "Unsere Architektur ist Local-First Edge AI. Das bedeutet: Patientendaten verlassen niemals den Rechner. Kein Cloud-Export, keine externe API. Das Modell läuft lokal mit ONNX Runtime."

**Aktion auf dem Bildschirm:**
1. `code/01_HARNESS.md` auf Beamer öffnen.
2. Routing-Matrix zeigen: Opus 4.7 für Architektur, Sonnet 4.6 für Code, Haiku 4.5 für atomare Edits.
3. Stack-Diagramm: React 19 + Cornerstone3D Frontend, FastAPI + ONNX Runtime Backend, Ollama + Hermes lokale KI.

**CLI-Befehl (optional):**
```bash
curl -s http://localhost:8000/health | python -m json.tool
```

**Erwartete visuelle Reaktion:**
- Health-Endpoint gibt `{ "status": "ok", "model_loaded": true }` zurück.

---

## Min 2:00–3:30 — Live-Demo (DICOM-Upload + AI-Inferenz)

**Was Lou sagt:**
> "Jetzt die Live-Demo. Ich lade ein synthetisches DICOM hoch — das ist ein Demo-Datensatz ohne PII, kein Klinikum-Patient. Die KI quantifiziert die Stenose und zeigt eine Grad-CAM-Heatmap."

**Aktion auf dem Bildschirm:**
1. Browser auf `http://localhost:3000`.
2. "Datei auswählen" klicken, `data/demo/dicoms/case_003.dcm` auswählen.
3. DICOM wird in Cornerstone3D gerendert.
4. AI-Panel rechts zeigt:
   - Stenosegrad (z.B. 67 % — rot, da > 70)
   - Confidence (z.B. 0.89)
   - Vulnerability-Marker (4 farbige Labels)
5. Heatmap-Overlay über dem DICOM, Opacity-Slider testen.

**Aktion Decision-Tree:**
1. Formular unten ausfüllen:
   - `physician_role_hash`: "Radiologe"
   - `agreement_with_ai.verdict`: "partial_agreement"
   - `physician_decision.stenosis_pct_nascet`: 65
   - Speichern.

**Erwartete visuelle Reaktion:**
- DICOM rendert in < 2 Sekunden.
- AI-Panel zeigt Werte an.
- Heatmap ist als Overlay sichtbar.

---

## Min 3:30–4:30 — Audit-Trail

**Was Lou sagt:**
> "Jede Inferenz ist nachvollziehbar. Unser Audit-Trail speichert SHA-256-Hashes, keine PII. Das ist für die MDR-Zulassung und die Ethikkommission essentiell."

**Aktion auf dem Bildschirm:**
1. Konsole öffnen.
2. Befehl eingeben:

```bash
curl -s -H "X-API-Key: <API_KEY>" \
  http://localhost:8000/api/v1/audit/trail | python -m json.tool
```

**Erwartete visuelle Reaktion:**
- JSON-Array mit 10+ Einträgen (die Demo-Decision-Trees aus K-20).
- Jedes Objekt hat `timestamp`, `event_type`, `actor`, `payload_json`.
- Keine Patientennamen, keine IDs — nur Hashes.

---

## Min 4:30–5:00 — Engineering Harness

**Was Lou sagt:**
> "Wir arbeiten mit einem Engineering-Harness: Jedes Modell bekommt einen Prompt, der Ergebnisse werden in Run-Logs dokumentiert. Das verhindert, dass wir zweimal denselben Bug fixen."

**Aktion auf dem Bildschirm:**
1. `09b_KIMI_PROMPT_SEQUENCE.md` in VS Code öffnen.
2. Scroll durch K-01..K-22 — zeigt die komplette Prompt-Historie.
3. `memory/runs/` im Explorer zeigen — 8+ Run-Logs.
4. `memory/anomalies/2026-04-29_kimi_e2e_13_bugs.md` kurz zeigen.

**Erwartete visuelle Reaktion:**
- Professionelle Dokumentation, keine ad-hoc Änderungen.
- Jeder Schritt ist nachvollziehbar und reproduzierbar.

---

## Post-Demo — Shutdown

```bash
# Linux/macOS
bash scripts/teardown_demo.sh

# Windows
.\scripts\teardown_demo.ps1
```

---

*Letztes Update: 2026-04-29 · K-21*
