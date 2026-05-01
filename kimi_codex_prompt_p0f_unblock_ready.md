# P0f v2 — Deploy-Unblock Prompts (Kimi K2.6 + Codex GPT-5.5 + Opus 4.7)

> **Stand:** 2026-04-30 · **Refs:** REPO_CLEANUP_AND_DEPLOY_HANDOFF.md, ULTRAPLAN.md, `memory/runs/2026-04-30_codex_clean_repo_handoff.md`, `memory/runs/2026-04-30_opus47_p0f_aligned.md`
>
> **Ziel:** P0f abschliessen — Demo lauffaehig unter `carotis.diggai.de` (Fly) und `api.carotis.diggai.de` (Hetzner), Mail v3 mit Live-Link versendet.
>
> **Architektur (final):** Frontend Fly.io · Backend Hetzner 204.168.230.127:/opt/carotis-ai · DNS via INWX
>
> **Repo:** `https://github.com/DiggAiHH/CarotisAi.git` master · **Pre-Flight:** ULTRAPLAN.md Sektion 2

---

## Manuelle Vorarbeit (nur Lou — kein Modell)

**Diese 4 Schritte muss Lou selbst durchziehen, bevor U-01 startet. Kein Agent kann das.**

### M-1 — Fly-Token rotieren
```text
1. Browser: https://fly.io/dashboard/personal/tokens
2. Alten Token revoken (der im Chat war)
3. "Create access token" → Name: "carotis-deploy-2026-04-30"
4. Token kopieren — nicht im Chat oder Datei!
5. Browser: https://github.com/DiggAiHH/CarotisAi/settings/secrets/actions
6. Secret "FLY_API_TOKEN" anlegen mit dem neuen Token
7. Token aus Zwischenablage loeschen (Win+V → Clear all)
```

### M-2 — Hetzner-SSH-Key autorisieren
```powershell
# Public-Key Inhalt anzeigen
Get-Content "deploy/hetzner_deploy_key.pub"

# Auf den Hetzner-Server zugreifen (egal wie — Web-Console wenn SSH nicht geht)
# https://console.hetzner.cloud/projects → Server → Console
# Login als root mit existierendem Passwort

# Public Key in authorized_keys eintragen
mkdir -p /root/.ssh
chmod 700 /root/.ssh
echo "<INHALT_VON_OBEN>" >> /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys

# Lokal verifizieren:
ssh -i deploy/hetzner_deploy_key root@204.168.230.127 "uptime"
```

### M-3 — INWX DNS setzen
```text
1. Browser: https://www.inwx.de/de/customer/domain
2. diggai.de → Nameserver → DNS
3. Neuer Eintrag: api.carotis  Type A     Value 204.168.230.127  TTL 300
4. Neuer Eintrag: carotis      Type CNAME Value carotis-ai-frontend.fly.dev  TTL 300

(Falls Fly nach App-Erstellung andere Records will, kommen die in U-02.)
```

### M-4 — Hetzner-Server vorbereiten
```bash
ssh root@204.168.230.127

# einmalige Vorbereitung
apt-get update
apt-get install -y docker.io docker-compose-plugin rsync
mkdir -p /opt/carotis-ai
exit
```

**Nach M-1..M-4:** Lou sagt `go` im Chat → Codex startet U-01.

---

## Welle U — Deploy + Smoke

### U-01 — Fly Frontend App + Cert anlegen (Codex GPT-5.5)

**Pre-Flight:** ULTRAPLAN.md Sektion 2, REPO_CLEANUP_AND_DEPLOY_HANDOFF.md, `deploy/fly.frontend.toml`.

