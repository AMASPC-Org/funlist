from app import app, db
from models import User
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

def update_schema():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Add profile columns if they don't exist
        profile_columns = {
            'username': 'VARCHAR(50)',
            'first_name': 'VARCHAR(50)',
            'last_name': 'VARCHAR(50)',
            'bio': 'TEXT',
            'location': 'VARCHAR(100)',
            'interests': 'VARCHAR(200)',
            'birth_date': 'DATE',
            'profile_updated_at': 'TIMESTAMP'
        }
        
        with db.engine.connect() as conn:
            for column, data_type in profile_columns.items():
                try:
                    result = conn.execute(text(
                        f"SELECT column_name FROM information_schema.columns "
                        f"WHERE table_name='user' AND column_name='{column}'"
                    ))
                    if result.fetchone() is None:
                        conn.execute(text(f'ALTER TABLE "user" ADD COLUMN {column} {data_type}'))
                        logger.info(f"Added {column} column to User table")
                    else:
                        logger.info(f"{column} column already exists in User table")
                except Exception as e:
                    logger.error(f"Error adding column {column}: {str(e)}")
                    raise
            
            conn.commit()
    
    logger.info("Database schema updated successfully.")

if __name__ == "__main__":
    update_schema()
