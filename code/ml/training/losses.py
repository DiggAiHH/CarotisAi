from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F
from monai.losses import DiceLoss


class CarotisCompositeLoss(nn.Module):
    """
    Loss = α·dice + α·stenosis_mse + β·vuln_bce + γ·reasoning_align
         + 0.2·feature_ce + 0.1·deep_supervision

    γ wird empirisch via hyperparam-search getuned (siehe
    scripts/hp_search.py). γ=0 schaltet Reasoning-Alignment-Loss aus
    (Fallback fuer Notfaelle).
    """

    def __init__(
        self,
        alpha: float = 1.0,
        beta: float = 0.5,
        gamma: float = 0.3,
        feature_weight: float = 0.2,
        deep_super_weight: float = 0.1,
    ) -> None:
        super().__init__()
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.feature_weight = feature_weight
        self.deep_super_weight = deep_super_weight
        self.dice = DiceLoss(sigmoid=True)
        self.bce = nn.BCEWithLogitsLoss()
        self.mse = nn.MSELoss()
        self.ce = nn.CrossEntropyLoss()

    def forward(
        self, predictions: dict, targets: dict
    ) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        l_dice = self.dice(predictions["segmentation"], targets["mask"])
        l_stenosis = self.mse(
            predictions["stenosis"].squeeze(-1),
            targets["stenosis_pct"],
        )
        l_vuln = self.bce(predictions["vulnerability"], targets["vulnerability_4d"])
        l_feat = self.ce(
            predictions["deciding_feature"],
            targets["deciding_feature_label"],
        )

        # Reasoning-Alignment: nur wenn Mask vorhanden
        reasoning_mask = targets.get("reasoning_region_mask")
        if reasoning_mask is not None and self.gamma > 0:
            seg_sig = torch.sigmoid(predictions["segmentation"])
            seg_flat = seg_sig.flatten(1)
            mask_flat = reasoning_mask.flatten(1).float()
            cos = F.cosine_similarity(seg_flat, mask_flat, dim=1)
            l_align = (1.0 - cos).mean()
        else:
            l_align = torch.tensor(0.0, device=predictions["segmentation"].device)

        # Deep Supervision
        if "side_outputs" in predictions:
            l_deep = sum(
                self.dice(side, targets["mask"]) for side in predictions["side_outputs"]
            ) / max(len(predictions["side_outputs"]), 1)
        else:
            l_deep = torch.tensor(0.0, device=predictions["segmentation"].device)

        total = (
            self.alpha * (l_dice + l_stenosis)
            + self.beta * l_vuln
            + self.gamma * l_align
            + self.feature_weight * l_feat
            + self.deep_super_weight * l_deep
        )

        return total, {
            "dice": l_dice.detach(),
            "stenosis_mse": l_stenosis.detach(),
            "vulnerability_bce": l_vuln.detach(),
            "reasoning_align": l_align.detach(),
            "feature_ce": l_feat.detach(),
            "deep_super": l_deep.detach(),
            "total": total.detach(),
        }
