from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models.auth.user import User
from models.auth.refresh_tokens import RefreshToken
from models import db
from datetime import datetime, timedelta
import hashlib
import os

auth_routes = Blueprint('auth_routes', __name__)

def generate_refresh_token():
    raw_token = os.urandom(32).hex()
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
    return raw_token, hashed_token

def verify_refresh_token(raw_token, user_id):
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
    refresh_token = RefreshToken.query.filter_by(user_id=user_id, token=hashed_token).first()
    return refresh_token

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "All fields are required!"}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists!"}), 400

    user = User(username=username, email=email)
    user.password_hash = generate_password_hash(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required!"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid username or password!"}), 401

    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(minutes=30))

    raw_token, hashed_token = generate_refresh_token()  # Hem düz metin, hem hash oluştur
    refresh_token = RefreshToken(
        user_id=user.id,
        token=hashed_token,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.session.add(refresh_token)
    db.session.commit()

    return jsonify({
        "message": "Login successful!",
        "access_token": access_token,
        "refresh_token": raw_token
    }), 200

@auth_routes.route('/refresh', methods=['POST'])
def refresh_token():
    data = request.get_json()
    raw_token = data.get('refresh_token')

    if not raw_token:
        return jsonify({"error": "Refresh token is required!"}), 400

    user_id = get_jwt_identity()
    refresh_token = verify_refresh_token(raw_token, user_id)

    if not refresh_token or refresh_token.is_expired():
        return jsonify({"error": "Invalid or expired refresh token!"}), 401

    # Yeni access token oluştur
    access_token = create_access_token(identity=str(user_id), expires_delta=timedelta(minutes=30))
    return jsonify({"access_token": access_token}), 200

@auth_routes.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    raw_token = data.get('refresh_token')

    if not raw_token:
        return jsonify({"error": "Refresh token is required!"}), 400

    user_id = get_jwt_identity()
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()

    refresh_token = RefreshToken.query.filter_by(user_id=user_id, token=hashed_token).first()

    if refresh_token:
        db.session.delete(refresh_token)
        db.session.commit()

    return jsonify({"message": "Logout successful!"}), 200
