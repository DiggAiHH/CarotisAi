---
name: 2026-05-04_Codex_GPT55-Run16_master_demo_token
type: run
agent: Codex GPT-5.5
date: 2026-05-04
---

## Goal

Einen dauerhaft nutzbaren Master-Demo-Token fuer Lou-Demos und Tests aktivieren.

## Done

- `Settings.master_demo_token_hash` in `code/backend/app/core/config.py` ergaenzt.
- `verify_demo_token()` in `code/backend/app/core/security.py` erweitert: Wenn der Hash passt, wird ein synthetischer `master-admin-demo` Token ohne DB-Whitelist, Ablauf oder Quota-Verbrauch akzeptiert.
- Der Roh-Token wurde nicht in Memory/Docs wiederholt; persistiert ist nur der SHA-256-Hash. Lou kennt den Rohwert aus dem Prompt.
- Test `test_master_demo_token_bypasses_db_quota` ergaenzt.
- Backend auf Hetzner neu gebaut und gestartet.

## Verification

- Lokal gezielt: `pytest tests/test_demo_token.py::test_master_demo_token_bypasses_db_quota tests/test_security_timing_attack.py::TestHashDemoToken -v` -> 4 passed.
- Gemeinsamer Lauf `tests/test_demo_token.py tests/test_security_timing_attack.py -v`: 16 Tests logisch passed, aber eine vorhandene aiosqlite Thread-Teardown-Warnung im alten Expiry-Test wird als Error gemeldet.
- Live: `https://api.carotis.diggai.de/health/` -> status ok.
- Live: `/api/v1/demo/whoami` mit dem Master-Demo-Token -> `label=master-admin-demo`, `requests_remaining=2147483647`.

## Safety

Der Master-Demo-Token ist nur Demo-Gate-Zugang (`X-Demo-Token`), kein `X-Admin-Key` fuer Admin-Endpunkte. Keine Patientendaten verwendet.
