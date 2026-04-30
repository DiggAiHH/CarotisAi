# Carotis-AI Demo Deployment

Production-ready deployment configuration for `app.carotis.diggai.de`.

## Prerequisites

- Docker + Docker Compose
- Domain `app.carotis.diggai.de` pointing to server IP
- `.env` file with `API_KEY` (≥32 chars)

## Quick Start

```bash
cd code/frontend
npm ci
npm run build

cd ../..
docker compose -f docker-compose.yml -f deploy/docker-compose.demo.yml up -d --build
```

## Generate Rohde Token

```bash
cd code
python scripts/generate_rohde_token.py --label "Rohde P0f Demo"
```

Copy the RAW token and send it via encrypted channel.

## Verify Deployment

```bash
curl -H "X-Demo-Token: <token>" http://app.carotis.diggai.de/api/v1/health/
```

## Architecture

```
User → Caddy (:443) → Frontend (nginx) + Backend (:8000)
              ↓
         SQLite (/data)
```

- Caddy handles TLS, security headers, and API proxying
- Frontend is static build served by nginx
- Backend runs FastAPI with demo-token auth
- No patient data ever leaves the server
