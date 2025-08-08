"""
Authentication utilities.
This module contains helper functions for authentication and security.
"""

import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def hash_password(password):
    """
    Hash a password using bcrypt.
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password
    """
    if isinstance(password, str):
        password = password.encode('utf-8')
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode('utf-8')
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def verify_password(password, hashed_password):
    """
    Verify a password against its hash.
    
    Args:
        password (str): Plain text password
        hashed_password (str): Hashed password from database
        
    Returns:
        bool: True if password matches, False otherwise
    """
    if isinstance(password, str):
        password = password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(password, hashed_password)

def generate_token(user_id, expires_in=3600):
    """
    Generate a JWT token for user authentication.
    
    Args:
        user_id (int): User ID
        expires_in (int): Token expiration time in seconds
        
    Returns:
        str: JWT token
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    
    return token

def decode_token(token):
    """
    Decode and validate a JWT token.
    
    Args:
        token (str): JWT token
        
    Returns:
        dict: Decoded payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """
    Decorator to require JWT token authentication.
    
    Args:
        f: Function to wrap
        
    Returns:
        function: Wrapped function
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid token format',
                    'message': 'Token should be in format: Bearer <token>'
                }), 401
        
        if not token:
            return jsonify({
                'success': False,
                'error': 'Missing token',
                'message': 'Authentication token is required'
            }), 401
        
        try:
            payload = decode_token(token)
            if not payload:
                return jsonify({
                    'success': False,
                    'error': 'Invalid token',
                    'message': 'Token is invalid or expired'
                }), 401
            
            current_user_id = payload['user_id']
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Token validation failed',
                'message': str(e)
            }), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated

def validate_email_format(email):
    """
    Validate email format using regex.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def generate_random_password(length=12):
    """
    Generate a random password.
    
    Args:
        length (int): Password length
        
    Returns:
        str: Random password
    """
    import random
    import string
    
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def sanitize_input(input_string):
    """
    Sanitize user input to prevent XSS attacks.
    
    Args:
        input_string (str): Input to sanitize
        
    Returns:
        str: Sanitized input
    """
    if not input_string:
        return input_string
    
    # Basic HTML entity encoding
    input_string = input_string.replace('&', '&amp;')
    input_string = input_string.replace('<', '&lt;')
    input_string = input_string.replace('>', '&gt;')
    input_string = input_string.replace('"', '&quot;')
    input_string = input_string.replace("'", '&#x27;')
    
    return input_string.strip()