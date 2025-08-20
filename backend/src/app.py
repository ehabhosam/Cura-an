from flask import Flask
from config import Config
from routes import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(api.bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)