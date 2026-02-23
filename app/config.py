from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    app_name: str = "MrCopywriteBot"
    debug: bool = False
    secret_key: str = "change-me-to-a-random-secret"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/copywritebot"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Telegram
    telegram_bot_token: str = ""

    # OpenRouter
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    # Billing
    free_daily_limit: int = 2
    trial_days: int = 7


settings = Settings()
