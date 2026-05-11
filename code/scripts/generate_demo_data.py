from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pydicom
from pydicom.dataset import FileDataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid

SALT = "demo-only-salt-do-not-use-in-prod"
PROJECT_ROOT = Path(__file__).resolve().parents[2]

_MARKERS_POOL = [
    "intraplaque_hemorrhage",
    "thin_fibrous_cap",
    "lipid_rich_necrotic_core",
    "systolic_motion_anomaly",
    "calcified_shell_partial",
]

_DECIDING_FEATURES = [
    "echolucent_zone_dorsal",
    "calcified_shell_partial",
    "intraplaque_hemorrhage_signal",
    "fibrous_cap_thinning",
]

_STAR_SCENARIOS: list[dict] = [
    {
        "dicom": {
            "pixel_mean": 110,
            "pixel_std": 20,
            "lesion_intensity": 380,
            "lesion_radius_sq": 900,
        },
        "tree": {
            "ai_stenosis": 25.0,
            "physician_stenosis": 25.0,
            "confidence": 0.88,
            "vulnerability_markers": {
                "intraplaque_hemorrhage": 0.05,
                "thin_fibrous_cap": 0.02,
                "lipid_rich_necrotic_core": 0.10,
                "systolic_motion_anomaly": 0.01,
                "calcified_shell_partial": 0.92,
            },
            "confirmed_markers": ["calcified_shell_partial"],
            "rejected_markers": [
                "intraplaque_hemorrhage",
                "thin_fibrous_cap",
                "lipid_rich_necrotic_core",
                "systolic_motion_anomaly",
            ],
            "added_markers": [],
            "confidence_self_reported": "high",
            "trust_score": 5,
            "verdict": "full_agreement",
            "reasoning": {
                "deciding_feature": "calcified_shell_partial",
                "ruled_out": [],
                "ruled_out_reason": "",
                "would_consult": None,
                "would_re_image_if": None,
            },
        },
    },
    {
        "dicom": {
            "pixel_mean": 115,
            "pixel_std": 28,
            "lesion_intensity": 420,
            "lesion_radius_sq": 1400,
        },
        "tree": {
            "ai_stenosis": 55.0,
            "physician_stenosis": 52.0,
            "confidence": 0.82,
            "vulnerability_markers": {
                "intraplaque_hemorrhage": 0.15,
                "thin_fibrous_cap": 0.25,
                "lipid_rich_necrotic_core": 0.88,
                "systolic_motion_anomaly": 0.05,
                "calcified_shell_partial": 0.12,
            },
            "confirmed_markers": ["lipid_rich_necrotic_core"],
            "rejected_markers": ["calcified_shell_partial", "systolic_motion_anomaly"],
            "added_markers": [],
            "confidence_self_reported": "medium",
            "trust_score": 3,
            "verdict": "partial_agreement",
            "reasoning": {
                "deciding_feature": "echolucent_zone_dorsal",
                "ruled_out": [],
                "ruled_out_reason": "",
                "would_consult": None,
                "would_re_image_if": None,
            },
        },
    },
    {
        "dicom": {
            "pixel_mean": 125,
            "pixel_std": 35,
            "lesion_intensity": 480,
            "lesion_radius_sq": 2200,
        },
        "tree": {
            "ai_stenosis": 78.0,
            "physician_stenosis": 84.0,
            "confidence": 0.71,
            "vulnerability_markers": {
                "intraplaque_hemorrhage": 0.91,
                "thin_fibrous_cap": 0.78,
                "lipid_rich_necrotic_core": 0.45,
                "systolic_motion_anomaly": 0.08,
                "calcified_shell_partial": 0.15,
            },
            "confirmed_markers": ["intraplaque_hemorrhage", "thin_fibrous_cap"],
            "rejected_markers": ["calcified_shell_partial", "systolic_motion_anomaly"],
            "added_markers": [],
            "confidence_self_reported": "high",
            "trust_score": 2,
            "verdict": "disagreement",
            "reasoning": {
                "deciding_feature": "intraplaque_hemorrhage_signal",
                "ruled_out": [],
                "ruled_out_reason": "",
                "would_consult": None,
                "would_re_image_if": None,
            },
        },
    },
    {
        "dicom": {
            "pixel_mean": 130,
            "pixel_std": 40,
            "lesion_intensity": 520,
            "lesion_radius_sq": 2800,
        },
        "tree": {
            "ai_stenosis": 92.0,
            "physician_stenosis": 92.0,
            "confidence": 0.95,
            "vulnerability_markers": {
                "intraplaque_hemorrhage": 0.75,
                "thin_fibrous_cap": 0.89,
                "lipid_rich_necrotic_core": 0.55,
                "systolic_motion_anomaly": 0.10,
                "calcified_shell_partial": 0.20,
            },
            "confirmed_markers": ["thin_fibrous_cap", "intraplaque_hemorrhage"],
            "rejected_markers": [
                "calcified_shell_partial",
                "lipid_rich_necrotic_core",
                "systolic_motion_anomaly",
            ],
            "added_markers": [],
            "confidence_self_reported": "high",
            "trust_score": 5,
            "verdict": "full_agreement",
            "reasoning": {
                "deciding_feature": "fibrous_cap_thinning",
                "ruled_out": [],
                "ruled_out_reason": "",
                "would_consult": None,
                "would_re_image_if": None,
            },
        },
    },
    {
        "dicom": {
            "pixel_mean": 118,
            "pixel_std": 22,
            "lesion_intensity": 360,
            "lesion_radius_sq": 700,
        },
        "tree": {
            "ai_stenosis": 32.0,
            "physician_stenosis": 28.0,
            "confidence": 0.74,
            "vulnerability_markers": {
                "intraplaque_hemorrhage": 0.10,
                "thin_fibrous_cap": 0.15,
                "lipid_rich_necrotic_core": 0.20,
                "systolic_motion_anomaly": 0.85,
                "calcified_shell_partial": 0.30,
            },
            "confirmed_markers": ["systolic_motion_anomaly"],
            "rejected_markers": [
                "calcified_shell_partial",
                "intraplaque_hemorrhage",
            ],
            "added_markers": [],
            "confidence_self_reported": "low",
            "trust_score": 2,
            "verdict": "partial_agreement",
            "reasoning": None,
        },
    },
]


