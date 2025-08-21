# Middleware System Documentation

## Overview

The middleware system provides a clean, modular way to process requests before they reach the main business logic. Currently, it includes translation middleware for handling multi-language input.

## Architecture

### Base Components

- **BaseTranslationMiddleware**: Abstract base class for all translation implementations
- **TranslationMiddleware**: Main facade class that manages different implementations
- **Factory Functions**: Easy creation of middleware instances

### Available Implementations

1. **AITranslationMiddleware**: Uses AI service for translation
2. **NoOpTranslationMiddleware**: Pass-through implementation (no translation)

## Configuration

### Environment Variables

Add to your `.env` file:

```bash
# Enable/disable translation middleware
TRANSLATION_ENABLED=true

# Translation model (optional)
TRANSLATION_MODEL=gemini-2.5-flash
```

### Programmatic Configuration

```python
from middleware.config import MiddlewareConfig

# Check if translation is enabled
if MiddlewareConfig.is_translation_enabled():
    # Initialize AI translation
    pass
else:
    # Use no-op translation
    pass
```

## Usage Examples

### 1. Enable AI Translation

```python
from middleware import create_ai_translation_middleware
from prompts import translation_prompt
from services import services

# Create AI-powered translation middleware
translation_middleware = create_ai_translation_middleware(
    services.genai,  # AI service
    translation_prompt  # Prompt function
)

# Set in services
services.set_translation_middleware(translation_middleware)
```

### 2. Disable Translation

```python
from middleware import create_noop_translation_middleware
from services import services

# Create no-op translation middleware
translation_middleware = create_noop_translation_middleware()

# Set in services
services.set_translation_middleware(translation_middleware)
```

### 3. Use in Routes

```python
@bp.route('/therapy-search', methods=['POST'])
def therapy_search():
    user_issue = request.json['issue']
    
    # Process through translation middleware
    if services.translation_middleware:
        processed_issue = services.translation_middleware.process(user_issue)
    else:
        processed_issue = user_issue
    
    # Continue with business logic...
```

## Removing Translation Feature

### Option 1: Configuration-based Disable

Set in `.env`:
```bash
TRANSLATION_ENABLED=false
```

### Option 2: Code-based Disable

In `app.py`, replace the translation middleware initialization with:
```python
from middleware import create_noop_translation_middleware
services.set_translation_middleware(create_noop_translation_middleware())
```

### Option 3: Complete Removal

1. Delete the `middleware/` directory
2. Remove middleware imports from `app.py`
3. Update the API route to process `user_issue` directly

## Replacing Translation Implementation

### Custom Translation Service

```python
from middleware.translation import BaseTranslationMiddleware, TranslationMiddleware

class CustomTranslationMiddleware(BaseTranslationMiddleware):
    def __init__(self, custom_service):
        self.custom_service = custom_service
    
    def process(self, text: str) -> str:
        # Your custom translation logic
        return self.custom_service.translate(text)

# Use it
custom_impl = CustomTranslationMiddleware(my_service)
middleware = TranslationMiddleware(custom_impl)
services.set_translation_middleware(middleware)
```

### Third-party Translation API

```python
import requests
from middleware.translation import BaseTranslationMiddleware

class GoogleTranslateMiddleware(BaseTranslationMiddleware):
    def __init__(self, api_key):
        self.api_key = api_key
    
    def process(self, text: str) -> str:
        # Call Google Translate API
        response = requests.post(
            'https://translation.googleapis.com/language/translate/v2',
            params={'key': self.api_key},
            json={
                'q': text,
                'target': 'en'
            }
        )
        return response.json()['data']['translations'][0]['translatedText']
```

## Error Handling

The middleware includes built-in error handling:

- **Translation failures**: Automatically fallback to original text
- **Service unavailable**: Use no-op middleware as fallback
- **Configuration errors**: Graceful degradation

## Testing

### Test Translation Middleware

```python
from middleware import create_ai_translation_middleware
from prompts import translation_prompt

# Test with mock AI service
class MockAIService:
    def generate(self, prompt):
        return "Mocked translation"

middleware = create_ai_translation_middleware(MockAIService(), translation_prompt)
result = middleware.process("Hola mundo")
print(result)  # "Mocked translation"
```

### Test No-Op Middleware

```python
from middleware import create_noop_translation_middleware

middleware = create_noop_translation_middleware()
result = middleware.process("Any text")
print(result)  # "Any text" (unchanged)
```

## Benefits

1. **Modularity**: Easy to add/remove/replace translation functionality
2. **Configuration**: Enable/disable without code changes
3. **Fallback**: Graceful handling of failures
4. **Testability**: Easy to mock and test
5. **Extensibility**: Simple to add new middleware types

## Future Extensions

The middleware system can be extended for:

- **Authentication middleware**
- **Rate limiting middleware**
- **Input validation middleware**
- **Logging middleware**
- **Caching middleware**

Each would follow the same pattern with base classes, implementations, and factory functions.
