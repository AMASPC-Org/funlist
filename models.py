from flask_login import UserMixin
from datetime import datetime
from db_init import db
import logging
from werkzeug.security import generate_password_hash, check_password_hash

logger = logging.getLogger(__name__)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    all_day = db.Column(db.Boolean, default=False)
    recurring = db.Column(db.Boolean, default=False)
    recurrence_type = db.Column(db.String(20))
    recurrence_end_date = db.Column(db.Date)
    street = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=False)
    target_audience = db.Column(db.String(50), nullable=False)
    fun_meter = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class SourceWebsite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    events = db.relationship('Event', backref='source_website')

    def __repr__(self):
        return f'<SourceWebsite {self.name}>'


    zip_code = db.Column(db.String(20), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    target_audience = db.Column(db.String(50), nullable=False)
    fun_meter = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    website = db.Column(db.String(200))
    facebook = db.Column(db.String(200))
    instagram = db.Column(db.String(200))
    twitter = db.Column(db.String(200))
    event_url = db.Column(db.String(200))
    ticket_url = db.Column(db.String(200))
    ticket_price = db.Column(db.String(100))
    source_website_id = db.Column(db.Integer, db.ForeignKey('source_website.id'))
    scraped_at = db.Column(db.DateTime)
    last_updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    is_validated = db.Column(db.Boolean, default=False)
    needs_permission = db.Column(db.Boolean, default=False)
    permission_requested_at = db.Column(db.DateTime)
    permission_granted = db.Column(db.Boolean, default=False)

    # Add relationship to User model
    organizer = db.relationship('User', backref='organized_events')

    def __repr__(self):
        return f'<Event {self.title}>'

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
    is_admin = db.Column(db.Boolean, default=False)
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    interests = db.Column(db.String(200))
    birth_date = db.Column(db.Date)
    profile_updated_at = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Subscriber {self.email}>'