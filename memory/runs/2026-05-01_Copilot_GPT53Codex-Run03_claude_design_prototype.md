---
name: 2026-05-01_Copilot_Sonnet46-Run03_claude_design_prototype
type: run
model: GitHub Copilot (Claude Sonnet 4.6)
phase: P0f
---

## Goal
Build a fully interactive Carotis AI medical imaging prototype in claude.ai/design. Send optimized iteration prompts, verify all 8 interactions, then update the ULTRAPLAN browser harness with learnings.

## Done
- Navigated to `https://claude.ai/design/p/019de4bf-5dbc-7c47-b1fe-8a0466e64c9c?file=Carotis+AI.html`
- Sent comprehensive 3-column medical AI prototype prompt (900+ tokens) via chat composer
- Claude Design generated 4 component files:
  - `components/tweaks-panel.jsx` — Tweaks panel UI
  - `components/DicomViewer.jsx` — DICOM viewer with canvas + Grad-CAM + windowing presets
  - AI Panel component — stenosis gauge + SHAP + physician override
  - `Carotis AI.html` — main app file tying everything together
- Verifier agent auto-caught and fixed `useTweaks` destructuring bug → "Clean load"
- Verified all 3 columns functional via mobile tab switching:
  - **Column 1 (Patients)**: Carotis AI header + v0.1 Demo badge + search + 4 patients (Müller 72% red, Schmidt 45% emerald, Weber 68% amber, Fischer 31% emerald) + "4 records" label
  - **Column 2 (Viewer)**: CTA axial canvas + Grad-CAM jet heatmap overlay + Vessel windowing active + HU overlays + AI: 72% stenosis badge + slice slider 42/120
  - **Column 3 (AI)**: AI Analysis LIVE + 72% gauge + 84% confidence + HIGH vulnerability + SHAP section (Vessel Diameter +38%, Plaque Density -25%, Wall Irregularity +18%) + Trust Score 0.78/1.0 + Physician Override + Generate Report PDF + Send to RIS
- Sent Iteration 2 prompt: fix console errors + gauge animation + patient switching UX + SHAP expand + RIS spinner + desktop 3-col layout fix

## Surprised by
1. **Claude Design verifier agent** runs automatically after every generation — looks for runtime errors and auto-fixes them without user prompting. Caught `useTweaks` destructuring: `const { showAnnotations } = useTweaks()` was wrong → auto-corrected.
2. **Component file splitting**: Claude Design generates multiple named files (not one monolithic file) — `tweaks-panel.jsx`, `DicomViewer.jsx`, etc.
3. **Tweaks panel opens by default** when prototype renders. It overlaps Column 3 (AI Panel). Must click the "Tweaks" toggle (blue switch) in the toolbar to close it.
4. **Tweaks panel toggle**: Not a normal button. It's a switch element. Accessible via coordinate click (`page.mouse.click(490, 43)`) or via `[ref=e739]` in the snapshot ("Toggle tweak controls").
5. **iframe structure**: The prototype renders in a cross-origin iframe at `<projectid>.claudeusercontent.com`. Main page controls (toolbar, Tweaks toggle) are in the parent. Prototype interactions (tab bar, patient clicks) must be accessed via `page.frames()` and iterating frames.
6. **20 console errors**: Remain after generation but are non-blocking. Verifier agent said "app loads cleanly" despite them. Likely React dev warnings.
7. **Mobile-first layout**: On viewport < 1024px, the 3-column layout shows as tab-based mobile view. Desktop columns may need explicit CSS check.
8. **Generation completeness signal**: 
   - File tab appears at top: "Carotis AI.html"
   - Verifier section: "Verifier agent check completed"
   - Claude message: "Fixed — [bug description]. Everything should be working as expected."
9. **Chat composer**: `page.getByTestId('chat-composer-input')` — use `.fill()` not `.type()` for large text (avoids character-by-character slowness).
10. **beforeunload dialog**: Can appear when navigating. Dismiss with `page.on('dialog', d => d.dismiss())`.

## Avoided
- Sending multiple overlapping iteration prompts before first was processed
- Retrying same click selector after failure — switched to coordinate-based clicks and frame iteration
- Blocking on Tweaks panel (just acknowledged it and used iframe frame refs to access prototype content)
- Re-generating entire prototype after small bug (verifier handles it automatically)

## Next
- Wait for Iteration 2 to render (~2-3 min), then verify improvements
- Send Iteration 3 (desktop layout screenshot, patient switching test)
- Update `ULTRAPLAN.md` §4.12 with Claude Design browser harness
- Download/save final `Carotis AI.html` to workspace as reference artifact

## Memory updates
- ULTRAPLAN.md §4.12 Claude Design Browser Harness Patterns — see below
- AGENTS.md prototype section — Carotis AI prototype in cloud, project ID documented
