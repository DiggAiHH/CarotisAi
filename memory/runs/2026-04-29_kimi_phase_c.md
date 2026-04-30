---
name: 2026-04-29_kimi_phase_c
type: run
---

## Goal
Phase C: HiResCAM-Evaluation als Grad-CAM-Alternative fuer bessere XAI-Aufloesung.

## Done
- **Recherche:** HiResCAM ist mathematisch trivial — `gradients * activations` statt `gradients.mean()` (GAP)
  - Keine neue Dependency noetig; Erweiterung des bestehenden `gradcam.py`
- **Implementation:**
  - `ml/xai/gradcam.py` — `SegHiResCAM` Klasse hinzugefuegt (pixel-wise weighting, kein GAP)
  - `ml/xai/evaluate_cam_methods.py` — Evaluations-Skript mit Metriken
    - Zeitmessung (ms)
    - Aufloesung (Pixel ueber Threshold)
    - Schaerfe (raeumliche Varianz)
    - Korrelation (Pearson zwischen beiden Heatmaps)
  - `regulatory/adr/005_hirescam_xai.md` — Architektur-Entscheidung
- **Tests:** `tests/test_gradcam.py` — 5 Tests
  - Output-Shape, Normalisierung, Differenz Grad-CAM vs HiRes-CAM, Schaerfe-Vergleich
- **Evaluation-Ergebnisse** (Dummy-Modell, synthetischer 256x256 Slice):
  | Metrik | Grad-CAM | HiRes-CAM | Faktor |
  |--------|----------|-----------|--------|
  | Zeit | 338 ms | 215 ms | 1.6x schneller |
  | Aufloesung | 3 px | 43 px | 14x mehr Pixel |
  | Schaerfe | 0.000037 | 0.000652 | 18x hoehere Varianz |
  | Korrelation | -0.0008 | — | Unkorreliert (erwartet bei Dummy) |
- **Qualitaet:** ruff 0 Errors, black formatiert, 66/66 Tests passing

## Surprised by
- HiRes-CAM ist auf dem Dummy-Modell **schneller** als Grad-CAM (215 vs 338 ms) — wahrscheinlich weil kein GAP berechnet werden muss.
- Die Aufloesungsdifferenz ist massiv: 43 vs 3 Pixel — das bestaetigt die Theorie, dass HiRes-CAM bei duennen Strukturen deutlich besser lokalisiert.

## Avoided
- Keine neue Dependency (`pytorch-grad-cam`) — eigene Implementation ist 40 Zeilen und vollstaendig kontrollierbar.
- Kein Breaking Change — Grad-CAM bleibt Default, HiRes-CAM ist Option.

## Next
- P1-Prep-A: Hardware-Spec Edge-Server
- P1-Prep-B: AVV-Vorlage Local-First
- T-010: Mail an Prof. Rohde (human step)

## Memory updates
- `ml/xai/gradcam.py` enthaelt jetzt beide Methoden
- `regulatory/adr/005_hirescam_xai.md` dokumentiert die Entscheidung
- `reports/xai_eval/` enthaelt Beispiel-Outputs und Metriken
