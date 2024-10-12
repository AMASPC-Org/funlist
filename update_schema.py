from app import app, db
from models import User, UserGroup, Event, OrganizerProfile
from sqlalchemy import text

def update_schema():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Add opt_in_email column if it doesn't exist
        with db.engine.connect() as conn:
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='user' AND column_name='opt_in_email'"))
            if result.fetchone() is None:
                conn.execute(text("ALTER TABLE \"user\" ADD COLUMN opt_in_email BOOLEAN DEFAULT FALSE"))
                print("Added opt_in_email column to User table")
        
        # Create default user groups if they don't exist
        default_groups = ['adult', 'parent', 'single', 'senior', 'young_adult', 'couple', '21_plus']
        for group_name in default_groups:
            group = UserGroup.query.filter_by(name=group_name).first()
            if group is None:
                new_group = UserGroup(name=group_name)
                db.session.add(new_group)
        
        db.session.commit()
    
    print("Database schema updated successfully.")

if __name__ == "__main__":
    update_schema()
