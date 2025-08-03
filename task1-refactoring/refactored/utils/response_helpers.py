from flask import jsonify
from typing import Any, Dict

def success_response(data: Any = None, message: str = "Success", status_code: int = 200):
    """Standard success response format"""
    response = {
        'success': True,
        'message': message
    }
    
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code

def error_response(message: str, status_code: int = 400):
    """Standard error response format"""
    response = {
        'success': False,
        'error': message
    }
    
    return jsonify(response), status_code
