from flask import Blueprint
from utils.response_helpers import success_response

health_bp = Blueprint('health', __name__)

@health_bp.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return success_response(
        data={'status': 'healthy'},
        message="URL Shortener service is running"
    )

@health_bp.route('/health', methods=['GET'])
def detailed_health():
    """Detailed health check"""
    return success_response(
        data={
            'status': 'healthy',
            'service': 'URL Shortener',
            'version': '1.0.0'
        },
        message="Service is operational"
    )
