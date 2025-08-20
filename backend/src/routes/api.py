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
            return jsonify({'error': 'service not initialized'}), 503

        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Query text is required'}), 400

        results = services.search.search(data['text'], data.get('k', 5))
        
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
