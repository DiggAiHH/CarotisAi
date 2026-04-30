# Carotis-AI Clean Repo + Deploy Handoff

Stand: 2026-04-30, aktualisiert durch Codex nach `go weiter`.

## Critical Security Note

The Fly token and a GitHub token were exposed in chat / local remote config.
Treat both as compromised.

Do this before any deploy:

1. Fly.io: revoke the exposed Fly token and create a new deploy token.
2. GitHub: revoke the exposed personal access token and create a new one only if needed.
3. Never paste raw tokens into chat again. Put them directly into GitHub Secrets.

## Clean Repo State

The Carotis workspace now has its own local `.git` repository at:

```text
c:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI
```

The unsafe token-bearing local `origin` remote was removed. A clean remote is now configured:

```text
origin https://github.com/DiggAiHH/CarotisAi.git
```

Current target:

- Branch: `master`
- GitHub repo: `DiggAiHH/CarotisAi`
- Default branch: `master`
- Current `origin/master`: synced as of 2026-04-30.

## Correct Deployment Architecture

Lou corrected the architecture:

- Frontend: Fly.io
- Backend: Hetzner
- Domain root: `diggai.de`

Recommended DNS:

| Host | Target | Purpose |
|---|---|---|
| `carotis.diggai.de` | Fly.io frontend app | React demo frontend |
| `api.carotis.diggai.de` | Hetzner server `204.168.230.127` | FastAPI backend |

Avoid using the existing Anamnese backend path for Carotis. Keep the Docker Compose project and folder separate:

```text
/opt/carotis-ai
```

## Prepared Files

Frontend on Fly.io:

- `deploy/Dockerfile.frontend-fly`
- `deploy/nginx.frontend-fly.conf`
- `deploy/fly.frontend.toml`
- `.github/workflows/deploy-frontend-fly.yml`

Backend on Hetzner:

- `deploy/hetzner-backend.compose.yml`
- `deploy/Caddyfile.backend`
- `deploy/Dockerfile.caddy`
- `.github/workflows/deploy-backend-hetzner.yml`

Existing W-02 demo auth/backend files remain in place:

- `code/backend/app/core/security.py`
- `code/backend/app/db/models.py`
- `code/backend/app/api/routes/demo.py`
- `code/tests/test_demo_token.py`

## GitHub Secrets Required

GitHub Secrets status:

```text
DONE: HETZNER_SERVER_IP=204.168.230.127
DONE: HETZNER_SSH_USER=root
DONE: ACME_EMAIL=<set in GitHub Secrets>
DONE: API_KEY=<generated 64 hex chars, set in GitHub Secrets>
DONE: ADMIN_API_KEY=<generated 64 hex chars, set in GitHub Secrets>
TODO: FLY_API_TOKEN=<new rotated Fly deploy token>
TODO: HETZNER_SSH_PRIVATE_KEY=<private SSH key that can deploy to Hetzner>
```

Do not use the leaked Fly token from chat.

## DNS Required in INWX

Create:

```text
api.carotis.diggai.de  A      204.168.230.127
carotis.diggai.de      CNAME  <Fly hostname from fly certs/show>
```

If Fly requires A/AAAA instead of CNAME for your setup, use the records shown by:

```bash
fly certs create carotis.diggai.de --config deploy/fly.frontend.toml
fly certs show carotis.diggai.de --config deploy/fly.frontend.toml
```

## Manual Stop Points

I cannot complete these without your authenticated browser / provider sessions:

1. Revoke and rotate the exposed Fly token.
2. Add the new `FLY_API_TOKEN` to GitHub Secrets.
3. Add `HETZNER_SSH_PRIVATE_KEY` to GitHub Secrets.
4. Add INWX DNS records.
5. Confirm SSH access to Hetzner.

After those are done, say `go`.

## Deploy Commands After Secrets Are In Place

Frontend:

```bash
fly apps create carotis-ai-frontend --org personal
fly certs create carotis.diggai.de --config deploy/fly.frontend.toml
git push origin master
```

Backend first-time Hetzner prep:

```bash
ssh root@204.168.230.127
mkdir -p /opt/carotis-ai
apt-get update
apt-get install -y docker.io docker-compose-plugin rsync
```

Then push to `master`; GitHub Actions deploys backend over SSH.

## Verification

```bash
curl -i https://carotis.diggai.de/robots.txt
curl -i https://api.carotis.diggai.de/health/
curl -i -H "X-Demo-Token: <raw-demo-token>" https://api.carotis.diggai.de/api/v1/demo/whoami
```

