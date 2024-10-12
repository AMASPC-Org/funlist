from app import app, db
from models import Event, User

def update_schema():
    with app.app_context():
        # Remove the username column from the User table
        with db.engine.connect() as conn:
            conn.execute(db.text("ALTER TABLE user DROP COLUMN IF EXISTS username"))
            
            # Add the is_organizer column to the User table if it doesn't exist
            conn.execute(db.text("ALTER TABLE user ADD COLUMN IF NOT EXISTS is_organizer BOOLEAN DEFAULT FALSE"))
            
            conn.commit()
    
    print("Database schema updated successfully.")

if __name__ == "__main__":
    update_schema()
