"""
Middleware configuration settings.

This file allows easy configuration of middleware components.
"""
import os


class MiddlewareConfig:
    """Configuration for middleware components."""
    
    # Translation Middleware Settings
    TRANSLATION_ENABLED = os.getenv('TRANSLATION_ENABLED', 'true').lower() == 'true'
    TRANSLATION_FALLBACK_TO_ORIGINAL = True  # If translation fails, use original text
    
    # AI Translation Settings
    TRANSLATION_MODEL = os.getenv('TRANSLATION_MODEL', 'gemini-2.5-flash')
    
    @classmethod
    def is_translation_enabled(cls) -> bool:
        """Check if translation middleware should be enabled."""
        return cls.TRANSLATION_ENABLED
    
    @classmethod
    def should_fallback_on_translation_error(cls) -> bool:
        """Check if we should fallback to original text on translation errors."""
        return cls.TRANSLATION_FALLBACK_TO_ORIGINAL
