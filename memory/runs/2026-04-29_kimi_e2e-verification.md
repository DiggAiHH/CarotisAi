---
name: 2026-04-29_kimi_e2e-verification
type: run
---

## Goal
End-to-End-Verifikation nach K-01..K-16: pytest + Frontend-Typecheck + Docker-Smoke.

## Done
- Backend: 22/24 Tests passed (2 ML-Deps `mlflow`/`torch` fehlen — erwartet)
- Frontend: `tsc --noEmit` 0 errors
- 13 Bugs gefixt während Verifikation (Import-Fehler, Schema-Validierung, DB-Isolation, Mock-Await, Pydantic-Namespace, Enum-Werte, Unicode-Encoding)
- `requirements.txt` mit `jsonschema` + relaxierten Versionen aktualisiert

## Surprised by
`dependencies.py` hat `settings = get_settings()` beim Modul-Import gecacht — alle Tests mit wechselndem API_KEY failen. Fix: `get_settings()` inline in Funktionen aufrufen.

## Avoided
Keine Quick-Fixes in Produktionscode ohne Test-Abdeckung; alle Änderungen durch pytest validiert.

## Next
- Docker Desktop starten für `docker compose up -d`
- `ml/requirements.txt` installieren für ML-Test-Green
- Run-Log-Zeile in `MEMORY.md` ergänzen

## Memory updates
- `backend/app/api/dependencies.py` — niemals Settings beim Modul-Import cachen.
- `backend/app/db/models.py` — `SQLEnum` braucht `values_callable` für String-Werte in DB.
- `tests/conftest.py` — `engine.begin() + drop_all` vor `init_db()` für saubere DB-Isolation.
