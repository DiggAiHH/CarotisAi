from __future__ import annotations

import csv
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pydicom
import pytest
import yaml


def _write_mock_dicom(path: Path) -> None:
    ds = pydicom.Dataset()
    ds.PatientName = "Synthetic"
    ds.Rows = 256
    ds.Columns = 256
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.PixelRepresentation = 0
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelData = np.zeros((256, 256), dtype=np.uint16).tobytes()
    pydicom.dcmwrite(str(path), ds, little_endian=True, implicit_vr=False)


def _make_manifest(tmp_path: Path) -> Path:
    dicom_dir = tmp_path / "dicoms"
    dicom_dir.mkdir(exist_ok=True)
    samples = []
    for i in range(10):
        dcm_path = dicom_dir / f"case_{i:02d}.dcm"
        _write_mock_dicom(dcm_path)
        samples.append(
            {
                "case_id": f"{i:064x}",
                "anonymized_path": str(dcm_path.relative_to(tmp_path)),
                "stenosis_pct_nascet": str(i * 10.0),
                "vuln_iph": "0.5",
                "vuln_thincap": "0.2",
                "vuln_lrnc": "0.3",
                "vuln_sma": "0.1",
                "deciding_feature_label": str(i % 12),
            }
        )
    manifest = tmp_path / "manifest.csv"
    with open(manifest, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=samples[0].keys())
        writer.writeheader()
        writer.writerows(samples)
    return manifest


def test_train_one_epoch(tmp_path: Path, monkeypatch):
    pytest.importorskip("torch")
    pytest.importorskip("mlflow")
    monkeypatch.setenv("MLFLOW_TRACKING_URI", f"file://{tmp_path / 'mlruns'}")
    manifest = _make_manifest(tmp_path)
    config = {
        "seed": 42,
        "data_root": str(tmp_path),
        "manifest_csv": str(manifest),
        "val_split": 0.2,
        "alpha": 1.0,
        "beta": 0.5,
        "gamma": 0.0,
        "lr": 1e-4,
        "batch_size": 2,
        "num_workers": 0,
    }
    config_path = tmp_path / "config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(config, f)

    env = os.environ.copy()
    env["PYTHONPATH"] = "code"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "ml.training.train",
            "--config",
            str(config_path),
            "--max-epochs",
            "1",
            "--early-stopping-patience",
            "1",
            "--output-dir",
            str(tmp_path / "ckpt"),
        ],
        check=True,
        env=env,
    )


def test_export_onnx_roundtrip(tmp_path: Path):
    torch = pytest.importorskip("torch")
    pytest.importorskip("mlflow")
    from ml.models.mfsd_unet import MFSDUNet

    model = MFSDUNet(in_channels=1, base_filters=8, num_features_classes=12)
    checkpoint = tmp_path / "mini.ckpt"

    torch.save(model.state_dict(), checkpoint)

    env = os.environ.copy()
    env["PYTHONPATH"] = "code"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "ml.inference.onnx_export",
            "--checkpoint",
            str(checkpoint),
            "--output",
            str(tmp_path / "mini.onnx"),
        ],
        check=True,
        env=env,
    )
