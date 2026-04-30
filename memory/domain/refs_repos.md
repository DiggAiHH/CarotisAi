---
name: refs_repos
description: GitHub-Repos und Hosting-Pointer für Carotis-AI. dr-aroob-ki ist die UI-Codebase, Dr-Aroob-Portal das Backend-Skelett, Demo läuft auf Netlify-Subdomain.
type: reference
last_updated: 2026-04-27
---

# Repos & Hosting

## GitHub

- **DiggAiHH/dr-aroob-ki** — Frontend-Codebase (React 19, Vite, TS, Tailwind v4). Wird zur Carotis-AI-UI ausgebaut (DICOM-Viewer + AI-Panel + Decision-Tree-Capture-Form).
  - URL: https://github.com/DiggAiHH/dr-aroob-ki
  - Branch: main
  - CI: github.com/DiggAiHH/dr-aroob-ki/actions
  - Lokaler Pfad bei Lou: `C:\Users\tubbeTEC\dr-aroob-ki`
  - Bestehender Engineering-Harness: `C:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Prompts & Engineering Harnessing` (Tasks T-001 bis T-032 für UI-Refactor; siehe HARNESS.md dort)

- **DiggAiIT/Dr-Aroob-Portal** — Portal/Backend-Skelett (vermutlich Auth + Dashboard). Status unklar, muss in P0/P1 gecheckt werden.
  - URL: https://github.com/DiggAiIT/Dr-Aroob-Portal
  - To-do: erste P0-Aktion ist `git clone` und Inventur. Siehe `memory/runs/<datum>_repo_audit.md` wenn gemacht.

## Hosting

- **aroob-ai-demo.diggai.de** (Netlify) — Demo-Domain für UI-Mockups + Stakeholder-Demo (Rohde-Termin). Niemals echte Patientendaten.
- **diggai.de** (Netlify) — Lou's Hauptplattform. Carotis-AI wird ab P5 als Modul integriert.

## Future Repos (geplant für P3+)

- `DiggAiHH/carotis-ai-edge` — FastAPI-Backend + ONNX-Runtime (P3+)
- `DiggAiHH/carotis-ai-training` — PyTorch-Trainings-Pipeline (P3+; läuft auf HAW-Workstation, nicht im Klinikum)
- `DiggAiHH/carotis-ai-regulatory` — MDR-Bundle, Risk-File, Klinische Bewertung (P1+)

## Git Conventions

- Branches: `main` ist deploy. Feature-Branches `feat/<phase>-<short-name>` (z.B. `feat/p2-anonymize-pipeline`).
- Commits: English, Conventional Commits format (`feat: ...`, `fix: ...`, `docs: ...`).
- Tags: `v<phase>.<sub>.<patch>` (z.B. `v0.1.0` = P1-MVP, `v0.4.0` = P4-Edge-Integration).
- PR-Titel: `[P<N>] <short description>` damit Phasen-Filter im GitHub-Dashboard funktioniert.

## Secrets / .env

- **Niemals in Git.** Doppler-Vault wenn schon konfiguriert (siehe Elbtronika-Setup), sonst lokal `.env` + `.env.example` mit Platzhaltern.
- Patientendaten-Pfade: nie in committed Files, nicht mal als Beispielwert.
