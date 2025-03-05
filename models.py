
from datetime import datetime
from flask_login import UserMixin
from db_init import db
from werkzeug.security import generate_password_hash, check_password_hash
import json
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    first_name = Column(String(120))
    last_name = Column(String(120))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    profile_image = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    bio = Column(Text)
    location = Column(String(200))
    website = Column(String(200))
    phone = Column(String(20))
    newsletter_opt_in = Column(Boolean, default=True)
    marketing_opt_in = Column(Boolean, default=False)
    user_preferences = Column(Text)  # Stored as JSON
    last_login = Column(DateTime)
    
    # Define relationships
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def get_preferences(self):
        if self.user_preferences:
            return json.loads(self.user_preferences)
        return {}
        
    def set_preferences(self, preferences_dict):
        self.user_preferences = json.dumps(preferences_dict)

class Event(db.Model):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    location = Column(String(255))
    street = Column(String(255))
    # address column removed as it doesn't exist in the database
    city = Column(String(100))
    state = Column(String(100))
    zip_code = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)
    image_url = Column(String(500))
    website = Column(String(255))
    contact_email = Column(String(120))
    contact_phone = Column(String(20))
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    price = Column(String(100))
    category = Column(String(100))
    target_audience = Column(String(255))
    tags = Column(String(255))  # Comma-separated tags
    attendance_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    featured = Column(Boolean, default=False)
    fun_rating = Column(Integer, default=3)  # Scale of 1-5
    fun_meter = Column(Integer, default=3)  # Alias for fun_rating
    status = Column(String(50), default="pending")  # draft, pending, approved, rejected
    
    # Define relationships
    user = relationship("User", back_populates="events")
    
    @hybrid_property
    def is_past(self):
        return self.end_date < datetime.utcnow() if self.end_date else self.start_date < datetime.utcnow()

class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    first_name = Column(String(120))
    last_name = Column(String(120))
    zip_code = Column(String(20))
    preferences = Column(Text)  # JSON string of preferences
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_preferences(self):
        if self.preferences:
            return json.loads(self.preferences)
        return {}
        
    def set_preferences(self, preferences_dict):
        self.preferences = json.dumps(preferences_dict)
