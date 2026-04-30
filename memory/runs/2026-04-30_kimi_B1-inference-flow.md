---
date: 2026-04-30
model: kimi
session: B1-inference-flow
---

## Goal
B1 Critical Blocker fixen: App.tsx war statischer Shell. Full inference flow wiren.

## Done
- App.tsx: AuthGate-Wrapper, useInference, StatusBadge, AiPanel+DecisionForm wired
- apiClient.ts: X-Demo-Token Header aus localStorage in alle Requests injiziert
- HeatmapOverlay.tsx: base64-string support hinzugefügt (backend sendet heatmap_b64)
- DicomViewer.tsx: heatmap Prop auf number[][] | string geändert
- AuthGate: useDemoToken in eigene Datei extrahiert (ESLint fix)
- i18n.ts: Neue Keys für Status-Badges und Logout
- typecheck + lint grün
- Gepusht zu DiggAiHH/CarotisAi (efcf06c)

## Surprised by
- Vitest hängt lokal (jsdom+Cornerstone3D WASM), nicht durch Änderung verursacht

## Next
- Nutzer will Copilot-Plan-Mode Workflow für "alles erledigen was noch offen ist"
- Prompt 1 + Prompt 2 vorbereiten
