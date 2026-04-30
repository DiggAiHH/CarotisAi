from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pydicom
import pytest
import yaml

from ml.training.train import main


def _write_mock_dicom(path: Path, rows: int = 256, cols: int = 256) -> None:
    ds = pydicom.Dataset()
    ds.PatientName = "Synthetic"
    ds.Rows = rows
    ds.Columns = cols
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.PixelRepresentation = 0
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelData = np.zeros((rows, cols), dtype=np.uint16).tobytes()
    ds.is_little_endian = True
    ds.is_implicit_VR = False
    pydicom.dcmwrite(str(path), ds)


def _make_manifest(tmp_path: Path, prefix: str = "case", bad: bool = False) -> Path:
    dicom_dir = tmp_path / "dicoms"
    dicom_dir.mkdir(exist_ok=True)
    samples = []
    for i in range(10):
        dcm_path = dicom_dir / f"{prefix}_{i:02d}.dcm"
        if not dcm_path.exists():
            _write_mock_dicom(dcm_path)
        stenosis = str(100.0 if bad else i * 10.0)
        samples.append(
            {
                "case_id": f"{i:064x}",
                "anonymized_path": str(dcm_path.relative_to(tmp_path)),
                "stenosis_pct_nascet": stenosis,
                "vuln_iph": "0.5" if i % 2 == 0 else "0.0",
                "vuln_thincap": "0.2",
                "vuln_lrnc": "0.3",
                "vuln_sma": "0.1",
                "deciding_feature_label": str(i % 12),
            }
        )
    manifest = tmp_path / f"manifest_{'bad' if bad else 'good'}.csv"
    with open(manifest, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=samples[0].keys())
        writer.writeheader()
        writer.writerows(samples)
    return manifest


@pytest.fixture
def good_config(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("MLFLOW_TRACKING_URI", f"file://{tmp_path / 'mlruns'}")
    good_manifest = _make_manifest(tmp_path, bad=False)
    config = {
        "seed": 42,
        "data_root": str(tmp_path),
        "manifest_csv": str(good_manifest),
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
    return tmp_path, config_path


def test_one_epoch_runs(good_config):
    tmp_path, config_path = good_config
    main(
        [
            "--config",
            str(config_path),
            "--max-epochs",
            "1",
            "--early-stopping-patience",
            "1",
            "--output-dir",
            str(tmp_path / "checkpoints"),
        ]
    )


def test_incremental_rollback(good_config):
    tmp_path, config_path = good_config
    bad_manifest = _make_manifest(tmp_path, prefix="bad", bad=True)

    # Use bad manifest for training, good manifest for base-test
    config = {
        "seed": 42,
        "data_root": str(tmp_path),
        "manifest_csv": str(bad_manifest),
        "test_manifest_csv": str(tmp_path / "manifest_good.csv"),
        "historical_data_root": str(tmp_path),
        "historical_manifest_csv": str(bad_manifest),
        "val_split": 0.2,
        "alpha": 1.0,
        "beta": 0.5,
        "gamma": 0.0,
        "lr": 1e-2,
        "batch_size": 2,
        "num_workers": 0,
    }
    bad_config_path = tmp_path / "config_bad.yaml"
    with open(bad_config_path, "w") as f:
        yaml.dump(config, f)

    with pytest.raises(SystemExit) as exc_info:
        main(
            [
                "--config",
                str(bad_config_path),
                "--incremental",
                "--max-epochs",
                "1",
                "--early-stopping-patience",
                "1",
                "--output-dir",
                str(tmp_path / "checkpoints_bad"),
            ]
        )
    assert exc_info.value.code == 1
