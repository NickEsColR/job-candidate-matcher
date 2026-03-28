"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized app configuration. Loaded once, validated, immutable."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)
    debug: bool = Field(default=False)

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://jcm_user:jcm_password@localhost:5432/job_candidate_matcher"
    )

    # LLM Configuration
    llm_provider: str = Field(...)
    llm_model: str = Field(...)
    llm_temperature: float = Field(default=0.0)
    llm_max_tokens: int = Field(default=2048)
    llm_timeout: int = Field(default=60)
    llm_max_retries: int = Field(default=3)
    llm_max_concurrency: int = Field(default=10)
    llm_api_key: str | None = Field(default=None)
    llm_base_url: str | None = Field(default=None)


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings singleton."""
    return Settings()  # pyright: ignore[reportCallIssue]
