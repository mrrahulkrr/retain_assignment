import re
from flask import request
from typing import Dict, List, Any

def validate_email(email: str) -> bool:
    """Validate email format"""
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None

def validate_password(password: str) -> bool:
    """Validate password strength"""
    if not password or not isinstance(password, str):
        return False
    
    return len(password) >= 8

def validate_json_input(request_obj, required_fields: List[str] = None) -> Dict[str, Any]:
    """Validate JSON input from request"""
    if not request_obj.is_json:
        raise ValueError("Request must be JSON")
    
    data = request_obj.get_json()
    if not data:
        raise ValueError("Request body cannot be empty")
    
    if required_fields:
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    return data