**Prompt:**
```text
Du bist Codex GPT-5.5. Pre-Flight strikt nach ULTRAPLAN.md Sektion 2.

Aufgabe U-01: Fly-App "carotis-ai-frontend" anlegen + Custom-Domain-Cert.

Voraussetzungen (von Lou bestaetigt):
- M-1 done: FLY_API_TOKEN gesetzt
- M-3 done: DNS-CNAME gesetzt
- flyctl installiert ODER Action verwenden

Vorgehen Pfad A (flyctl lokal):
  fly auth login
  fly apps create carotis-ai-frontend --org personal
  fly certs create carotis.diggai.de --config deploy/fly.frontend.toml --app carotis-ai-frontend
  fly certs show carotis.diggai.de --config deploy/fly.frontend.toml --app carotis-ai-frontend
  -> Output protokollieren in run-log

Vorgehen Pfad B (GitHub Actions):
  Falls flyctl fehlt:
  - Workflow .github/workflows/deploy-frontend-fly.yml triggern via:
    gh workflow run deploy-frontend-fly.yml --repo DiggAiHH/CarotisAi --ref master
  - Logs lesen: gh run list --workflow=deploy-frontend-fly.yml --repo DiggAiHH/CarotisAi
  - Nach Erfolg: gh run view <run-id> --log

DoD:
- Fly-App existiert
- Cert "carotis.diggai.de" hat Status "ready" (oder "awaiting cname" wenn DNS noch nicht propagiert)
- Erste deployte Version laeuft (curl -i https://carotis.diggai.de gibt 200 oder 308)

Fehlerfaelle (stoppen, nicht raten):
- Token ungueltig → Lou rotiert nochmal
- DNS nicht propagiert → 5 Minuten warten, dann erneut
- Cert "needs CNAME" Konflikt → Output zeigen, Lou aendert DNS

Run-Log: memory/runs/2026-04-30_Codex_GPT55-Run04_fly_frontend_deploy.md (ULTRAPLAN-Format)
```

---

### U-02 — Hetzner Backend Deploy (Codex GPT-5.5)

**Pre-Flight:** `deploy/hetzner-backend.compose.yml`, `deploy/Caddyfile.backend`, `deploy/Dockerfile.caddy`, `.github/workflows/deploy-backend-hetzner.yml`.

**Prompt:**
```text
Du bist Codex GPT-5.5. Pre-Flight nach ULTRAPLAN.md Sektion 2.

Aufgabe U-02: Backend-Stack auf Hetzner 204.168.230.127:/opt/carotis-ai deployen.

Voraussetzungen:
- M-2 done: SSH-Key in authorized_keys
- M-3 done: DNS-A-Record api.carotis.diggai.de → 204.168.230.127
- M-4 done: Docker installiert auf Hetzner
- 6 GH-Secrets gesetzt (HETZNER_*, ACME_EMAIL, API_KEY, ADMIN_API_KEY)

Vorgehen:
  gh workflow run deploy-backend-hetzner.yml --repo DiggAiHH/CarotisAi --ref master
  gh run list --workflow=deploy-backend-hetzner.yml --repo DiggAiHH/CarotisAi
  gh run view <id> --log

Workflow erwartet:
  rsync deploy/ + code/ → root@204.168.230.127:/opt/carotis-ai
  ssh: docker compose -f hetzner-backend.compose.yml pull
  ssh: docker compose -f hetzner-backend.compose.yml up -d
  Caddy zieht Let's-Encrypt-Cert fuer api.carotis.diggai.de via ACME_EMAIL

DoD:
- 3 Container laufen: backend, caddy, ggf. ollama-stub
- curl -i https://api.carotis.diggai.de/health/ → 200
- curl -i -H "X-API-Key: <wrong>" https://api.carotis.diggai.de/api/v1/inference/predict → 401
- ssh root@204.168.230.127 "docker logs carotis-backend --tail 50" zeigt sauberen Start

Fehlerfaelle:
- Cert-Issue → Caddy-Logs lesen, ACME-Rate-Limit oder DNS-Propagation
- Backend startet nicht → Pydantic-Validation-Error in Logs, API_KEY zu kurz?

Run-Log: memory/runs/2026-04-30_Codex_GPT55-Run05_hetzner_backend_deploy.md
```

---

### U-03 — Demo-Token fuer Rohde generieren (Codex GPT-5.5)

**Voraussetzung:** U-02 done (Backend laeuft, DemoToken-Tabelle migriert).

