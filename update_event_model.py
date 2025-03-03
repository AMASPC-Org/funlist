
from flask_migrate import Migrate
from app import create_app
from db_init import db
from models import Event
from sqlalchemy import Column, Text, inspect

def update_event_model():
    """Update the Event model with new fields for fun rating justification and target audience description"""
    app = create_app()

    with app.app_context():
        try:
            # Check if the columns already exist using database-agnostic approach
            inspector = inspect(db.engine)
            columns = [column['name'] for column in inspector.get_columns('event')]
            
            # Add the new columns if they don't exist
            with db.engine.connect() as conn:
                # Use transactions for better reliability
                conn = conn.execution_options(isolation_level="AUTOCOMMIT")
                
                if 'fun_rating_justification' not in columns:
                    print("Adding fun_rating_justification field to Event model...")
                    conn.execute(db.text('ALTER TABLE event ADD COLUMN fun_rating_justification TEXT'))
                    print("Field fun_rating_justification added successfully")
                else:
                    print("Field fun_rating_justification already exists")
                
                if 'target_audience_description' not in columns:
                    print("Adding target_audience_description field to Event model...")
                    conn.execute(db.text('ALTER TABLE event ADD COLUMN target_audience_description TEXT'))
                    print("Field target_audience_description added successfully")
                else:
                    print("Field target_audience_description already exists")
            
            # Ensure SQLAlchemy knows about these new columns
            db.session.commit()
            db.metadata.clear()
            db.reflect()
            print("Database updated successfully")
        except Exception as e:
            print(f"Error updating database: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    update_event_model()
