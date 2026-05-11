# Pre-Deploy Checklist — Carotis-AI P0f

> Letzte Pruefung vor dem ersten Production-Deploy. Jeder Punkt muss abgehakt sein.
> Sign-Off: Lou ___________  Datum: ___________

---

## 1. Secrets & Zugang

- [ ] `FLY_API_TOKEN` in GitHub Secrets gesetzt (rotated, nicht kompromittiert)
- [ ] `HETZNER_SSH_PRIVATE_KEY` in GitHub Secrets gesetzt
- [ ] `HETZNER_SERVER_IP` in GitHub Secrets gesetzt (204.168.230.127)
- [ ] `HETZNER_SSH_USER` in GitHub Secrets gesetzt
- [ ] `ACME_EMAIL` in GitHub Secrets gesetzt
- [ ] `API_KEY` in GitHub Secrets gesetzt (>= 32 Zeichen)
- [ ] `ADMIN_API_KEY` in GitHub Secrets gesetzt (>= 32 Zeichen, != API_KEY)
- [ ] `ANONYMIZATION_SALT` in GitHub Secrets gesetzt (>= 16 Zeichen)
- [ ] `.env` auf Hetzner manuell geprueft (keine Hardcoded Secrets)

## 2. DNS & Domains

- [ ] `carotis.diggai.de` → CNAME `carotis-ai-frontend.fly.dev` (INWX)
- [ ] `api.carotis.diggai.de` → A `204.168.230.127` (INWX)
- [ ] DNS-Propagation geprueft (`nslookup carotis.diggai.de`, `nslookup api.carotis.diggai.de`)
- [ ] SSL-Zertifikat Fly: `fly certs show carotis.diggai.de`
- [ ] SSL-Zertifikat Hetzner: Caddy holt TLS via Let's Encrypt

## 3. Infrastruktur

- [ ] Hetzner-Server: Docker + Docker Compose installiert
- [ ] Hetzner-Server: `/opt/carotis-ai` Verzeichnis angelegt
- [ ] Hetzner-Server: SSH-Key `deploy/hetzner_deploy_key.pub` in `~/.ssh/authorized_keys`
- [ ] Hetzner-Server: UFW/Firewall erlaubt 80, 443, 22
- [ ] Fly.io: App `carotis-ai-frontend` existiert
- [ ] Fly.io: `deploy/fly.frontend.toml` ist gueltig

## 4. CI/CD

- [ ] `.github/workflows/ci.yml` laeuft gruen auf `master`
  - lint: ruff + black + bandit + frontend lint/typecheck
  - test-backend: pytest 123 passed, 11 skipped
  - test-mcp: MCP smoke tests 16 PASS, 2 WARN (soft)
  - test-frontend: vitest 29 passed
- [ ] `.github/workflows/deploy-frontend-fly.yml` laeuft gruen
- [ ] `.github/workflows/deploy-backend-hetzner.yml` laeuft gruen
- [ ] Deploy-Workflows haben Health-Checks
- [ ] Rollback-Verfahren dokumentiert (vorheriger Git-Commit)
- [ ] `deploy/autopilot_preflight.ps1` ausgefuehrt (Exit Code 0)

## 5. Backend-Checks

- [ ] `pytest tests/` → 123 passed, 11 skipped (torch/transformers SKIPPED — erwartet)
- [ ] `ruff check backend/app tests` → 0 Errors
- [ ] `black --check backend/app tests` → 0 Changes
- [ ] `bandit -r backend/app -ll` → keine High-Severity Issues
- [ ] Optional: `pytest ml/` in ML-venv (mit `torch` + `mlflow`)
- [ ] `/health/` Endpoint antwortet mit 200
- [ ] `/api/v1/demo/whoami` mit Token antwortet mit 200
- [ ] Rate-Limiting aktiv (30/Min Inference, 60/Min Decision-Tree)
- [ ] `/metrics` erfordert Admin-Key
- [ ] Security Headers aktiv (CSP, HSTS, X-Frame-Options)
- [ ] Gzip Compression aktiv
- [ ] ONNX-Modell existiert in `/data/models/mfsd_unet.onnx`

## 6. Frontend-Checks

- [ ] `npm run typecheck` → 0 Errors
- [ ] `npm test -- --run` → 29 passed
- [ ] `npm run lint` → 0 Errors
- [ ] `npm run build` → SUCCESS
- [ ] Keine `window.alert()` mehr im Code
- [ ] Error Boundary aktiv
- [ ] apiClient hat Timeout + Retry
- [ ] Bundle-Report existiert (`npm run analyze`)

## 7. Security

- [ ] Keine Secrets im Repo (`.gitignore` pruefen)
- [ ] `deploy/hetzner_deploy_key` nicht committed
- [ ] `deploy/hetzner_deploy_key.pub` nicht committed
- [ ] Keine `.env` Dateien committed
- [ ] CORS erlaubt nur `https://carotis.diggai.de`
- [ ] SQLite ist einzige DB (keine PostgreSQL/MySQL)
- [ ] DICOM-Anonymisierung aktiv (33 PII-Tags)

## 8. Demo-Readiness

- [ ] Rohde-Token generiert und in DB gespeichert
- [ ] Demo-Daten (30 Cases) generiert
- [ ] Walkthrough funktioniert (5 Schritte)
- [ ] i18n alle Strings uebersetzt
- [ ] Stride V3 Prompts erstellt (W-07, W-08, W-09, W-10)

## 9. Monitoring & Logging

- [ ] Structlog JSON-Format in Produktion
- [ ] Audit-Trail append-only
- [ ] Container-Logs rotieren (Docker default)
- [ ] Health-Check Endpoints erreichbar

## 10. Rollback-Plan

- [ ] Vorheriger Commit auf `master` ist stabil
- [ ] Rollback-Befehl dokumentiert:

```bash
git revert HEAD
git push origin master
```

- [ ] Hetzner: `docker compose -f hetzner-backend.compose.yml down` funktioniert
- [ ] Fly: `flyctl deploy --config deploy/fly.frontend.toml --remote-only --image previous` getestet

---

## Verifikations-Befehle

```bash
# Frontend
curl -i https://carotis.diggai.de/robots.txt

# Backend Health
curl -i https://api.carotis.diggai.de/health/

# Backend Auth
curl -i -H "X-Demo-Token: <YOUR_DEMO_TOKEN>" \
  https://api.carotis.diggai.de/api/v1/demo/whoami

# Backend Rate-Limit (sollte 429 nach 30 Requests)
# Bash:
for i in {1..35}; do curl -s -o /dev/null -w "%{http_code}\n" \
  -H "X-Demo-Token: TOKEN" https://api.carotis.diggai.de/api/v1/demo/whoami; done

# PowerShell:
1..35 | ForEach-Object {
  curl.exe -s -o NUL -w "%{http_code}`n" -H "X-Demo-Token: TOKEN" "https://api.carotis.diggai.de/api/v1/demo/whoami"
}

# Metrics (sollte 401 ohne Admin-Key)
curl -i https://api.carotis.diggai.de/metrics

# Metrics mit Admin-Key (sollte 200)
curl -i -H "X-Admin-Key: ADMIN_KEY" https://api.carotis.diggai.de/metrics
```

---

**Sign-Off:**

| Rolle | Name | Datum | Unterschrift |
| ----- | ---- | ----- | ----------- |
| Technical Lead | Lou (Laith Alshdaifat) | | |
| Medical Lead | Dr. Aroob Alrawashdeh | | |
| Agent-Verifizierung | Kimi/Codex/Claude | | |
