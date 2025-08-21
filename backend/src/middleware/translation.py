"""
Translation middleware for processing user input in different languages.

This middleware automatically translates non-English user input to English
for consistent processing by the AI services.
"""
import logging
from typing import Optional, Callable
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseTranslationMiddleware(ABC):
    """Abstract base class for translation middleware."""
    
    @abstractmethod
    def process(self, text: str) -> str:
        """
        Process the input text and return English version.
        
        Args:
            text: Input text in any language
            
        Returns:
            Text in English
        """
        pass


class NoOpTranslationMiddleware(BaseTranslationMiddleware):
    """No-operation translation middleware that returns text as-is."""
    
    def process(self, text: str) -> str:
        """Return text without any translation."""
        logger.debug("NoOp translation: returning text as-is")
        return text


class AITranslationMiddleware(BaseTranslationMiddleware):
    """AI-powered translation middleware using injected AI service."""
    
    def __init__(self, ai_service, prompt_function: Callable[[str], str]):
        """
        Initialize AI translation middleware.
        
        Args:
            ai_service: AI service instance with generate() method
            prompt_function: Function that creates translation prompt from text
        """
        self.ai_service = ai_service
        self.prompt_function = prompt_function
    
    def process(self, text: str) -> str:
        """
        Translate text to English using AI service.
        
        Args:
            text: Input text in any language
            
        Returns:
            Text translated to English
            
        Raises:
            Exception: If translation fails
        """
        try:
            # Create translation prompt
            prompt = self.prompt_function(text)
            
            # Get translation from AI service
            translated_text = self.ai_service.generate(prompt)
            
            logger.info(f"Translation completed: '{text}' -> '{translated_text}'")
            return translated_text
            
        except Exception as e:
            logger.error(f"Translation failed for text: '{text}'. Error: {e}")
            # Fallback to original text if translation fails
            logger.warning("Falling back to original text")
            return text


class TranslationMiddleware:
    """
    Main translation middleware that can be easily configured or disabled.
    
    This class acts as a facade for different translation implementations,
    making it easy to switch between AI translation, no translation, or
    other translation services.
    """
    
    def __init__(self, middleware_impl: Optional[BaseTranslationMiddleware] = None):
        """
        Initialize translation middleware.
        
        Args:
            middleware_impl: Translation implementation to use. 
                           If None, uses NoOp (no translation)
        """
        self.middleware_impl = middleware_impl or NoOpTranslationMiddleware()
        self.enabled = middleware_impl is not None
    
    def process(self, text: str) -> str:
        """
        Process text through the configured translation middleware.
        
        Args:
            text: Input text
            
        Returns:
            Processed text (translated or original)
        """
        if not self.enabled:
            logger.debug("Translation middleware disabled, returning original text")
            return text
        
        return self.middleware_impl.process(text)
    
    def enable(self, middleware_impl: BaseTranslationMiddleware):
        """Enable translation with the specified implementation."""
        self.middleware_impl = middleware_impl
        self.enabled = True
        logger.info(f"Translation middleware enabled with {type(middleware_impl).__name__}")
    
    def disable(self):
        """Disable translation middleware."""
        self.middleware_impl = NoOpTranslationMiddleware()
        self.enabled = False
        logger.info("Translation middleware disabled")
    
    def is_enabled(self) -> bool:
        """Check if translation middleware is enabled."""
        return self.enabled


def create_ai_translation_middleware(ai_service, prompt_function: Callable[[str], str]) -> TranslationMiddleware:
    """
    Factory function to create AI-powered translation middleware.
    
    Args:
        ai_service: AI service instance
        prompt_function: Function that creates translation prompts
        
    Returns:
        Configured TranslationMiddleware instance
    """
    ai_impl = AITranslationMiddleware(ai_service, prompt_function)
    return TranslationMiddleware(ai_impl)


def create_noop_translation_middleware() -> TranslationMiddleware:
    """
    Factory function to create no-operation translation middleware.
    
    Returns:
        TranslationMiddleware that doesn't translate anything
    """
    return TranslationMiddleware(NoOpTranslationMiddleware())
