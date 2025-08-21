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
        
        # Initialize GenAI service with Gemini
        try:
            from services.gemini import create_gemini_function
            # Initialize Gemini function with API key and model name
            gemini_function = create_gemini_function(api_key=os.getenv('GEMINI_API_KEY', None), model_name="gemini-2.5-flash")
            # inject the Gemini function into GenAI service
            genai_success = services.initialize_genai_service(gemini_function)
            if genai_success:
                app.logger.info("GenAI service initialized successfully with Gemini")
                
                # Initialize translation middleware
                try:
                    from middleware.config import MiddlewareConfig
                    
                    if MiddlewareConfig.is_translation_enabled():
                        from middleware import create_ai_translation_middleware
                        from prompts import translation_prompt
                        
                        translation_middleware = create_ai_translation_middleware(
                            services.genai, 
                            translation_prompt
                        )
                        services.set_translation_middleware(translation_middleware)
                        app.logger.info("AI translation middleware initialized successfully")
                    else:
                        from middleware import create_noop_translation_middleware
                        services.set_translation_middleware(create_noop_translation_middleware())
                        app.logger.info("Translation middleware disabled by configuration")
                    
                except Exception as middleware_error:
                    app.logger.warning(f"Translation middleware initialization failed: {middleware_error}")
                    # Set up no-op middleware as fallback
                    from middleware import create_noop_translation_middleware
                    services.set_translation_middleware(create_noop_translation_middleware())
                    app.logger.info("Fallback translation middleware (no-op) initialized")
                    
            else:
                app.logger.error("Failed to initialize GenAI service")
        except Exception as genai_error:
            app.logger.warning(f"GenAI service initialization failed: {genai_error}")
            # Set up no-op middleware as fallback
            try:
                from middleware import create_noop_translation_middleware
                services.set_translation_middleware(create_noop_translation_middleware())
                app.logger.info("Fallback translation middleware (no-op) initialized")
            except Exception:
                pass
        
    except Exception as e:
        app.logger.error(f"Failed to initialize services: {e}")

    # Register blueprints
    app.register_blueprint(api_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)