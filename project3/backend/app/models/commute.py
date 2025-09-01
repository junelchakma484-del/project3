from app import db
from datetime import datetime
import uuid

class Commute(db.Model):
    __tablename__ = 'commutes'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    housing_id = db.Column(db.String(36), db.ForeignKey('housing.id'), nullable=False)
    
    # Commute details
    distance_miles = db.Column(db.Float, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    traffic_duration_minutes = db.Column(db.Integer, nullable=True)
    route_type = db.Column(db.String(20), nullable=False)  # driving, walking, transit, biking
    departure_time = db.Column(db.Time, nullable=True)  # Preferred departure time
    arrival_time = db.Column(db.Time, nullable=True)  # Calculated arrival time
    
    # Route details
    route_summary = db.Column(db.Text, nullable=True)
    route_polyline = db.Column(db.Text, nullable=True)  # Encoded polyline for map display
    waypoints = db.Column(db.JSON, nullable=True)  # Route waypoints
    
    # Cost analysis
    fuel_cost = db.Column(db.Float, nullable=True)
    transit_cost = db.Column(db.Float, nullable=True)
    parking_cost = db.Column(db.Float, nullable=True)
    total_commute_cost = db.Column(db.Float, nullable=True)
    
    # Metadata
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_favorite = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'housing_id': self.housing_id,
            'distance_miles': self.distance_miles,
            'duration_minutes': self.duration_minutes,
            'traffic_duration_minutes': self.traffic_duration_minutes,
            'route_type': self.route_type,
            'departure_time': self.departure_time.isoformat() if self.departure_time else None,
            'arrival_time': self.arrival_time.isoformat() if self.arrival_time else None,
            'route_summary': self.route_summary,
            'route_polyline': self.route_polyline,
            'waypoints': self.waypoints,
            'fuel_cost': self.fuel_cost,
            'transit_cost': self.transit_cost,
            'parking_cost': self.parking_cost,
            'total_commute_cost': self.total_commute_cost,
            'calculated_at': self.calculated_at.isoformat() if self.calculated_at else None,
            'is_favorite': self.is_favorite
        }
    
    def __repr__(self):
        return f'<Commute {self.id}>'
