from datetime import datetime
from flask_login import UserMixin
from db_init import db
from werkzeug.security import generate_password_hash, check_password_hash
import json
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

# Define ProhibitedAdvertiserCategory FIRST
class ProhibitedAdvertiserCategory(db.Model):
    __tablename__ = 'prohibited_advertiser_categories'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

# Define the association table BEFORE Event model
event_prohibited_advertisers = Table(
    'event_prohibited_advertisers',
    db.Model.metadata,
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('prohibited_advertiser_categories.id'), primary_key=True),
    extend_existing=True
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    username = Column(String(80), unique=True, nullable=True)
    password_hash = Column(String(256), nullable=False)
    first_name = Column(String(120), nullable=True)
    last_name = Column(String(120), nullable=True)
    title = Column(String(100), nullable=True)
    account_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_subscriber = Column(Boolean, default=True)
    _is_event_creator = Column('is_event_creator', Boolean, default=False)
    is_organizer = Column(Boolean, default=False)
    is_vendor = Column(Boolean, default=False)
    is_sponsor = Column(Boolean, default=False)  # Added per requirements
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
    phone = Column(String(20), nullable=True)
    newsletter_opt_in = Column(Boolean, default=True)
    marketing_opt_in = Column(Boolean, default=False)
    user_preferences = Column(Text, nullable=True)

    oauth_provider = Column(String(20), nullable=True)
    oauth_provider_id = Column(String(255), nullable=True, unique=True)
    email_verified = Column(Boolean, default=False)
    business_street = Column(String(100), nullable=True)
    business_city = Column(String(50), nullable=True)
    business_state = Column(String(50), nullable=True)
    business_zip = Column(String(20), nullable=True)
    business_phone = Column(String(20), nullable=True)
    business_email = Column(String(120), nullable=True)

    facebook_url = Column(String(255), nullable=True)
    instagram_url = Column(String(255), nullable=True)
    twitter_url = Column(String(255), nullable=True)
    linkedin_url = Column(String(255), nullable=True)
    tiktok_url = Column(String(255), nullable=True)

    roles_last_updated = Column(DateTime, nullable=True)
    is_event_creator_last_known = Column(Boolean, default=False)
    is_organizer_last_known = Column(Boolean, default=False)
    is_vendor_last_known = Column(Boolean, default=False)
    is_sponsor_last_known = Column(Boolean, default=False)

    def is_active(self):
        return self.account_active

    @property
    def is_event_creator(self):
        return self.is_admin or self._is_event_creator

    @is_event_creator.setter
    def is_event_creator(self, value):
        self._is_event_creator = value

    @property
    def is_investor(self):
        # Placeholder role flag; not persisted while investor role is disabled
        return getattr(self, "_is_investor_flag", False)

    @is_investor.setter
    def is_investor(self, value):
        self._is_investor_flag = bool(value)

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

    def update_organizer_profile(self, data):
        if 'company_name' in data: self.company_name = data['company_name']
        if 'organizer_description' in data: self.organizer_description = data['organizer_description']
        if 'organizer_website' in data: self.organizer_website = data['organizer_website']
        if 'advertising_opportunities' in data: self.advertising_opportunities = data['advertising_opportunities']
        if 'sponsorship_opportunities' in data: self.sponsorship_opportunities = data['sponsorship_opportunities']
        self.organizer_profile_updated_at = datetime.utcnow()

    def update_profile(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        if self.is_organizer and 'company_name' in data:
            self.organizer_profile_updated_at = datetime.utcnow()
        if self.is_vendor and ('vendor_type' in data or 'vendor_description' in data):
            self.vendor_profile_updated_at = datetime.utcnow()

class Event(db.Model):
    __tablename__ = 'events'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    all_day = Column(Boolean, default=False)
    start_time = Column(String(8), nullable=True)
    end_time = Column(String(8), nullable=True)
    location = Column(String(255))
    street = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    zip_code = Column(String(20))
    parent_event_id = Column(Integer, ForeignKey('events.id'), nullable=True)
    is_recurring = Column(Boolean, default=False)
    recurring_pattern = Column(String(50), nullable=True)
    recurring_end_date = Column(DateTime, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
    website = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    venue_id = Column(Integer, ForeignKey('venues.id'))
    category = Column(String(100))
    target_audience = Column(String(255))
    tags = Column(String(255))
    attendance_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    featured = Column(Boolean, default=False)
    fun_rating = Column(Integer, default=50)  # UPDATED DEFAULT FOR 1-100 SCALE
    fun_meter = Column(Integer, default=50)   # UPDATED DEFAULT FOR 1-100 SCALE
    status = Column(String(50), default="pending")
    network_opt_out = Column(Boolean, default=False)

    event_frequency = Column(String(50), default="once")
    frequency_deduction = Column(Float, default=0.0)

    rsvp_required = Column(Boolean, default=False)
    ticket_required = Column(Boolean, default=False)
    ticket_purchase_url = Column(String(500), nullable=True)
    ticket_must_purchase_ahead = Column(Boolean, default=False)
    ticket_can_purchase_at_event = Column(Boolean, default=False)

    special_instructions = Column(Text, nullable=True)

    is_public_event = Column(Boolean, default=True)
    membership_required = Column(Boolean, default=False)
    membership_type = Column(String(255), nullable=True)

    host_name = Column(String(255), nullable=True)
    host_website = Column(String(500), nullable=True)
    host_social_media = Column(Text, nullable=True)

    venue_website = Column(String(500), nullable=True)
    venue_social_media = Column(Text, nullable=True)

    event_submitted_timestamp = Column(DateTime, default=datetime.utcnow)
    event_source = Column(String(50), nullable=True)
    disclaimer_checked = Column(Boolean, default=False)

    prohibited_advertisers = relationship(
        'ProhibitedAdvertiserCategory',
        secondary=event_prohibited_advertisers,
        backref=backref('events', lazy='dynamic'),
        lazy='joined'
    )
    user = relationship("User", back_populates="events")
    venue = relationship("Venue", back_populates="events")

    @hybrid_property
    def is_past(self):
        return self.end_date < datetime.utcnow() if self.end_date else self.start_date < datetime.utcnow()

    def is_advertiser_prohibited(self, advertiser_category_id):
        return any(cat.id == advertiser_category_id for cat in self.prohibited_advertisers)

    def get_prohibited_category_ids(self):
        return [cat.id for cat in self.prohibited_advertisers]

    def get_special_instructions(self):
        if self.special_instructions: return json.loads(self.special_instructions)
        return {}

    def set_special_instructions(self, instructions_dict):
        self.special_instructions = json.dumps(instructions_dict)

    def get_host_social_media(self):
        if self.host_social_media: return json.loads(self.host_social_media)
        return {}

    def set_host_social_media(self, socials_dict):
        self.host_social_media = json.dumps(socials_dict)

    def get_venue_social_media(self):
        if self.venue_social_media: return json.loads(self.venue_social_media)
        return {}

    def set_venue_social_media(self, socials_dict):
        self.venue_social_media = json.dumps(socials_dict)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'location': self.location,
            'city': self.city,
            'state': self.state,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'category': self.category,
            'fun_meter': self.fun_meter,
            'status': self.status
        }

class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    first_name = Column(String(120))
    last_name = Column(String(120))
    zip_code = Column(String(20))
    preferences = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    def get_preferences(self):
        if self.preferences: return json.loads(self.preferences)
        return {}
    def set_preferences(self, preferences_dict):
        self.preferences = json.dumps(preferences_dict)

class VenueType(db.Model):
    __tablename__ = 'venue_types'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    venues = relationship("Venue", back_populates="venue_type")
    def __repr__(self): return f"<VenueType {self.name}>"

class Venue(db.Model):
    __tablename__ = 'venues'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    street = Column(String(100), nullable=True)
    city = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    zip_code = Column(String(20), nullable=True)
    country = Column(String(50), default='United States')
    phone = Column(String(20), nullable=True)
    email = Column(String(120), nullable=True)
    website = Column(String(200), nullable=True)
    venue_type_id = Column(Integer, ForeignKey('venue_types.id'))
    contact_name = Column(String(100), nullable=True)
    contact_phone = Column(String(20), nullable=True)
    contact_email = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by_user_id = Column(Integer, ForeignKey('users.id'))
    owner_manager_user_id = Column(Integer, ForeignKey('users.id'))
    is_verified = Column(Boolean, default=False)
    verification_notes = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    description = Column(Text)
    venue_type = relationship("VenueType", back_populates="venues")
    created_by = relationship("User", foreign_keys=[created_by_user_id], backref=backref("created_venues", lazy="dynamic"))
    owner_manager = relationship("User", foreign_keys=[owner_manager_user_id], backref=backref("managed_venues", lazy="dynamic"))
    events = relationship("Event", back_populates="venue")
    def __repr__(self): return f"<Venue {self.name}>"

class Chapter(db.Model):
    __tablename__ = 'chapters'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), default='United States')
    logo_url = Column(String(255), nullable=True)
    banner_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    leader_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    leader = relationship("User", foreign_keys=[leader_user_id], backref="led_chapters")
    def __repr__(self): return f"<Chapter {self.name}>"

