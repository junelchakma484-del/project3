from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)  # Nullable for OAuth users
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    work_address = db.Column(db.String(255), nullable=True)
    work_lat = db.Column(db.Float, nullable=True)
    work_lng = db.Column(db.Float, nullable=True)
    max_commute_time = db.Column(db.Integer, nullable=True)  # in minutes
    budget_min = db.Column(db.Integer, nullable=True)
    budget_max = db.Column(db.Integer, nullable=True)
    preferred_areas = db.Column(db.JSON, nullable=True)  # List of preferred areas
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # OAuth fields
    oauth_provider = db.Column(db.String(20), nullable=True)  # 'google', 'github'
    oauth_id = db.Column(db.String(100), nullable=True)
    
    # Relationships
    favorites = db.relationship('Favorite', backref='user', lazy=True, cascade='all, delete-orphan')
    commutes = db.relationship('Commute', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'work_address': self.work_address,
            'work_lat': self.work_lat,
            'work_lng': self.work_lng,
            'max_commute_time': self.max_commute_time,
            'budget_min': self.budget_min,
            'budget_max': self.budget_max,
            'preferred_areas': self.preferred_areas,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
