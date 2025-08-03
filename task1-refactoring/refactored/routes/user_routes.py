from flask import Blueprint, request, jsonify
from models.user import User
from utils.validators import validate_json_input
from utils.response_helpers import success_response, error_response
import logging

user_bp = Blueprint('users', __name__)
logger = logging.getLogger(__name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users with pagination"""
    try:
        limit = min(int(request.args.get('limit', 100)), 100)  # Max 100 users per request
        offset = int(request.args.get('offset', 0))
        
        users = User.get_all(limit=limit, offset=offset)
        users_data = [user.to_dict() for user in users]
        
        return success_response(
            data=users_data,
            message=f"Retrieved {len(users_data)} users"
        )
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error getting users: {str(e)}")
        return error_response("Internal server error", 500)

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user by ID"""
    try:
        user = User.get_by_id(user_id)
        if not user:
            return error_response("User not found", 404)
        
        return success_response(
            data=user.to_dict(),
            message="User retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {str(e)}")
        return error_response("Internal server error", 500)

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Create new user"""
    try:
        # Validate JSON input
        data = validate_json_input(request, required_fields=['name', 'email', 'password'])
        
        user = User.create(
            name=data['name'],
            email=data['email'],
            password=data['password']
        )
        
        logger.info(f"User created: {user.email}")
        return success_response(
            data=user.to_dict(),
            message="User created successfully",
            status_code=201
        )
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return error_response("Internal server error", 500)

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user"""
    try:
        user = User.get_by_id(user_id)
        if not user:
            return error_response("User not found", 404)
        
        data = validate_json_input(request)
        
        # Update user with provided fields
        updated = user.update(
            name=data.get('name'),
            email=data.get('email')
        )
        
        if not updated:
            return error_response("No changes made", 400)
        
        logger.info(f"User updated: {user.email}")
        return success_response(
            data=user.to_dict(),
            message="User updated successfully"
        )
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {str(e)}")
        return error_response("Internal server error", 500)

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    try:
        user = User.get_by_id(user_id)
        if not user:
            return error_response("User not found", 404)
        
        deleted = user.delete()
        if not deleted:
            return error_response("Failed to delete user", 500)
        
        logger.info(f"User deleted: {user.email}")
        return success_response(
            message="User deleted successfully"
        )
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        return error_response("Internal server error", 500)

@user_bp.route('/users/search', methods=['GET'])
def search_users():
    """Search users by name"""
    try:
        name = request.args.get('name', '').strip()
        if not name:
            return error_response("Name parameter is required", 400)
        
        if len(name) < 2:
            return error_response("Search term must be at least 2 characters", 400)
        
        users = User.search_by_name(name)
        users_data = [user.to_dict() for user in users]
        
        return success_response(
            data=users_data,
            message=f"Found {len(users_data)} users matching '{name}'"
        )
    except Exception as e:
        logger.error(f"Error searching users: {str(e)}")
        return error_response("Internal server error", 500)
