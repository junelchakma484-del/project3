from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'username', 'password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 409
    
    # Create new user
    user = User(
        email=data['email'],
        username=data['username'],
        first_name=data.get('first_name'),
        last_name=data.get('last_name')
    )
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update allowed fields
    allowed_fields = [
        'first_name', 'last_name', 'work_address', 'work_lat', 'work_lng',
        'max_commute_time', 'budget_min', 'budget_max', 'preferred_areas'
    ]
    
    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Profile update failed'}), 500

@auth_bp.route('/oauth/google', methods=['POST'])
def google_oauth():
    """Google OAuth login"""
    data = request.get_json()
    
    if not data.get('token'):
        return jsonify({'error': 'Google token is required'}), 400
    
    # In a real implementation, you would verify the Google token
    # For now, we'll simulate OAuth flow
    google_user_data = {
        'email': data.get('email'),
        'name': data.get('name'),
        'google_id': data.get('google_id')
    }
    
    # Check if user exists
    user = User.query.filter_by(email=google_user_data['email']).first()
    
    if not user:
        # Create new user
        user = User(
            email=google_user_data['email'],
            username=google_user_data['email'].split('@')[0],
            first_name=google_user_data['name'].split()[0] if google_user_data['name'] else None,
            last_name=' '.join(google_user_data['name'].split()[1:]) if google_user_data['name'] else None,
            oauth_provider='google',
            oauth_id=google_user_data['google_id']
        )
        
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'OAuth registration failed'}), 500
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'OAuth login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200
