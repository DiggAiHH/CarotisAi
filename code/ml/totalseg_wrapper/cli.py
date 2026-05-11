"""CLI-Frontend für TotalSegmentatorWrapper.

Beispiel::

    python -m ml.totalseg_wrapper.cli \\
        --input /data/imagecas/case_001.nii.gz \\
        --case-id research-case-001 \\
        --output /tmp/seg/case_001 \\
        --json

Liefert PII-freies Audit-JSON auf stdout (Bequemlichkeit für Pipeline-Integration).
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from .types import SegmentationLabels, WrapperConfig
from .wrapper import TotalSegmentatorWrapper


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="totalseg-wrapper",
        description="TotalSegmentator-Wrapper für Carotis-AI Forschungsprototyp.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Pfad zu NIfTI-Datei oder DICOM-Series-Verzeichnis.",
    )
    parser.add_argument(
        "--case-id",
        type=str,
        required=True,
        help="Forscher-vergebene Fall-ID (NIEMALS Patient-ID).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output-Verzeichnis für Segmentations-Masken.",
    )
    parser.add_argument(
        "--task",
        type=str,
        default="headneck_bones_vessels",
        help="TotalSegmentator-Task (Default: headneck_bones_vessels).",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        help="auto | cpu | cuda | cuda:0",
    )
    parser.add_argument(
        "--resolution-mm",
        type=float,
        default=1.5,
        help="Voxel-Resampling-Auflösung in mm.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Audit-Payload auf stdout als JSON ausgeben.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Debug-Logs aktivieren.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    config = WrapperConfig(
        task=args.task,
        resolution_mm=args.resolution_mm,
        device=args.device,
        labels_of_interest=(
            SegmentationLabels.ICA_LEFT,
            SegmentationLabels.ICA_RIGHT,
        ),
    )
    wrapper = TotalSegmentatorWrapper(config)
    result = wrapper.segment(
        input_path=args.input,
        case_id=args.case_id,
        output_dir=args.output,
    )

    if args.json:
        print(json.dumps(result.to_audit_payload(), indent=2))
    else:
        print(f"Case {result.case_id} segmentiert in {result.inference_seconds:.2f}s")
        for summary in result.label_summaries:
            print(
                f"  {summary.label.value}: voxels={summary.voxel_count} "
                f"vol={summary.volume_mm3:.1f} mm³"
            )
        if result.mask_path:
            print(f"Kombinierte Maske: {result.mask_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
