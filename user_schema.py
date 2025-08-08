"""
User schema definition.
This module contains Marshmallow schemas for user data validation and serialization.
"""

from marshmallow import Schema, fields, validate, ValidationError, post_load
import re
from app.models.user import User
from app import ma

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True
        load_only = ("password",)
        dump_only = ("id",)

# Single user schema
user_schema = UserSchema()

# Multiple users schema
users_schema = UserSchema(many=True)


class UserSchema(Schema):
    """Schema for user data validation and serialization."""
    
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=100),
            validate.Regexp(
                r'^[a-zA-Z\s]+$',
                error='Name can only contain letters and spaces'
            )
        ],
        error_messages={'required': 'Name is required'}
    )
    email = fields.Email(
        required=True,
        validate=validate.Length(max=120),
        error_messages={'required': 'Email is required'}
    )
    age = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1, max=150),
        error_messages={'invalid': 'Age must be between 1 and 150'}
    )
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=6, max=128),
        error_messages={
            'required': 'Password is required',
            'invalid': 'Password must be at least 6 characters long'
        }
    )
    is_active = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @post_load
    def validate_email_format(self, data, **kwargs):
        """Additional email validation."""
        email = data.get('email')
        if email:
            # Simple email regex validation
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                raise ValidationError({'email': ['Invalid email format']})
        return data

class UserUpdateSchema(Schema):
    """Schema for user update operations (all fields optional)."""
    
    name = fields.Str(
        validate=[
            validate.Length(min=2, max=100),
            validate.Regexp(
                r'^[a-zA-Z\s]+$',
                error='Name can only contain letters and spaces'
            )
        ]
    )
    email = fields.Email(
        validate=validate.Length(max=120)
    )
    age = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1, max=150),
        error_messages={'invalid': 'Age must be between 1 and 150'}
    )
    password = fields.Str(
        load_only=True,
        validate=validate.Length(min=6, max=128),
        error_messages={'invalid': 'Password must be at least 6 characters long'}
    )
    is_active = fields.Bool()
    
    @post_load
    def validate_email_format(self, data, **kwargs):
        """Additional email validation."""
        email = data.get('email')
        if email:
            # Simple email regex validation
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                raise ValidationError({'email': ['Invalid email format']})
        return data

class UserLoginSchema(Schema):
    """Schema for user login validation."""
    
    email = fields.Email(
        required=True,
        error_messages={'required': 'Email is required'}
    )
    password = fields.Str(
        required=True,
        error_messages={'required': 'Password is required'}
    )