from app import app, db
from models import Event

def update_schema():
    with app.app_context():
        # Add the new columns to the Event table
        with db.engine.connect() as conn:
            conn.execute(db.text("ALTER TABLE event ADD COLUMN IF NOT EXISTS target_audience VARCHAR(50)"))
            conn.execute(db.text("ALTER TABLE event ADD COLUMN IF NOT EXISTS fun_meter INTEGER"))
            conn.commit()
    
    print("Database schema updated successfully.")

if __name__ == "__main__":
    update_schema()
