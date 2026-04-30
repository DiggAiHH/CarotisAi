# scripts/ — Carotis-AI Tooling

Operative Skripte für die Anonymisierungs-Pipeline, Pre-Flight-Checks und Validierung.

---

## Übersicht

| Skript | Zweck | Status | Phase |
|--------|-------|--------|-------|
| `preflight.sh` (bash) | Pre-Flight-Check Memory + Tasks | ✅ ready | Jeder Modell-Run |
| `preflight.ps1` (PowerShell) | Pre-Flight-Check für Windows | ✅ ready | Jeder Modell-Run |
| `anonymize.py` | DICOM PS 3.15 Anonymisierungs-Skeleton + k-Anonymity-Check | ✅ Skeleton + Tests | P0 (Skeleton) → P2 (full) |
| `test_anonymize.py` | pytest-Tests für anonymize.py | ✅ ready | P0 |
| `validate_decision_tree.py` | JSON-Schema-Validierung der Decision-Trees | 🔒 P5 | — |
| `nightly_retrain.py` | Daily-Learning-Loop mit Auto-Rollback | 🔒 P4 | — |

---

## Pre-Flight verwenden

```bash
# Bash / Git Bash / WSL
./scripts/preflight.sh

# PowerShell
.\scripts\preflight.ps1
```

Output:
- letzte 3 Run-Logs
- aktuelle Phase aus CLAUDE.md
- in_progress Tasks aus tasks.jsonl
- bekannte Anomalien aus memory/anomalies/

---

## Anonymisierung verwenden

```bash
# Self-Test (kein DICOM-Input nötig)
python scripts/anonymize.py --self-test

# Trockenlauf auf einem Verzeichnis
python scripts/anonymize.py --input ./test_data --output ./out --check

# Echter Lauf mit Salt aus Doppler / .env
python scripts/anonymize.py \
  --input /klinikum/pacs/export \
  --output /klinikum/training/anon \
  --salt "$ANONYMIZATION_SALT" \
  --salt-version v2026-04 \
  --min-k 5
```

**Wichtig:**
- `--salt` muss in Produktion über Doppler / Vault injiziert werden, nie auf der Kommandozeile direkt
- `--min-k 5` ist der harte Default; nie unter 5 setzen ohne ADR + Margaritoff-Konsultation
- Manifest-File (JSON) wird automatisch in das Output-Verzeichnis geschrieben — der Audit-Trail

---

## Tests laufen lassen

```bash
# Mit pytest (empfohlen)
pip install pytest
pytest scripts/test_anonymize.py -v

# Ohne pytest (Skeleton-Self-Test reicht für CI)
python scripts/anonymize.py --self-test
```

Erwartung: alle Tests grün. Falls nicht: STOP, Fix, Re-Test. Kein Push mit roten Tests.

---

## Hinzufügen neuer Skripte

1. Neue `.py` Datei in `scripts/` anlegen
2. Test-File `test_<name>.py` daneben
3. Eintrag in der Tabelle oben mit Status + Phase
4. Wenn das Skript Patientendaten berührt: in `memory/domain/fb_local_first.md` prüfen, dass es keine Cloud-Calls macht
5. Wenn das Skript regulatorische Auswirkungen hat: ADR in `regulatory/adr/`
