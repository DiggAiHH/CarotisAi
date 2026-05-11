# 2026-05-01 - Codex GPT-5.5 Run06 - Browser-Smoke + Claude Design Prompt

## Ziel

- Nach dem ML/Harness- und Task-Cleanup einen echten Chromium-Browser-Smoke fuer das Frontend ausfuehren.
- Blank-Screen-/Runtime-Probleme identifizieren und beheben.
- Oeffentliche Claude-Design-Dokumentation recherchieren und einen massgeschneiderten Prompt fuer Carotis-AI vorbereiten.

## Durchgefuehrt

- Vite-Dev-Server lokal auf `http://127.0.0.1:3001/` genutzt.
- Chromium via Playwright-CLI gegen Token-Gate und App-Inhalt getestet.
- Runtime-Crash beim App-Start behoben:
  - Cornerstone/vtk-Imports in `DicomViewer.tsx` von Top-Level auf Lazy-Imports verschoben.
  - Vite-Aliases fuer problematische CJS/ESM-Default-Imports gesetzt: `globalthis`, `fast-deep-equal`, `seedrandom`.
  - Kleine lokale Shims in `src/lib/*Shim.ts` hinzugefuegt.
- DICOM-Dropzone tastaturbedienbar gemacht (`role="button"`, `tabIndex`, Enter/Space).
- Frontend-Testmocks in `FreeTextField.test.tsx` und `Walkthrough.test.tsx` ohne `any` typisiert.

## Verifikation

- `npm run lint` - gruen.
- `npm run typecheck` - gruen.
- `npm run build` - gruen, nur bekannte Cornerstone/WASM-Externalisierung und Chunk-Size-Warnungen.
- `npm test -- --run` - 6 Files / 29 Tests gruen.
- `npx playwright screenshot --browser=chromium ...`:
  - Token-Gate rendert, kein Blank Screen.
  - App-Inhalt rendert mit synthetischem Demo-Token auf Desktop und Mobile.
  - Beobachtung: Mobile View ist funktional sichtbar, aber horizontal sehr dicht/teilweise abgeschnitten; P3/UI-Responsive-Arbeit bleibt sinnvoll.

## Claude-Design-Recherche

- Offizielle Quellen geprueft:
  - Anthropic Launch-Post: Claude Design ist Research Preview fuer Pro/Max/Team/Enterprise und erzeugt Designs, Prototypen, Slides, One-Pager.
  - Claude Help Center: Workflow mit Chat links, Canvas rechts, Iteration ueber Chat/Kommentare.
  - Design-System-Setup: Codebase, Brand Assets, Slides/Dokumente und bestehende Prototypen als Quellen; Claude extrahiert Farben, Typografie, Komponenten und Layoutmuster.
- `https://claude.ai/design` selbst erfordert eingeloggten Zugriff; keine Aktion im Nutzerkonto ausgefuehrt.

## Offene Punkte

- Optional P3/UI: echtes responsive Layout fuer mobile Breiten statt nur verkleinerter Desktop-Arbeitsflaeche.
- Optional: Playwright-Testdependency (`@playwright/test`) als Dev-Dependency aufnehmen, wenn Browser-Smokes dauerhaft in CI laufen sollen.

