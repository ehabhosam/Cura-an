"""Simple guardrails middleware using Guardrails AI framework."""
import logging
import os
from typing import Tuple

logger = logging.getLogger(__name__)

try:
    from guardrails import Guard
    from guardrails.validators import ToxicLanguage, ProfanityFree
    GUARDRAILS_AVAILABLE = True
except ImportError:
    GUARDRAILS_AVAILABLE = False
    logger.warning("Guardrails AI not available")


class GuardrailsMiddleware:
    """Simple guardrails middleware to validate user input."""
    
    def __init__(self):
        """Initialize guardrails middleware."""
        self.enabled = self._is_enabled() and GUARDRAILS_AVAILABLE
        self.guard = None
        
        if self.enabled:
            try:
                self.guard = self._create_guard()
                logger.info("Guardrails middleware initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to create guardrails: {e}")
                self.enabled = False
    
    def _is_enabled(self) -> bool:
        """Check if guardrails is enabled via environment variable."""
        return os.getenv('GUARDRAILS_ENABLED', 'true').lower() == 'true'
    
    def _create_guard(self) -> Guard:
        """Create a simple guard with basic validators."""
        guard = Guard()
        
        # Add toxic language detection
        guard.use(ToxicLanguage, threshold=0.5, on_fail="exception")
        
        # Add profanity detection  
        guard.use(ProfanityFree, on_fail="exception")
        
        return guard
    
    def _is_meaningful_content(self, text: str) -> Tuple[bool, str]:
        """Check if content appears to be a genuine life issue."""
        text_lower = text.lower().strip()
        
        # Too short
        if len(text_lower) < 10:
            return False, "Input too short - please describe your issue in more detail"
        
        # Test/spam keywords
        spam_keywords = {'test', 'testing', 'hello', 'hi', 'example', 'sample', 'demo'}
        words = set(text_lower.split())
        if words.intersection(spam_keywords) and len(words) <= 3:
            return False, "Input appears to be test content"
        
        # Life issue keywords (positive indicators)
        life_keywords = {
            'feel', 'feeling', 'emotion', 'sad', 'happy', 'anxious', 'worried', 'stress',
            'problem', 'issue', 'struggle', 'difficult', 'hard', 'help', 'guidance',
            'relationship', 'family', 'work', 'life', 'faith', 'spiritual', 'peace'
        }
        
        # If it contains life keywords or is reasonably long, likely valid
        if words.intersection(life_keywords) or len(words) >= 5:
            return True, "Input appears to be a genuine concern"
        
        return True, "Input accepted"
    
    def validate(self, text: str) -> Tuple[bool, str]:
        """
        Validate user input for appropriateness and relevance.
        
        Returns:
            Tuple of (is_valid: bool, reason: str)
        """
        if not self.enabled:
            return True, "Guardrails disabled"
        
        # First check if it's meaningful content
        is_meaningful, reason = self._is_meaningful_content(text)
        if not is_meaningful:
            return False, reason
        
        # Then check with Guardrails AI
        if self.guard:
            try:
                self.guard.validate(text)
                logger.info(f"Input validation passed: '{text[:50]}...'")
                return True, "Input validation passed"
            except Exception as e:
                error_msg = str(e).lower()
                if 'toxic' in error_msg:
                    reason = "Content contains inappropriate language"
                elif 'profanity' in error_msg:
                    reason = "Content contains profanity"
                else:
                    reason = "Content violates safety guidelines"
                
                logger.warning(f"Input validation failed: {reason}")
                return False, reason
        
        return True, "Input accepted (basic validation)"
