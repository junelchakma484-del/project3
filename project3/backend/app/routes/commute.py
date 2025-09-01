from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.commute import Commute
from app.models.housing import Housing
from app.models.user import User
import math

commute_bp = Blueprint('commute', __name__)

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two points"""
    R = 3959  # Earth's radius in miles
    lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

@commute_bp.route('/calculate', methods=['POST'])
@jwt_required()
def calculate_commute():
    """Calculate commute time for a housing listing"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    data = request.get_json()
    
    if not data.get('housing_id'):
        return jsonify({'error': 'Housing ID is required'}), 400
    
    if not user.work_lat or not user.work_lng:
        return jsonify({'error': 'Work location not set'}), 400
    
    housing = Housing.query.get(data['housing_id'])
    if not housing:
        return jsonify({'error': 'Housing not found'}), 404
    
    # Calculate distance and estimated time
    distance_miles = calculate_distance(
        user.work_lat, user.work_lng,
        housing.latitude, housing.longitude
    )
    
    route_type = data.get('route_type', 'driving')
    duration_minutes = int(distance_miles * 2)  # Rough estimate
    
    # Calculate costs
    fuel_cost = (distance_miles / 25) * 3.50 if route_type == 'driving' else None
    total_commute_cost = fuel_cost + 10 if fuel_cost else None  # Add parking
    
    # Create commute record
    commute = Commute(
        user_id=user_id,
        housing_id=data['housing_id'],
        distance_miles=distance_miles,
        duration_minutes=duration_minutes,
        route_type=route_type,
        fuel_cost=fuel_cost,
        total_commute_cost=total_commute_cost
    )
    
    try:
        db.session.add(commute)
        db.session.commit()
        
        return jsonify({
            'message': 'Commute calculated successfully',
            'commute': commute.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to calculate commute'}), 500

@commute_bp.route('/history', methods=['GET'])
@jwt_required()
def get_commute_history():
    """Get user's commute history"""
    user_id = get_jwt_identity()
    
    commutes = Commute.query.filter_by(user_id=user_id).order_by(
        Commute.calculated_at.desc()
    ).all()
    
    commute_list = [commute.to_dict() for commute in commutes]
    
    return jsonify({'commutes': commute_list}), 200
