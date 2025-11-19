# users.py

from flask import Blueprint, jsonify, request
from models import db, User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
import datetime

users_bp = Blueprint('users', __name__)
bcrypt = Bcrypt()

# ✅ Fetch all users
@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name, "email": u.email} for u in users]), 200


# ✅ Signup (Register new user)
@users_bp.route('/signup', methods=['POST'])
def signup_user():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({"error": "All fields are required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(name=name, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "Registration successful",
        "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email}
    }), 201


#  Login (Authenticate user)
@users_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=3))

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {"id": user.id, "name": user.name, "email": user.email}
    }), 200
