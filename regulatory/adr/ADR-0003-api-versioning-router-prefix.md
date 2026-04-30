# ADR-0003: API-Versionierung via zentralem Router-Prefix `/api/v1`

| Feld | Wert |
|------|------|
| **Status** | Accepted |
| **Datum** | 2026-04-29 |
| **Autor** | Lou (Laith Alshdaifat) + Kimi K2.6 |
| **Reviewer** | — |
| **Phase** | P0a |
| **Compliance-Impact** | Nein — rein technisch |

---

## Kontext

Während der E2E-Verifikation von K-01..K-16 wurde festgestellt, dass die FastAPI-Router unterschiedliche Pfadkonventionen verwenden: `health` am Root, `/inference/predict`, `/decision-tree/capture`, `/audit/trail` ohne gemeinsames Versionierungs-Schema. Für ein medizinisches System, das über Jahre gewartet und iteriert wird, fehlt eine explizite API-Versionierung. Die Frage: Wie versionieren wir die REST-API, ohne bestehende Routen zu zerstören und ohne die Code-Organisation zu verschlechtern?

## Optionen

### Option A — Keine Versionierung (Status Quo)
- **Pro:** Keine Änderung nötig; Pfade bleiben kurz; Frontend-Code braucht keine Anpassung
- **Contra:** Kein Upgrade-Pfad für Breaking Changes; Mischung aus Root- und verschachtelten Pfaden ist inkonsistent; Klinikum-IT kann API-Changes nicht vorhersagen
- **Aufwand:** XS (nichts tun)
- **Reversibilität:** trivial — aber der technische Schuldenberg wächst

### Option B — Zentraler Prefix in `main.py` ( gewählt )
Domain-Router behalten ihre internen Prefixe (`/inference`, `/decision-tree`, `/audit`); `create_app()` setzt einen äußeren Wrapper `prefix="/api/v1"` auf `include_router()`. Health bleibt bewusst am Root (`/health`), da es von Load-Balancern und Docker-Health-Checks ohne API-Key erreichbar sein muss.
- **Pro:** Minimale Invasivität (keine Router-Dateien ändern); klare Trennung von public health vs. versionierter API; Frontend braucht nur BASE_URL + API_PREFIX
- **Contra:** Zwei Ebenen von Prefixen (`/api/v1` + `/inference`) sind für Neueinsteiger nicht intuitiv; Router-Dateien enthalten implizit nur halbe Pfade
- **Aufwand:** S
- **Reversibilität:** trivial — Prefixe in `main.py` entfernen

### Option C — Vollständige Pfade in jedem Router
Jeder Router definiert seinen kompletten Pfad selbst (`/api/v1/inference`, `/api/v1/decision-tree`, etc.); `main.py` setzt keine Prefixe.
- **Pro:** Jede Router-Datei ist selbsterklärend; kein mentales Mapping nötig
- **Contra:** Versions-String ist über alle Dateien verteilt; Upgrade auf `/api/v2` erfordert N Datei-Änderungen; Inkonsistenz-Risiko bei zukünftigen Routern
- **Aufwand:** M
- **Reversibilität:** mittel — N Dateien müssen geändert werden

## Entscheidung

Option B. Die zentrale Prefix-Setzung in `main.py` ist der Kompromiss zwischen Option A (keine Zukunftssicherheit) und Option C (hoher Wartungsaufwand). Health am Root ist bewusst: Docker-Compose-Healthchecks und Load-Balancer sollen keine API-Keys mitführen müssen.

## Konsequenzen

### Positiv
- Einfacher Upgrade-Pfad auf `/api/v2`: nur `main.py` anpassen
- Frontend hat eine zentrale `API_PREFIX`-Konstante
- Test-Suite hat konsistente `/api/v1/*` Pfade

### Negativ
- Neue Entwickler müssen wissen, dass Router-Pfade in `main.py` + Router-Datei zusammengesetzt werden
- Swagger/OpenAPI Docs zeigen kombinierte Pfade, was die Navigation leicht erschwert

### Folge-Tasks
- K-17: Pfade in `test_smoke.py`, `demo.sh`, `apiClient.ts` anpassen
- Dokumentation: API-Pfad-Struktur in `HARNESS.md` vermerken

## Reversibilität

Trivial. Entfernen von `prefix="/api/v1"` in `main.py` stellt sofort den Status Quo wieder her. Keine Datenbank-Migration, keine Breaking Changes für interne Clients solange die Versionierung noch nicht extern kommuniziert wurde.

## Compliance-Impact

Keine. Rein technische Organisations-Entscheidung.

## Referenzen

- `memory/runs/2026-04-29_kimi_K-17.md`
- `code/backend/app/main.py` (Zeilen 103–106)
- `code/frontend/src/lib/apiClient.ts`