**Prompt:**
```text
Du bist Codex GPT-5.5. Pre-Flight wie ueblich.

Aufgabe U-03: Personalisierten Demo-Token fuer Prof. Rohde erzeugen via SSH-Tunnel zur Hetzner-Backend.

Vorgehen:
  ssh root@204.168.230.127 "docker exec carotis-backend python scripts/generate_rohde_token.py --label rohde-2026-05-01 --max-requests 500 --expires-days 30 --output /tmp/rohde_token.txt"
  scp root@204.168.230.127:/tmp/rohde_token.txt outputs/rohde_token.local-only.txt
  ssh root@204.168.230.127 "rm /tmp/rohde_token.txt"

Sicherheits-Check:
- outputs/rohde_token.local-only.txt mit chmod 600 / Windows-Equivalent
- gitignore-Eintrag verifizieren (outputs/*.local-only.txt MUSS ignoriert sein)
- NICHT in chat ausgeben — nur dass Datei existiert

DoD:
- Token in lokaler Datei (nur Lou liest sie)
- DB-Eintrag verifizierbar via:
  ssh root@204.168.230.127 "docker exec carotis-backend python -c 'from app.db.database import get_db; ...'"
  (oder admin-api: curl -H "X-Admin-Key: <key>" https://api.carotis.diggai.de/api/v1/audit/anomalies)
- Token funktioniert:
  curl -i -H "X-Demo-Token: <raw>" https://api.carotis.diggai.de/api/v1/demo/whoami
  → liefert label und quota

Run-Log: memory/runs/2026-04-30_Codex_GPT55-Run06_rohde_token.md
```

---

### U-04 — Walkthrough-Mode + i18n-DE-Audit (Kimi K2.6)

**Disjunkt zu U-01..U-03. Kann parallel laufen.**

**Prompt:**
```text
Du bist Kimi K2.6. Pre-Flight nach ULTRAPLAN.md Sektion 2.

Aufgabe U-04: Walkthrough-Mode (5 Steps) + i18n-Dict + DE-UI-Audit.

Ownership (disjunkt):
- code/frontend/src/components/Walkthrough/ (neu)
  - Walkthrough.tsx, WalkthroughStep.tsx, useWalkthrough.ts, Walkthrough.test.tsx
- code/frontend/src/lib/i18n.ts (neu)
- code/frontend/src/lib/i18n.test.ts (neu)
- Edit der bestehenden Komponenten zu data-tour-id + t()-Aufrufe:
  - AiPanel.tsx, ConfidenceBadge.tsx, DecisionForm.tsx, FreeTextField.tsx, DicomViewer.tsx, App.tsx

Berührt NICHT: backend, deploy, .github, ml, scripts, regulatory, ethics.

Inhalt: identisch zu kimi_prompt_p0f_pivot_ready.md W-03 + W-04 (5-Step-Tour deutsche Texte; i18n.ts mit t()-Funktion).

DoD:
- npm test -- --run: 12 + 4 (Walkthrough) + 3 (i18n) = 19 passed
- npm run typecheck/lint/build alle 0
- grep auf englische UI-Strings in components leer
- Branch: feat/walkthrough-i18n
- PR gegen master mit Titel: "feat(frontend): walkthrough mode + DE i18n (U-04)"

Run-Log: memory/runs/2026-04-30_Kimi_K26-Run01_walkthrough_i18n.md
```

---

### U-05 — Demo-Daten-Erweiterung 30 Cases (Kimi K2.6)

**Disjunkt zu U-04.**

**Prompt:**
```text
Du bist Kimi K2.6. Pre-Flight wie ueblich.

Aufgabe U-05: Demo-Daten von 10 auf 30 Cases erweitern, 5 vorgespielte Decision-Trees.

Ownership (disjunkt zu U-04):
- code/scripts/generate_demo_data.py (extend)
- code/scripts/test_generate_demo_data.py (extend)
- code/data/demo/case_catalog.json (neu)

Berührt NICHT: frontend (U-04 Owner), deploy, backend/app, .github.

Inhalt: identisch zu kimi_prompt_p0f_pivot_ready.md W-05 (30 Cases mit Coverage-Matrix, 5 Decision-Tree-Beispiele).

DoD:
- pytest 107 + 4 (W-05-Tests) = 111 passed
- python scripts/generate_demo_data.py --with-decision-trees laeuft idempotent
- 30 .dcm in code/data/demo/dicom/
- case_catalog.json valide JSON

Run-Log: memory/runs/2026-04-30_Kimi_K26-Run02_demo_data_30.md
```

