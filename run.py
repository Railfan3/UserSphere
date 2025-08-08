#!/usr/bin/env python3
"""
Entry point for the UserSphere Flask application.
This script creates and runs the Flask app.
"""

import os
from app import create_app, db
from flask_migrate import Migrate

# Create Flask application
app = create_app(os.getenv('FLASK_ENV', 'development'))

# Setup database migrations
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    """Make database and models available in Flask shell."""
    from app.models.user import User
    return {
        'db': db,
        'User': User
    }

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database initialized successfully!")

@app.cli.command()
def create_sample_users():
    """Create sample users for testing."""
    from app.models.user import User
    from app.utils.auth_utils import hash_password
    
    # Sample users
    sample_users = [
        {'name': 'John Doe', 'email': 'john@example.com', 'age': 30, 'password': 'password123'},
        {'name': 'Jane Smith', 'email': 'jane@example.com', 'age': 25, 'password': 'password456'},
        {'name': 'Bob Johnson', 'email': 'bob@example.com', 'age': 35, 'password': 'password789'},
    ]
    
    for user_data in sample_users:
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if not existing_user:
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                age=user_data['age'],
                password=hash_password(user_data['password'])
            )
            db.session.add(user)
    
    db.session.commit()
    print("Sample users created successfully!")

if __name__ == '__main__':
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port, debug=True)