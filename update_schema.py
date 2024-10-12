from app import app, db
from models import Event, User

def update_schema():
    with app.app_context():
        # Add the new columns to the Event table
        with db.engine.connect() as conn:
            conn.execute(db.text("ALTER TABLE event ADD COLUMN IF NOT EXISTS target_audience VARCHAR(50)"))
            conn.execute(db.text("ALTER TABLE event ADD COLUMN IF NOT EXISTS fun_meter INTEGER"))
            conn.execute(db.text("ALTER TABLE event ADD COLUMN IF NOT EXISTS latitude FLOAT"))
            conn.execute(db.text("ALTER TABLE event ADD COLUMN IF NOT EXISTS longitude FLOAT"))
            
            # Create the event_interests table
            conn.execute(db.text("""
                CREATE TABLE IF NOT EXISTS event_interests (
                    user_id INTEGER REFERENCES "user" (id),
                    event_id INTEGER REFERENCES event (id),
                    PRIMARY KEY (user_id, event_id)
                )
            """))
            
            # Create the event_attendances table
            conn.execute(db.text("""
                CREATE TABLE IF NOT EXISTS event_attendances (
                    user_id INTEGER REFERENCES "user" (id),
                    event_id INTEGER REFERENCES event (id),
                    PRIMARY KEY (user_id, event_id)
                )
            """))
            
            conn.commit()
    
    print("Database schema updated successfully.")

if __name__ == "__main__":
    update_schema()
