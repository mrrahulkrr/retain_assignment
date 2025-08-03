from flask import Blueprint, request
from models.user import User
from utils.validators import validate_json_input
from utils.response_helpers import success_response, error_response
import logging

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = validate_json_input(request, required_fields=['email', 'password'])
        
        user = User.get_by_email(data['email'])
        if not user or not user.check_password(data['password']):
            logger.warning(f"Failed login attempt for email: {data['email']}")
            return error_response("Invalid email or password", 401)
        
        logger.info(f"Successful login: {user.email}")
        return success_response(
            data={
                'user_id': user.id,
                'name': user.name,
                'email': user.email
            },
            message="Login successful"
        )
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return error_response("Internal server error", 500)
