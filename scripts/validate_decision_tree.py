"""
Carotis-AI — Decision Tree JSON Validator

Validiert ein einzelnes Decision-Tree-File oder ein ganzes Verzeichnis gegen
das JSON-Schema in schemas/decision_tree.schema.json.

CLI:
    python validate_decision_tree.py memory/decisions/2026-08-15_a3f4e8c9.json
    python validate_decision_tree.py memory/decisions/        # alle .json im Dir
    python validate_decision_tree.py --self-test

Exit code:
    0 = alle Files valid
    1 = mind. ein File invalid (Details auf stdout)
    2 = Schema selbst kaputt oder Setup-Problem

Author: Lou
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_schema() -> dict[str, Any]:
    """Lädt das Decision-Tree-Schema aus dem schemas/ Ordner."""
    here = Path(__file__).resolve().parent
    schema_path = here.parent / "schemas" / "decision_tree.schema.json"
    if not schema_path.exists():
        print(f"ERROR: Schema nicht gefunden bei {schema_path}", file=sys.stderr)
        sys.exit(2)
    return json.loads(schema_path.read_text(encoding="utf-8"))


def validate_file(path: Path, validator) -> tuple[bool, list[str]]:
    """Validiert ein einzelnes JSON-File. Returnt (ok, errors)."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return False, [f"JSON-Decode-Fehler: {e.msg} (line {e.lineno})"]

    # _comment Key in Samples ist erlaubt — entfernen vor Validierung
    data.pop("_comment", None)

    errors = []
    for err in validator.iter_errors(data):
        path_str = " → ".join(str(p) for p in err.absolute_path) or "(root)"
        errors.append(f"  {path_str}: {err.message}")
    return len(errors) == 0, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "target",
        nargs="?",
        type=Path,
        help="Pfad zu einer .json Datei oder einem Verzeichnis mit .json Files",
    )
    parser.add_argument("--self-test", action="store_true", help="Validiert das Sample-File")
    args = parser.parse_args(argv)

    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        print("ERROR: jsonschema-Paket fehlt. Installiere: pip install jsonschema", file=sys.stderr)
        return 2

    schema = load_schema()
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: Schema selbst ist kaputt: {e}", file=sys.stderr)
        return 2
    validator = Draft202012Validator(schema)

    if args.self_test:
        sample_path = Path(__file__).resolve().parent.parent / "schemas" / "decision_tree.sample.json"
        ok, errors = validate_file(sample_path, validator)
        if ok:
            print(f"OK {sample_path.name} valid")
            return 0
        print(f"FAIL {sample_path.name} INVALID:")
        for e in errors:
            print(e)
        return 1

    if args.target is None:
        parser.error("Bitte Pfad angeben oder --self-test verwenden")

    if args.target.is_file():
        files = [args.target]
    elif args.target.is_dir():
        files = sorted(args.target.glob("*.json"))
        if not files:
            print(f"Keine .json Files in {args.target}", file=sys.stderr)
            return 1
    else:
        print(f"ERROR: {args.target} existiert nicht", file=sys.stderr)
        return 2

    total = len(files)
    passed = 0
    failed_files: list[tuple[Path, list[str]]] = []
    for f in files:
        ok, errors = validate_file(f, validator)
        if ok:
            passed += 1
        else:
            failed_files.append((f, errors))

    print(f"\nValidiert: {passed}/{total} OK")
    if failed_files:
        print("\nFehler:")
        for path, errors in failed_files:
            print(f"\nFAIL {path.name}")
            for e in errors:
                print(e)
        return 1
    print("Alle Decision-Trees valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
