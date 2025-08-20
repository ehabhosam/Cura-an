from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

users = {}  # In-memory user storage for demonstration purposes

def register_user(username, password):
    if username in users:
        return {"message": "User already exists"}, 400
    hashed_password = generate_password_hash(password)
    users[username] = hashed_password
    return {"message": "User registered successfully"}, 201

def login_user(username, password):
    if username not in users or not check_password_hash(users[username], password):
        return {"message": "Invalid username or password"}, 401
    return {"message": "Login successful"}, 200