"""MONAI-based dataset for MFSD-UNet training.

Expects the data directory to contain:
  data/
    images/   *.dcm  (CTA slices — anonymised)
    masks/    *.nii.gz  (manual segmentation labels)
    labels.csv  (case_hash, stenosis_pct_nascet, iph, thin_cap, lrnc, motion)

Splits: 70% train / 15% val / 15% test  (stratified by stenosis severity bucket).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pydicom
import torch
from monai.transforms import (
    Compose,
    EnsureChannelFirstd,
    EnsureTyped,
    NormalizeIntensityd,
    RandAffined,
    RandFlipd,
    RandGaussianNoised,
    RandScaleIntensityd,
    Resized,
    ToTensord,
)
from torch.utils.data import Dataset


@dataclass
class CaseMeta:
    case_hash: str
    dcm_path: Path
    mask_path: Path
    stenosis_pct: float
    vuln: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0])


def _load_labels(csv_path: Path) -> dict[str, dict]:
    result: dict[str, dict] = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            result[row["case_hash"]] = row
    return result


def _build_cases(data_root: Path) -> list[CaseMeta]:
    img_dir = data_root / "images"
    mask_dir = data_root / "masks"
    labels = _load_labels(data_root / "labels.csv")

    cases = []
    for dcm_path in sorted(img_dir.glob("*.dcm")):
        h = dcm_path.stem
        mask_path = mask_dir / f"{h}.nii.gz"
        if not mask_path.exists() or h not in labels:
            continue
        row = labels[h]
        cases.append(
            CaseMeta(
                case_hash=h,
                dcm_path=dcm_path,
                mask_path=mask_path,
                stenosis_pct=float(row["stenosis_pct_nascet"]),
                vuln=[
                    float(row.get("iph", 0)),
                    float(row.get("thin_cap", 0)),
                    float(row.get("lrnc", 0)),
                    float(row.get("motion", 0)),
                ],
            )
        )
    return cases


def _stratified_split(
    cases: list[CaseMeta],
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    seed: int = 42,
) -> tuple[list[CaseMeta], list[CaseMeta], list[CaseMeta]]:
    rng = np.random.default_rng(seed)

    # Bucket by severity: low (<50), moderate (50-70), severe (>70)
    buckets: dict[str, list[CaseMeta]] = {"low": [], "mod": [], "sev": []}
    for c in cases:
        if c.stenosis_pct < 50:
            buckets["low"].append(c)
        elif c.stenosis_pct <= 70:
            buckets["mod"].append(c)
        else:
            buckets["sev"].append(c)

    train, val, test = [], [], []
    for bucket in buckets.values():
        arr = rng.permuted(bucket)
        n = len(arr)
        t_end = int(n * train_ratio)
        v_end = t_end + int(n * val_ratio)
        train.extend(arr[:t_end])
        val.extend(arr[t_end:v_end])
        test.extend(arr[v_end:])

    return list(train), list(val), list(test)


_TRAIN_TRANSFORMS = Compose(
    [
        EnsureChannelFirstd(keys=["image", "mask"]),
        Resized(keys=["image", "mask"], spatial_size=(512, 512)),
        NormalizeIntensityd(keys=["image"]),
        RandFlipd(keys=["image", "mask"], spatial_axis=1, prob=0.5),
        RandAffined(
            keys=["image", "mask"],
            rotate_range=(0.1,),
            scale_range=(0.1,),
            prob=0.5,
            mode=("bilinear", "nearest"),
        ),
        RandGaussianNoised(keys=["image"], prob=0.2, std=0.05),
        RandScaleIntensityd(keys=["image"], factors=0.1, prob=0.3),
        EnsureTyped(keys=["image", "mask"]),
        ToTensord(keys=["image", "mask"]),
    ]
)

_EVAL_TRANSFORMS = Compose(
    [
        EnsureChannelFirstd(keys=["image", "mask"]),
        Resized(keys=["image", "mask"], spatial_size=(512, 512)),
        NormalizeIntensityd(keys=["image"]),
        EnsureTyped(keys=["image", "mask"]),
        ToTensord(keys=["image", "mask"]),
    ]
)


class CarotisDataset(Dataset):
    def __init__(self, cases: list[CaseMeta], train: bool = True) -> None:
        self.cases = cases
        self.transforms = _TRAIN_TRANSFORMS if train else _EVAL_TRANSFORMS

    def __len__(self) -> int:
        return len(self.cases)

    def __getitem__(self, idx: int) -> dict:
        case = self.cases[idx]

        # Load DICOM
        ds = pydicom.dcmread(str(case.dcm_path))
        image = ds.pixel_array.astype(np.float32)

        # Load mask (nibabel or monai)
        import nibabel as nib

        nii = nib.load(str(case.mask_path))
        mask = nii.get_fdata().astype(np.float32)
        if mask.ndim == 3:
            mask = mask[:, :, 0]  # take first slice if 3D

        data = {"image": image, "mask": mask}
        data = self.transforms(data)

        return {
            "image": data["image"],
            "mask": data["mask"],
            "stenosis": torch.tensor([case.stenosis_pct], dtype=torch.float32),
            "vuln": torch.tensor(case.vuln, dtype=torch.float32),
            "case_hash": case.case_hash,
        }


def build_dataloaders(
    data_root: str | Path,
    batch_size: int = 4,
    num_workers: int = 4,
    seed: int = 42,
):
    """Return (train_loader, val_loader, test_loader)."""
    from torch.utils.data import DataLoader

    cases = _build_cases(Path(data_root))
    train_cases, val_cases, test_cases = _stratified_split(cases, seed=seed)

    train_loader = DataLoader(
        CarotisDataset(train_cases, train=True),
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
    )
    val_loader = DataLoader(
        CarotisDataset(val_cases, train=False),
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
    )
    test_loader = DataLoader(
        CarotisDataset(test_cases, train=False),
        batch_size=1,
        shuffle=False,
        num_workers=num_workers,
    )
    return train_loader, val_loader, test_loader
