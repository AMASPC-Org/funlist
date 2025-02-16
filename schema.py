from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    account_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    is_admin = Column(Boolean, default=False)

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(String(2000))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)
    category = Column(String(50))
    fun_meter = Column(Float)
    status = Column(String(20), default='pending')  # pending, approved, rejected
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

# Export the table definitions for use in routes
users = User.__table__
events = Event.__table__