---

### U-06 — End-to-End Smoke-Verifikation (Codex GPT-5.5)

**Voraussetzung:** U-01..U-05 done.

**Prompt:**
```text
Du bist Codex GPT-5.5. Pre-Flight wie ueblich.

Aufgabe U-06: Komplette Demo-Pipeline testen wie Rohde sie laufen wuerde.

Smoke-Sequenz (PowerShell-kompatibel):
  curl -i https://carotis.diggai.de
  curl -i https://carotis.diggai.de/robots.txt
  curl -i https://api.carotis.diggai.de/health/
  curl -i -H "X-Demo-Token: <token-aus-U-03>" https://api.carotis.diggai.de/api/v1/demo/whoami
  curl -i -H "X-API-Key: <api-key-aus-secrets>" https://api.carotis.diggai.de/docs

Frontend-Walkthrough manuell pruefen:
  Browser: https://carotis.diggai.de?tour=1
  -> 5 Steps durchklicken
  -> einen Demo-Case auswaehlen
  -> AI-Panel laed Heatmap + Trust-Score
  -> Decision-Form abschicken
  -> in Audit-Trail (admin-key) auftauchen

E2E-Test laufen lassen:
  cd code
  $env:DEBUG="true"
  & .\.venv313\Scripts\python.exe -m pytest tests/test_rohde_walkthrough_e2e.py -v

DoD:
- Alle curls 200/308
- Walkthrough manuell durchklickbar ohne Fehler
- E2E-Test gruen
- Audit-Eintrag fuer Rohde-Token sichtbar mit label "rohde-2026-05-01"
- Screenshot von /docs + Demo-Walkthrough fuer Aroob in outputs/demo_screenshots/

Run-Log: memory/runs/2026-04-30_Codex_GPT55-Run07_e2e_smoke.md
```

---

### U-07 — Mail v3 Stride-Prompt (Opus 4.7)

**Voraussetzung:** U-01..U-06 done. Lou hat Token + Demo-URL bereit.

**Prompt:**
```text
Du bist Opus 4.7. Pre-Flight wie ueblich. Lies zusaetzlich:
- 06_ROHDE_MEETING_KIT.md (Master-Entwurf der alten Mail)
- Stride V2/Anschreiben_Aroob_an_Rohde_v2.docx
- outputs/Aroob_Status_Briefing_v1.md
- outputs/rohde_token.local-only.txt (NUR Lou — du kennst Inhalt nicht, Lou pasted in Stride-UI)

Aufgabe U-07: Generiere Stride V3 Prompt fuer Anschreiben v3.

Ownership (disjunkt):
- Stride V3/Anschreiben_Aroob_an_Rohde_v3_PROMPT.md (neu)

Berührt NICHT: irgendeine .docx direkt.

Inhalt: identisch zu kimi_prompt_p0f_pivot_ready.md W-09, aber mit Realstand:
- Live-URL: https://carotis.diggai.de
- Demo-URL: https://carotis.diggai.de?tour=1 (Tour startet automatisch)
- Token: <REPLACE_BY_LOU_FROM_outputs/rohde_token.local-only.txt>
- Anlagen: KI_Tools_Marktanalyse_v2.pdf + Carotis_AI_Konzept_v2.pdf + Rohde_Anleitung_v1.pdf + CV_Laith.pdf
- 3 Termin-Optionen aus Aroobs Kalender (Lou setzt ein)

DoD:
- Stride V3 Prompt-File existiert
- Lou kann den Inhalt 1:1 in Stride starten
- Token-Platzhalter klar markiert
- Aroob-Briefing-Hinweis: "Aroob hat das gelesen und abgesegnet, siehe outputs/Aroob_Status_Briefing_v1.md"

Run-Log: memory/runs/2026-04-30_Opus47-Run02_mail_v3_stride.md
```

