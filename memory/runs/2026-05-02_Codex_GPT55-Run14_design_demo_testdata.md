---
name: 2026-05-02_Codex_GPT55-Run14_design_demo_testdata
type: run
date: 2026-05-02
agent: Codex GPT-5.5
phase: P0f
---

## Goal

Claude-Design-Prototyp nicht nur als Screenshot haben, sondern im echten Online-Frontend sichtbar machen. Zusaetzlich synthetische Test-DICOMs fuer Rohde/Nico bereitstellen und den Upload-/Inference-Pfad online pruefen.

## Done

- `code/frontend/src/App.tsx`: sofort sichtbare 4-Fall-Demo mit Patientenliste, Download-Link und synthetischem Default-Result integriert.
- `code/frontend/src/components/DicomViewer/DicomViewer.tsx`: synthetische CTA-Preview mit Heatmap, Windowing-Badges, Slice-Bar und Upload-Fallback eingebaut.
- `code/frontend/src/components/AiPanel/AiPanel.tsx`: Claude-Design-naeheres AI-Panel mit Gauge, Confidence, Trust, Vulnerability-Markern, SHAP-Sektion und Aktionen umgesetzt.
- `code/frontend/public/demo/dicoms/`: vier synthetische DICOMs fuer Online-Download bereitgestellt.
- `code/scripts/generate_demo_data.py`: leere PII-Tags entfernt; Backend-Check erwartet Abwesenheit der Tags, nicht nur leere Werte.
- `code/backend/app/services/gradcam.py`: Demo-ONNX-kompatible Score-Extraktion und sequenziellen Perturbation-Fallback fuer feste Batch-Dimension `1` implementiert.
- `deploy/hetzner-backend.compose.yml`: Frontend-Build bekommt `VITE_API_KEY` aus Server-Env, damit Online-Upload den echten API-Key nutzt.
- `outputs/Rohde_Testdaten_Demo_2026-05-02.md`: Testdaten-Links und manuellen Testablauf dokumentiert.
- Backend + Frontend direkt auf Hetzner-Fallback `https://api.carotis.diggai.de/` deployed.

## Verified

- `npm run typecheck` gruen.
- `npm run lint` gruen.
- `npm test -- --run` -> 29/29 Frontend-Tests gruen.
- `npm run build` gruen; bekannte Cornerstone/WASM Chunk-Warnungen bleiben.
- Backend focused tests: `tests/test_gradcam.py tests/test_inference_full.py` -> 1 passed / 4 skipped wegen fehlendem torch.
- Lokaler Playwright-Smoke mit `VITE_SKIP_AUTH=true` gruen.
- Online Playwright-Smoke mit frisch generiertem Demo-Token gruen.
- Online Upload-Smoke mit `RUN_UPLOAD=true BASE_URL=https://api.carotis.diggai.de` gruen.
- Online backend logs: `POST /api/v1/inference/predict` -> 200, `inference_completed`, Stenosewert ausgegeben.
- `https://api.carotis.diggai.de/` -> 200.
- `https://api.carotis.diggai.de/health/` -> 200.
- `https://api.carotis.diggai.de/demo/dicoms/case_002.dcm` -> 200.
- Lokaler PII-Tag-Check der vier Public-DICOMs -> keine Basic-PII-Tags gefunden.

## Surprised by

- Der sichtbare Online-Designstand war vorher leer, weil der Viewer ohne Upload nur Dropzone zeigte und die Fallliste ein Platzhalter war.
- Die synthetischen DICOMs hatten zwar leere Patient-Felder, aber die Tags existierten noch; der Backend-Check lehnt das korrekt ab.
- Das online laufende Backend war aelter als der lokale Fix und hatte noch fragiles ONNX-Output-Postprocessing.
- Der Demo-ONNX akzeptiert keine batched Grad-CAM-Perturbationen; sequenziell ist fuer P0f stabiler.

## Avoided

- Keine echten Patientendaten.
- Keine Office-Dokumente direkt editiert.
- Keine Secrets in Dateien geschrieben; frische Smoke-Test-Tokens wurden nur temporaer genutzt und nicht persistiert.
- Kein Ruecksetzen fremder Dirty-Worktree-Aenderungen.

## Next

Lou kann Rohde/Nico mit `https://api.carotis.diggai.de/` testen. Vor Versand einen frischen Demo-Token erzeugen und separat sicher uebergeben. Hauptdomain `carotis.diggai.de` bleibt separat durch Fly/DNS blockiert; der funktionierende Fallback ist `api.carotis.diggai.de`.
