import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI API."""

    def __init__(self):
        """Initialize OpenAI service with API key from environment."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set. "
                "Please set OPENAI_API_KEY in your .env file or environment."
            )
        
        self.client = OpenAI(api_key=self.api_key)
        logger.info(f"OpenAI service initialized with model: {self.model}")

    def generate_text(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
        """
        Generate text using OpenAI API.

        Args:
            prompt: The prompt to send to OpenAI
            temperature: Sampling temperature (0-2). Lower = more deterministic
            max_tokens: Maximum tokens in response

        Returns:
            Generated text response from OpenAI

        Raises:
            Exception: If OpenAI API call fails
        """
        try:
            logger.debug(f"Calling OpenAI API with model {self.model}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a specialized legal research assistant. Provide concise, focused analysis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            result = response.choices[0].message.content
            logger.debug(f"OpenAI API response received ({len(result)} characters)")
            return result
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise


# Global service instance
_openai_service = None


def get_openai_service() -> OpenAIService:
    """Get or create the OpenAI service singleton."""
    global _openai_service
    if _openai_service is None:
        _openai_service = OpenAIService()
    return _openai_service
