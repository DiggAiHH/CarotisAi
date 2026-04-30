# ADR-0004: Lazy Database Engine Initialisierung via `@lru_cache` für Test-Isolierung

| Feld | Wert |
|------|------|
| **Status** | Accepted |
| **Datum** | 2026-04-29 |
| **Autor** | Lou (Laith Alshdaifat) + Kimi K2.6 |
| **Reviewer** | — |
| **Phase** | P0a |
| **Compliance-Impact** | Nein — rein technisch; indirekt DIN EN 62304 Kapitel 5.3.5 (Testbarkeit) |

---

## Kontext

Während der E2E-Verifikation von K-01..K-16 traten sporadische Test-Fehler auf, die auf eine gemeinsame `engine`-Instanz zurückzuführen waren: `code/backend/app/db/database.py` erstellte `create_async_engine()` beim Modul-Import. Tests, die `monkeypatch.setenv("DATABASE_URL", "...")` verwendeten, teilten sich denselben Engine-Pool, was zu "database locked"-Fehlern und Cross-Test-Kontamination führte. Die Frage: Wie initialisieren wir die async SQLAlchemy-Engine so, dass Tests vollständig isoliert laufen, ohne die Produktions-Performance zu beeinträchtigen?

## Optionen

### Option A — Status Quo (Modul-Level Engine)
`engine = create_async_engine(settings.database_url)` beim Import von `database.py`.
- **Pro:** Einfach; keine Änderung nötig; Engine existiert sofort
- **Contra:** Unmöglich, in Tests einen anderen DATABASE_URL zu verwenden ohne Prozess-Neustart; `get_settings.cache_clear()` allein reicht nicht, da `engine` bereits gebunden ist; führt zu Heisenbugs in parallelen Test-Runs
- **Aufwand:** XS (nichts tun)
- **Reversibilität:** trivial

### Option B — Lazy Init via Factory-Funktion mit `@lru_cache` (gewählt)
`get_engine()` mit `@lru_cache(maxsize=1)` erstellt die Engine erst beim ersten Aufruf. Tests können `get_engine.cache_clear()` aufrufen, um den Cache zu invalidieren, und dann `monkeypatch.setenv()` + `get_settings.cache_clear()` verwenden, um eine frische Engine mit einem neuen DATABASE_URL zu erhalten. `get_session_factory()` baut auf `get_engine()` auf; `reset_db()` kapselt `drop_all` + `create_all`.
- **Pro:** Test-Isolierung ohne Prozess-Neustart; Produktions-Code bleibt unverändert in der Nutzung (`init_db()`, `get_db()`); `@lru_cache` ist Python-Idiom und gut verständlich
- **Contra:** Erster Aufruf von `get_engine()` ist marginal langsamer (ca. 1–2 ms); `@lru_cache` fühlt sich für manche Entwickler wie versteckter globaler State an
- **Aufwand:** S
- **Reversibilität:** trivial — `@lru_cache` entfernen, Engine wieder auf Modul-Level

### Option C — Dependency-Injection Container
Ein expliziter DI-Container (z.B. `dependency-injector` oder eigene Registry) hält die Engine-Instanz und wird in Tests durch einen Mock ersetzt.
- **Pro:** Maximale Flexibilität; Engine ist nie global; Test-Mocks sind explizit
- **Contra:** Zusätzliche Dependency (`dependency-injector`); übermäßig für ein Projekt mit < 10 Services; Lernkurve für neue Entwickler; fühlt sich "enterprisey" an
- **Aufwand:** M
- **Reversibilität:** mittel — DI-Container aus allen Services entfernen

## Entscheidung

Option B. `@lru_cache` auf einer Factory-Funktion ist der sweet spot zwischen "einfach genug, dass jeder Python-Entwickler es versteht" und "flexibel genug für saubere Tests". Die 1–2 ms Verzögerung beim ersten Aufruf sind im medizinischen Kontext irrelevant (keine Echtzeit-Anforderung). Option C wäre überkonstruiert für die aktuelle Projektgröße.

## Konsequenzen

### Positiv
- Tests können parallele DATABASE_URL-Konfigurationen verwenden (z.B. `:memory:` vs. Datei-SQLite)
- `reset_db()` als expliziter Test-Helper vereinfacht Fixture-Code
- Keine zusätzlichen Dependencies

### Negativ
- `AsyncSessionLocal` als globale Variable existiert nicht mehr; zwei Route-Files (`audit.py`, `decision_tree.py`) mussten auf `get_session_factory()` umgestellt werden
- Engine-Lebenszyklus ist weniger explizit sichtbar als beim Modul-Import

### Folge-Tasks
- K-18: `database.py`, `conftest.py`, `audit.py`, `decision_tree.py` anpassen
- Dokumentation: Test-Pattern in `AGENTS.md` ergänzen

## Reversibilität

Trivial. Entfernen von `@lru_cache`, Rückkehr zum Modul-Level `engine = create_async_engine(...)`. Alle Aufrufer verwenden bereits `get_engine()`, daher keine Änderung an den Call-Sites nötig.

## Compliance-Impact

Kein direkter Compliance-Impact. Indirekt unterstützt saubere Test-Isolierung die DIN EN 62304 Anforderung an Unit- und Integrationstests (Kapitel 5.3.5).

## Referenzen

- `memory/runs/2026-04-29_kimi_K-18.md`
- `memory/anomalies/2026-04-29_kimi_e2e_13_bugs.md` (Anomalie A-03)
- `code/backend/app/db/database.py`
- `code/backend/tests/conftest.py`
