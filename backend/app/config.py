"""
Configuration loader for environment variables.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    """Application configuration from environment variables."""
    
    # App settings
    APP_ENV: str = os.getenv("APP_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    
    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change_me")
    
    # Weather API
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
    
    # Firebase Admin SDK
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "")
    FIREBASE_CLIENT_EMAIL: str = os.getenv("FIREBASE_CLIENT_EMAIL", "")
    FIREBASE_PRIVATE_KEY: Optional[str] = os.getenv("FIREBASE_PRIVATE_KEY", "")
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        if cls.JWT_SECRET == "change_me":
            print("WARNING: Using default JWT_SECRET. Set in production!")


config = Config()
