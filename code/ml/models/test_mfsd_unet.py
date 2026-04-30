from __future__ import annotations

import torch

from ml.models.mfsd_unet import MFSDUNet, count_parameters


def test_forward_shapes():
    model = MFSDUNet(in_channels=1, base_filters=32, num_features_classes=12)
    x = torch.randn(1, 1, 512, 512)
    out = model(x)

    assert out["segmentation"].shape == (1, 1, 512, 512)
    assert out["stenosis"].shape == (1, 1)
    assert out["vulnerability"].shape == (1, 4)
    assert out["deciding_feature"].shape == (1, 12)
    assert len(out["side_outputs"]) == 3
    for side in out["side_outputs"]:
        assert side.shape == (1, 1, 512, 512)


def test_parameter_count():
    model = MFSDUNet(in_channels=1, base_filters=32, num_features_classes=12)
    params = count_parameters(model)
    assert (
        10_000_000 < params < 80_000_000
    ), f"Param count {params} out of expected range"


def test_backward():
    model = MFSDUNet(in_channels=1, base_filters=32, num_features_classes=12)
    x = torch.randn(1, 1, 512, 512)
    out = model(x)

    loss = (
        out["segmentation"].sum()
        + out["stenosis"].sum()
        + out["vulnerability"].sum()
        + out["deciding_feature"].sum()
    )
    loss.backward()

    for name, param in model.named_parameters():
        if param.requires_grad and param.grad is not None:
            assert not torch.isnan(param.grad).any(), f"NaN gradient in {name}"
