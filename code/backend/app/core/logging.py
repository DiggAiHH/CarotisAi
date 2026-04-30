import logging
import structlog
from app.core.config import get_settings


def configure_logging() -> None:
    settings = get_settings()
    level = logging.getLevelName(settings.log_level.upper())

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            # IMPORTANT: never log PII — enforce via processor
            _strip_pii,
            (
                structlog.dev.ConsoleRenderer()
                if settings.env == "development"
                else structlog.processors.JSONRenderer()
            ),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )


def _strip_pii(logger, method, event_dict: dict) -> dict:
    """Remove any field that might contain patient-identifiable data.

    Hard guard: PII must never reach logs per DSGVO requirements.
    """
    pii_keys = {
        "patient_name",
        "patient_id",
        "birth_date",
        "study_date",
        "accession_number",
        "referring_physician",
    }
    return {k: v for k, v in event_dict.items() if k not in pii_keys}


def get_logger(name: str) -> structlog.BoundLogger:
    return structlog.get_logger(name)
