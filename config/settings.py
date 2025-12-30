"""
Configuration settings for Auto Trade Sync App
"""
from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "Auto Trade Sync App"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # API
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/auto_trade_sync"

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Telegram
    TELEGRAM_API_ID: Optional[int] = None
    TELEGRAM_API_HASH: Optional[str] = None
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_SESSION_NAME: str = "auto_trade_bot"

    @field_validator('TELEGRAM_API_ID', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        """Convert empty strings to None for optional integer fields"""
        if v == '' or v is None:
            return None
        return v

    # Broker API Keys (will be stored per-user in database, these are defaults)
    # Angel One
    ANGEL_ONE_API_KEY: Optional[str] = None
    ANGEL_ONE_CLIENT_ID: Optional[str] = None

    # Zerodha
    ZERODHA_API_KEY: Optional[str] = None
    ZERODHA_API_SECRET: Optional[str] = None

    # Dhan
    DHAN_CLIENT_ID: Optional[str] = None
    DHAN_ACCESS_TOKEN: Optional[str] = None

    # Upstox
    UPSTOX_API_KEY: Optional[str] = None
    UPSTOX_API_SECRET: Optional[str] = None
    UPSTOX_REDIRECT_URI: Optional[str] = None

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/auto_trade_sync.log"

    # Signal Processing
    MAX_SIGNAL_AGE_MINUTES: int = 5  # Ignore signals older than 5 minutes
    ENABLE_SIGNAL_VALIDATION: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