def _make_dicom(case_idx: int, output_dir: Path, overrides: dict | None = None) -> Path:
    """Generate synthetic 512x512 DICOM. Already anonymized (all 33 PII tags absent).

    Args:
        case_idx: Numeric index used as default RNG seed.
        output_dir: Directory where the .dcm file is written.
        overrides: Optional dict with keys such as ``pixel_mean``, ``pixel_std``,
            ``lesion_intensity``, ``lesion_radius_sq``, or ``seed`` to override
            random generation for deterministic star cases.
    """
    overrides = overrides or {}
    rng = np.random.default_rng(seed=overrides.get("seed", case_idx))
    pixel_mean = overrides.get("pixel_mean", 120)
    pixel_std = overrides.get("pixel_std", 30)
    pixel_array = rng.normal(pixel_mean, pixel_std, (512, 512)).clip(-100, 600).astype(np.int16)
    cx, cy = rng.integers(200, 312, size=2)
    rr, cc = np.ogrid[:512, :512]
    lesion_radius_sq = overrides.get("lesion_radius_sq", 1500)
    mask = (rr - cx) ** 2 + (cc - cy) ** 2 < lesion_radius_sq
    lesion_intensity = overrides.get("lesion_intensity", 400)
    pixel_array[mask] = lesion_intensity

    file_meta = pydicom.dataset.FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = pydicom.uid.CTImageStorage
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    file_meta.ImplementationClassUID = generate_uid()

    ds = FileDataset(
        str(output_dir / f"case_{case_idx:03d}.dcm"),
        {},
        file_meta=file_meta,
        preamble=b"\0" * 128,
    )
    ds.SOPClassUID = pydicom.uid.CTImageStorage
    ds.Modality = "CT"
    ds.StudyDate = ""
    ds.Manufacturer = "Demo"
    ds.Rows = 512
    ds.Columns = 512
    ds.BitsAllocated = 16
    ds.BitsStored = 12
    ds.HighBit = 11
    ds.PixelRepresentation = 1
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.RescaleIntercept = 0
    ds.RescaleSlope = 1
    ds.WindowCenter = 200
    ds.WindowWidth = 800
    ds.is_little_endian = True
    ds.is_implicit_VR = False
    ds.PixelData = pixel_array.tobytes()

    output_path = output_dir / f"case_{case_idx:03d}.dcm"
    ds.save_as(output_path)
    return output_path


