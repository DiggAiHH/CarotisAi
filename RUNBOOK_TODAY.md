# RUNBOOK_TODAY - Was Lou jetzt tut

> Stand: 2026-05-04. Die alten Stride-v2-Schritte sind erledigt. Diese Datei zeigt nur noch den aktuellen P0f-Pfad.

## Ziel von heute

Rohde-Paket versandbereit halten und die Live-Demo unblocken. Keine echten Patientendaten verwenden.

## Fertig

- Office-Docs v2 liegen in `Stride V2/`.
- V3-Mail-/Office-Prompts liegen in `Stride V3/`.
- Rohde-Video-Skript liegt in `outputs/Rohde_Video_Script_v1.md`.
- Pre-Send-Smoke-Runbook liegt in `deploy/runbook_pre_send.md`.
- Rohde-E2E-Test ist gruen: 7 passed.
- Hauptdomain ist online: `https://carotis.diggai.de/` liefert 200.
- Hetzner-Fallback/API ist online: `https://api.carotis.diggai.de/` und `/health/` liefern 200.
- Caddy auf Hetzner ist healthy und bedient `api.carotis.diggai.de` und `carotis.diggai.de`.

## Jetzt

1. `deploy/runbook_pre_send.md` oeffnen.
2. Live-Smoke pruefen:
   - `Resolve-DnsName carotis.diggai.de`
   - `curl https://carotis.diggai.de/`
   - `curl https://api.carotis.diggai.de/health/`
3. Live-Smoke anhand `deploy/runbook_pre_send.md` durchgehen.
4. Aroob final reviewen lassen.
5. Mail v3 senden.

## Bei Deploy-/Online-Prompts

Wenn Lou "mach online", "Deploy", "carotis erreichbar machen", "DNS fixen" oder aehnlich sagt:

1. `memory/domain/p0f_deploy_state_compact_2026-05-02.md` lesen.
2. `memory/runs/2026-05-04_Codex_GPT55-Run15_dns_hetzner_proxy.md` lesen.
3. Serverstatus ueber `api.carotis.diggai.de/health/` pruefen.
4. INWX-Hauptdomain nur dann anfassen, wenn User explizit Schreib-Go gibt oder selbst die UI bedient.

## Nicht Jetzt

- Keine P1/P2/P3 klinische Datenarbeit vor Rohde-Go.
- Keine echten DICOMs in Browser, Cloud, GitHub, Fly oder Hetzner-Demo.
- Keine Office-Dokumente direkt durch Modelle editieren.

## Wenn Rohde Antwortet

`memory/runs/2026-04-30_t012_rohde_reply_kit.md` nutzen und Rohdes Originalantwort als Kontext geben.
