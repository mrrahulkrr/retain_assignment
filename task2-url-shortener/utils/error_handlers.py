from flask import jsonify
from utils.response_helpers import error_response
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    """Register global error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        return error_response("Resource not found", 404)
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return error_response("Method not allowed", 405)
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return error_response("Internal server error", 500)
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f"Unhandled exception: {str(error)}")
        return error_response("An unexpected error occurred", 500)
