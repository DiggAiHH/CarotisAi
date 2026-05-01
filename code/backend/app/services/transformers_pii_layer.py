"""Transformers-based PII Detection Layer.

Supports any HuggingFace Token-Classification model for NER/PII detection.
Default: OpenMed/OpenMed-PII-German-ClinicalLongformer-Base-149M-v1

Lazy-loaded (B-16) — torch and transformers are optional dependencies.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    pass

log = structlog.get_logger()

# Mapping from model-specific labels to unified PIISpan categories
# OpenMed-PII-German-ClinicalLongformer has 76 labels (B-/I- tags)
_LABEL_TO_CATEGORY: dict[str, str] = {
    # PERSON
    "FIRSTNAME": "PERSON",
    "LASTNAME": "PERSON",
    "MIDDLENAME": "PERSON",
    "PREFIX": "PERSON",
    "OCCUPATION": "PERSON",
    "JOBTITLE": "PERSON",
    "JOBDEPARTMENT": "PERSON",
    # EMAIL
    "EMAIL": "EMAIL",
    # PHONE
    "PHONE": "PHONE",
    # ID
    "ACCOUNTNAME": "ID",
    "SSN": "ID",
    "IBAN": "ID",
    "BANKACCOUNT": "ID",
    "CREDITCARD": "ID",
    "IPADDRESS": "ID",
    "USERNAME": "ID",
    "PASSWORD": "ID",
    "VIN": "ID",
    "VRM": "ID",
    "IMEI": "ID",
    "MASKEDNUMBER": "ID",
    "BITCOINADDRESS": "ID",
    "ETHEREUMADDRESS": "ID",
    "LITECOINADDRESS": "ID",
}

# Optional labels (mapped if enable_extended_pii is True)
_EXTENDED_LABELS: dict[str, str] = {
    "DATE": "DATE",
    "DATEOFBIRTH": "DATE",
    "AGE": "AGE",
    "STREET": "ADDRESS",
    "CITY": "ADDRESS",
    "ZIPCODE": "ADDRESS",
    "STATE": "ADDRESS",
    "ORGANIZATION": "ORG",
    "GENDER": "GENDER",
    "SEX": "GENDER",
}


def _map_label(label: str, extended: bool = False) -> str | None:
    """Map a model-specific BIO label to unified category.

    Args:
        label: Raw model label (e.g., "B-FIRSTNAME", "I-PHONE")
        extended: Whether to include extended PII categories

    Returns:
        Unified category or None if label should be ignored
    """
    # Strip BIO prefix
    if label.startswith(("B-", "I-")):
        core = label[2:]
    else:
        core = label

    if core == "O":
        return None

    if core in _LABEL_TO_CATEGORY:
        return _LABEL_TO_CATEGORY[core]

    if extended and core in _EXTENDED_LABELS:
        return _EXTENDED_LABELS[core]

    return None


@lru_cache(maxsize=1)
def _get_transformers_pipeline(model_id: str, device: str, revision: str):
    """Lazy-load Transformers pipeline for token classification.

    Args:
        model_id: HuggingFace model identifier
        device: "cpu" or "cuda"

    Returns:
        transformers pipeline or None if dependencies missing
    """
    try:
        from transformers import (
            AutoModelForTokenClassification,
            AutoTokenizer,
            pipeline,
        )
    except ImportError as e:
        log.warning("transformers_not_installed", error=str(e))
        return None

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
        model = AutoModelForTokenClassification.from_pretrained(
            model_id, revision=revision
        )

        # Longformer uses token_type_ids which pipeline handles automatically
        pipe = pipeline(
            "token-classification",
            model=model,
            tokenizer=tokenizer,
            aggregation_strategy="simple",  # Merge B-/I- tokens into entities
            device=device,
        )
        log.info(
            "transformers_pii_model_loaded",
            model_id=model_id,
            revision=revision,
            device=device,
            num_labels=model.config.num_labels,
        )
        return pipe
    except Exception as e:
        log.error("transformers_pii_model_load_failed", model_id=model_id, error=str(e))
        return None


class TransformersPIILayer:
    """PII detection using HuggingFace Token-Classification models."""

    def __init__(
        self,
        model_id: str = "OpenMed/OpenMed-PII-German-ClinicalLongformer-Base-149M-v1",
        device: str = "cpu",
        revision: str | None = None,
        threshold: float = 0.85,
        extended_labels: bool = False,
    ):
        self.model_id = model_id
        self.device = device
        self.revision = revision or os.environ.get(
            "TRANSFORMERS_PII_MODEL_REVISION", "main"
        )
        self.threshold = threshold
        self.extended_labels = extended_labels
        self._pipe = None

    def _get_pipe(self):
        """Lazy-initialize pipeline."""
        if self._pipe is None:
            self._pipe = _get_transformers_pipeline(
                self.model_id,
                self.device,
                self.revision,
            )
        return self._pipe

    def detect(self, text: str) -> list[dict]:
        """Detect PII spans in text.

        Returns list of dicts with keys: start, end, label, score, text
        Compatible with PIISpan creation.
        """
        if not text:
            return []

        pipe = self._get_pipe()
        if pipe is None:
            return []

        try:
            # Longformer handles up to 4096 tokens; truncate if needed
            results = pipe(text, truncation=True, max_length=4096)
        except Exception as e:
            log.error("transformers_pii_inference_failed", error=str(e))
            return []

        spans: list[dict] = []
        for ent in results:
            score = ent.get("score", 1.0)
            if score < self.threshold:
                continue

            label = _map_label(ent["entity_group"], self.extended_labels)
            if label is None:
                continue

            spans.append(
                {
                    "start": ent["start"],
                    "end": ent["end"],
                    "label": label,
                    "score": score,
                    "text": ent["word"],
                }
            )

        return spans

    def is_available(self) -> bool:
        """Check if the transformers model is loaded and ready."""
        # Fast path: check if dependencies are installed without loading model
        try:
            import torch  # noqa: F401
            import transformers  # noqa: F401
        except ImportError:
            return False
        return self._get_pipe() is not None
