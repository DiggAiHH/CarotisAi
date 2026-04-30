from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F
from timm.models.swin_transformer import SwinTransformerBlock


class ConvBlock(nn.Module):
    """Doppel-Conv mit BatchNorm + ReLU."""

    def __init__(self, in_ch: int, out_ch: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1, bias=False),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1, bias=False),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.block(x)


class MFSDUNet(nn.Module):
    """
    Multi-Scale Feature with Swin Deep-Supervision UNet.

    Inputs:  (B, 1, 512, 512)
    Outputs: dict with
        - segmentation: (B, 1, 512, 512) Vessel-Maske, Sigmoid
        - stenosis:     (B, 1) NASCET % regression
        - vulnerability:(B, 4) IPH / ThinCap / LRNC / SystolicMotion
        - deciding_feature: (B, 12) Klassifikations-Logits
        - side_outputs: list of 3 (B,1,H,W) fuer Deep-Supervision
    """

    def __init__(
        self,
        in_channels: int = 1,
        base_filters: int = 32,
        num_features_classes: int = 12,
    ) -> None:
        super().__init__()

        # Encoder: 4 Stufen
        self.enc1 = ConvBlock(in_channels, base_filters)  # 512x512
        self.enc2 = ConvBlock(base_filters, base_filters * 2)  # 256x256
        self.enc3 = ConvBlock(base_filters * 2, base_filters * 4)  # 128x128
        self.enc4 = ConvBlock(base_filters * 4, base_filters * 8)  # 64x64
        self.pool = nn.MaxPool2d(2)

        # Bottleneck: Swin-Transformer-Block
        self.swin = SwinTransformerBlock(
            dim=base_filters * 8,
            num_heads=8,
            window_size=8,  # 64 / 8 = 8
            shift_size=0,
        )
        self.bn_proj = nn.Conv2d(base_filters * 8, base_filters * 16, 1)

        # Decoder
        self.up3 = nn.ConvTranspose2d(base_filters * 16, base_filters * 8, 2, stride=2)
        self.dec3 = ConvBlock(base_filters * 16, base_filters * 8)
        self.up2 = nn.ConvTranspose2d(base_filters * 8, base_filters * 4, 2, stride=2)
        self.dec2 = ConvBlock(base_filters * 8, base_filters * 4)
        self.up1 = nn.ConvTranspose2d(base_filters * 4, base_filters * 2, 2, stride=2)
        self.dec1 = ConvBlock(base_filters * 4, base_filters * 2)
        self.up0 = nn.ConvTranspose2d(base_filters * 2, base_filters, 2, stride=2)
        self.dec0 = ConvBlock(base_filters * 2, base_filters)

        # Heads
        self.seg_head = nn.Conv2d(base_filters, 1, 1)
        self.gap = nn.AdaptiveAvgPool2d(1)
        self.stenosis_head = nn.Sequential(
            nn.Linear(base_filters * 16, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )
        self.vuln_head = nn.Sequential(
            nn.Linear(base_filters * 16, 64),
            nn.ReLU(),
            nn.Linear(64, 4),  # 4 Marker, BCEWithLogits in Loss
        )
        self.feat_head = nn.Sequential(
            nn.Linear(base_filters * 16, 64),
            nn.ReLU(),
            nn.Linear(64, num_features_classes),
        )

        # Deep-Supervision Side-Outputs
        self.side3 = nn.Conv2d(base_filters * 8, 1, 1)
        self.side2 = nn.Conv2d(base_filters * 4, 1, 1)
        self.side1 = nn.Conv2d(base_filters * 2, 1, 1)

    def forward(self, x: torch.Tensor) -> dict[str, torch.Tensor | list[torch.Tensor]]:
        # Encoder
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))
        e4 = self.enc4(self.pool(e3))

        # Bottleneck
        b = self.pool(e4)  # (B, 256, 32, 32) bei base_filters=32
        B, C, H, W = b.shape
        b_flat = b.flatten(2).transpose(1, 2)  # (B, H*W, C)
        b_swin = self.swin(b_flat)
        b = b_swin.transpose(1, 2).reshape(B, C, H, W)
        b = self.bn_proj(b)

        # Decoder
        d3 = self.dec3(torch.cat([self.up3(b), e4], dim=1))
        d2 = self.dec2(torch.cat([self.up2(d3), e3], dim=1))
        d1 = self.dec1(torch.cat([self.up1(d2), e2], dim=1))
        d0 = self.dec0(torch.cat([self.up0(d1), e1], dim=1))

        # Heads
        seg = self.seg_head(d0)  # (B, 1, 512, 512)
        gap = self.gap(b).flatten(1)  # (B, base_filters*16)

        return {
            "segmentation": seg,
            "stenosis": self.stenosis_head(gap),
            "vulnerability": self.vuln_head(gap),
            "deciding_feature": self.feat_head(gap),
            "side_outputs": [
                F.interpolate(
                    self.side3(d3),
                    size=512,
                    mode="bilinear",
                    align_corners=False,
                ),
                F.interpolate(
                    self.side2(d2),
                    size=512,
                    mode="bilinear",
                    align_corners=False,
                ),
                F.interpolate(
                    self.side1(d1),
                    size=512,
                    mode="bilinear",
                    align_corners=False,
                ),
            ],
        }


def count_parameters(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


if __name__ == "__main__":
    m = MFSDUNet()
    print(f"Params: {count_parameters(m):,}")
    x = torch.randn(2, 1, 512, 512)
    out = m(x)
    for k, v in out.items():
        if isinstance(v, list):
            print(f"{k}: list of {len(v)} tensors, shape {v[0].shape}")
        else:
            print(f"{k}: {v.shape}")
