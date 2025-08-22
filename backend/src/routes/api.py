from flask import Blueprint, request, jsonify
from utils.responses import success_response, validation_error, internal_error, service_error
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/health')
def health():
    return success_response({"status": "healthy"}, "Service is running")

@bp.route('/search', methods=['POST'])
def search_verses():
    """Search for Quran verses using vector similarity."""    
    try:
        from services import services
        
        if services.search is None:
            return service_error('Search service not initialized')

        data = request.get_json()
        if not data or 'text' not in data:
            return validation_error('Query text is required')

        results = services.search.search(data['text'], data.get('k', 5))
        
        return success_response({'results': results}, 'Search completed successfully')
    
    except Exception as e:
        return internal_error(f'Search failed: {str(e)}')

@bp.route('/therapy-search', methods=['POST'])
def therapy_search():
    """Process user issue through therapy AI and search for relevant Quran verses."""
    try:
        from services import services
        from prompts import therapy_prompt
        
        if services.search is None:
            return service_error('Search service not initialized')
        
        if services.genai is None:
            return service_error('AI service not initialized')

        data = request.get_json()
        if not data or 'issue' not in data:
            return validation_error('User issue is required')

        user_issue = data['issue']
        
        # Step 0: Validate input with guardrails
        if services.guardrails_middleware:
            is_valid, validation_reason = services.guardrails_middleware.validate(user_issue)
            if not is_valid:
                return validation_error(validation_reason)
        
        # Step 1: Process through translation middleware (if available)
        translated_issue = user_issue
        if services.translation_middleware:
            translated_issue = services.translation_middleware.process(user_issue)
        
        # Step 2: Generate therapy prompt using processed issue
        prompt = therapy_prompt(translated_issue)
        
        # Step 3: Get AI therapy response
        try:
            ai_response = services.genai.generate(prompt)
            print(f"AI Therapy Response: {ai_response}")  # Log to terminal
        except Exception as ai_error:
            return internal_error(f'AI service failed: {str(ai_error)}')
        
        # Step 4: Search for relevant verses using AI response
        try:
            search_results = services.search.search(ai_response, data.get('k', 5))
        except Exception as search_error:
            return internal_error(f'Search failed: {str(search_error)}')
        
        return success_response({
            'ai_response': ai_response,
            'search_query': ai_response,
            'results': search_results
        }, 'Therapy guidance completed successfully')
    
    except Exception as e:
        return internal_error(f'Therapy search failed: {str(e)}')
