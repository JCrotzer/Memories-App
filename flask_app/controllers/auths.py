import re
import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_app import db, bcrypt 
from flask_app.models.user import User
from flask_app.utils.jwt_utils import token_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({
        "message": f'Welcome, {current_user}!',
        "user_id": current_user.id,
        "email": current_user.email
    }), 200

# Regex patterns
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
PASSWORD_REGEX = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+=\-{}[\]|:;"\'<>,.?/]).{8,}$'

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')

    # Basic presence check
    if not all([first_name, email, password]):
        return jsonify({'error': 'First name, email, and password are required'}), 400

    # Email format check
    if not re.match(EMAIL_REGEX, email):
        return jsonify({'message': 'Invalid email format'}), 400

    # Password strength check
    if not re.match(PASSWORD_REGEX, password):
        return jsonify({
            'message': 'Password must be at least 8 characters long, include uppercase and lowercase letters, a number, and a special character.'
        }), 400

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    # Hash and store user
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(first_name=first_name, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': f"User {first_name} registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        token = jwt.encode({
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            'message': 'Login successful',
            'token': token.decode('utf-8') if isinstance(token, bytes) else token
        }), 200

    return jsonify({'message': 'Invalid credentials'}), 401
