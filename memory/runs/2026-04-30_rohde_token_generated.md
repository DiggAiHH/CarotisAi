---
date: 2026-04-30
model: kimi
session: rohde-token-generation
---

## Goal
Demo-Token fuer Prof. Rohde generieren und in DB speichern.

## Done
- Token generiert (32-Byte URL-safe)
- SHA-256 Hash in SQLite DB `demo_tokens` eingefuegt
- Label: "Prof. Rohde P0f Demo"
- Expires: 2026-05-30 (30 Tage)
- Max requests: 50
- rohde_tag: true
- Token-Hash: 83d532993c20ea55...

## Token-Verteilung
- Raw-Token wurde an Lou uebergeben (nicht im Log aus Sicherheitsgruenden)
- Token wird in Mail v3 + Rohde-Anleitung eingesetzt

## Verify
```bash
curl -H "X-Demo-Token: <RAW_TOKEN>" http://localhost:8000/api/v1/demo/whoami
```

## Next
- Token in Mail v3 einsetzen (W-09)
- Token in Rohde-Anleitung einsetzen (W-07)
