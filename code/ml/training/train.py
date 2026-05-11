from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path
from typing import Any

import mlflow
import numpy as np
import torch
import torch.nn as nn
import yaml
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts, LinearLR
from torch.utils.data import ConcatDataset, DataLoader, Subset
from torch.amp import autocast, GradScaler

from ml.data.dataset import CarotisDataset
from ml.data.transforms import get_train_transforms, get_val_transforms
from ml.models.mfsd_unet import MFSDUNet
from ml.training.losses import CarotisCompositeLoss


def set_seed(seed: int) -> None:
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.use_deterministic_algorithms(True, warn_only=True)


def load_config(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _prepare_batch(
    batch: dict, device: torch.device
) -> tuple[torch.Tensor, dict[str, Any]]:
    images = batch["image"].to(device)
    # Dummy mask: segmentation target not present in K-10 dataset skeleton
    mask = torch.zeros_like(images[:, :1, :, :])
    targets: dict[str, Any] = {
        "mask": mask.to(device),
        "stenosis_pct": batch["stenosis"].to(device).float(),
        "vulnerability_4d": batch["vulnerability"].to(device),
        "deciding_feature_label": batch["deciding_feature_label"].to(device),
    }
    rrm = batch.get("reasoning_region_mask")
    if rrm is not None:
        targets["reasoning_region_mask"] = rrm.to(device)
    return images, targets


def _train_epoch(
    model: nn.Module,
    loader: DataLoader,
    loss_fn: CarotisCompositeLoss,
    optimizer: AdamW,
    device: torch.device,
    scaler: GradScaler | None = None,
    grad_clip: float = 1.0,
) -> tuple[float, dict[str, float]]:
    model.train()
    total_loss = 0.0
    for batch in loader:
        images, targets = _prepare_batch(batch, device)
        optimizer.zero_grad()

        if scaler is not None:
            with autocast(device_type=str(device)):
                preds = model(images)
                loss, _ = loss_fn(preds, targets)
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
            scaler.step(optimizer)
            scaler.update()
        else:
            preds = model(images)
            loss, _ = loss_fn(preds, targets)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
            optimizer.step()

        total_loss += loss.item()
    return total_loss / max(len(loader), 1), {}


def _validate(
    model: nn.Module,
    loader: DataLoader,
    loss_fn: CarotisCompositeLoss,
    device: torch.device,
) -> tuple[float, dict[str, float]]:
    model.eval()
    total_loss = 0.0
    composite_val = 0.0
    with torch.no_grad():
        for batch in loader:
            images, targets = _prepare_batch(batch, device)
            preds = model(images)
            loss, metrics = loss_fn(preds, targets)
            total_loss += loss.item()
            composite_val += metrics["total"].item()
    n = max(len(loader), 1)
    return total_loss / n, {
        "composite": composite_val / n,
        "loss": total_loss / n,
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Train MFSD-UNet")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--resume", type=Path, default=None)
    parser.add_argument("--incremental", action="store_true")
    parser.add_argument("--max-epochs", type=int, default=100)
    parser.add_argument("--early-stopping-patience", type=int, default=10)
    parser.add_argument("--output-dir", type=Path, default=Path("checkpoints"))
    args = parser.parse_args(argv)

    config = load_config(args.config)
    set_seed(config.get("seed", 42))

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Datasets
    train_ds = CarotisDataset(
        root_dir=Path(config["data_root"]),
        manifest_csv=Path(config["manifest_csv"]),
        transform=get_train_transforms(),
        mode="train",
    )
    val_ds = CarotisDataset(
        root_dir=Path(config["data_root"]),
        manifest_csv=Path(config["manifest_csv"]),
        transform=get_val_transforms(),
        mode="val",
    )

    if args.incremental:
        hist_root = Path(config.get("historical_data_root", config["data_root"]))
        hist_manifest = Path(
            config.get("historical_manifest_csv", config["manifest_csv"])
        )
        hist_ds = CarotisDataset(
            root_dir=hist_root,
            manifest_csv=hist_manifest,
            transform=get_train_transforms(),
            mode="train",
        )
        hist_size = min(len(hist_ds), len(train_ds))
        hist_indices = torch.randperm(len(hist_ds))[:hist_size].tolist()
        hist_subset = Subset(hist_ds, hist_indices)
        train_ds = ConcatDataset([train_ds, hist_subset])

    train_loader = DataLoader(
        train_ds,
        batch_size=config["batch_size"],
        shuffle=True,
        num_workers=config["num_workers"],
        persistent_workers=config["num_workers"] > 0,
        pin_memory=device.type == "cuda",
        prefetch_factor=2 if config["num_workers"] > 0 else None,
    )
    val_loader = DataLoader(
        val_ds,
        batch_size=config["batch_size"],
        shuffle=False,
        num_workers=config["num_workers"],
        persistent_workers=config["num_workers"] > 0,
        pin_memory=device.type == "cuda",
    )

    model = MFSDUNet(
        in_channels=1,
        base_filters=32,
        num_features_classes=12,
    ).to(device)

    # PyTorch 2.x compile for faster training (CPU fallback gracefully)
    if hasattr(torch, "compile") and device.type == "cuda":
        try:
            model = torch.compile(model, mode="reduce-overhead")
            print("[train] torch.compile enabled")
        except Exception as exc:
            print(f"[train] torch.compile skipped: {exc}")

    if args.resume:
        model.load_state_dict(torch.load(args.resume, map_location=device, weights_only=True))

    loss_fn = CarotisCompositeLoss(
        alpha=config.get("alpha", 1.0),
        beta=config.get("beta", 0.5),
        gamma=config.get("gamma", 0.3),
    )
    optimizer = AdamW(
        model.parameters(),
        lr=config["lr"],
        weight_decay=1e-4,
    )

    # Warmup + cosine annealing scheduler
    warmup_epochs = config.get("warmup_epochs", 5)
    total_epochs = args.max_epochs
    warmup_scheduler = LinearLR(
        optimizer, start_factor=0.01, end_factor=1.0, total_iters=warmup_epochs
    )
    cosine_scheduler = CosineAnnealingWarmRestarts(
        optimizer, T_0=max(total_epochs - warmup_epochs, 10), T_mult=2
    )
    scheduler = torch.optim.lr_scheduler.SequentialLR(
        optimizer,
        schedulers=[warmup_scheduler, cosine_scheduler],
        milestones=[warmup_epochs],
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    best_val_composite = float("-inf")
    patience_counter = 0
    base_model_composite: float | None = None
    scaler = GradScaler() if device.type == "cuda" else None
    grad_clip = config.get("grad_clip", 1.0)

    if args.incremental:
        test_manifest = Path(config.get("test_manifest_csv", config["manifest_csv"]))
        test_ds = CarotisDataset(
            root_dir=Path(config["data_root"]),
            manifest_csv=test_manifest,
            transform=get_val_transforms(),
            mode="test",
        )
        test_loader = DataLoader(
            test_ds,
            batch_size=config["batch_size"],
            shuffle=False,
            num_workers=config["num_workers"],
        )
        _, base_metrics = _validate(model, test_loader, loss_fn, device)
        base_model_composite = base_metrics["composite"]
        print(f"Base model composite: {base_model_composite:.4f}")

    mlflow.start_run()
    mlflow.log_params(config)
    mlflow.log_artifact(str(args.config))

    for epoch in range(1, args.max_epochs + 1):
        train_loss, _ = _train_epoch(
            model, train_loader, loss_fn, optimizer, device, scaler, grad_clip
        )
        val_loss, val_metrics = _validate(model, val_loader, loss_fn, device)
        scheduler.step()

        mlflow.log_metrics(
            {
                "train_loss": train_loss,
                "val_loss": val_loss,
                "val_composite": val_metrics["composite"],
                "lr": optimizer.param_groups[0]["lr"],
            },
            step=epoch,
        )
        print(
            f"Epoch {epoch}: train_loss={train_loss:.4f} "
            f"val_composite={val_metrics['composite']:.4f}"
        )

        if val_metrics["composite"] > best_val_composite:
            best_val_composite = val_metrics["composite"]
            patience_counter = 0
            ckpt_path = output_dir / "best.pt"
            torch.save(
                {
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "scheduler_state_dict": scheduler.state_dict(),
                    "scaler_state_dict": scaler.state_dict() if scaler else None,
                    "best_val_composite": best_val_composite,
                    "config": config,
                },
                ckpt_path,
            )
            mlflow.log_artifact(str(ckpt_path))
        else:
            patience_counter += 1

        # Periodic checkpoint every 10 epochs for resume safety
        if epoch % 10 == 0:
            periodic_path = output_dir / f"epoch_{epoch:03d}.pt"
            torch.save(
                {
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "scheduler_state_dict": scheduler.state_dict(),
                    "scaler_state_dict": scaler.state_dict() if scaler else None,
                    "best_val_composite": best_val_composite,
                    "config": config,
                },
                periodic_path,
            )

        if args.incremental and base_model_composite is not None:
            if val_metrics["composite"] < base_model_composite - 0.005:
                mlflow.log_metric("rollback_triggered", 1, step=epoch)
                print("ROLLBACK TRIGGERED: new model worse than base")
                mlflow.end_run()
                return  # Graceful exit instead of sys.exit

        if patience_counter >= args.early_stopping_patience:
            print(f"Early stopping at epoch {epoch}")
            break

    mlflow.end_run()
    print("Training finished")


if __name__ == "__main__":
    main()
