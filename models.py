from flask_login import UserMixin
from datetime import datetime
from db_init import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    account_active = db.Column(db.Boolean, default=True, nullable=False)
    last_login = db.Column(db.DateTime)

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return self.account_active

    def __repr__(self):
        return f'<User {self.email}>'
