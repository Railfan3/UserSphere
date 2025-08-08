# 🌐 UserSphere – Advanced User Management REST API

UserSphere is a robust, modular, and production-ready REST API built with **Flask** that enables full user management capabilities including registration, login (with JWT authentication), and secure CRUD operations. Designed for scalability and integration, UserSphere is ideal for any application requiring secure and efficient user handling.

---

## 🚀 Features

- ✅ RESTful API with modular architecture
- ✅ User Registration & Login
- ✅ JWT Authentication & Authorization
- ✅ Secure CRUD operations
- ✅ Search and filter users
- ✅ Global error handling
- ✅ Environment-based configuration
- ✅ Health check & base welcome endpoint
- ✅ Ready for Postman & Swagger documentation

---

## 📁 Folder Structure

UserSphere/
│
├── app/
│ ├── models/ # SQLAlchemy models
│ ├── routes/ # All route blueprints (user, auth)
│ ├── schemas/ # Marshmallow schemas
│ ├── utils/ # Utility functions (e.g. hashing)
│ ├── init.py # App factory
│
├── config.py # Environment-based configurations
├── requirements.txt # Python dependencies
├── .env # Environment variables
├── run.py # App entry point
├── README.md # Project documentation

markdown
Copy
Edit

---

## ⚙️ Technology Stack

- **Framework**: Flask (with Blueprints & App Factory)
- **ORM**: SQLAlchemy
- **Schema Serialization**: Marshmallow
- **Authentication**: JWT (`flask-jwt-extended`)
- **Documentation**: Flasgger (Swagger UI) *(optional)*
- **Testing**: Postman-ready (collection export supported)

---

## 🔐 Authentication

UserSphere uses **JWT (JSON Web Tokens)** for stateless authentication.

- `POST /api/register` → Register new user
- `POST /api/login` → Returns JWT token
- Use token in headers to access protected endpoints:
  
Authorization: Bearer <your_token_here>

pgsql
Copy
Edit

---

## 📌 API Endpoints

### 🔓 Public

| Method | Endpoint             | Description             |
|--------|----------------------|-------------------------|
| GET    | `/api/health`        | Health check            |
| GET    | `/`                  | API base info           |
| POST   | `/api/register`      | Register new user       |
| POST   | `/api/login`         | Login & get token       |

### 🔐 Protected (Require JWT Token)

| Method | Endpoint                            | Description               |
|--------|-------------------------------------|---------------------------|
| GET    | `/api/users`                        | Get all users             |
| GET    | `/api/users/<id>`                   | Get user by ID            |
| POST   | `/api/users`                        | Create user               |
| PUT    | `/api/users/<id>`                   | Update user               |
| DELETE | `/api/users/<id>`                   | Delete user               |
| GET    | `/api/users/search?q=<keyword>`     | Search users by keyword   |

📦 Getting Started

 1. Clone the Repo
bash
git clone https://github.com/yourusername/usersphere.git
cd usersphere

2. Create Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Set Environment Variables
Create a .env file:

env
Copy
Edit
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
5. Run the App
bash
Copy
Edit
flask run
App runs on: http://127.0.0.1:5000 '''

🧪 Testing with Postman
🔹 Steps:
Use POST /api/register to create a user

Use POST /api/login to get a JWT token

Use token to access protected endpoints (/api/users etc.)

👉 You can import the Postman Collection to test all routes instantly.

📚 Optional: Swagger Documentation
To enable Swagger UI:

Install Flasgger:

bash
Copy
Edit
pip install flasgger
Access documentation at:

arduino
Copy
Edit
http://127.0.0.1:5000/docs
🛡️ Security Notes
Passwords are hashed using SHA256

All write routes are secured using JWT tokens

Environment variables are used for secrets

🧩 Future Improvements
✅ Pagination for users list

✅ Role-based permissions

✅ Forgot password flow

✅ Email verification integration

✅ Docker support for deployment



📄 License
This project is licensed under the MIT License. See LICENSE file for details.

Made with ❤️ using Flask and JWT – ready for production or integration into any frontend (React, Angular, etc.)










