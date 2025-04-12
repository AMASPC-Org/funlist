
import logging
from flask import Flask
from db_init import db
from sqlalchemy import text, inspect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_network_opt_out_column():
    app = Flask(__name__)
    # Use the existing database configuration from your app
    app.config.from_object('app.config.Config')
    db.init_app(app)
    
    with app.app_context():
        try:
            # Check if network_opt_out column exists using inspect
            inspector = inspect(db.engine)
            columns = [column['name'] for column in inspector.get_columns('events')]
            
            if 'network_opt_out' not in columns:
                logger.info("Adding missing network_opt_out column to events table")
                # Use PostgreSQL syntax for adding column
                db.session.execute(text("ALTER TABLE events ADD COLUMN IF NOT EXISTS network_opt_out BOOLEAN DEFAULT FALSE"))
                db.session.commit()
                logger.info("Added network_opt_out column successfully")
            else:
                logger.info("network_opt_out column already exists")
                
            return True
        except Exception as e:
            logger.error(f"Error adding network_opt_out column: {str(e)}")
            return False

if __name__ == "__main__":
    success = add_network_opt_out_column()
    if success:
        print("Database schema updated successfully.")
    else:
        print("Failed to update database schema.")
