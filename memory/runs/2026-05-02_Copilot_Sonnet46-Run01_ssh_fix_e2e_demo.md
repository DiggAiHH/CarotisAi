---
name: 2026-05-02_Copilot_Sonnet46-Run01_ssh_fix_e2e_demo
type: run
agent: Copilot
model: Sonnet46
---

## Goal
1. Hetzner SSH-Key-Problem lösen (deploy key für GitHub Actions)
2. ULTRAPLAN + Harness-Protokoll lesen
3. Vollständiger E2E-Test des Demo-Stacks
4. Demo-Zugangsdaten generieren (Rohde-Token)
5. Playwright Browser-Test

## Done

### SSH Fix (Session-Vorgänger, hier dokumentiert)
- Rescue Mode auf Hetzner-Server aktiviert (IP: 204.168.230.127)
- `add_deploy_key.py` via Paramiko ausgeführt — Deploy-Key in `/root/.ssh/authorized_keys` geschrieben
- `ssh -i deploy/hetzner_deploy_key root@204.168.230.127 "echo SSH_DEPLOY_KEY_WORKS"` → `SSH_DEPLOY_KEY_WORKS` ✅
- GitHub Actions Backend-Deploy (`deploy-backend-hetzner.yml`) erfolgreich getriggert
- Docker-Container `deploy-carotis-backend-1` + `deploy-caddy-1` gestartet

### E2E Tests
- `https://api.carotis.diggai.de/health/` → HTTP 200 `{"status":"ok"}` ✅
- `https://api.carotis.diggai.de/health/ready` → HTTP 200 `model_loaded=true, db_ok=true` ✅
- `https://api.carotis.diggai.de/health/live` → HTTP 200 ✅
- `https://carotis.diggai.de/` → HTTP 502 ❌ (Fly.io Trial abgelaufen)

### Demo-Token
- Token generiert via SSH → `docker exec deploy-carotis-backend-1 python3 /tmp/gen_token.py`
- Token: `EKZmnbk-Y-N-xQlSXOZdYIMsOoKwJUe-NdOEHSj6ed4`
- Gültig bis: 2026-06-01, max 200 Requests, Label: "Rohde Demo 2026-05-02"
- `GET /api/v1/demo/whoami` mit `X-Demo-Token` → HTTP 200 `requests_remaining=199` ✅

### Playwright Browser-Test
- Backend `https://api.carotis.diggai.de/health/ready` im Browser: `{"status":"ok","model_loaded":true,"db_ok":true}` ✅
- Frontend `https://carotis.diggai.de/` im Browser: leer/weiß, HTTP 502 ❌

### Caddy Health-Check-False-Alarm
- Container `deploy-caddy-1` zeigt `unhealthy` in `docker ps`
- Ursache: Health-Check nutzt `curl`, aber `curl` nicht im Caddy-Container vorhanden
- Backend funktioniert trotzdem korrekt (HTTPS läuft, Cert via ACME/Let's Encrypt erhalten)

## Surprised by

- **Fly.io Trial abgelaufen**: Frontend 502, weil Fly.io-Trial ended → needs credit card at https://fly.io/trial
- **SSH known_hosts veraltet**: Nach Rescue-Mode-Reboot hat sich der Host-Key geändert → `ssh-keygen -R 204.168.230.127` nötig
- **generate_rohde_token.py nicht im Container**: Die Scripts wurden nicht via rsync in den Container kopiert. Workaround: temp script via `scp` + `docker cp`
- **Backend Docs 404**: `/docs` nicht verfügbar (wahrscheinlich im Production-Mode deaktiviert)

## Avoided

- Kein Rescue-Mode mehr aktiviert (Server läuft normal)
- Kein Git-Push mit Secrets
- Kein Überschreiben bestehender authorized_keys (append-only)

## Next

1. **KRITISCH — Fly.io Billing**: Kreditkarte unter https://fly.io/trial hinterlegen, dann `gh workflow run deploy-frontend-fly.yml --repo DiggAiHH/CarotisAi --ref master`
2. **Caddy Health Check fixen**: `docker-compose.yml` health check von `curl` auf `wget` oder `nc` umstellen (curl nicht im Image)
3. **Backend CI Health Check**: `deploy-backend-hetzner.yml` health check Timeout erhöhen (Caddy braucht ~10s für ACME-Cert)
4. **Demo-Token sicher weiterleiten**: Token `EKZmnbk-Y-N-xQlSXOZdYIMsOoKwJUe-NdOEHSj6ed4` an Prof. Rohde via verschlüsselter Mail
5. **Scripts in Deploy-Sync aufnehmen**: `code/scripts/` zu rsync-Pfaden in `deploy-backend-hetzner.yml` hinzufügen

## Memory updates

- MEMORY.md mit Pointer auf diesen Run aktualisieren
- Known credentials: Deploy-Key `deploy/hetzner_deploy_key`, Server `204.168.230.127`
- Token-Generation-Workaround via `scp` + `docker cp` dokumentiert
