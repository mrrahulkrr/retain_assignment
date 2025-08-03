from flask import Blueprint, request, jsonify, redirect
from models.url import URL
from utils.validators import validate_json_input
from utils.response_helpers import success_response, error_response
import logging

shortener_bp = Blueprint('shortener', __name__)
logger = logging.getLogger(__name__)

@shortener_bp.route('/shorten', methods=['POST'])
def shorten_url():
    """Shorten a URL"""
    try:
        data = validate_json_input(request, required_fields=['url'])
        original_url = data['url'].strip()
        
        # Create short URL
        url_obj = URL.create(original_url)
        
        # Build short URL
        short_url = f"{request.host_url}{url_obj.short_code}"
        
        logger.info(f"URL shortened: {original_url} -> {url_obj.short_code}")
        
        return success_response(
            data={
                'short_code': url_obj.short_code,
                'short_url': short_url
            },
            message="URL shortened successfully",
            status_code=201
        )
    
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error shortening URL: {str(e)}")
        return error_response("Internal server error", 500)

@shortener_bp.route('/stats/<short_code>', methods=['GET'])
def get_stats(short_code):
    """Get statistics for a short code"""
    try:
        if not short_code or len(short_code) != 6:
            return error_response("Invalid short code format", 400)
        
        url_obj = URL.get_by_short_code(short_code)
        if not url_obj:
            return error_response("Short code not found", 404)
        
        return success_response(
            data=url_obj.get_stats(),
            message="Statistics retrieved successfully"
        )
    
    except Exception as e:
        logger.error(f"Error getting stats for {short_code}: {str(e)}")
        return error_response("Internal server error", 500)

# Redirect endpoint (not under /api prefix)
@shortener_bp.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    """Redirect to original URL"""
    try:
        if not short_code or len(short_code) != 6:
            return error_response("Invalid short code format", 400)
        
        url_obj = URL.get_by_short_code(short_code)
        if not url_obj:
            return error_response("Short code not found", 404)
        
        # Increment click count
        url_obj.increment_clicks()
        
        logger.info(f"Redirecting {short_code} to {url_obj.original_url}")
        
        # Redirect to original URL
        return redirect(url_obj.original_url, code=302)
    
    except Exception as e:
        logger.error(f"Error redirecting {short_code}: {str(e)}")
        return error_response("Internal server error", 500)
