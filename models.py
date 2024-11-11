from flask_login import UserMixin
from datetime import datetime
from db_init import db
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    account_active = db.Column(db.Boolean, default=False, nullable=False)  # Changed default to False
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    email_verification_sent_at = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return self.account_active

    def __repr__(self):
        return f'<User {self.email}>'

    @staticmethod
    def generate_verification_token(email, secret_key):
        serializer = URLSafeTimedSerializer(secret_key)
        return serializer.dumps(email, salt='email-verification')

    @staticmethod
    def verify_token(token, secret_key, expiration=3600):
        serializer = URLSafeTimedSerializer(secret_key)
        try:
            email = serializer.loads(token, salt='email-verification', max_age=expiration)
            return email
        except (SignatureExpired, BadSignature):
            return None
