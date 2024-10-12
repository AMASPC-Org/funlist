from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

user_groups = db.Table('user_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_name', db.String(50), db.ForeignKey('user_group.name'), primary_key=True)
)

event_interests = db.Table('event_interests',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

event_attendances = db.Table('event_attendances',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

class UserGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_organizer = db.Column(db.Boolean, default=False)
    opt_in_email = db.Column(db.Boolean, default=False)  # Added this line
    reset_token = db.Column(db.String(100), unique=True)
    events = db.relationship('Event', backref='organizer', lazy='dynamic')
    groups = db.relationship('UserGroup', secondary=user_groups,
        primaryjoin=(user_groups.c.user_id == id),
        secondaryjoin=(user_groups.c.group_name == UserGroup.name),
        backref=db.backref('users', lazy='dynamic'))
    interested_events = db.relationship('Event', secondary=event_interests, backref=db.backref('interested_users', lazy='dynamic'))
    attended_events = db.relationship('Event', secondary=event_attendances, backref=db.backref('attendees', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    category = db.Column(db.String(50), nullable=False)
    target_audience = db.Column(db.String(50), nullable=False)
    fun_meter = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class OrganizerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    website = db.Column(db.String(200))
    advertising_opportunities = db.Column(db.Text)
    sponsorship_opportunities = db.Column(db.Text)
