"""
User model definition.
This module contains the User SQLAlchemy model.
"""

from datetime import datetime
from app import db

class User(db.Model):
    """User model for storing user information."""
    
    __tablename__ = 'users'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # User information
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    age = db.Column(db.Integer, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    def __init__(self, name, email, password, age=None):
        """Initialize a new User instance."""
        self.name = name
        self.email = email
        self.password = password
        self.age = age
    
    def __repr__(self):
        """String representation of User."""
        return f'<User {self.name}>'
    
    def to_dict(self):
        """Convert User instance to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def find_by_email(cls, email):
        """Find user by email address."""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, user_id):
        """Find user by ID."""
        return cls.query.get(user_id)
    
    def save(self):
        """Save user to database."""
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """Delete user from database."""
        db.session.delete(self)
        db.session.commit()
    
    def update(self, **kwargs):
        """Update user attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()