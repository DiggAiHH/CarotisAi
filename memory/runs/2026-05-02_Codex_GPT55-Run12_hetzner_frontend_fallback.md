---
name: 2026-05-02_Codex_GPT55-Run12_hetzner_frontend_fallback
type: run
---

## Goal
`carotis.diggai.de` nach User-Eskalation erneut live pruefen und die Demo ohne weitere Rueckfrage so weit wie moeglich online bringen.

## Done
- Live-Status geprueft: `https://carotis.diggai.de/` und `https://carotis-ai-frontend.fly.dev/` liefern 502.
- GitHub-Action-Log geprueft: Fly-Deploy scheitert an beendetem Trial/Billing, nicht an Code.
- Backend verifiziert: `https://api.carotis.diggai.de/health/` liefert 200.
- Hetzner-Fallback gebaut: `carotis-frontend` als zweiter Compose-Service, Caddy routet Root/Assets an Frontend und `/health`, `/api`, `/metrics`, Docs an Backend.
- Frontend-Quellpaket ohne `node_modules`, `dist`, Reports nach Hetzner synchronisiert und Compose remote neu gebaut.
- Workflow gehaertet: Hetzner-Deploy synchronisiert jetzt `code/frontend/` und prueft Backend + Frontend ueber Caddy.
- `browser-harness` per `uv tool install -e` installiert; Attach an Chrome blockiert weiter, weil Remote-Debugging im aktiven Profil nicht freigegeben ist.

## Verified
- `docker compose -f deploy/hetzner-backend.compose.yml config --quiet` gruen mit Dummy-Env.
- `curl -I https://api.carotis.diggai.de/` -> 200 OK, React HTML.
- `curl https://api.carotis.diggai.de/health/` -> `status: ok`.
- `BASE_URL=https://api.carotis.diggai.de npm run e2e:chromium:visual` -> 1/1 passed.
- `https://carotis.diggai.de/` bleibt 502, weil DNS noch auf Fly zeigt.

## Surprised by
Der vorherige Frontend-200 war nicht stabil; spaetere Fly-Deploys schlagen hart mit `trial has ended` fehl. Die lokale `browser-harness`-Skill-Installation enthielt zunaechst keine Runtime-Dependencies im PATH.

## Avoided
Keine Secrets in Dateien geschrieben, keine Patientendaten verwendet, keine fremden Git-Changes zurueckgesetzt, keine Fly-Billing-Aktion vorgetaeuscht.

## Next
INWX DNS fuer `carotis.diggai.de` von Fly-CNAME auf Hetzner `A 204.168.230.127` drehen oder Fly-Billing aktivieren. Bis dahin ist die Demo unter `https://api.carotis.diggai.de/` online.
