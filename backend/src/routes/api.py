from flask import Blueprint, jsonify, request
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@bp.route('/search', methods=['POST'])
def search_verses():
    """Search for Quran verses using vector similarity."""    
    try:
        from services import services
        
        if services.search is None:
            return jsonify({'error': 'search service not initialized'}), 503

        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Query text is required'}), 400

        results = services.search.search(data['text'], data.get('k', 5))
        
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/therapy-search', methods=['POST'])
def therapy_search():
    """Process user issue through therapy AI and search for relevant Quran verses."""
    try:
        from services import services
        from prompts import therapy_prompt
        
        if services.search is None:
            return jsonify({'error': 'search service not initialized'}), 503
        
        if services.genai is None:
            return jsonify({'error': 'AI service not initialized'}), 503

        data = request.get_json()
        if not data or 'issue' not in data:
            return jsonify({'error': 'User issue is required'}), 400

        user_issue = data['issue']
        
        # Step 1: Process through translation middleware
        translated_issue = user_issue  # default fallback
        if services.translation_middleware:
            try:
                translated_issue = services.translation_middleware.process(user_issue)
            except Exception as translation_error:
                print(f"Translation middleware failed: {translation_error}")
                # Continue with original text if translation fails
        
        # Step 2: Generate therapy prompt using processed issue
        prompt = therapy_prompt(translated_issue)
        
        # Step 3: Get AI therapy response
        try:
            ai_response = services.genai.generate(prompt)
            print(f"AI Therapy Response: {ai_response}")  # Log to terminal
        except Exception as ai_error:
            return jsonify({'error': f'AI service failed: {str(ai_error)}'}), 500
        
        # Step 4: Search for relevant verses using AI response
        try:
            search_results = services.search.search(ai_response, data.get('k', 5))
        except Exception as search_error:
            return jsonify({'error': f'Search failed: {str(search_error)}'}), 500
        
        return jsonify({
            'ai_response': ai_response,
            'search_query': ai_response,
            'results': search_results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
