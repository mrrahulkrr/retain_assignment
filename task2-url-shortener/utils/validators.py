import re
from flask import request
from typing import Dict, List, Any
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """Validate URL format"""
    if not url or not isinstance(url, str):
        return False
    
    try:
        result = urlparse(url.strip())
        return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
    except Exception:
        return False

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
