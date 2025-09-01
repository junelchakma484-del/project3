from app import db
from datetime import datetime
import uuid

class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    housing_id = db.Column(db.String(36), db.ForeignKey('housing.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Notes and preferences
    notes = db.Column(db.Text, nullable=True)
    priority = db.Column(db.Integer, default=1)  # 1-5 scale
    visit_date = db.Column(db.Date, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'housing_id': self.housing_id,
            'notes': self.notes,
            'priority': self.priority,
            'visit_date': self.visit_date.isoformat() if self.visit_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Favorite {self.id}>'
