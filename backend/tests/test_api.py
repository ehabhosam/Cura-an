from flask import Flask, jsonify
import pytest

def create_app():
    app = Flask(__name__)

    @app.route('/api/test', methods=['GET'])
    def test_endpoint():
        return jsonify({"message": "API is working!"}), 200

    return app

def test_api():
    app = create_app()
    client = app.test_client()

    response = client.get('/api/test')
    assert response.status_code == 200
    assert response.get_json() == {"message": "API is working!"}