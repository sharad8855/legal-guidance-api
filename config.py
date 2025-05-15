import os
import logging
from typing import Optional
from pydantic import BaseSettings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """Application settings."""
    GEMINI_API_KEY: str = ""  # Default API key
    GEMINI_URL: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    MAX_CONVERSATION_HISTORY: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()
