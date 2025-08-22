"""Consistent response utilities for the Flask API."""
from flask import jsonify
from typing import Dict, Any, Optional


class APIError:
    """Standard API error response."""
    
    VALIDATION_ERROR = "validation_error"
    INTERNAL_ERROR = "internal_error"
    SERVICE_ERROR = "service_error"
    NOT_FOUND = "not_found"
    
    def __init__(self, message: str, error_type: str, status_code: int = 400, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_type = error_type
        self.status_code = status_code
        self.details = details or {}
    
    def to_response(self):
        """Convert to Flask JSON response."""
        return jsonify({
            "success": False,
            "error": {
                "message": self.message,
                "type": self.error_type,
                "details": self.details
            }
        }), self.status_code


class APISuccess:
    """Standard API success response."""
    
    def __init__(self, data: Dict[str, Any], message: str = "Success"):
        self.data = data
        self.message = message
    
    def to_response(self):
        """Convert to Flask JSON response."""
        return jsonify({
            "success": True,
            "message": self.message,
            "data": self.data
        }), 200


# Convenience functions
def validation_error(message: str, details: Optional[Dict[str, Any]] = None):
    """Create a validation error response."""
    return APIError(message, APIError.VALIDATION_ERROR, 400, details).to_response()


def internal_error(message: str = "Internal server error"):
    """Create an internal error response."""
    return APIError(message, APIError.INTERNAL_ERROR, 500).to_response()


def service_error(message: str):
    """Create a service error response."""
    return APIError(message, APIError.SERVICE_ERROR, 503).to_response()


def success_response(data: Dict[str, Any], message: str = "Success"):
    """Create a success response."""
    return APISuccess(data, message).to_response()
