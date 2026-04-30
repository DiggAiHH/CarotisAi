# Modell-Update-Verfahren (MUP)

## Ziel
Reproduzierbare, sichere Aktualisierung der ONNX-Inferenzmodelle auf dem Edge-Gerät im Klinikum ohne Cloud-Kontakt.

## 1. Bundle-Struktur

Ein signiertes Modell-Bundle (`.tar.gz`) enthält mindestens:

```
mfsd_unet_vX.Y.Z.tar.gz
├── model.onnx          # Inferenz-Graph
├── meta.json           # Version, SHA-256, Trainings-Metriken
├── signature.json      # Signatur-Hierarchie (cosign / GPG / SHA-256+Timestamp)
└── checksums.sha256    # SHA-256 aller Dateien
```

## 2. Update-Pfade

| Pfad | Medium | Verschlüsselung | Rollen |
|------|--------|-----------------|--------|
| Primär | USB-Stick (LUKS/BitLocker) | AES-256 | Medizinphysiker + IT-Sicherheit |
| Sekundär | Gesichertes Klinik-LAN (VLAN-isoliert) | TLS 1.3 + mTLS | IT-Admin |
| Notfall | Air-Gapped Laptop im Geräteraum | Full-Disk-Encryption | Bereichsleiter + 2-Augen-Prinzip |

**Kein Cloud-Upload, kein Fernzugriff, kein automatischer Download.**

## 3. Verify-Schritt (vor Installation)

```bash
scripts/verify_model.py \
  --bundle mfsd_unet_vX.Y.Z.tar.gz \
  --expected-sha256 <aus Change-Log> \
  --max-age-days 90
```

Abbruchkriterien:
- SHA-256-Mismatch → sofortiger Abbruch, Incident an IT-Sicherheit
- Signatur ungültig → Abbruch, Key-Rotation prüfen
- Bundle älter als `max_age_days` → Warnung, manuelle Freigabe erforderlich
- `meta.json` fehlt Pflichtfelder (`model_version`, `training_data_hash`) → Abbruch

## 4. Rollback

- Vor Installation wird das aktive Modell nach `/data/models/backup/` kopiert.
- Rollback-Skript: `scripts/rollback_model.py --to-backup`
- Automatischer Rollback bei Health-Check-Fehlschlag innerhalb von 60 s nach Modell-Wechsel.

## 5. Audit

Jeder Update-Versuch schreibt einen `AuditEvent`:
- `event_type`: `model_update_attempted`, `model_update_verified`, `model_update_rolled_back`
- `actor`: Hash des ausführenden Benutzers (SHA-256 mit project_salt)
- `payload_json`: `{model_version, bundle_sha256, verify_result, rollback_reason|null}`

## 6. Rollen

| Rolle | Verantwortung |
|-------|---------------|
| Modell-Verantwortlicher (Promovend) | Bundle erstellen, signieren, meta.json validieren |
| Medizinphysiker | Verify vor Ort, Installation durchführen |
| IT-Sicherheit | Schlüsselverwaltung, Audit-Review |
| Bereichsleiter | Notfall-Freigabe, 2-Augen-Prinzip bei Abweichungen |

## 7. Notfallmodus

Falls das aktive Modell korrupt ist und kein Backup verfügbar:
1. Demo-Modell (`scripts/generate_demo_model.py`) erzeugen
2. Mit Wasserzeichen "NOT FOR DIAGNOSIS" markieren
3. Überwiegende Nutzung nur für UI-Smoke-Tests
4. Vollständige Re-Installation aus quarantäntem Backup innerhalb 24 h

## 8. Compliance-Mapping

- DSGVO §32: Integrität durch Signatur + SHA-256
- MDR Anhang I, Kap. III: Software-Updates als design change → Dokumentation in `regulatory/adr/`
- ISO 27001 A.12.1.2: Change Management → dieses Verfahren
