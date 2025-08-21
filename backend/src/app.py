from flask import Flask
from config import Config
from routes.api import bp as api_bp
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize search service
    try:
        from services import services
        
        # Use the correct paths for embeddings and bilingual metadata
        embeddings_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "quran_embeddings.npy")
        metadata_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "quran_bilingual_metadata.json")
        
        success = services.initialize_search_service(embeddings_path, metadata_path)
        if success:
            app.logger.info("Search service initialized successfully with bilingual metadata")
        else:
            app.logger.error("Failed to initialize search service")
        
    except Exception as e:
        app.logger.error(f"Failed to initialize search service: {e}")

    # Register blueprints
    app.register_blueprint(api_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)