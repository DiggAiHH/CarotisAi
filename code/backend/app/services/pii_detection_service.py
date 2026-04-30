"""PII Detection Service for free-text notes.

Layered architecture:
  1. RegexLayer — deterministic, fast, always active
  2. TransformersPIILayer — ML-based, optional, lazy-loaded (B-16)
  3. Ensemble.merge() — dedupe with span preference

Dependencies:
  - Regex: none (stdlib only)
  - Transformers: torch + transformers (optional, NOT in base image)
  - Spacy: spacy + de_core_news_lg (optional, legacy, will be deprecated)
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache

import structlog

log = structlog.get_logger()


@dataclass(frozen=True)
class PIISpan:
    start: int
    end: int
    label: str  # PERSON, PHONE, ID, EMAIL
    text: str  # only for preview in Reject-Response — NEVER in Logs (B-15)


# Regex fallbacks (DE-specific)
_PHONE_RE = re.compile(
    r"(?:\+49|0)\s?\d{2,4}[\s/-]?\d{3,8}",
    re.IGNORECASE,
)
_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_ID_RE = re.compile(
    # Patient-IDs / Versicherten-Nr / Studien-Akten-Nr
    r"\b[A-Z]{1,3}[-_]?\d{4,12}\b",
)
_GERMAN_NAME_RE = re.compile(
    # Conservative: titles + capitalized words
    r"\b(?:Herr|Frau|Dr|Prof)\.?\s+[A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)?",
)


@lru_cache(maxsize=1)
def _get_nlp():
    """Lazy-load Spacy DE model. ~500 MB on first call. LEGACY — will be deprecated."""
    try:
        import spacy
    except ImportError as e:
        log.warning("spacy_not_installed", error=str(e))
        return None
    try:
        nlp = spacy.load("de_core_news_lg")
        log.info("spacy_loaded", model="de_core_news_lg")
        return nlp
    except OSError:
        log.warning(
            "spacy_model_missing",
            hint="run: python -m spacy download de_core_news_lg",
        )
        return None


def _get_transformers_layer():
    """Lazy-load Transformers PII layer."""
    try:
        from app.services.transformers_pii_layer import TransformersPIILayer
    except ImportError:
        return None

    try:
        from app.core.config import get_settings

        settings = get_settings()
        if not settings.transformers_pii_enabled:
            return None

        layer = TransformersPIILayer(
            model_id=settings.transformers_pii_model,
            device=settings.transformers_pii_device,
            threshold=settings.transformers_pii_threshold,
            extended_labels=settings.transformers_pii_extended_labels,
        )
        return layer
    except Exception as e:
        log.error("transformers_layer_init_failed", error=str(e))
        return None


class RegexLayer:
    """Deterministic regex-based PII detection. Always active."""

    @staticmethod
    def detect(text: str) -> list[PIISpan]:
        if not text:
            return []
        spans: list[PIISpan] = []
        for m in _PHONE_RE.finditer(text):
            spans.append(PIISpan(m.start(), m.end(), "PHONE", m.group()))
        for m in _EMAIL_RE.finditer(text):
            spans.append(PIISpan(m.start(), m.end(), "EMAIL", m.group()))
        for m in _ID_RE.finditer(text):
            spans.append(PIISpan(m.start(), m.end(), "ID", m.group()))
        for m in _GERMAN_NAME_RE.finditer(text):
            spans.append(PIISpan(m.start(), m.end(), "PERSON", m.group()))
        return spans


class SpacyLayer:
    """Spacy NER layer. LEGACY — will be deprecated in favor of Transformers."""

    @staticmethod
    def detect(text: str) -> list[PIISpan]:
        if not text:
            return []
        spans: list[PIISpan] = []
        nlp = _get_nlp()
        if nlp is not None:
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ in ("PER", "PERSON"):
                    spans.append(
                        PIISpan(ent.start_char, ent.end_char, "PERSON", ent.text)
                    )
        return spans


class Ensemble:
    """Merge spans from multiple layers. Prefer longer spans on overlap."""

    @staticmethod
    def merge(spans: list[PIISpan]) -> list[PIISpan]:
        if not spans:
            return []
        # Sort by start, then by descending length
        spans = sorted(set(spans), key=lambda s: (s.start, -(s.end - s.start)))
        deduped: list[PIISpan] = []
        for s in spans:
            if not any(d.start <= s.start and d.end >= s.end for d in deduped):
                deduped.append(s)
        return deduped


class PIIDetectionService:
    """Detects PII in free-text using layered architecture.

    Layers (in order):
      1. RegexLayer — deterministic, always active
      2. SpacyLayer — legacy, optional
      3. TransformersPIILayer — ML-based, optional, configurable
    """

    def __init__(self) -> None:
        self._transformers_layer = None

    def _get_transformers(self):
        if self._transformers_layer is None:
            self._transformers_layer = _get_transformers_layer()
        return self._transformers_layer

    def detect(self, text: str) -> list[PIISpan]:
        if not text:
            return []

        spans: list[PIISpan] = []

        # Layer 1: Regex (always active)
        spans.extend(RegexLayer.detect(text))

        # Layer 2: Spacy (legacy, optional)
        spans.extend(SpacyLayer.detect(text))

        # Layer 3: Transformers (optional, lazy)
        transformers = self._get_transformers()
        if transformers is not None and transformers.is_available():
            try:
                tf_spans = transformers.detect(text)
                for s in tf_spans:
                    spans.append(PIISpan(s["start"], s["end"], s["label"], s["text"]))
            except Exception as e:
                log.error("transformers_detect_failed", error=str(e))

        # Ensemble: dedupe overlapping spans
        return Ensemble.merge(spans)

    def is_clean(self, text: str) -> bool:
        return len(self.detect(text)) == 0

    def redact(self, text: str) -> str:
        """Replace PII spans with [REDACTED-LABEL] tokens."""
        spans = self.detect(text)
        if not spans:
            return text
        for s in sorted(spans, key=lambda x: -x.start):
            text = text[: s.start] + f"[REDACTED-{s.label}]" + text[s.end :]
        return text


def get_pii_service() -> PIIDetectionService:
    """FastAPI Dependency helper."""
    return PIIDetectionService()
