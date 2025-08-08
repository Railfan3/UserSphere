"""
User routes definition.
This module contains all user-related API endpoints.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService
from app.schemas.user_schema import UserSchema, UserUpdateSchema
from app.utils.auth_utils import token_required
from marshmallow import ValidationError

# Create blueprint
user_bp = Blueprint('users', __name__)

# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_update_schema = UserUpdateSchema()

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    """Get all users."""
    try:
        users = UserService.get_all_users()
        result = users_schema.dump(users)
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result),
            'message': 'Users retrieved successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve users'
        }), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a single user by ID."""
    try:
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found',
                'message': f'User with ID {user_id} does not exist'
            }), 404
        
        result = user_schema.dump(user)
        return jsonify({
            'success': True,
            'data': result,
            'message': 'User retrieved successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve user'
        }), 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    try:
        # Validate request data
        json_data = request.get_json()
        if not json_data:
            return jsonify({
                'success': False,
                'error': 'No input data provided',
                'message': 'Request body must contain JSON data'
            }), 400
        
        # Validate with schema
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'details': err.messages,
                'message': 'Invalid input data'
            }), 400
        
        # Create user
        user = UserService.create_user(data)
        result = user_schema.dump(user)
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'User created successfully'
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to create user'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Internal server error'
        }), 500

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user."""
    try:
        # Check if user exists
        existing_user = UserService.get_user_by_id(user_id)
        if not existing_user:
            return jsonify({
                'success': False,
                'error': 'User not found',
                'message': f'User with ID {user_id} does not exist'
            }), 404
        
        # Validate request data
        json_data = request.get_json()
        if not json_data:
            return jsonify({
                'success': False,
                'error': 'No input data provided',
                'message': 'Request body must contain JSON data'
            }), 400
        
        # Validate with schema
        try:
            data = user_update_schema.load(json_data)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'details': err.messages,
                'message': 'Invalid input data'
            }), 400
        
        # Update user
        user = UserService.update_user(user_id, data)
        result = user_schema.dump(user)
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'User updated successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to update user'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Internal server error'
        }), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user."""
    try:
        # Check if user exists
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found',
                'message': f'User with ID {user_id} does not exist'
            }), 404
        
        # Delete user
        UserService.delete_user(user_id)
        
        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to delete user'
        }), 500

@user_bp.route('/users/search', methods=['GET'])
def search_users():
    """Search users by name or email."""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query required',
                'message': 'Please provide a search query using ?q=search_term'
            }), 400
        
        users = UserService.search_users(query)
        result = users_schema.dump(users)
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result),
            'message': f'Search results for: {query}'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to search users'
        }), 500

# Health check endpoint
@user_bp.route('/health', methods=['GET'])
def health_check():
    """API health check endpoint."""
    return jsonify({
        'success': True,
        'message': 'UserSphere API is running',
        'status': 'healthy'
    }), 200