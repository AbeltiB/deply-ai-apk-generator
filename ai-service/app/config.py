"""
Application configuration management using Pydantic Settings.
LLAMA3 ONLY VERSION - fully corrected for defaults and lists/dicts.
"""
import logging
import os
from typing import Literal, Optional, Dict, Any
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from dotenv import load_dotenv
from app.models.schemas.component_catalog import get_available_components

# Load .env first
load_dotenv()

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """Application settings - Llama3 Only Version (fixed for defaults)"""
    
    # -------------------------
    # APPLICATION METADATA & RUNTIME
    # -------------------------
    app_name: str = "AI App Builder Service (Llama3)"
    app_version: str = "0.1.0"
    api_title: str = "AI Service API - Llama3"
    api_version: str = "1.0.0"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = True
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    # -------------------------
    # LLM SETTINGS (Llama3 Only)
    # -------------------------
    llama3_api_url: str = "https://fastchat.ideeza.com/v1/chat/completions"
    llama3_model: str = "llama-3-70b-instruct"
    llama3_api_key: Optional[str] = "pJ53Y9gusCRsIqblyMyI2E9r1y1FeLOGDUrY9ZHSiKKjRy9MabGmBUpsL2nAQ6Mz"
    llama3_timeout: float = 60.0
    llama3_max_tokens: int = 4096
    llama3_temperature: float = 0.7
    llama3_max_retries: int = 5
    llama3_retry_delay: int = 2

    llm_primary_provider: Literal["llama3"] = "llama3"
    llm_fallback_enabled: bool = True
    llm_fallback_sequence: list[str] = ["llama3", "heuristic"]
    llm_failure_threshold: int = 3
    llm_failure_window_minutes: int = 5
    llm_health_check_interval: int = 60
    llm_default_temperature: float = 0.7
    llm_default_max_tokens: int = 4096

    LAYOUT_LLM_DEBUG: bool = True
    LAYOUT_LLM_DEBUG_DIR: str = "./debug/llm_layout_dumps"


    # -------------------------
    # PROMPT ENGINEERING
    # -------------------------
    default_prompt_version: str = "v2"
    prompt_cache_enabled: bool = True
    prompt_cache_ttl: int = 3600
    system_prompt_path: str = "prompts/system"
    user_prompt_path: str = "prompts/user"

    # -------------------------
    # PROCESSING & RETRIES
    # -------------------------
    max_retries: int = 3
    retry_delay: int = 2
    retry_backoff_factor: float = 1.5
    request_timeout: int = 30
    batch_processing_size: int = 10
    concurrent_workers: int = 4

    # -------------------------
    # RATE LIMITING & SECURITY
    # -------------------------
    rate_limit_enabled: bool = True
    rate_limit_requests_per_hour: int = 100
    rate_limit_requests_per_minute: int = 20
    rate_limit_window_size: int = 60
    rate_limit_storage_backend: Literal["redis", "memory"] = "redis"
    api_key_header: str = "X-API-Key"
    jwt_secret_key: Optional[str] = None
    jwt_algorithm: str = "HS256"
    jwt_token_expire_minutes: int = 60

    # -------------------------
    # UI / CANVAS SETTINGS
    # -------------------------
    canvas_width: int = 375
    canvas_height: int = 667
    canvas_safe_area_top: int = 44
    canvas_safe_area_bottom: int = 34
    canvas_background_color: str = "#FFFFFF"
    canvas_grid_size: int = 8
    canvas_snap_to_grid: bool = True

    # -------------------------
    # COMPONENT LIBRARY
    # -------------------------
    
    available_components: list[str] = get_available_components()
    
    min_touch_target_size: int = 44
    default_font_family: str = "San Francisco, Roboto, sans-serif"
    default_font_size: int = 16
    default_spacing_unit: int = 8

    # -------------------------
    # FILE STORAGE
    # -------------------------
    upload_directory: str = "./uploads"
    max_upload_size: int = 10 * 1024 * 1024
    allowed_file_types: list[str] = [".png", ".jpg", ".jpeg", ".gif", ".pdf", ".txt"]
    asset_base_url: str = "https://assets.example.com"

    # -------------------------
    # METRICS & MONITORING
    # -------------------------
    metrics_enabled: bool = True
    metrics_port: int = 9090
    health_check_endpoint: str = "/health"
    readiness_endpoint: str = "/ready"
    prometheus_endpoint: str = "/metrics"

    # -------------------------
    # VALIDATORS
    # -------------------------
    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        logger.info(f"Setting log level to: {v}")
        return v.upper()

    @field_validator('environment')
    @classmethod
    def validate_environment(cls, v: str) -> str:
        valid_envs = ["development", "staging", "production"]
        if v not in valid_envs:
            logger.warning(f"Invalid environment '{v}', defaulting to 'development'")
            return "development"
        return v

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"

    @property
    def llm_config(self) -> Dict[str, Any]:
        return {
            "primary_provider": self.llm_primary_provider,
            "fallback_enabled": self.llm_fallback_enabled,
            "fallback_sequence": self.llm_fallback_sequence,
            "failure_threshold": self.llm_failure_threshold,
            "failure_window_minutes": self.llm_failure_window_minutes,
            "default_temperature": self.llm_default_temperature,
            "default_max_tokens": self.llm_default_max_tokens,
            "llama3_api_url": self.llama3_api_url,
            "llama3_model": self.llama3_model,
        }

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow", 
        env_prefix="APP_",
        validate_default=True,
    )


def get_settings() -> Settings:
    logger.info("Initializing settings...")
    return Settings()


settings = get_settings()
