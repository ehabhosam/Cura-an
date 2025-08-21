"""
Google Gemini API service implementation.
"""
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("Google GenerativeAI library not available. Install with: pip install google-generativeai")


class GeminiService:
    """Service for interacting with Google Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-pro"):
        """
        Initialize Gemini service.
        
        Args:
            api_key: Gemini API key. If None, will try to get from environment
            model_name: Name of the Gemini model to use
        """
        if not GEMINI_AVAILABLE:
            raise ImportError("Google GenerativeAI library is required. Install with: pip install google-generativeai")
        
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable or pass api_key parameter.")
        
        self.model_name = model_name
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        
        logger.info(f"Gemini service initialized with model: {model_name}")
    
    def generate_response(self, prompt: str) -> str:
        """
        Generate response from Gemini API.
        
        Args:
            prompt: Input prompt text
            
        Returns:
            Generated response text
            
        Raises:
            Exception: If API call fails
        """
        try:
            logger.info(f"Sending prompt to Gemini (model: {self.model_name})")
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise Exception("Empty response from Gemini API")
            
            generated_text = response.text.strip()
            logger.info(f"Gemini response: {generated_text}")
            return generated_text
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise Exception(f"Failed to generate response from Gemini: {e}")


def create_gemini_function(api_key: Optional[str] = None, model_name: str = "gemini-pro") -> callable:
    """
    Create a Gemini function that can be injected into GenAI service.
    
    Args:
        api_key: Gemini API key
        model_name: Name of the Gemini model to use
        
    Returns:
        Function that takes a prompt and returns a response
    """
    gemini_service = GeminiService(api_key, model_name)
    return gemini_service.generate_response