class HelpArticle(db.Model):
    __tablename__ = 'help_articles'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = Column(Boolean, default=True)
    view_count = Column(Integer, default=0)
    def __repr__(self): return f"<HelpArticle {self.title}>"

class AIAccessLog(db.Model):
    __tablename__ = 'ai_access_logs'
    __table_args__ = (
        db.Index('idx_ai_access_created_desc', 'created_at'),
        db.Index('idx_ai_access_consumer_created', 'consumer', 'created_at'),
        {'extend_existing': True}
    )
    id = Column(Integer, primary_key=True)
    consumer = Column(String(255), nullable=False, index=True)
    purpose = Column(String(255), nullable=False)
    api_key = Column(String(64), nullable=False)
    path = Column(String(255), nullable=False)
    ip_address = Column(String(45), nullable=False, index=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    success = Column(Boolean, default=True)
    error_message = Column(String(255), nullable=True)
    def __repr__(self): return f"<AIAccessLog {self.consumer} - {self.path}>"
    def to_dict(self):
        return {
            'id': self.id, 'consumer': self.consumer, 'purpose': self.purpose,
            'api_key_suffix': self.api_key[-4:] if len(self.api_key) > 4 else '****',
            'path': self.path, 'ip_address': self.ip_address, 'user_agent': self.user_agent,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'success': self.success, 'error_message': self.error_message
        }

class EventExclusionRule(db.Model):
    __tablename__ = 'event_exclusion_rules'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    exclusion_id = Column(String(50), unique=True, nullable=False, index=True)
    category_to_exclude = Column(String(255), nullable=False)
    exclusion_reason = Column(String(500), nullable=False)
    keywords_for_exclusion = Column(Text, nullable=True)
    status = Column(String(50), default='active', nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow, nullable=False)
    notes = Column(Text, nullable=True)
    created_by_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_by = relationship("User", foreign_keys=[created_by_user_id], backref="created_exclusion_rules")
    def __repr__(self): return f"<EventExclusionRule {self.exclusion_id}>"
    def get_keywords_list(self):
        if self.keywords_for_exclusion:
            return [kw.strip().lower() for kw in self.keywords_for_exclusion.split(',')]
        return []
    def matches_event(self, event_category, event_description):
        if self.status != 'active': return False
        if event_category and self.category_to_exclude.lower() in event_category.lower(): return True
        keywords = self.get_keywords_list()
        if keywords and event_description:
            event_desc_lower = event_description.lower()
            for keyword in keywords:
                if keyword in event_desc_lower: return True
        return False

class OrganizerMaster(db.Model):
    __tablename__ = 'organizer_master'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    website = Column(String(500), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(120), nullable=True)
    facebook_url = Column(String(255), nullable=True)
    instagram_url = Column(String(255), nullable=True)
    twitter_url = Column(String(255), nullable=True)
    linkedin_url = Column(String(255), nullable=True)
    tiktok_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_verified = Column(Boolean, default=False)
    def __repr__(self): return f"<OrganizerMaster {self.name}>"

class VenueMaster(db.Model):
    __tablename__ = 'venue_master'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    street = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(50), nullable=True)
    zip_code = Column(String(20), nullable=True)
    website = Column(String(500), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(120), nullable=True)
    facebook_url = Column(String(255), nullable=True)
    instagram_url = Column(String(255), nullable=True)
    twitter_url = Column(String(255), nullable=True)
    linkedin_url = Column(String(255), nullable=True)
    wheelchair_accessible = Column(Boolean, default=False)
    parking_available = Column(Boolean, default=False)
    parking_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_verified = Column(Boolean, default=False)
    def __repr__(self): return f"<VenueMaster {self.name}>"
