"""
Application configuration loaded from environment variables.
Uses pydantic-settings to validate and parse .env values.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Google Cloud API Key (simple string from Cloud Console)
    GOOGLE_CLOUD_API_KEY: str = ""

    # Google Cloud credentials path (alternative: service account JSON)
    GOOGLE_APPLICATION_CREDENTIALS: str = ""

    # Comma-separated list of valid API keys
    API_KEYS: str = "test-api-key-1,test-api-key-2"

    # Rate limit string (e.g., "10/minute", "100/hour")
    RATE_LIMIT: str = "10/minute"

    # Application metadata
    APP_TITLE: str = "Google Cloud Natural Language API Service"
    APP_DESCRIPTION: str = (
        "A production-ready FastAPI application that exposes Google Cloud "
        "Natural Language API capabilities behind authenticated, rate-limited endpoints."
    )
    APP_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def api_keys_list(self) -> list[str]:
        """Parse the comma-separated API_KEYS string into a list."""
        return [key.strip() for key in self.API_KEYS.split(",") if key.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — loaded once and reused."""
    return Settings()
