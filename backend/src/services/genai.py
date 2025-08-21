"""
GenAI service with dependency injection for different AI models.
"""
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)


class GenAIService:
    """Generic AI service that uses dependency injection for different models."""
    
    def __init__(self, model_function: Callable[[str], str]):
        """
        Initialize GenAI service with a model function.
        
        Args:
            model_function: A callable that takes a prompt string and returns a response string
        """
        self.model_function = model_function
    
    def generate(self, prompt: str) -> str:
        """
        Generate response using the injected model function.
        
        Args:
            prompt: The input prompt string
            
        Returns:
            Generated response string
            
        Raises:
            Exception: If model function fails
        """
        try:
            logger.info(f"Generating response for prompt (length: {len(prompt)})")
            response = self.model_function(prompt)
            logger.info(f"Generated response: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            raise
