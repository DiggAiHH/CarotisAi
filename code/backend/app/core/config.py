from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        protected_namespaces=("settings_",),
    )

    # Paths
    project_root: str = Field(
        default_factory=lambda: str(Path(__file__).resolve().parents[4])
    )

    # API Security
    api_key: str = Field(..., min_length=32)
    admin_api_key: str = Field(..., min_length=32)

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/carotis.db"

    # Model
    onnx_model_path: str = "/data/models/mfsd_unet.onnx"
    model_version: str = "v0.0.0"
    model_sha: str = Field(default="", pattern=r"^([a-f0-9]{64})?$")

    # Local AI
    ollama_url: str = "http://ollama:11434"
    hermes_url: str = "http://hermes:8200"
    default_local_model: str = "nous-hermes-3-llama-3.1"
    compression_model: str = "qwen2.5-coder:7b"

    # Anonymization
    anonymization_salt: str = Field(..., min_length=16)
    anonymization_salt_version: str = "v2026-04"
    min_k_anonymity: int = Field(default=5, ge=5)

    # Audit
    audit_db_path: str = "/data/audit.db"
    audit_retention_years: int = 25

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # Security
    max_file_size_mb: int = Field(default=50, ge=1, le=500)

    # CORS / CSP
    cors_origins: str = "http://localhost:3000"
    csp_connect_src: str = "https://api.carotis.diggai.de"

    @field_validator("cors_origins")
    @classmethod
    def validate_cors_origins(cls, v: str) -> str:
        origins = [o.strip() for o in v.split(",") if o.strip()]
        if not origins:
            raise ValueError("cors_origins must contain at least one origin")
        return ",".join(origins)

    # Features
    enable_decision_tree_capture: bool = True
    enable_daily_learning_loop: bool = False
    enable_grad_cam_overlay: bool = True

    # PII Detection
    transformers_pii_enabled: bool = False
    transformers_pii_model: str = (
        "OpenMed/OpenMed-PII-German-ClinicalLongformer-Base-149M-v1"
    )
    transformers_pii_device: str = "cpu"
    transformers_pii_threshold: float = Field(default=0.85, ge=0.0, le=1.0)
    transformers_pii_extended_labels: bool = False

    # Dev
    debug: bool = False
    reload: bool = False

    @field_validator("api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError("API_KEY must be at least 32 characters")
        return v

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith("sqlite"):
            raise ValueError(
                "Only SQLite databases are allowed for local-first compliance"
            )
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR"}
        if v.upper() not in allowed:
            raise ValueError(f"log_level must be one of {allowed}")
        return v.upper()

    @field_validator("min_k_anonymity")
    @classmethod
    def validate_min_k(cls, v: int) -> int:
        if v < 5:
            raise ValueError("min_k_anonymity must be >= 5")
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