---

### U-08 — Pre-Send Final-Check (Lou + Aroob)

**Manuell, kein Modell.**

```text
Pre-Send-Checklist (Lou + Aroob 30 Minuten gemeinsam):

- [ ] outputs/Aroob_Status_Briefing_v1.md gelesen, abgenickt
- [ ] 3 Termin-Optionen aus Aroobs Kalender raus
- [ ] CC-Frage geklaert (Lou im CC vs. nur Erwaehnung)
- [ ] Stride V3 Mail v3 generiert, Token eingesetzt, alle Anlagen dabei
- [ ] Mail-Vorschau: max 25 Zeilen, Sie-Form, kein "revolutionaer"
- [ ] Demo-URL klickbar (lokal getestet incognito)
- [ ] Token funktioniert (curl whoami zeigt label rohde-2026-05-01)
- [ ] Webseite Lighthouse >= 90/95 (nur Vibes — Rohde testet keine Web-Performance)
- [ ] Walkthrough vollstaendig durchklickbar
- [ ] Mail kommt von Aroobs Klinikum-Konto
- [ ] Aroob klickt Senden

Nach Versand:
- tasks.jsonl: T-001..T-009 auf done
- memory/runs/2026-05-XX_Lou_T-009_mail_sent.md mit:
  - Versand-Datum
  - Empfaenger + CC
  - Anlagen-Hash (sha256sum jeder PDF)
  - Erwartetes Antwort-Datum (+14 Tage)
- Kalender: 14-Tage-Reminder fuer Status-Update falls keine Antwort
- runs/2026-04-30_t012_rohde_reply_kit.md ist scharfgestellt fuer alle 6 Antwort-Szenarien
```

---

## Routing & Tooling Cheat Sheet

| Welle | Modell | Zeit |
|-------|--------|------|
| M-1..M-4 | Lou (Browser/SSH) | 30-60 Min |
| U-01 | Codex GPT-5.5 | 15 Min |
| U-02 | Codex GPT-5.5 | 20 Min |
| U-03 | Codex GPT-5.5 | 5 Min |
| U-04 | Kimi K2.6 (parallel) | 60 Min |
| U-05 | Kimi K2.6 (parallel) | 30 Min |
| U-06 | Codex GPT-5.5 | 20 Min |
| U-07 | Opus 4.7 | 15 Min |
| U-08 | Lou + Aroob | 30 Min |

**Total:** 3-4 Stunden konzentrierte Arbeit, verteilt auf 1-2 Tage.

---

## Verbote (aus ULTRAPLAN.md Sektion 12 + CLAUDE.md)

- Niemals Patientendaten in Cloud/Chat/Browser
- Niemals Secrets in Datei oder Chat
- Niemals direkt nach `master` pushen ohne PR (ausser explizit vom User erlaubt)
- Niemals Office-Dokument direkt editieren — nur Stride-Prompt
- Niemals den alten kompromittierten Fly-Token wiederverwenden
- Niemals Provider-Aktion vortaeuschen wenn Auth fehlt → Stop und User informieren

---

## Stop-Regeln

Sofort stoppen + Lou informieren wenn:
- Fly-Token ungueltig → Lou rotiert
- DNS noch nicht propagiert → 5 Min warten, dann erneut, dann Lou fragen
- Hetzner SSH-Permission-denied → Lou prueft authorized_keys
- Tests rot → Diff zeigen, nicht "fixen"-Heuristik
- Backend antwortet nicht → Logs zeigen, nicht raten

---

## Memory-Disziplin

Jeder Run erzeugt:
- Run-Log nach ULTRAPLAN-Format unter `memory/runs/YYYY-MM-DD_<Agent>_<Model>-RunNN_<topic>.md`
- Pointer-Zeile in MEMORY.md
- Falls neue Top-Level-Datei → MEMORY.md "Harness-Files"-Sektion

---

*Erstellt: 2026-04-30 · Modell: Opus 4.7 · Plan-Run: `memory/runs/2026-04-30_opus47_p0f_aligned.md` · Status: bereit nach M-1..M-4*
