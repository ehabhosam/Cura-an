from flask import Blueprint

api_bp = Blueprint('api', __name__)

from .api import *  # Import all API routes from api.py