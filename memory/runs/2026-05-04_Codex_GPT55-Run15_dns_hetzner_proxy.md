---
name: 2026-05-04_Codex_GPT55-Run15_dns_hetzner_proxy
type: run
---

## Goal
`carotis.diggai.de` Erreichbarkeit prüfen und DNS-/Proxy-Blocker für den Hetzner-Fallback beseitigen.

## Done
- DNS geprüft: `carotis.diggai.de` zeigt weiter als CNAME auf `carotis-ai-frontend.fly.dev`; Fly liefert 502.
- DNS geprüft: `api.carotis.diggai.de` zeigt korrekt auf `204.168.230.127`.
- Hetzner-SSH-Key-ACL lokal repariert, damit OpenSSH den Key akzeptiert.
- Hetzner geprüft: Backend und Frontend liefen, Caddy war gestoppt.
- `deploy/Caddyfile.backend` erweitert: Caddy akzeptiert jetzt `api.carotis.diggai.de` und `carotis.diggai.de`.
- Aktualisierte Caddyfile auf Hetzner kopiert und Caddy wieder gestartet.
- `deploy/hetzner-backend.compose.yml` Healthcheck auf Caddy-Admin-Endpoint umgestellt, weil das Caddy-Image kein `curl` enthält.
- Haupt-Memory aktualisiert: `CLAUDE.md`, `ULTRAPLAN.md`, `memory/domain/p0f_deploy_state_compact_2026-05-02.md`, `RUNBOOK_TODAY.md`, `MEMORY.md`.
- Nach User-Go wurde INWX-DNS final umgestellt: `carotis.diggai.de` ist jetzt `A 204.168.230.127`.
- Caddy nach DNS-Propagation neu gestartet; Let’s Encrypt TLS fuer `carotis.diggai.de` wurde erfolgreich ausgestellt.
- Verifiziert: `https://carotis.diggai.de/` 200, `https://api.carotis.diggai.de/` 200, `https://api.carotis.diggai.de/health/` status ok, Caddy healthy.

## Surprised by
Caddy war sauber beendet, während Backend/Frontend weiter liefen. Dadurch war auch der funktionierende Fallback `api.carotis.diggai.de` kurzfristig nicht erreichbar. Der alte Healthcheck konnte im Caddy-Image nicht funktionieren, weil `curl` nicht installiert ist.

## Avoided
Keine Patientendaten, keine Secrets ausgegeben, keine fremden Worktree-Änderungen zurückgesetzt. INWX wurde nicht automatisiert geändert, weil Browser-Harness ohne Chrome Remote Debugging nicht attachen konnte.

## Next
Hauptdomain ist online. Fly.io bleibt separat durch Trial/Billing blockiert; nicht erneut auf Fly-CNAME drehen, solange Fly `trial has ended` meldet. Bei jedem neuen Deploy-/Online-Prompt zuerst die oben aktualisierten Memory-Dateien lesen.
