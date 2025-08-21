"""Simple translation middleware."""
import logging
import os

logger = logging.getLogger(__name__)


class TranslationMiddleware:
    """Simple translation middleware that translates non-English text to English."""
    
    def __init__(self, ai_service=None, prompt_function=None):
        """Initialize with optional AI service for translation."""
        self.ai_service = ai_service
        self.prompt_function = prompt_function
        self.enabled = bool(ai_service and prompt_function and self._is_enabled())
    
    def _is_enabled(self):
        """Check if translation is enabled via environment variable."""
        return os.getenv('TRANSLATION_ENABLED', 'true').lower() == 'true'
    
    def process(self, text: str) -> str:
        """Process text - translate if enabled, otherwise return as-is."""
        if not self.enabled:
            return text
        
        try:
            prompt = self.prompt_function(text)
            translated = self.ai_service.generate(prompt)
            logger.info(f"Translated: '{text}' -> '{translated}'")
            return translated
        except Exception as e:
            logger.warning(f"Translation failed: {e}, using original text")
            return text
