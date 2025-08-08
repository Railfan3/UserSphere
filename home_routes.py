"""
Home routes for the UserSphere API.
Provides welcome page and documentation.
"""

from flask import Blueprint, jsonify

# Create blueprint
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    """Welcome page with API information."""
    return jsonify({
        "message": "🚀 Welcome to UserSphere REST API",
        "version": "1.0.0",
        "status": "running",
        "description": "Professional User Management System",
        "endpoints": {
            "health": "/api/health",
            "users": "/api/users",
            "user_by_id": "/api/users/{id}",
            "create_user": "/api/users (POST)",
            "update_user": "/api/users/{id} (PUT)",
            "delete_user": "/api/users/{id} (DELETE)",
            "search_users": "/api/users/search?q={query}"
        },
        "documentation": "/docs",
        "supported_methods": ["GET", "POST", "PUT", "DELETE"],
        "quick_test": {
            "health_check": "http://127.0.0.1:5000/api/health",
            "get_users": "http://127.0.0.1:5000/api/users",
            "search_example": "http://127.0.0.1:5000/api/users/search?q=john"
        }
    })

@home_bp.route('/docs')
def docs():
    """API documentation page."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>UserSphere API Documentation</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container { 
                max-width: 900px; 
                margin: 0 auto; 
                background: white; 
                padding: 40px; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 { 
                color: #333; 
                border-bottom: 3px solid #667eea; 
                padding-bottom: 15px; 
                margin-bottom: 30px;
                font-size: 2.5rem;
            }
            h2 { 
                color: #555; 
                margin: 30px 0 20px 0; 
                font-size: 1.5rem;
            }
            .endpoint { 
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                padding: 20px; 
                margin: 15px 0; 
                border-radius: 8px; 
                border-left: 5px solid #667eea;
                transition: transform 0.3s ease;
            }
            .endpoint:hover { transform: translateX(5px); }
            .method { 
                font-weight: bold; 
                color: white; 
                padding: 6px 12px; 
                border-radius: 20px; 
                font-size: 12px; 
                margin-right: 10px;
                display: inline-block;
            }
            .get { background: #28a745; }
            .post { background: #007bff; }
            .put { background: #fd7e14; }
            .delete { background: #dc3545; }
            code { 
                background: #2d3748; 
                color: #e2e8f0;
                padding: 8px 12px; 
                border-radius: 6px; 
                font-family: 'Courier New', monospace;
                display: inline-block;
                margin: 5px 0;
            }
            pre { 
                background: #2d3748; 
                color: #e2e8f0;
                padding: 15px; 
                border-radius: 6px; 
                overflow-x: auto;
                margin: 10px 0;
                font-size: 0.9rem;
            }
            .quick-links { 
                background: #667eea; 
                color: white; 
                padding: 20px; 
                border-radius: 8px; 
                margin: 20px 0;
            }
            .quick-links a { 
                color: #fff; 
                text-decoration: none; 
                background: rgba(255,255,255,0.2);
                padding: 8px 12px;
                border-radius: 4px;
                margin-right: 10px;
                display: inline-block;
                margin-bottom: 5px;
                transition: background 0.3s ease;
            }
            .quick-links a:hover { background: rgba(255,255,255,0.3); }
            .status { 
                background: #28a745; 
                color: white; 
                padding: 10px 15px; 
                border-radius: 20px; 
                display: inline-block;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 UserSphere REST API</h1>
            <div class="status">✅ API Status: Running</div>
            
            <div class="quick-links">
                <h3 style="margin-bottom: 10px;">🧪 Quick Test Links:</h3>
                <a href="/api/health" target="_blank">Health Check</a>
                <a href="/api/users" target="_blank">Get All Users</a>
                <a href="/api/users/search?q=john" target="_blank">Search Users</a>
            </div>
            
            <h2>📡 Available Endpoints</h2>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/health</code>
                <p><strong>Health Check:</strong> Verify API status and connectivity</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/users</code>
                <p><strong>Get All Users:</strong> Retrieve list of all active users</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/users/{id}</code>
                <p><strong>Get User by ID:</strong> Retrieve a specific user</p>
                <p><em>Example:</em> <code>/api/users/1</code></p>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <code>/api/users</code>
                <p><strong>Create User:</strong> Add a new user to the system</p>
                <p><strong>Request Body:</strong></p>
                <pre>{"name": "John Doe", "email": "john@example.com", "age": 30, "password": "secure123"}</pre>
            </div>
            
            <div class="endpoint">
                <span class="method put">PUT</span>
                <code>/api/users/{id}</code>
                <p><strong>Update User:</strong> Modify existing user information</p>
                <p><strong>Request Body (partial update allowed):</strong></p>
                <pre>{"name": "John Smith", "age": 31}</pre>
            </div>
            
            <div class="endpoint">
                <span class="method delete">DELETE</span>
                <code>/api/users/{id}</code>
                <p><strong>Delete User:</strong> Remove user from system (soft delete)</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/users/search?q={query}</code>
                <p><strong>Search Users:</strong> Find users by name or email</p>
                <p><em>Example:</em> <code>/api/users/search?q=john</code></p>
            </div>
            
            <h2>📱 Testing Examples</h2>
            
            <h3>Using curl:</h3>
            <pre># Health check
curl http://127.0.0.1:5000/api/health

# Get all users
curl http://127.0.0.1:5000/api/users

# Create user
curl -X POST http://127.0.0.1:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com", "age": 25, "password": "test123"}'

# Update user (replace 1 with actual user ID)
curl -X PUT http://127.0.0.1:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name", "age": 26}'

# Delete user
curl -X DELETE http://127.0.0.1:5000/api/users/1</pre>

            <h3>Using PowerShell:</h3>
            <pre># Get all users
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/users" -Method GET

# Create user
$body = @{name="Test User"; email="test@example.com"; age=25; password="test123"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/users" -Method POST -Body $body -ContentType "application/json"</pre>

            <div style="margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 8px; text-align: center;">
                <p><strong>🎉 Your UserSphere API is ready to use!</strong></p>
                <p>Base URL: <code>http://127.0.0.1:5000</code></p>
            </div>
        </div>
    </body>
    </html>
    """