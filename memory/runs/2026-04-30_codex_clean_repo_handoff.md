---
name: 2026-04-30_codex_clean_repo_handoff
type: run
---
## Goal
Carotis-AI von falschem/unsicherem Remote-Kontext trennen und saubere Repo-/Deploy-Handoff fuer Fly-Frontend + Hetzner-Backend vorbereiten.
## Done
Git-origin mit eingebettetem Token lokal entfernt, neue Root-Deploy-Artefakte fuer Fly-Frontend und Hetzner-Backend erstellt, GitHub-Actions-Workflows vorbereitet, Handoff-Dokument geschrieben.
Nach `go weiter`: sauberer Remote `https://github.com/DiggAiHH/CarotisAi.git` bestaetigt, origin/master synchron, sichere GitHub-Secrets gesetzt (`HETZNER_SERVER_IP`, `HETZNER_SSH_USER`, `ACME_EMAIL`, `API_KEY`, `ADMIN_API_KEY`).
## Surprised by
Der lokale Remote enthielt einen GitHub-PAT; zusammen mit dem im Chat geposteten Fly-Token muessen beide rotiert werden.
## Avoided
Keine Secrets in Dateien gespeichert, keine Pushes, keine Verbindung zum Anamnese-Repo, keine Provider-Aktionen ohne verifizierte Auth.
## Next
Lou rotiert Fly-Token, setzt `FLY_API_TOKEN`, setzt `HETZNER_SSH_PRIVATE_KEY`, konfiguriert INWX DNS; danach `go` fuer Deploy-Verifikation.
## Memory updates
Run-Log angelegt; Handoff liegt in REPO_CLEANUP_AND_DEPLOY_HANDOFF.md.
