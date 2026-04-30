"""Global error handlers for FastAPI.

Provides structured error responses across all endpoints.
"""

from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError
import structlog

log = structlog.get_logger()


class AppError(Exception):
    """Base application error with code and message."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 500,
        details: dict | None = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class PIIError(AppError):
    def __init__(self, message: str, details: dict | None = None):
        super().__init__("PII_DETECTED", message, 422, details)


class AuthError(AppError):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__("UNAUTHORIZED", message, 401)


class NotFoundError(AppError):
    def __init__(self, resource: str = "Resource"):
        super().__init__("NOT_FOUND", f"{resource} not found", 404)


class AppValidationError(AppError):
    def __init__(self, message: str, details: dict | None = None):
        super().__init__("VALIDATION_ERROR", message, 422, details)


def register_error_handlers(app):
    """Register all error handlers on the FastAPI app."""

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        log.error(
            "app_error",
            code=exc.code,
            message=exc.message,
            status=exc.status_code,
            path=request.url.path,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                }
            },
        )

    @app.exception_handler(PydanticValidationError)
    async def pydantic_validation_handler(
        request: Request, exc: PydanticValidationError
    ):
        log.warning(
            "validation_error",
            errors=exc.errors() if hasattr(exc, "errors") else str(exc),
            path=request.url.path,
        )
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "details": {
                        "errors": exc.errors() if hasattr(exc, "errors") else str(exc)
                    },
                }
            },
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        log.warning("value_error", message=str(exc), path=request.url.path)
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "INVALID_VALUE",
                    "message": str(exc),
                    "details": {},
                }
            },
        )

    @app.exception_handler(Exception)
    async def generic_error_handler(request: Request, exc: Exception):
        log.error(
            "unhandled_error",
            error_type=type(exc).__name__,
            message=str(exc),
            path=request.url.path,
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An internal error occurred",
                    "details": {},
                }
            },
        )
