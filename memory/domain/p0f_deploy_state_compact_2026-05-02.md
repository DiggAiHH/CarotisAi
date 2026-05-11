---
name: p0f_deploy_state_compact_2026-05-02
type: compact_memory
phase: P0f
mode: summary-first
---

# P0f Deploy State Compact 2026-05-02

## Update 2026-05-04: Online-Stand nach DNS-Fix

Wenn ein Prompt "Deploy", "mach online", "carotis erreichbar", "DNS", "INWX" oder aehnlich sagt, diese Reihenfolge verwenden:

1. `memory/runs/2026-05-04_Codex_GPT55-Run15_dns_hetzner_proxy.md` lesen.
2. DNS pruefen: `Resolve-DnsName carotis.diggai.de` und `Resolve-DnsName api.carotis.diggai.de`.
3. Server pruefen: `curl https://api.carotis.diggai.de/health/`.
4. Falls jemand `carotis.diggai.de` wieder auf Fly-CNAME drehen will: stoppen, solange Fly `trial has ended` meldet.

Fakten:

- `api.carotis.diggai.de` zeigt korrekt auf `204.168.230.127` und war nach Caddy-Restart wieder online.
- `carotis.diggai.de` zeigt jetzt korrekt auf `204.168.230.127`.
- Hetzner SSH funktioniert mit `deploy/hetzner_deploy_key`; lokale ACL wurde repariert.
- Caddy war gestoppt, wurde neu gestartet und ist auf dem Server healthy.
- `deploy/Caddyfile.backend` akzeptiert jetzt `api.carotis.diggai.de` und `carotis.diggai.de`.
- `deploy/hetzner-backend.compose.yml` nutzt einen Caddy-Admin-Healthcheck, weil das Caddy-Image kein `curl` hat.
- Let’s Encrypt TLS fuer `carotis.diggai.de` wurde nach DNS-Propagation erfolgreich ausgestellt.
- Fly.io liefert ueber GitHub Action/Fly CLI `trial has ended`; Fly ist nicht der aktuelle Produktionspfad.

Aktuelle INWX-Zielrecords:

```text
carotis   A       204.168.230.127               TTL 300
api.carotis   A   204.168.230.127               TTL 300
api           A   204.168.230.127               TTL 300
```

## Architektur

- Aktueller P0f-Fallback: Hetzner bedient Frontend + Backend. Ziel: `api.carotis.diggai.de` und nach DNS-Fix auch `carotis.diggai.de`.
- Historischer Frontend-Plan: Fly.io, Ziel `carotis.diggai.de`, App `carotis-ai-frontend`; aktuell wegen Fly Trial/Billing 502 nicht verwenden.
- Backend/Server: Hetzner, `204.168.230.127`.
- GitHub Repo: `DiggAiHH/CarotisAi`, Branch `master`.
- Echte Patientendaten sind verboten; Demo darf nur synthetische/anonymisierte Daten nutzen.

## Erwartete Voraussetzungen

- SSH-Key in `/root/.ssh/authorized_keys` auf Hetzner.
- GitHub Secrets fuer Backend und Frontend Deploy gesetzt.
- DNS: `api.carotis` auf Hetzner; `carotis` fuer aktuellen Fallback ebenfalls auf Hetzner.
- Workflows: `deploy-backend-hetzner.yml`, `deploy-frontend-fly.yml`, `create-fly-app.yml`, `test-ssh-key.yml`.

## Aktuelle Risk Notes

- Zugangsdaten wurden im Chat gepostet; nicht persistieren, nicht in Logs kopieren, nach erfolgreichem Deploy rotieren.
- Lokale Datei `add_ssh_key.py` muss secretfrei bleiben und Env Vars nutzen.
- `browser-harness` ist installiert, aber aktueller Shell-PATH sieht den Befehl nicht.

## Deploy Check Reihenfolge

1. Lokalen Secret-Scan.
2. SSH-Key-Test gegen Hetzner.
3. `gh auth status` und GitHub Secret-Existenz pruefen.
4. Workflows ausloesen oder aktuellen Status lesen.
5. Health checks: Backend `/health/`, Frontend Root.
6. Lokaler/online visueller Smoke mit synthetischem Demo-Kontext.

## Ergebnis 2026-05-04 Run15

- Run11/Run12 sind durch Run15 ueberholt.
- `https://carotis.diggai.de/` ist jetzt Hetzner-Fallback fuer Frontend + Backend: Root liefert React HTML 200.
- `https://api.carotis.diggai.de/` ist online: Root liefert React HTML 200, `/health/` liefert Backend 200.
- SSH gegen `root@204.168.230.127` funktioniert mit `deploy/hetzner_deploy_key`; die lokale Key-ACL wurde repariert.
- INWX-DNS ist final fuer den aktuellen P0f-Fallback: `carotis` und `api.carotis` zeigen auf `A 204.168.230.127`.
- Caddy bedient beide Domains, ist healthy und hat TLS fuer `carotis.diggai.de` erfolgreich via Let’s Encrypt ausgestellt.
- Fly.io bleibt wegen beendetem Trial/Billing (`trial has ended`) blockiert. Nicht auf `carotis CNAME carotis-ai-frontend.fly.dev` zurueckstellen, solange Fly nicht repariert ist.
