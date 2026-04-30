from __future__ import annotations


class AnonymizationError(Exception):
    """Raised when DICOM anonymization fails or PII is detected."""


class SchemaValidationError(Exception):
    """Raised when a payload does not conform to the JSON schema."""


class ModelNotLoadedError(Exception):
    """Raised when inference is requested but the ONNX model is not loaded."""
