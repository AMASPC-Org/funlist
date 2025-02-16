from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def init_engine(app):
    return create_engine(
        app.config['SQLALCHEMY_DATABASE_URI'],
        poolclass=QueuePool,
        pool_size=20,
        max_overflow=30,
        pool_timeout=30,
        pool_recycle=300,
        pool_pre_ping=True,
        echo_pool=True
    )

# Add error handling, logging, and rate limiting here.  This is a placeholder for the features omitted from the provided changes.