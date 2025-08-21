# Therapy Search Feature

This feature combines AI-powered psychological therapy responses with Quranic verse search to provide comfort and guidance.

## How it works

1. **User Input**: User provides their issue/problem in any language
2. **Translation**: The issue is automatically translated to English if needed
3. **AI Therapy**: The translated issue is sent to Gemini AI with a therapy prompt
4. **Verse Search**: The AI response is used as a search query for relevant Quranic verses
5. **Response**: User receives the translation, AI therapy response, and matching verses in English and Arabic

## Setup

1. **Install Dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   - Copy `.env.example` to `.env`
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     ```
   - Configure translation middleware (optional):
     ```
     TRANSLATION_ENABLED=true
     TRANSLATION_MODEL=gemini-2.5-flash
     ```
   - Get your API key from: https://makersuite.google.com/app/apikey

3. **Run the Application**:
   ```bash
   cd backend/src
   python app.py
   ```

## API Endpoints

### POST /api/therapy-search

**Request**:
```json
{
    "issue": "أشعر بالقلق حول مستقبلي",  // Can be in any language
    "k": 5  // optional, number of verses to return (default: 5)
}
```

**Response**:
```json
{
    "ai_response": "Trust in Allah's plan for you, as every moment of anxiety can be transformed into an opportunity for spiritual growth and inner peace.",
    "search_query": "Trust in Allah's plan for you...",
    "results": [
        {
            "id": "2:286",
            "verse_en": "Allah does not burden a soul beyond that it can bear...",
            "verse_ar": "لَا يُكَلِّفُ ٱللَّهُ نَفْسًا إِلَّا وُسْعَهَا...",
            "score": 0.85,
            "surah_name": "al-Baqarah"
        }
    ]
}
```

### POST /api/search (Original)

Direct verse search without AI processing.

**Request**:
```json
{
    "text": "guidance",
    "k": 5
}
```

## Architecture

- **Translation Middleware**: Modular translation system with configurable implementations
  - **AI Translation**: Uses Gemini AI for automatic language detection and translation
  - **No-Op Translation**: Pass-through implementation for when translation is disabled
- **GenAI Service**: Generic AI service with dependency injection
- **Gemini Service**: Google Gemini API implementation
- **Prompts Module**: Translation and therapy prompt templates
- **Vector Search**: FAISS-based semantic search with bilingual results

## Features

- **Multi-language Support**: Accepts user input in any language
- **Configurable Translation**: Enable/disable translation via environment variables
- **Modular Architecture**: Easy to replace or remove translation components
- **AI Therapy**: Provides therapeutic responses using Quranic wisdom
- **Bilingual Results**: Returns verses in both English and Arabic
- **Semantic Search**: Uses vector embeddings for relevant verse matching
- **Error Handling**: Graceful fallback when translation fails

## Testing

Run the test script to verify functionality:
```bash
python test_therapy_search.py
```

Make sure the Flask app is running first.

## Error Handling

The API includes comprehensive error handling for:
- Missing API keys
- AI service failures
- Search service failures
- Invalid requests

Check the server logs for detailed error information.
