from flask_login import UserMixin
from datetime import datetime, timedelta
from db_init import db  # Import db from db_init.py
import logging
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import time

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

    # Add relationship to User and SourceWebsite models
    organizer = db.relationship('User', backref='organized_events')
    source_website = db.relationship('SourceWebsite', backref='events')

    def __repr__(self):
        return f'<Event {self.title}>'

class SourceWebsite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<SourceWebsite {self.name}>'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    account_active = db.Column(db.Boolean, default=True, nullable=False)
    last_login = db.Column(db.DateTime)
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)

    # User roles
    is_subscriber = db.Column(db.Boolean, default=True)  # Default role for all users
    is_event_creator = db.Column(db.Boolean, default=False)  # Can create events
    is_admin = db.Column(db.Boolean, default=False)  # Admin access

    # Profile fields
    username = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    # is_admin is already defined above
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    interests = db.Column(db.String(200))
    birth_date = db.Column(db.Date)
    profile_updated_at = db.Column(db.DateTime)

    # User preferences
    audience_type = db.Column(db.String(20), nullable=True)
    preferred_locations = db.Column(db.String(255), nullable=True)
    event_interests = db.Column(db.String(255), nullable=True)
    is_premium = db.Column(db.Boolean, default=False)


    # Organizer fields
    is_organizer = db.Column(db.Boolean, default=False)
    company_name = db.Column(db.String(100))
    organizer_description = db.Column(db.Text)
    organizer_website = db.Column(db.String(200))
    advertising_opportunities = db.Column(db.Text)
    sponsorship_opportunities = db.Column(db.Text)
    organizer_profile_updated_at = db.Column(db.DateTime)

    # Vendor fields
    is_vendor = db.Column(db.Boolean, default=False)
    vendor_type = db.Column(db.String(50))
    vendor_description = db.Column(db.Text)
    vendor_profile_updated_at = db.Column(db.DateTime)

    def update_organizer_profile(self, organizer_data):
        for key, value in organizer_data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.is_organizer = True
        self.organizer_profile_updated_at = datetime.utcnow()

    def update_vendor_profile(self, vendor_data):
        for key, value in vendor_data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.is_vendor = True
        self.vendor_profile_updated_at = datetime.utcnow()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        if not password:
            return False
        result = check_password_hash(self.password_hash, password)
        return result

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

    # Password reset token methods
    def get_reset_token(self, expires_in=3600):
        # Generate a secure token with 32 bytes of randomness
        token = secrets.token_hex(32)
        # Set expiration timestamp (current time + expiration in seconds)
        expiry = int(time.time()) + expires_in

        # Try setting the fields and handle missing column exceptions gracefully
        try:
            self.reset_token = token
            self.reset_token_expiry = datetime.fromtimestamp(expiry)
            db.session.commit()
        except Exception as e:
            logger.error(f"Error setting reset token: {e}")
            # If the columns don't exist, we just return the token anyway
            db.session.rollback()

        return token

    @staticmethod
    def verify_reset_token(token):
        try:
            user = User.query.filter_by(reset_token=token).first()
            if not user:
                return None

            # Check if token is expired
            if datetime.utcnow() > user.reset_token_expiry:
                # Clear expired token
                user.reset_token = None
                user.reset_token_expiry = None
                db.session.commit()
                return None

            return user
        except Exception as e:
            logger.error(f"Error verifying reset token: {e}")
            return None

    def clear_reset_token(self):
        try:
            self.reset_token = None
            self.reset_token_expiry = None
            db.session.commit()
        except Exception as e:
            logger.error(f"Error clearing reset token: {e}")
            db.session.rollback()

# Add Subscriber Model
class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Subscriber {self.email}>'