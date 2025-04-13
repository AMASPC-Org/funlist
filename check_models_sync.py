
from app import create_app
from sqlalchemy import inspect
from models import User, Event, Venue, VenueType, ProhibitedAdvertiserCategory, Subscriber
from db_init import db
import sys

def check_model_sync():
    """Check if SQLAlchemy models are in sync with the database"""
    app = create_app()
    
    models = [User, Event, Venue, VenueType, ProhibitedAdvertiserCategory, Subscriber]
    
    with app.app_context():
        inspector = inspect(db.engine)
        tables_in_db = inspector.get_table_names()
        
        print(f"Tables in database: {tables_in_db}")
        
        # Check if all model tables exist in database
        for model in models:
            table_name = model.__tablename__
            if table_name not in tables_in_db:
                print(f"WARNING: Table '{table_name}' for model {model.__name__} does not exist in database")
                continue
                
            print(f"Checking model {model.__name__} (table: {table_name})...")
            
            # Get columns from model
            model_columns = {column.name for column in model.__table__.columns}
            
            # Get columns from database
            db_columns = {column['name'] for column in inspector.get_columns(table_name)}
            
            # Find differences
            missing_in_db = model_columns - db_columns
            extra_in_db = db_columns - model_columns
            
            if missing_in_db:
                print(f"  WARNING: Columns in model but not in database: {missing_in_db}")
            if extra_in_db:
                print(f"  INFO: Columns in database but not in model: {extra_in_db}")
            
            if not missing_in_db and not extra_in_db:
                print(f"  OK: Model {model.__name__} is in sync with database")

if __name__ == "__main__":
    print("Checking if SQLAlchemy models are in sync with the database...")
    check_model_sync()
    print("Check complete.")
