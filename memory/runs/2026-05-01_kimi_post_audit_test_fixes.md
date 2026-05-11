---
name: 2026-05-01_kimi_post_audit_test_fixes
type: run
---

## Goal

Alle nach dem Deep-Audit-Implementierungssprint (Run06) verbleibenden Test-Failures beheben: 8 Backend-Failures + 17 Frontend-Failures auf 0 reduzieren. Typecheck und Build muessen ebenfalls gruen sein.

## Done

- **Backend (8 Failures → 0):**
  - `test_lazy_schema_loading.py`: Test robust gemacht (Save/Restore des globalen Schema-Cache)
  - `test_onnx_session_optimization.py`: Mock auf dynamische Batch-Groesse umgestellt (side_effect)
  - `test_security_timing_attack.py`: Alle 6 Test-Methoden mit `@pytest.mark.asyncio` + `await` versehen

- **Frontend (17 Failures → 0):**
  - `vitest.setup.ts`: `localStorage.clear()` + stateful Storage-Map implementiert
  - `Walkthrough.tsx`: Doppeltes `role="dialog"` entfernt (Overlay vs Step-Card)
  - `FreeTextField.test.tsx`: `use-debounce`-Mock auf delay-basiertes Caching umgestellt (verhindert Infinite Re-Render)
  - `DecisionForm.test.tsx`: `QueryClientProvider`-Wrapper hinzugefuegt; Queries auf `getByRole("spinbutton")` umgestellt
  - `AuthGate.tsx`: `htmlFor` + `id` fuer Label/Input Association (Accessibility)
  - `AuthGate.test.tsx`: `AbortError` korrekt erzeugt; `Promise<Response>` Generic fix
  - `DecisionForm.test.tsx`: `trust_score` in `mockResult` ergaenzt
  - `Walkthrough.test.tsx`: Unused `storeModule` Import entfernt

- **Verifikation:**
  - Backend: **120 passed, 11 skipped** (~83s)
  - Frontend: **29 passed** (6 files, ~43s)
  - Typecheck: **0 errors**
  - Build: **successful** (Cornerstone WASM Warnings erwartet)

## Surprised by

- Der `use-debounce`-Mock war subtiler als erwartet: ein simples `(fn) => fn` fuehrt zu Infinite Re-Renders, weil `useEffect` die sich aendernde Funktions-Reference als Dependency sieht. Die Loesung (delay-basiertes Caching) war elegant und verhindert auch Cross-Contamination zwischen mehreren `useDebouncedCallback`-Aufrufen im selben Component.
- `pytest.mark.asyncio` war noetig, obwohl `pytest.ini` bereits `asyncio_mode = auto` hat. Die Auto-Discovery greift offenbar nicht, wenn eine Funktion direkt (nicht via FastAPI TestClient) aufgerufen wird.

## Avoided

- Keine Aenderungen an Produktions-Logik ausser minimalen Accessibility-Fixes (`htmlFor`/`id` in AuthGate, `role="dialog"` in Walkthrough). Keine neuen Features, kein Scope-Creep.
- Keine Aenderungen an den 13 dokumentierten Frontend High-Severity Issues (Focus-Trap, Canvas-Role etc.) — diese bleiben fuer P3 reserviert.

## Next

1. Opus 4.7 liest diesen Handoff und entscheidet ueber naechste P0-Prioritaet (vermutlich: Stride-Prompts G/H oder Deploy-Unblock-Unterstuetzung fuer Lou).
2. Wenn Deploy-Blocker geloest: Codex/Kimi parallel fuer Fly-Deploy + Hetzner-Setup.
3. P3-Vorbereitung: Cornerstone3D WASM-Initialisierung + echtes DICOM-Rendering.

## Memory updates

- `memory/runs/2026-05-01_handoff_opus47_post_audit_fixes.md` — Opus-Handoff mit vollstaendiger Failure/Fix-Matrix
- `AGENTS.md` — Test-Baseline aktualisiert (120 passed / 29 passed); Anomalien-Status auf GREEN gesetzt
- `MEMORY.md` — Run-Log Zeile hinzugefuegt
