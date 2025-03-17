
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
    username = Column(String(120), unique=True, nullable=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    first_name = Column(String(120), nullable=True)
    last_name = Column(String(120), nullable=True)
    account_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_event_creator = Column(Boolean, default=False)
    is_organizer = Column(Boolean, default=False)
    is_vendor = Column(Boolean, default=False)
    vendor_type = Column(String(50), nullable=True)
    vendor_description = Column(Text, nullable=True)
    vendor_profile_updated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    company_name = Column(String(100), nullable=True)
    organizer_description = Column(Text, nullable=True)
    organizer_website = Column(String(200), nullable=True)
    advertising_opportunities = Column(Text, nullable=True)
    sponsorship_opportunities = Column(Text, nullable=True)
    organizer_profile_updated_at = Column(DateTime, nullable=True)
    bio = Column(Text, nullable=True)
    location = Column(String(200), nullable=True)
    phone = Column(String(20), nullable=True)
    newsletter_opt_in = Column(Boolean, default=True)
    marketing_opt_in = Column(Boolean, default=False)
    user_preferences = Column(Text, nullable=True)  # Stored as JSON
    birth_date = Column(DateTime, nullable=True)
    interests = Column(Text, nullable=True)

    def is_active(self):
        return self.account_active
        
    @property
    def is_event_creator(self):
        return self.is_admin or self._is_event_creator

    @is_event_creator.setter
    def is_event_creator(self, value):
        self._is_event_creator = value

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
    all_day = Column(Boolean, default=False)
    start_time = Column(String(8), nullable=True)  # Format: HH:MM:SS
    end_time = Column(String(8), nullable=True)    # Format: HH:MM:SS
    location = Column(String(255))
    street = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    zip_code = Column(String(20))
    parent_event_id = Column(Integer, ForeignKey('events.id'), nullable=True)
    is_recurring = Column(Boolean, default=False)
    recurring_pattern = Column(String(50), nullable=True)  # daily, weekly, monthly, etc.
    recurring_end_date = Column(DateTime, nullable=True)
    
    # Relationships
    parent_event = relationship("Event", remote_side=[id], backref=backref("sub_events"))
    latitude = Column(Float)
    longitude = Column(Float)
    website = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
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
