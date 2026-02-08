"""
Configuration settings for the Todo Web Application.
"""

import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import field_validator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database settings - with SQLite as default for local development
    DATABASE_URL: str = "sqlite:///./todo_app_local.db"

    # JWT settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Application settings
    APP_NAME: str = "Todo Web Application"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # CORS settings
    BACKEND_CORS_ORIGINS: str = ""

    # Better Auth settings
    BETTER_AUTH_SECRET: str

    # Hugging Face settings
    HF_MODEL_NAME: str = "microsoft/DialoGPT-medium"
    HF_API_KEY: str = ""  # API key for Hugging Face Inference API (optional if not using HF)

    # Google Gemini settings
    GEMINI_API_KEY: str = ""  # API key for Google Gemini API (optional if not using Gemini)
    GEMINI_MODEL_NAME: str = "gemini-pro"
    AI_PROVIDER: str = "gemini"  # Options: "gemini", "huggingface"

    @field_validator('JWT_SECRET_KEY')
    @classmethod
    def validate_jwt_secret(cls, v):
        if v == "your-secret-key-change-in-production":
            raise ValueError('JWT_SECRET_KEY must be changed from default value in production')
        return v

    @field_validator('BETTER_AUTH_SECRET')
    @classmethod
    def validate_auth_secret(cls, v):
        if v == "better-auth-secret-change-in-production":
            raise ValueError('BETTER_AUTH_SECRET must be changed from default value in production')
        return v

    @field_validator('DATABASE_URL')
    @classmethod
    def validate_database_url(cls, v):
        # Allow SQLite for local development, but warn about changing for production
        if v.startswith("postgresql://") and v == "postgresql://user:password@localhost/todo_db":
            raise ValueError('DATABASE_URL must be changed from default value in production')
        return v

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert the CORS origins string to a list."""
        if self.BACKEND_CORS_ORIGINS:
            return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]
        return []


settings = Settings()


def get_database_url():
    """Return the database URL from settings."""
    return settings.DATABASE_URL