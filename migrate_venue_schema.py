import os
import sys
import logging
from sqlalchemy import Column, Boolean, DateTime, Float, Text, ForeignKey, String, Integer
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def add_column(conn, cursor, table, column_name, column_type):
    """Add a column to the table if it doesn't exist"""
    try:
        # First commit any pending transactions (to avoid transaction block errors)
        conn.commit()
        
        # Check if column exists
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}' AND column_name = '{column_name}'")
        if cursor.fetchone() is None:
            logger.info(f"Adding {column_name} column to {table} table")
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column_name} {column_type}")
            conn.commit()
            return True
        return False
    except Exception as e:
        logger.error(f"Error adding column {column_name}: {str(e)}")
        conn.rollback()
        return False

def migrate_venue_schema():
    """Updates venue table schema to match the current model."""
    try:
        from app import db
        from sqlalchemy import inspect
        import psycopg2
        
        # Check if venues table exists
        inspector = inspect(db.engine)
        if 'venues' not in inspector.get_table_names():
            logger.info("Venues table doesn't exist. Creating it...")
            # Create venues table using SQLAlchemy
            with db.engine.connect() as conn:
                conn.execute(text("""
                CREATE TABLE venues (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    street VARCHAR(100),
                    city VARCHAR(50),
                    state VARCHAR(50),
                    zip_code VARCHAR(20),
                    country VARCHAR(50) DEFAULT 'United States',
                    phone VARCHAR(20),
                    email VARCHAR(120),
                    website VARCHAR(200),
                    venue_type_id INTEGER REFERENCES venue_types(id),
                    contact_name VARCHAR(100),
                    contact_phone VARCHAR(20),
                    contact_email VARCHAR(120),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_verified BOOLEAN DEFAULT FALSE,
                    verification_notes TEXT,
                    latitude FLOAT,
                    longitude FLOAT,
                    description TEXT,
                    created_by_user_id INTEGER REFERENCES users(id),
                    owner_manager_user_id INTEGER REFERENCES users(id)
                )
                """))
                conn.commit()
            logger.info("Venues table created successfully.")
            return True
        
        # If the venues table exists but might be missing columns,
        # get database connection from environment
        db_url = os.environ.get('DATABASE_URL')
        
        if not db_url:
            logger.error("DATABASE_URL environment variable not set")
            return False
        
        # Connect to the database
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # List of columns to check and add if they don't exist
        columns_to_check = [
            ('created_by_user_id', 'INTEGER REFERENCES users(id)'),
            ('owner_manager_user_id', 'INTEGER REFERENCES users(id)'),
            ('is_verified', 'BOOLEAN DEFAULT FALSE'),
            ('verification_notes', 'TEXT'),
            ('latitude', 'FLOAT'),
            ('longitude', 'FLOAT'),
            ('description', 'TEXT'),
            ('updated_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
        ]
        
        # Add columns if they don't exist
        added_columns = []
        for column_name, column_type in columns_to_check:
            if add_column(conn, cursor, 'venues', column_name, column_type):
                added_columns.append(column_name)
        
        # Check if venue_types table exists
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'venue_types')")
        venue_types_exists = cursor.fetchone()[0]
        
        if not venue_types_exists:
            logger.info("Creating venue_types table...")
            cursor.execute("""
            CREATE TABLE venue_types (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(100),
                description TEXT
            )
            """)
            
            # Add some default venue types
            cursor.execute("""
            INSERT INTO venue_types (name, category) VALUES
            ('Conference Center', 'Commercial'),
            ('Hotel', 'Commercial'),
            ('Restaurant', 'Commercial'),
            ('Theater', 'Entertainment'),
            ('Museum', 'Cultural'),
            ('Park', 'Outdoor'),
            ('Sports Arena', 'Sports'),
            ('Community Center', 'Public'),
            ('University', 'Educational'),
            ('Bar/Club', 'Entertainment'),
            ('Gallery', 'Cultural'),
            ('Stadium', 'Sports'),
            ('Other', 'Miscellaneous')
            """)
            conn.commit()
            logger.info("venue_types table created and populated with default values.")
        
        if added_columns:
            logger.info(f"Added the following columns to the venues table: {', '.join(added_columns)}")
        else:
            logger.info("All required columns already exist in the venues table")
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        return True
    except SQLAlchemyError as e:
        logger.error(f"SQL error updating venue schema: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error updating venue schema: {str(e)}")
        return False

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        migrate_venue_schema()