def _make_decision_tree(
    case_idx: int, dicom_path: Path, overrides: dict | None = None
) -> dict:
    """Generate synthetic Decision-Tree for the DICOM.

    Args:
        case_idx: Numeric index used as default RNG seed.
        dicom_path: Path to the corresponding DICOM file (used for case_id salt).
        overrides: Optional dict with deterministic values for star cases.
            Supported keys: ``ai_stenosis``, ``physician_stenosis``, ``confidence``,
            ``vulnerability_markers``, ``confirmed_markers``, ``rejected_markers``,
            ``added_markers``, ``confidence_self_reported``, ``trust_score``,
            ``verdict``, ``reasoning``, ``seed``.
    """
    overrides = overrides or {}
    rng = random.Random(overrides.get("seed", case_idx))
    salt_input = f"{dicom_path.stem}|{SALT}|2026-W18"
    case_id = hashlib.sha256(salt_input.encode()).hexdigest()
    role_salt_input = f"demo-attending|{SALT}"
    role_hash = hashlib.sha256(role_salt_input.encode()).hexdigest()

    ai_stenosis = overrides.get("ai_stenosis", round(rng.uniform(20, 90), 1))
    physician_stenosis = overrides.get(
        "physician_stenosis",
        ai_stenosis + rng.choice([-5, -2, 0, 2, 3, 5]),
    )
    physician_stenosis = max(0, min(100, physician_stenosis))
    delta = round(physician_stenosis - ai_stenosis, 1)

    if "verdict" in overrides:
        verdict = overrides["verdict"]
    else:
        verdict = (
            "full_agreement"
            if abs(delta) < 1
            else "partial_agreement" if abs(delta) < 5 else "disagreement"
        )

    if "confirmed_markers" in overrides:
        confirmed = overrides["confirmed_markers"]
    else:
        confirmed = rng.sample(_MARKERS_POOL, k=rng.randint(0, 3))

    if "rejected_markers" in overrides:
        rejected = overrides["rejected_markers"]
    else:
        rejected = [
            m for m in _MARKERS_POOL if m not in confirmed and rng.random() < 0.2
        ]

    added = overrides.get("added_markers", [])

    if "vulnerability_markers" in overrides:
        vulnerability_markers = overrides["vulnerability_markers"]
    else:
        vulnerability_markers = {m: round(rng.uniform(0, 1), 2) for m in _MARKERS_POOL}

    confidence = overrides.get("confidence", round(rng.uniform(0.65, 0.95), 2))

    if "confidence_self_reported" in overrides:
        confidence_self_reported = overrides["confidence_self_reported"]
    else:
        confidence_self_reported = rng.choice(["low", "medium", "high", None])

    if "trust_score" in overrides:
        trust_score = overrides["trust_score"]
    else:
        trust_score = rng.randint(2, 5)

    if "reasoning" in overrides:
        reasoning = overrides["reasoning"]
    elif rng.random() >= 0.3:
        reasoning = {
            "deciding_feature": rng.choice(_DECIDING_FEATURES),
            "ruled_out": [],
            "ruled_out_reason": "",
            "would_consult": None,
            "would_re_image_if": None,
        }
    else:
        reasoning = None

    return {
        "case_id": case_id,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "physician_role_hash": role_hash,
        "ai_prediction": {
            "stenosis_pct_nascet": ai_stenosis,
            "confidence": confidence,
            "vulnerability_markers": vulnerability_markers,
            "model_version": "v0.1.0",
            "model_sha": hashlib.sha256(b"demo-model-v0.1.0").hexdigest(),
        },
        "physician_decision": {
            "stenosis_pct_nascet": physician_stenosis,
            "confidence_self_reported": confidence_self_reported,
            "confirmed_markers": confirmed,
            "rejected_markers": rejected,
            "added_markers": added,
        },
        "reasoning": reasoning,
        "agreement_with_ai": {
            "verdict": verdict,
            "delta_pct": delta,
            "delta_markers": [],
            "trust_score_for_this_case": trust_score,
        },
        "anonymisation": {
            "method": "DICOM_PS_3.15_basic",
            "salt_version": "v2026-04",
            "audit_id": f"DEMO-{case_idx:03d}",
            "k_anonymity_min": 5,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate synthetic anonymized DICOMs + decision-trees for demo."
    )
    parser.add_argument(
        "--output-dir",
        default=Path("data/demo"),
        type=Path,
        help="Output directory (default: data/demo)",
    )
    parser.add_argument("--count", type=int, default=30)
    parser.add_argument(
        "--star-only",
        action="store_true",
        help="Generate only the 5 deterministic star examples (overrides --count)",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    dicoms_dir = args.output_dir / "dicoms"
    trees_dir = args.output_dir / "decision_trees"
    dicoms_dir.mkdir(exist_ok=True)
    trees_dir.mkdir(exist_ok=True)

    if args.star_only:
        indices = list(range(len(_STAR_SCENARIOS)))
    else:
        indices = list(range(args.count))

    for i in indices:
        star = _STAR_SCENARIOS[i] if i < len(_STAR_SCENARIOS) else None
        dicom_overrides = star.get("dicom") if star else None
        tree_overrides = star.get("tree") if star else None

        dicom_path = _make_dicom(i, dicoms_dir, overrides=dicom_overrides)
        tree = _make_decision_tree(i, dicom_path, overrides=tree_overrides)
        tree_path = trees_dir / f"case_{i:03d}.json"
        tree_path.write_text(json.dumps(tree, indent=2), encoding="utf-8")
        print(f"  generated case_{i:03d} -> {dicom_path.name} + {tree_path.name}")

    count = len(indices)
    print(f"\nDemo data ready in {args.output_dir}")
    print(f"  dicoms/          ({count} files)")
    print(f"  decision_trees/  ({count} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
