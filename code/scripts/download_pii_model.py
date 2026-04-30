"""Download PII detection model from HuggingFace.

Idempotent — skips if model already exists with matching files.
Usage: python scripts/download_pii_model.py [--model-id MODEL_ID] [--output-dir DIR]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Download PII model from HuggingFace")
    parser.add_argument(
        "--model-id",
        default="OpenMed/OpenMed-PII-German-ClinicalLongformer-Base-149M-v1",
        help="HuggingFace model identifier",
    )
    parser.add_argument(
        "--output-dir",
        default="data/models/nlp",
        help="Local directory to cache model",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download even if model exists",
    )
    args = parser.parse_args()

    output_path = Path(args.output_dir) / args.model_id.replace("/", "--")

    if output_path.exists() and not args.force:
        print(f"Model already exists at {output_path} — skipping.")
        print("Use --force to re-download.")
        return 0

    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        print("ERROR: huggingface_hub not installed.")
        print("Install: pip install huggingface_hub")
        return 1

    print(f"Downloading {args.model_id} ...")
    print(f"Target: {output_path}")

    try:
        snapshot_download(
            repo_id=args.model_id,
            local_dir=str(output_path),
            local_dir_use_symlinks=False,
        )
        print(f"OK: Model downloaded to {output_path}")
        return 0
    except Exception as e:
        print(f"ERROR: Download failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
