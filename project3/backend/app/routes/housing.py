from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.housing import Housing
from app.models.favorite import Favorite
from app.models.user import User
from sqlalchemy import and_, or_
import math

housing_bp = Blueprint('housing', __name__)

@housing_bp.route('/search', methods=['GET'])
@jwt_required()
def search_housing():
    """Search for housing listings with filters"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    bedrooms = request.args.get('bedrooms', type=int)
    bathrooms = request.args.get('bathrooms', type=float)
    property_type = request.args.get('property_type')
    city = request.args.get('city')
    state = request.args.get('state')
    pet_friendly = request.args.get('pet_friendly', type=bool)
    parking_available = request.args.get('parking_available', type=bool)
    
    # Build query
    query = Housing.query
    
    # Apply filters
    if min_price:
        query = query.filter(Housing.price >= min_price)
    if max_price:
        query = query.filter(Housing.price <= max_price)
    if bedrooms:
        query = query.filter(Housing.bedrooms >= bedrooms)
    if bathrooms:
        query = query.filter(Housing.bathrooms >= bathrooms)
    if property_type:
        query = query.filter(Housing.property_type == property_type)
    if city:
        query = query.filter(Housing.city.ilike(f'%{city}%'))
    if state:
        query = query.filter(Housing.state.ilike(f'%{state}%'))
    if pet_friendly is not None:
        query = query.filter(Housing.pet_friendly == pet_friendly)
    if parking_available is not None:
        query = query.filter(Housing.parking_available == parking_available)
    
    # Apply user preferences if available
    if user.budget_min:
        query = query.filter(Housing.price >= user.budget_min)
    if user.budget_max:
        query = query.filter(Housing.price <= user.budget_max)
    
    # Pagination
    pagination = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    housing_list = [housing.to_dict() for housing in pagination.items]
    
    return jsonify({
        'housing': housing_list,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }), 200

@housing_bp.route('/<housing_id>', methods=['GET'])
@jwt_required()
def get_housing(housing_id):
    """Get housing details by ID"""
    housing = Housing.query.get(housing_id)
    
    if not housing:
        return jsonify({'error': 'Housing not found'}), 404
    
    return jsonify(housing.to_dict()), 200

@housing_bp.route('/nearby', methods=['GET'])
@jwt_required()
def get_nearby_housing():
    """Get housing listings near user's work location"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user.work_lat or not user.work_lng:
        return jsonify({'error': 'Work location not set'}), 400
    
    # Get query parameters
    radius_miles = request.args.get('radius', 10, type=float)  # Default 10 miles
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Calculate bounding box for efficient querying
    lat_degree = radius_miles / 69.0  # Approximate miles per degree latitude
    lng_degree = radius_miles / (69.0 * math.cos(math.radians(user.work_lat)))
    
    min_lat = user.work_lat - lat_degree
    max_lat = user.work_lat + lat_degree
    min_lng = user.work_lng - lng_degree
    max_lng = user.work_lng + lng_degree
    
    # Query housing within bounding box
    query = Housing.query.filter(
        and_(
            Housing.latitude >= min_lat,
            Housing.latitude <= max_lat,
            Housing.longitude >= min_lng,
            Housing.longitude <= max_lng
        )
    )
    
    # Apply user preferences
    if user.budget_min:
        query = query.filter(Housing.price >= user.budget_min)
    if user.budget_max:
        query = query.filter(Housing.price <= user.budget_max)
    
    # Pagination
    pagination = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    housing_list = [housing.to_dict() for housing in pagination.items]
    
    return jsonify({
        'housing': housing_list,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }), 200

@housing_bp.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    """Get user's favorite housing listings"""
    user_id = get_jwt_identity()
    
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    
    favorite_housing = []
    for favorite in favorites:
        housing_data = favorite.housing.to_dict()
        housing_data['favorite_id'] = favorite.id
        housing_data['notes'] = favorite.notes
        housing_data['priority'] = favorite.priority
        housing_data['visit_date'] = favorite.visit_date.isoformat() if favorite.visit_date else None
        favorite_housing.append(housing_data)
    
    return jsonify({'favorites': favorite_housing}), 200

@housing_bp.route('/favorites', methods=['POST'])
@jwt_required()
def add_favorite():
    """Add housing to favorites"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('housing_id'):
        return jsonify({'error': 'Housing ID is required'}), 400
    
    # Check if housing exists
    housing = Housing.query.get(data['housing_id'])
    if not housing:
        return jsonify({'error': 'Housing not found'}), 404
    
    # Check if already favorited
    existing_favorite = Favorite.query.filter_by(
        user_id=user_id, housing_id=data['housing_id']
    ).first()
    
    if existing_favorite:
        return jsonify({'error': 'Already in favorites'}), 409
    
    # Create new favorite
    favorite = Favorite(
        user_id=user_id,
        housing_id=data['housing_id'],
        notes=data.get('notes'),
        priority=data.get('priority', 1)
    )
    
    try:
        db.session.add(favorite)
        db.session.commit()
        
        return jsonify({
            'message': 'Added to favorites',
            'favorite': favorite.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add to favorites'}), 500

@housing_bp.route('/favorites/<favorite_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(favorite_id):
    """Remove housing from favorites"""
    user_id = get_jwt_identity()
    
    favorite = Favorite.query.filter_by(
        id=favorite_id, user_id=user_id
    ).first()
    
    if not favorite:
        return jsonify({'error': 'Favorite not found'}), 404
    
    try:
        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify({'message': 'Removed from favorites'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to remove from favorites'}), 500

@housing_bp.route('/favorites/<favorite_id>', methods=['PUT'])
@jwt_required()
def update_favorite(favorite_id):
    """Update favorite notes and priority"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    favorite = Favorite.query.filter_by(
        id=favorite_id, user_id=user_id
    ).first()
    
    if not favorite:
        return jsonify({'error': 'Favorite not found'}), 404
    
    # Update fields
    if 'notes' in data:
        favorite.notes = data['notes']
    if 'priority' in data:
        favorite.priority = data['priority']
    if 'visit_date' in data:
        from datetime import datetime
        try:
            favorite.visit_date = datetime.strptime(data['visit_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
    
    try:
        db.session.commit()
        
        return jsonify({
            'message': 'Favorite updated',
            'favorite': favorite.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update favorite'}), 500
