# Opus 4.7 Handoff — Carotis Deploy + Agent Harness

Stand: 2026-05-01, Codex GPT-5.5

## Ziel

Opus 4.7 soll den P0f-Plan mit dem aktuellen Repo- und Deployment-Stand aktualisieren. Architektur ist jetzt:

- Frontend: Fly.io, Domain `carotis.diggai.de`
- Backend/API: Hetzner CX23, IP `204.168.230.127`, Domain `api.carotis.diggai.de`
- Kein Netlify/Render fuer diesen Pfad.
- Keine echten Patientendaten in Cloud-Demo. Demo-Daten/Token-Gate only.

## Im aktuellen Repo-Stand vorhanden/gesichert

1. Backend-Hetzner-Workflow robuster gemacht:
   - `.github/workflows/deploy-backend-hetzner.yml`
   - installiert `rsync` auf dem GitHub Runner
   - bereitet Hetzner-Host per SSH vor: Docker, Compose Plugin, rsync, curl
   - erstellt deterministische Remote-Pfade:
     - `/opt/carotis-ai/backend`
     - `/opt/carotis-ai/deploy`
     - `/opt/carotis-ai/data/models`
   - synchronisiert Backend, Deploy-Dateien und Demo-Modelle getrennt
   - triggert jetzt auch bei `code/data/models/**`

2. Hetzner-Compose-Pfad korrigiert:
   - `deploy/hetzner-backend.compose.yml`
   - Build-Kontext ist jetzt `../backend`, passend zum Remote-Ziel `/opt/carotis-ai/backend`
   - `/opt/carotis-ai/data` wird als Host-Bind nach `/data` gemountet
   - dadurch bleiben SQLite und Demo-ONNX-Modell persistent und sichtbar
   - Caddy-Healthcheck nutzt Host-Header `api.carotis.diggai.de` und `/health/`

3. Frontend-Fly-Workflow bereinigt:
   - `.github/workflows/deploy-frontend-fly.yml`
   - der alte Failure-Step hiess Rollback, deployte aber nur erneut
   - jetzt gibt er bei Fehlern Fly-Releases aus statt einen zweiten Deploy zu starten

## Verifiziert

- `docker compose -f deploy/hetzner-backend.compose.yml config --quiet` mit Dummy-Env: OK
- Workflow-Dateien haben keine Tabs.
- GitHub Secrets wurden nur nach Namen geprueft, keine Secret-Werte ausgegeben.
- `ANONYMIZATION_SALT` wurde am 2026-05-01 als neuer starker Zufallswert in GitHub Secrets gesetzt.

## Aktuelle externe Blocker

Diese Punkte sind nicht im Repo loesbar und muessen ueber Dashboard/Serverzugang erledigt werden:

1. GitHub Secret `FLY_API_TOKEN` fehlt.
   - `gh secret list --repo DiggAiHH/CarotisAi` zeigte es nicht.
   - Alten Fly-Token revoken, neuen erzeugen, als `FLY_API_TOKEN` setzen.

2. Hetzner SSH ist noch blockiert.
   - Test: `ssh -i deploy\hetzner_deploy_key ... root@204.168.230.127 "echo ok"`
   - Ergebnis: `Permission denied (publickey,password)`.
   - Public Key aus `deploy/hetzner_deploy_key.pub` muss in `/root/.ssh/authorized_keys`.

3. DNS zeigt noch falsch.
   - `api.carotis.diggai.de` -> `75.2.60.5`
   - `carotis.diggai.de` -> `75.2.60.5`
   - Soll:
     - `api.carotis` A `204.168.230.127`
     - `carotis` CNAME oder Fly-kompatibler Record fuer `carotis-ai-frontend.fly.dev`

4. Fly-App/Custom-Domain muss nach Token-Setup erstellt werden.
   - App: `carotis-ai-frontend`
   - Domain: `carotis.diggai.de`
   - Region: `fra`

## GitHub Secrets Ist-Stand

Vorhanden:

- `ACME_EMAIL`
- `ADMIN_API_KEY`
- `ANONYMIZATION_SALT`
- `API_KEY`
- `CAROTISAI` (unklarer Alt-/Sondersecret)
- `HETZNER_SERVER_IP`
- `HETZNER_SSH_PRIVATE_KEY`
- `HETZNER_SSH_USER`

Fehlt nach letztem Check:

- `FLY_API_TOKEN`

## Naechste Schritte nach Entsperrung

Nach Setzen von Secrets, SSH-Key und DNS:

```powershell
gh secret list --repo DiggAiHH/CarotisAi
ssh -i deploy\hetzner_deploy_key -o BatchMode=yes root@204.168.230.127 "echo ok"
Resolve-DnsName api.carotis.diggai.de
Resolve-DnsName carotis.diggai.de
```

Wenn alles stimmt:

```powershell
gh workflow run deploy-backend-hetzner.yml --repo DiggAiHH/CarotisAi --ref master
gh workflow run deploy-frontend-fly.yml --repo DiggAiHH/CarotisAi --ref master
gh run list --repo DiggAiHH/CarotisAi --limit 5
```

Smoke danach:

```powershell
curl.exe -fsS https://api.carotis.diggai.de/health/
curl.exe -fsS https://carotis.diggai.de/robots.txt
```

## Plan-Update fuer Opus 4.7

Bitte P0f-Plan aktualisieren:

- Deployment ist repo-seitig vorbereitet, aber noch nicht live.
- Kritischer Pfad ist nicht mehr Code, sondern Secret/DNS/SSH/Fly-App-Freischaltung.
- Danach nur noch Workflow-Run + Smoke-Test.
- Separat bleiben Code-Anomalien aus `AGENTS.md` offen: AuditService-Duplikate, Models-Duplikate, Frontend-Tests, Cornerstone3D.
- Deploy-PR/Branch muss nach Review nach `master`, weil beide Deploy-Workflows nur auf `master` push automatisch laufen.
