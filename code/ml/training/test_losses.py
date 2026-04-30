from __future__ import annotations

import torch

from ml.training.losses import CarotisCompositeLoss


def _make_tensors(batch_size: int = 2):
    return {
        "predictions": {
            "segmentation": torch.randn(batch_size, 1, 512, 512),
            "stenosis": torch.randn(batch_size, 1),
            "vulnerability": torch.randn(batch_size, 4),
            "deciding_feature": torch.randn(batch_size, 12),
            "side_outputs": [torch.randn(batch_size, 1, 512, 512) for _ in range(3)],
        },
        "targets": {
            "mask": torch.randint(0, 2, (batch_size, 1, 512, 512)).float(),
            "stenosis_pct": torch.rand(batch_size),
            "vulnerability_4d": torch.rand(batch_size, 4),
            "deciding_feature_label": torch.randint(0, 12, (batch_size,)),
            "reasoning_region_mask": torch.rand(batch_size, 1, 512, 512),
        },
    }


def test_happy_path():
    loss_fn = CarotisCompositeLoss()
    tensors = _make_tensors()
    total, metrics = loss_fn(tensors["predictions"], tensors["targets"])

    assert total.item() > 0.0
    assert total.requires_grad
    total.backward()
    assert metrics["dice"] >= 0
    assert metrics["stenosis_mse"] >= 0
    assert metrics["vulnerability_bce"] >= 0
    assert metrics["reasoning_align"] >= 0
    assert metrics["feature_ce"] >= 0
    assert metrics["deep_super"] >= 0


def test_reasoning_mask_none():
    loss_fn = CarotisCompositeLoss(gamma=0.3)
    tensors = _make_tensors()
    del tensors["targets"]["reasoning_region_mask"]

    total, metrics = loss_fn(tensors["predictions"], tensors["targets"])
    assert metrics["reasoning_align"].item() == 0.0
    assert total.item() > 0.0


def test_gamma_zero():
    loss_fn = CarotisCompositeLoss(gamma=0.0)
    tensors = _make_tensors()

    total, metrics = loss_fn(tensors["predictions"], tensors["targets"])
    assert metrics["reasoning_align"].item() == 0.0
    # Total should not include alignment term
    expected_without_align = (
        loss_fn.alpha * (metrics["dice"] + metrics["stenosis_mse"])
        + loss_fn.beta * metrics["vulnerability_bce"]
        + loss_fn.feature_weight * metrics["feature_ce"]
        + loss_fn.deep_super_weight * metrics["deep_super"]
    )
    torch.testing.assert_close(metrics["total"], expected_without_align)


def test_perfect_prediction():
    """Loss should be very small when predictions match targets exactly."""
    loss_fn = CarotisCompositeLoss()
    batch_size = 2
    mask = torch.ones(batch_size, 1, 512, 512)

    preds = {
        "segmentation": torch.ones(batch_size, 1, 512, 512) * 10.0,
        "stenosis": torch.tensor([[50.0], [50.0]]),
        "vulnerability": torch.ones(batch_size, 4) * 10.0,
        "deciding_feature": torch.zeros(batch_size, 12).scatter_(
            1, torch.zeros(batch_size, 1).long(), 10.0
        ),
        "side_outputs": [torch.ones(batch_size, 1, 512, 512) * 10.0 for _ in range(3)],
    }
    targets = {
        "mask": mask,
        "stenosis_pct": torch.tensor([50.0, 50.0]),
        "vulnerability_4d": torch.ones(batch_size, 4),
        "deciding_feature_label": torch.zeros(batch_size).long(),
        "reasoning_region_mask": mask,
    }

    total, metrics = loss_fn(preds, targets)
    assert total.item() < 0.5
    assert metrics["dice"].item() < 0.1
    assert metrics["stenosis_mse"].item() < 0.1
    assert metrics["vulnerability_bce"].item() < 0.1
    assert metrics["feature_ce"].item() < 0.1
