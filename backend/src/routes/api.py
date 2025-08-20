from flask import Blueprint, jsonify, request

api = Blueprint('api', __name__)

@api.route('/users', methods=['GET'])
def get_users():
    return jsonify({"message": "List of users"})

@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    return jsonify({"message": "User created", "data": data}), 201

@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify({"message": f"User {user_id}"})

@api.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    return jsonify({"message": f"User {user_id} updated", "data": data})

@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return jsonify({"message": f"User {user_id} deleted"})