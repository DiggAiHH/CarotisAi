#!/usr/bin/env python3
"""
Standalone CLI wrapper for AnonymizationService.

Called by Hermes skills, CI, and demo shells.
"""
from __future__ import annotations

import argparse
import asyncio
import csv
import hashlib
import os
import sys
from pathlib import Path

import structlog

# ---------------------------------------------------------------------------
# Path setup: scripts/ lives at code/scripts/, backend at code/backend/
# ---------------------------------------------------------------------------
_BACKENDS = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(_BACKENDS))

# ---------------------------------------------------------------------------
# Guard: app.core.config requires these env vars at import time.
# ---------------------------------------------------------------------------
os.environ.setdefault("API_KEY", "a" * 32)
os.environ.setdefault("ADMIN_API_KEY", "b" * 32)
os.environ.setdefault("ANONYMIZATION_SALT", "s" * 32)

from app.services.anonymization_service import AnonymizationService  # noqa: E402


def _configure_logging() -> None:
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(20),  # INFO
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _collect_dicom_files(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    files: list[Path] = []
    for pattern in ("**/*.dcm", "**/*.DCM"):
        files.extend(input_path.glob(pattern))
    # Deduplicate (case-insensitive filesystems may match both patterns)
    seen: set[Path] = set()
    unique: list[Path] = []
    for f in files:
        resolved = f.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(f)
    return sorted(unique)


async def _process_one(
    svc: AnonymizationService,
    file_path: Path,
    output_dir: Path | None,
    dry_run: bool,
) -> dict[str, object]:
    original_hash = _sha256_file(file_path)
    dicom_bytes = file_path.read_bytes()

    try:
        is_clean, found_tags = svc.check_only(dicom_bytes)
    except Exception as exc:  # noqa: BLE001
        return {
            "original_hash": original_hash,
            "output_path": "",
            "tags_removed": 0,
            "status": "failed",
            "error": str(exc),
        }

    if is_clean:
        if not dry_run and output_dir is not None:
            out_path = output_dir / file_path.name
            out_path.write_bytes(dicom_bytes)
        return {
            "original_hash": original_hash,
            "output_path": str(output_dir / file_path.name) if output_dir else "",
            "tags_removed": 0,
            "status": "skipped",
        }

    tags_removed = len(found_tags)
    if not dry_run and output_dir is not None:
        try:
            anonymized = await svc.ensure_anonymized(dicom_bytes)
            out_path = output_dir / file_path.name
            out_path.write_bytes(anonymized)
        except Exception as exc:  # noqa: BLE001
            return {
                "original_hash": original_hash,
                "output_path": "",
                "tags_removed": tags_removed,
                "status": "failed",
                "error": str(exc),
            }

    return {
        "original_hash": original_hash,
        "output_path": str(output_dir / file_path.name) if output_dir else "",
        "tags_removed": tags_removed,
        "status": "ok",
    }


async def _run(
    input_path: Path,
    output_dir: Path | None,
    dry_run: bool,
    manifest_path: Path | None,
    min_k: int,
) -> int:
    logger = structlog.get_logger("anonymize_cli")
    files = _collect_dicom_files(input_path)
    total = len(files)

    if total == 0:
        logger.error("no_dicom_files_found", input=str(input_path))
        return 2

    if total < min_k:
        logger.warning("k_anonymity_warning", total=total, min_k=min_k)

    svc = AnonymizationService()
    results: list[dict[str, object]] = []
    failed = 0

    for file_path in files:
        result = await _process_one(svc, file_path, output_dir, dry_run)
        results.append(result)
        if result["status"] == "failed":
            failed += 1

        logger.info(
            "file_processed",
            input=str(file_path),
            tags_removed=result["tags_removed"],
            status=result["status"],
        )

    summary = {
        "total": total,
        "cleaned": sum(1 for r in results if r["status"] == "ok"),
        "skipped": sum(1 for r in results if r["status"] == "skipped"),
        "failed": failed,
    }
    logger.info("batch_summary", **summary)

    if manifest_path:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with manifest_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(
                fh,
                fieldnames=["original_hash", "output_path", "tags_removed", "status"],
            )
            writer.writeheader()
            for row in results:
                writer.writerow({
                    "original_hash": row["original_hash"],
                    "output_path": row["output_path"],
                    "tags_removed": row["tags_removed"],
                    "status": row["status"],
                })

    if failed == total:
        return 2
    if failed > 0:
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="DICOM Anonymization CLI — wrapper around AnonymizationService",
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Single .dcm file or directory containing DICOM files",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory for anonymized / copied files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Check only — report PII without writing any files",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="CSV manifest path (columns: original_hash, output_path, tags_removed, status)",
    )
    parser.add_argument(
        "--min-k",
        type=int,
        default=5,
        help="Warn if batch size is below this k-anonymity threshold",
    )
    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"Error: input does not exist: {args.input}", file=sys.stderr)
        return 2

    if args.output:
        if args.output.resolve() == args.input.resolve():
            raise ValueError("output path must differ from input path")
        args.output.mkdir(parents=True, exist_ok=True)
    elif not args.dry_run:
        parser.error("--output is required unless --dry-run is set")

    _configure_logging()
    return asyncio.run(
        _run(
            input_path=args.input,
            output_dir=args.output,
            dry_run=args.dry_run,
            manifest_path=args.manifest,
            min_k=args.min_k,
        )
    )


if __name__ == "__main__":
    sys.exit(main())
