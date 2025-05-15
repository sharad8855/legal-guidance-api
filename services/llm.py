from enum import Enum
from typing import Dict, Any, Optional
from config import logger
from services.gemini import gemini_service

class LLMProvider(str, Enum):
    """Supported LLM providers."""
    GEMINI = "gemini"
    # Add more providers as needed

class LLMService:
    """Service for interacting with different LLM providers."""
    
    @staticmethod
    async def generate_response(
        query: str, 
        provider: LLMProvider = LLMProvider.GEMINI
    ) -> str:
        """Generate a response from the specified LLM provider."""
        logger.info(f"Generating response using {provider} provider")
        
        if provider == LLMProvider.GEMINI:
            return await gemini_service.generate_response(query)
        else:
            logger.error(f"Unsupported LLM provider: {provider}")
            raise ValueError(f"Unsupported LLM provider: {provider}")

# Create LLM service instance
llm_service = LLMService()
