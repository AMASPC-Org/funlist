from flask_login import UserMixin
from datetime import datetime
from db_init import db
import logging

logger = logging.getLogger(__name__)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    account_active = db.Column(db.Boolean, default=True, nullable=False)
    last_login = db.Column(db.DateTime)
    
    # Profile fields
    username = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    interests = db.Column(db.String(200))
    birth_date = db.Column(db.Date)
    profile_updated_at = db.Column(db.DateTime)

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return self.account_active

    def update_profile(self, profile_data):
        for key, value in profile_data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.profile_updated_at = datetime.utcnow()

    def __repr__(self):
        return f'<User {self.email}>'
