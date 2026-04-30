from __future__ import annotations

import argparse
from pathlib import Path

import torch

from ml.inference.onnx_export import export
from ml.models.mfsd_unet import MFSDUNet


def test_export_and_verify(tmp_path: Path):
    # Mini-Modell fuer Speed
    model = MFSDUNet(in_channels=1, base_filters=8, num_features_classes=12)
    checkpoint = tmp_path / "mini.ckpt"
    torch.save(model.state_dict(), checkpoint)

    output = tmp_path / "mini.onnx"
    args = argparse.Namespace(
        checkpoint=str(checkpoint), output=str(output), calibration_pkl=None
    )
    export(args)

    assert output.exists()
    assert output.stat().st_size > 0
