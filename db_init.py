from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import DeclarativeBase
import logging

logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def init_engine(app):
    from sqlalchemy.exc import OperationalError
    from time import sleep

    for attempt in range(3):
        try:
            engine = create_engine(
                app.config['SQLALCHEMY_DATABASE_URI'],
                poolclass=QueuePool,
                pool_size=20,
                max_overflow=30,
                pool_timeout=30,
                pool_recycle=300,
                pool_pre_ping=True,
                echo_pool=True,
                connect_args={'connect_timeout': 10}
            )
            engine.connect()
            return engine
        except OperationalError as e:
            if attempt == 2:
                raise
            sleep(2 ** attempt)

def init_db(app):
    """Initialize database and create all tables"""
    try:
        logger.info("Initializing database...")
        with app.app_context():
            # Import all models to ensure they are registered with SQLAlchemy
            from models import User, Event, SourceWebsite, Subscriber
            # Create all tables
            db.create_all()
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise