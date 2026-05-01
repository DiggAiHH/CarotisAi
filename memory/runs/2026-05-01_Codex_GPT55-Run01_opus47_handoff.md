---
name: 2026-05-01_Codex_GPT55-Run01_opus47_handoff
type: run
---
## Goal
Audit what is still missing for Fly+Hetzner deploy, fix repo-side deploy holes, and create an Opus 4.7 handoff.
## Done
Verified the current repo contains Hetzner deploy path fixes, remote prereq setup, model sync, persistent backend data bind mount, Caddy Host-header healthcheck, and Fly failure diagnostics; generated and set GitHub Secret `ANONYMIZATION_SALT`; wrote `OPUS47_HANDOFF_2026-05-01.md`.
## Surprised by
GitHub still lacks `FLY_API_TOKEN`; DNS still points both deploy domains to `75.2.60.5`; Hetzner SSH still rejects the deploy key.
## Avoided
Did not print secret values, did not touch patient-data paths, did not attempt dashboard-only actions, did not push directly to `master`.
## Next
Set `FLY_API_TOKEN`, authorize deploy public key on Hetzner, correct INWX DNS, create/verify Fly app and cert, then run both deploy workflows from `master`.
## Memory updates
Add pointer to this run and the Opus handoff in `MEMORY.md`.
