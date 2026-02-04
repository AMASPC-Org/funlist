from datetime import datetime
import json
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from firebase_config import get_db

class FirestoreModel:
    """Base class for Firestore-backed models."""
    collection_name = None

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get_collection(cls):
        db = get_db()
        return db.collection(cls.collection_name)

    @classmethod
    def get_by_id(cls, doc_id):
        if not doc_id:
            return None
        doc = cls.get_collection().document(str(doc_id)).get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return cls(**data)
        return None

    def save(self):
        db = get_db()
        data = {k: v for k, v in self.__dict__.items() if k != 'id' and not k.startswith('_')}
        if self.id:
            db.collection(self.collection_name).document(str(self.id)).set(data, merge=True)
        else:
            doc_ref = db.collection(self.collection_name).add(data)
            self.id = doc_ref[1].id
        return self

    def delete(self):
        if self.id:
            db = get_db()
            db.collection(self.collection_name).document(str(self.id)).delete()

    @classmethod
    def query(cls):
        """Returns the collection reference for querying."""
        return cls.get_collection()

class User(FirestoreModel, UserMixin):
    collection_name = 'users'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_active = kwargs.get('account_active', True)
        self.is_admin = kwargs.get('is_admin', False)
        self.is_subscriber = kwargs.get('is_subscriber', True)
        self._is_event_creator = kwargs.get('is_event_creator', False)
        self.created_at = kwargs.get('created_at', datetime.utcnow())

    @property
    def is_event_creator(self):
        return self.is_admin or self._is_event_creator

    @is_event_creator.setter
    def is_event_creator(self, value):
        self._is_event_creator = value

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        pass_hash = getattr(self, 'password_hash', None)
        if not pass_hash:
            return False
        return check_password_hash(pass_hash, password)

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        return self.account_active

class Event(FirestoreModel):
    collection_name = 'funlist_events'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status = kwargs.get('status', 'pending')
        self.created_at = kwargs.get('created_at', datetime.utcnow())

    def to_dict(self):
        # Maintain compatibility with existing to_dict calls
        return {
            'id': self.id,
            'title': getattr(self, 'title', ''),
            'description': getattr(self, 'description', ''),
            'start_date': self.start_date.strftime('%Y-%m-%d') if hasattr(self, 'start_date') and isinstance(self.start_date, datetime) else str(getattr(self, 'start_date', '')),
            'end_date': self.end_date.strftime('%Y-%m-%d') if hasattr(self, 'end_date') and isinstance(self.end_date, datetime) else str(getattr(self, 'end_date', '')),
            'location': getattr(self, 'location', ''),
            'city': getattr(self, 'city', ''),
            'state': getattr(self, 'state', ''),
            'status': self.status
        }

class Venue(FirestoreModel):
    collection_name = 'venues'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_verified = kwargs.get('is_verified', False)
        self.created_at = kwargs.get('created_at', datetime.utcnow())
