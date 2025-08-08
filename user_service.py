"""
User service layer.
This module contains business logic for user operations.
"""

from app import db
from app.models.user import User
from app.utils.auth_utils import hash_password, verify_password
from sqlalchemy import or_

class UserService:
    """Service class for user operations."""
    
    @staticmethod
    def get_all_users():
        """Retrieve all users from the database."""
        return User.query.filter_by(is_active=True).all()
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieve a user by their ID.
        
        Args:
            user_id (int): The user ID
            
        Returns:
            User: User object or None if not found
        """
        return User.query.filter_by(id=user_id, is_active=True).first()
    
    @staticmethod
    def get_user_by_email(email):
        """
        Retrieve a user by their email address.
        
        Args:
            email (str): The user email
            
        Returns:
            User: User object or None if not found
        """
        return User.query.filter_by(email=email, is_active=True).first()
    
    @staticmethod
    def create_user(user_data):
        """
        Create a new user.
        
        Args:
            user_data (dict): Dictionary containing user information
            
        Returns:
            User: Created user object
            
        Raises:
            ValueError: If email already exists or validation fails
        """
        # Check if email already exists
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if existing_user:
            raise ValueError('Email address already exists')
        
        # Hash password
        hashed_password = hash_password(user_data['password'])
        
        # Create new user
        user = User(
            name=user_data['name'],
            email=user_data['email'],
            password=hashed_password,
            age=user_data.get('age')
        )
        
        try:
            user.save()
            return user
        except Exception as e:
            db.session.rollback()
            raise Exception(f'Failed to create user: {str(e)}')
    
    @staticmethod
    def update_user(user_id, update_data):
        """
        Update an existing user.
        
        Args:
            user_id (int): The user ID to update
            update_data (dict): Dictionary containing fields to update
            
        Returns:
            User: Updated user object
            
        Raises:
            ValueError: If user not found or email already exists
        """
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        
        # Check if email is being updated and already exists
        if 'email' in update_data:
            existing_user = User.query.filter_by(email=update_data['email']).first()
            if existing_user and existing_user.id != user_id:
                raise ValueError('Email address already exists')
        
        # Hash password if being updated
        if 'password' in update_data:
            update_data['password'] = hash_password(update_data['password'])
        
        try:
            user.update(**update_data)
            return user
        except Exception as e:
            db.session.rollback()
            raise Exception(f'Failed to update user: {str(e)}')
    
    @staticmethod
    def delete_user(user_id):
        """
        Delete a user (soft delete by setting is_active to False).
        
        Args:
            user_id (int): The user ID to delete
            
        Returns:
            bool: True if successful
            
        Raises:
            ValueError: If user not found
        """
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        
        try:
            # Soft delete by setting is_active to False
            user.update(is_active=False)
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f'Failed to delete user: {str(e)}')
    
    @staticmethod
    def permanently_delete_user(user_id):
        """
        Permanently delete a user from the database.
        
        Args:
            user_id (int): The user ID to delete
            
        Returns:
            bool: True if successful
            
        Raises:
            ValueError: If user not found
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError('User not found')
        
        try:
            user.delete()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f'Failed to permanently delete user: {str(e)}')
    
    @staticmethod
    def search_users(query):
        """
        Search users by name or email.
        
        Args:
            query (str): Search query string
            
        Returns:
            List[User]: List of matching users
        """
        search_term = f'%{query}%'
        return User.query.filter(
            or_(
                User.name.ilike(search_term),
                User.email.ilike(search_term)
            ),
            User.is_active == True
        ).all()
    
    @staticmethod
    def authenticate_user(email, password):
        """
        Authenticate a user with email and password.
        
        Args:
            email (str): User email
            password (str): User password
            
        Returns:
            User: User object if authentication successful, None otherwise
        """
        user = User.query.filter_by(email=email, is_active=True).first()
        if user and verify_password(password, user.password):
            return user
        return None
    
    @staticmethod
    def get_user_count():
        """
        Get total count of active users.
        
        Returns:
            int: Number of active users
        """
        return User.query.filter_by(is_active=True).count()
    
    @staticmethod
    def toggle_user_status(user_id):
        """
        Toggle user active status.
        
        Args:
            user_id (int): The user ID
            
        Returns:
            User: Updated user object
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError('User not found')
        
        user.update(is_active=not user.is_active)
        return user