---
name: 2026-04-30_opus47_p0f_aligned
type: run
to: kimi-k2.6 + codex-5.5 + lou + aroob
session: P0f Alignment nach Codex-Repo-Cleanup
---

## Goal
Plan auf neuen Stand bringen nachdem Codex GPT-5.5 das Repo aufgeraeumt hat (`DiggAiHH/CarotisAi` master, Token-Leak entfernt) und die Architektur korrigiert hat (Frontend Fly + Backend Hetzner statt Cloudflare Pages + Hetzner). Aroob in den Loop holen. Next-Run-Prompt fuer Deploy-Unblock vorbereiten.

## Done
- REPO_CLEANUP_AND_DEPLOY_HANDOFF.md, ULTRAPLAN.md, codex_clean_repo_handoff.md gelesen.
- CLAUDE.md Phase-Status auf v1.5 aktualisiert: P0f Deploy-Blocker explizit benannt (FLY_API_TOKEN, Hetzner-SSH-authorized_keys, INWX-DNS, flyctl-Install).
- MEMORY.md mit Pointern auf REPO_CLEANUP_AND_DEPLOY_HANDOFF, ULTRAPLAN, Aroob-Briefing, neuen Prompt v2 erweitert.
- Aroob-Briefing geschrieben: `outputs/Aroob_Status_Briefing_v1.md` — nicht-technische 1-Pager + FAQ-Spickzettel falls Rohde unangemeldet anruft.
- Next-Run-Prompt: `kimi_codex_prompt_p0f_unblock_ready.md` mit 8 Unblock-Wellen U-01..U-08.

## Surprised by
Codex hat einen GitHub-PAT und Fly-Token aus alter Remote-Config bzw. Chat als kompromittiert markiert — beide muessen sofort rotiert werden. Architektur-Korrektur (Fly statt Cloudflare Pages) macht v1 des Prompt-Files (`kimi_prompt_p0f_pivot_ready.md`) teilweise stale. v2 ist `kimi_codex_prompt_p0f_unblock_ready.md`.

## Avoided
- Keine Secrets in Memory geschrieben oder geprintet (HARD RULE).
- Keine Provider-Aktion ohne Lou-Sichtkontakt — Fly/INWX/Hetzner-Console bleiben fuer Lou.
- Keine Reuse des kompromittierten Fly-Tokens.
- Keine Modifikation an deploy/* oder .github/workflows/* — Codex ist Owner, ich aligne nur den Plan.

## Plan-Delta gegenueber v1

| Was | Alt (v1) | Neu (v2 — durch Codex) |
|-----|----------|------------------------|
| Frontend-Hosting | Cloudflare Pages | **Fly.io** `carotis-ai-frontend.fly.dev` |
| Backend-Hosting | Hetzner | Hetzner `204.168.230.127:/opt/carotis-ai` (unveraendert) |
| Domain Frontend | `carotis.diggai.de` (CNAME-CF) | `carotis.diggai.de` (CNAME-Fly) |
| Domain Backend | `app.carotis.diggai.de` | `api.carotis.diggai.de` |
| Repo | nicht spezifiziert | `https://github.com/DiggAiHH/CarotisAi.git` master |
| Public Landing (W-01) | static HTML in `code/website/` | DEFERRED: erst React-App auf Fly, Landing kann spaeter als Marketing-Page kommen |
| Deploy-Pipeline | Caddy single-box | GitHub Actions → Fly + Hetzner-SSH |
| Auth-Gate (W-02) | Caddy basicauth | Bestehende W-02-Demo-Token-Auth (security.py + DemoToken-Tabelle + demo.py routes) |

## Aktuelle Blocker-Liste (Lou Manual)

```
B-1: Fly-Token rotieren
  - alten Token in Fly.io revoken
  - neuen Token erzeugen
  - GitHub Secret FLY_API_TOKEN setzen
  - Token NIE wieder in Chat oder Datei

B-2: Hetzner-SSH-Authorized
  - deploy/hetzner_deploy_key.pub Inhalt
  - in /root/.ssh/authorized_keys auf 204.168.230.127 eintragen
  - Lokal testen: ssh -i deploy/hetzner_deploy_key root@204.168.230.127

B-3: INWX-DNS
  - api.carotis.diggai.de  A      204.168.230.127
  - carotis.diggai.de      CNAME  carotis-ai-frontend.fly.dev
  - TTL 300

B-4: flyctl optional
  - Entweder lokal installieren: iwr https://fly.io/install.ps1 -useb | iex
  - ODER: nur via GitHub Actions deployen
```

## Memory updates
- CLAUDE.md auf v1.5
- MEMORY.md erweitert um Codex-Run, Aroob-Briefing, ULTRAPLAN, REPO_CLEANUP-Pointer und v2-Prompt
- 3 neue Top-Level-Datei-Pointer

## Next
1. Lou loest B-1..B-3 manuell (Browser/SSH).
2. Lou sagt `go` — dann Codex GPT-5.5 fuehrt U-01..U-04 aus (Workflow-Trigger via gh actions).
3. Verifikation U-05..U-06: curl-Smoke gegen carotis.diggai.de + api.carotis.diggai.de.
4. U-07: Walkthrough-Mode + i18n-DE-Audit (Kimi K2.6 — disjunkte Frontend-Pfade).
5. U-08: Rohde-Token + Mail v3 Stride-Prompt (Opus 4.7).
6. Lou + Aroob lesen Aroob_Status_Briefing_v1.md gemeinsam, klaeren ob Aroob mit FAQ-Spickzettel ok ist.
