import os
from config import logger

class KeyManager:
    """Manages API keys for different services."""
    
    @staticmethod
    def get_gemini_api_key() -> str:
        """Get Gemini API key from environment or config."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables, using default")
            # Use default key from config if not found in environment
            from config import settings
            api_key = settings.GEMINI_API_KEY
        
        return api_key

# Create key manager instance
key_manager = KeyManager()
