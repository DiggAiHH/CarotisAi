"""
Carotis-AI — DICOM Anonymisation Pipeline (Skeleton)

Implementiert das DICOM PS 3.15 Basic Application Confidentiality Profile
plus Carotis-AI-spezifische Erweiterungen (Salt-basierte case_id, k-Anonymity-Check).

Status: P0 = Skeleton + Schema-Tests grün. Echte DICOM-Verarbeitung
folgt in P2, sobald `pydicom` als Dependency ergänzt ist.

Use-Case:
    Edge-Server im Klinikum: vor jedem Modell-Training-Push wird ein Batch
    anonymisiert. Output: `data/anonymized/<batch>/*.dcm` + `data/manifest.csv`.

CLI:
    python anonymize.py --input <dir> --output <dir> --salt-version v2026-04
    python anonymize.py --check  # läuft alle PII-Tags-Audits ohne zu schreiben
    python anonymize.py --self-test  # läuft die unit tests

Spezifikation: 05_DECISION_TREE_HARVESTING.md, Sektion 5.

Author: Lou (mit Claude Opus 4.7 + Sonnet 4.6)
Date: 2026-04-27
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# DICOM PS 3.15 Basic Profile — die 33 Standard-PII-Tags die entfernt werden müssen.
# Quelle: DICOM Standard PS3.15 Annex E, Tabelle E.1-1.
# Dargestellt als (group, element) Paare.
DICOM_PII_TAGS_BASIC: tuple[tuple[int, int], ...] = (
    (0x0008, 0x0014),  # Instance Creator UID
    (0x0008, 0x0018),  # SOP Instance UID  → wird re-hashed, nicht entfernt
    (0x0008, 0x0050),  # Accession Number
    (0x0008, 0x0080),  # Institution Name
    (0x0008, 0x0081),  # Institution Address
    (0x0008, 0x0090),  # Referring Physician's Name
    (0x0008, 0x0092),  # Referring Physician's Address
    (0x0008, 0x0094),  # Referring Physician's Telephone Numbers
    (0x0008, 0x1010),  # Station Name
    (0x0008, 0x1030),  # Study Description (kann PII enthalten — wird gestrippt)
    (0x0008, 0x103E),  # Series Description (idem)
    (0x0008, 0x1040),  # Institutional Department Name
    (0x0008, 0x1048),  # Physician(s) of Record
    (0x0008, 0x1050),  # Performing Physician's Name
    (0x0008, 0x1060),  # Name of Physician(s) Reading Study
    (0x0008, 0x1070),  # Operators' Name
    (0x0008, 0x1080),  # Admitting Diagnoses Description
    (0x0010, 0x0010),  # Patient's Name
    (0x0010, 0x0020),  # Patient ID
    (0x0010, 0x0030),  # Patient's Birth Date  → auf Birth Year reduziert
    (0x0010, 0x0032),  # Patient's Birth Time
    (0x0010, 0x0040),  # Patient's Sex  → bleibt für Bias-Audit
    (0x0010, 0x1000),  # Other Patient IDs
    (0x0010, 0x1001),  # Other Patient Names
    (0x0010, 0x1010),  # Patient's Age
    (0x0010, 0x1020),  # Patient's Size
    (0x0010, 0x1030),  # Patient's Weight
    (0x0010, 0x1040),  # Patient's Address
    (0x0010, 0x2154),  # Patient's Telephone Numbers
    (0x0010, 0x2160),  # Ethnic Group
    (0x0010, 0x4000),  # Patient Comments
    (0x0020, 0x0010),  # Study ID
    (0x0040, 0xA730),  # Content Sequence (kann freitextliche PII enthalten)
)

# Tags die wir behalten (bewusst), für klinische Stratifizierung
DICOM_KEEP_TAGS: tuple[tuple[int, int], ...] = (
    (0x0010, 0x0040),  # Patient's Sex
    (0x0008, 0x0060),  # Modality
    (0x0008, 0x0070),  # Manufacturer
    (0x0018, 0x1030),  # Protocol Name (wird redaktioniert wenn PII enthalten)
    (0x0028, 0x0010),  # Rows
    (0x0028, 0x0011),  # Columns
)

# Quasi-identifier-Sets für k-Anonymity-Check.
# k-Anonymity-Definition: kein Datensatz ist allein durch die Quasi-Identifier
# identifizierbar; mind. k Datensätze müssen die identische Kombination teilen.
QUASI_IDENTIFIERS: tuple[str, ...] = (
    "patient_age_bucket",   # 5-Jahres-Bucket
    "patient_sex",          # M/F/Other
    "modality",             # CT, MR, US
    "study_year",           # 2024, 2025, 2026
    "institution_country",  # DE, JO
)

DEFAULT_SALT = "CHANGE-ME-IN-PRODUCTION-via-DOPPLER"  # niemals committen
MIN_K_ANONYMITY = 5


@dataclass
class AnonymisationConfig:
    """Konfiguration für einen Anonymisierungs-Lauf."""
    salt: str
    salt_version: str = "v2026-04"
    profile: str = "DICOM_PS_3.15_basic"
    min_k: int = MIN_K_ANONYMITY
    check_only: bool = False


@dataclass
class AnonymisationResult:
    """Ergebnis eines einzelnen Datei-Lauf."""
    source_path: str
    anonymized_path: str | None
    case_id: str
    audit_id: str
    pii_tags_removed: int
    k_anonymity: int
    status: str  # "ok", "rejected_low_k", "rejected_pii_leak", "skipped_check_only"
    error: str | None = None


@dataclass
class BatchManifest:
    """Manifest eines kompletten Batch-Laufs (geht in data/manifest.csv)."""
    batch_id: str
    started_at: str
    config: AnonymisationConfig
    results: list[AnonymisationResult] = field(default_factory=list)


def hash_with_salt(value: str, salt: str) -> str:
    """SHA-256 Hash eines Wertes mit Salt — für case_id-Generation."""
    h = hashlib.sha256()
    h.update(salt.encode("utf-8"))
    h.update(b":")
    h.update(value.encode("utf-8"))
    return h.hexdigest()


def make_case_id(study_uid: str, salt: str, week_bucket: str) -> str:
    """
    Generiert die case_id aus dem study_uid, dem Salt und dem Wochen-Bucket.

    week_bucket ist im Format 'YYYY-Www' (ISO 8601 week date), damit sich
    der Hash innerhalb einer Woche stabil bleibt aber zwischen Wochen rotiert.
    """
    composite = f"{study_uid}|{week_bucket}"
    return hash_with_salt(composite, salt)


def get_week_bucket(timestamp: datetime) -> str:
    """Gibt 'YYYY-Www' für einen Timestamp zurück."""
    iso_year, iso_week, _ = timestamp.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


def check_k_anonymity(
    quasi_identifier_combo: tuple[str, ...],
    population_counter: dict[tuple[str, ...], int],
) -> int:
    """
    Returnt das k-Level der gegebenen Quasi-Identifier-Kombination
    in der Population.

    population_counter wird bei jedem File inkrementiert (Caller-Verantwortung).
    """
    return population_counter.get(quasi_identifier_combo, 0)


def build_quasi_identifier_combo(metadata: dict[str, Any]) -> tuple[str, ...]:
    """Bildet die QI-Kombination aus den geprüften Tags."""
    return tuple(str(metadata.get(qi, "UNKNOWN")) for qi in QUASI_IDENTIFIERS)


def anonymize_file_skeleton(
    source_path: Path,
    output_dir: Path,
    config: AnonymisationConfig,
    population_counter: dict[tuple[str, ...], int],
) -> AnonymisationResult:
    """
    Skeleton: liest eine Datei, simuliert Anonymisierung, schreibt
    nach output_dir.

    Echte DICOM-Verarbeitung wird in P2 ergänzt mit pydicom:
      - dataset = pydicom.dcmread(source_path)
      - for tag in DICOM_PII_TAGS_BASIC: del dataset[tag]
      - dataset.save_as(output_path)
    """
    logger = logging.getLogger(__name__)
    audit_id = f"AT-{datetime.now(timezone.utc).strftime('%Y-%m-%d-%H%M%S')}-{source_path.stem}"

    # Skeleton: simulieren Metadaten-Extraktion
    fake_metadata = {
        "study_uid": f"1.2.3.4.5.{source_path.stem}",
        "patient_age_bucket": "60-64",
        "patient_sex": "M",
        "modality": "CT",
        "study_year": "2026",
        "institution_country": "DE",
    }

    # Quasi-Identifier-Kombination + k-Anonymity-Check
    qi_combo = build_quasi_identifier_combo(fake_metadata)
    population_counter[qi_combo] = population_counter.get(qi_combo, 0) + 1
    k = population_counter[qi_combo]

    if k < config.min_k:
        logger.warning(
            "k-Anonymity zu niedrig (%s < %s) für %s — abgelehnt",
            k, config.min_k, source_path.name,
        )
        return AnonymisationResult(
            source_path=str(source_path),
            anonymized_path=None,
            case_id="",
            audit_id=audit_id,
            pii_tags_removed=0,
            k_anonymity=k,
            status="rejected_low_k",
        )

    week_bucket = get_week_bucket(datetime.now(timezone.utc))
    case_id = make_case_id(fake_metadata["study_uid"], config.salt, week_bucket)

    if config.check_only:
        return AnonymisationResult(
            source_path=str(source_path),
            anonymized_path=None,
            case_id=case_id,
            audit_id=audit_id,
            pii_tags_removed=len(DICOM_PII_TAGS_BASIC),
            k_anonymity=k,
            status="skipped_check_only",
        )

    output_path = output_dir / f"{case_id[:16]}.anon.dcm"
    output_dir.mkdir(parents=True, exist_ok=True)
    # Skeleton: leere Datei schreiben (echte DICOM-Bytes kommen in P2)
    output_path.write_bytes(b"DICOM_ANONYMIZED_SKELETON\n")

    return AnonymisationResult(
        source_path=str(source_path),
        anonymized_path=str(output_path),
        case_id=case_id,
        audit_id=audit_id,
        pii_tags_removed=len(DICOM_PII_TAGS_BASIC),
        k_anonymity=k,
        status="ok",
    )


def run_batch(
    input_dir: Path,
    output_dir: Path,
    config: AnonymisationConfig,
) -> BatchManifest:
    """Läuft die Anonymisierungs-Pipeline über ein Verzeichnis."""
    logger = logging.getLogger(__name__)
    started_at = datetime.now(timezone.utc).isoformat()
    batch_id = f"batch-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    manifest = BatchManifest(batch_id=batch_id, started_at=started_at, config=config)

    population_counter: dict[tuple[str, ...], int] = {}
    files = sorted(input_dir.glob("*.dcm")) + sorted(input_dir.glob("*.DCM"))
    if not files:
        logger.warning("Keine .dcm Files gefunden in %s", input_dir)
        return manifest

    logger.info("Starte Batch %s mit %d Files", batch_id, len(files))
    for f in files:
        try:
            result = anonymize_file_skeleton(f, output_dir, config, population_counter)
        except Exception as exc:  # noqa: BLE001 — wir loggen alles
            logger.exception("Fehler bei %s", f.name)
            result = AnonymisationResult(
                source_path=str(f),
                anonymized_path=None,
                case_id="",
                audit_id="",
                pii_tags_removed=0,
                k_anonymity=0,
                status="rejected_pii_leak",
                error=str(exc),
            )
        manifest.results.append(result)

    return manifest


def write_manifest_json(manifest: BatchManifest, path: Path) -> None:
    """Schreibt das Manifest als JSON für den Audit-Trail."""
    data = {
        "batch_id": manifest.batch_id,
        "started_at": manifest.started_at,
        "config": {
            "salt_version": manifest.config.salt_version,
            "profile": manifest.config.profile,
            "min_k": manifest.config.min_k,
            "check_only": manifest.config.check_only,
        },
        "results": [
            {
                "source_path": r.source_path,
                "anonymized_path": r.anonymized_path,
                "case_id": r.case_id,
                "audit_id": r.audit_id,
                "pii_tags_removed": r.pii_tags_removed,
                "k_anonymity": r.k_anonymity,
                "status": r.status,
                "error": r.error,
            }
            for r in manifest.results
        ],
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Verzeichnis mit DICOM-Input-Files")
    parser.add_argument("--output", type=Path, help="Zielverzeichnis für anonymisierte Files")
    parser.add_argument("--salt", type=str, default=DEFAULT_SALT, help="Anonymisierungs-Salt")
    parser.add_argument("--salt-version", type=str, default="v2026-04")
    parser.add_argument("--min-k", type=int, default=MIN_K_ANONYMITY)
    parser.add_argument("--check", action="store_true", help="Trockenlauf — keine Files schreiben")
    parser.add_argument("--self-test", action="store_true", help="Run internal smoke tests")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    if args.self_test:
        return _run_self_test()

    if args.salt == DEFAULT_SALT:
        print("WARN: --salt ist Default-Placeholder. In Produktion via Doppler injizieren.", file=sys.stderr)

    if not args.input or not args.output:
        parser.error("--input und --output sind erforderlich (oder --self-test)")

    config = AnonymisationConfig(
        salt=args.salt,
        salt_version=args.salt_version,
        min_k=args.min_k,
        check_only=args.check,
    )
    manifest = run_batch(args.input, args.output, config)
    manifest_path = args.output / f"{manifest.batch_id}.manifest.json"
    write_manifest_json(manifest, manifest_path)
    print(f"Batch fertig: {manifest_path}")
    return 0


def _run_self_test() -> int:
    """Smoke-Test ohne pytest — schnell auf der CLI laufen lassen."""
    print("Self-test: hash_with_salt deterministic ...", end=" ")
    a = hash_with_salt("studyA", "salt1")
    b = hash_with_salt("studyA", "salt1")
    assert a == b, "Hash nicht deterministisch"
    assert hash_with_salt("studyA", "salt2") != a, "Salt-Wechsel ändert Hash nicht"
    print("ok")

    print("Self-test: week_bucket format ...", end=" ")
    bucket = get_week_bucket(datetime(2026, 4, 27, tzinfo=timezone.utc))
    assert bucket == "2026-W18", f"Wochen-Bucket falsch: {bucket}"
    print("ok")

    print("Self-test: k-anonymity rejection ...", end=" ")
    counter: dict[tuple[str, ...], int] = {}
    qi = ("60-64", "M", "CT", "2026", "DE")
    counter[qi] = 4
    assert check_k_anonymity(qi, counter) < MIN_K_ANONYMITY
    counter[qi] = 5
    assert check_k_anonymity(qi, counter) >= MIN_K_ANONYMITY
    print("ok")

    print("\nAlle Self-Tests grün.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
