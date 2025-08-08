from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import db
from app.models.user import User
from app.utils.auth_utils import hash_password, check_password
from app.schemas.user_schema import user_schema

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'msg': 'Email already exists'}), 409

    user = User(
        name=data['name'],
        email=data['email'],
        password=hash_password(data['password']),
        age=data.get('age', 0)
    )
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password(data['password'], user.password):
        return jsonify({'msg': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(token=access_token)
