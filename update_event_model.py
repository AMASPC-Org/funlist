
from flask_migrate import Migrate
from app import create_app
from db_init import db
from models import Event
from sqlalchemy import Column, Text

def update_event_model():
    """Update the Event model with new fields for fun rating justification and target audience description"""
    app = create_app()

    with app.app_context():
        # Check if the columns already exist first
        columns = [column.name for column in Event.__table__.columns]
        
        # Add the new columns if they don't exist
        if 'fun_rating_justification' not in columns:
            print("Adding fun_rating_justification field to Event model...")
            # Create a migration
            migrate = Migrate(app, db)
            with db.engine.connect() as conn:
                conn.execute(db.text('ALTER TABLE event ADD COLUMN fun_rating_justification TEXT'))
                print("Field fun_rating_justification added successfully")
        else:
            print("Field fun_rating_justification already exists")
            
        if 'target_audience_description' not in columns:
            print("Adding target_audience_description field to Event model...")
            # Create a migration
            migrate = Migrate(app, db)
            with db.engine.connect() as conn:
                conn.execute(db.text('ALTER TABLE event ADD COLUMN target_audience_description TEXT'))
                print("Field target_audience_description added successfully")
        else:
            print("Field target_audience_description already exists")
            
        # Commit the changes
        db.session.commit()
        print("Database updated successfully")

if __name__ == "__main__":
    update_event_model()
