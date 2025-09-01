from app import db
from datetime import datetime
import uuid

class Housing(db.Model):
    __tablename__ = 'housing'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    price = db.Column(db.Integer, nullable=False)  # Monthly rent/mortgage
    bedrooms = db.Column(db.Integer, nullable=True)
    bathrooms = db.Column(db.Float, nullable=True)
    square_feet = db.Column(db.Integer, nullable=True)
    property_type = db.Column(db.String(50), nullable=True)  # apartment, house, condo, etc.
    available_date = db.Column(db.Date, nullable=True)
    images = db.Column(db.JSON, nullable=True)  # List of image URLs
    amenities = db.Column(db.JSON, nullable=True)  # List of amenities
    pet_friendly = db.Column(db.Boolean, default=False)
    parking_available = db.Column(db.Boolean, default=False)
    furnished = db.Column(db.Boolean, default=False)
    source = db.Column(db.String(50), nullable=True)  # API source (zillow, realtor, etc.)
    source_id = db.Column(db.String(100), nullable=True)  # External ID from source
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    favorites = db.relationship('Favorite', backref='housing', lazy=True, cascade='all, delete-orphan')
    commutes = db.relationship('Commute', backref='housing', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'price': self.price,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'square_feet': self.square_feet,
            'property_type': self.property_type,
            'available_date': self.available_date.isoformat() if self.available_date else None,
            'images': self.images,
            'amenities': self.amenities,
            'pet_friendly': self.pet_friendly,
            'parking_available': self.parking_available,
            'furnished': self.furnished,
            'source': self.source,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Housing {self.title}>'
