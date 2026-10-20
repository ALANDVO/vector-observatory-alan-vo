"""Application configuration."""

from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "Vector Observatory"
    VERSION: str = "1.0.0"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # Database
    DATABASE_URL: str = "sqlite:///./vector_observatory.db"

    # LLM (optional)
    LLM_API_KEY: str | None = None
    LLM_PROVIDER: str = "openai-compatible"
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_BASE_URL: str | None = None

    # Keycloak
    KEYCLOAK_URL: str = "http://localhost:8080"
    KEYCLOAK_REALM: str = "vector-observatory"
    KEYCLOAK_CLIENT_ID: str = "vector-observatory-client"
    KEYCLOAK_CLIENT_SECRET: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()