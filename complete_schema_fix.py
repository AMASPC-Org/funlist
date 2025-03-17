
import logging
from sqlalchemy import inspect, text
from db_init import db
from app import create_app
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_database_schema():
    """Create or fix database tables to match current models"""
    app = create_app()
    
    with app.app_context():
        # Ensure the instance directory exists
        os.makedirs('instance', exist_ok=True)
        
        try:
            # First approach: Drop and recreate all tables
            # This is the most direct approach but will lose all existing data
            # Uncomment this if you want to start fresh:
            # db.drop_all()
            # db.create_all()
            # logger.info("All tables dropped and recreated")
            
            # Second approach: Keep existing data and alter tables
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            # Check if users table exists
            if 'users' not in tables:
                logger.info("Users table doesn't exist. Creating all tables...")
                db.create_all()
                logger.info("Tables created successfully.")
            else:
                # If users table exists, check and add missing columns
                columns = [column['name'] for column in inspector.get_columns('users')]
                logger.info(f"Existing columns in users table: {columns}")
                
                # Define required columns
                required_columns = [
                    ('is_event_creator', 'BOOLEAN DEFAULT FALSE'), 
                    ('is_organizer', 'BOOLEAN DEFAULT FALSE'),
                    ('is_vendor', 'BOOLEAN DEFAULT FALSE'),
                    ('vendor_type', 'VARCHAR(50)'),
                    ('vendor_description', 'TEXT'),
                    ('vendor_profile_updated_at', 'TIMESTAMP'),
                    ('company_name', 'VARCHAR(100)'),
                    ('organizer_description', 'TEXT'),
                    ('organizer_website', 'VARCHAR(200)'),
                    ('advertising_opportunities', 'TEXT'),
                    ('sponsorship_opportunities', 'TEXT'),
                    ('organizer_profile_updated_at', 'TIMESTAMP'),
                    ('bio', 'TEXT'),
                    ('location', 'VARCHAR(200)'),
                    ('phone', 'VARCHAR(20)'),
                    ('newsletter_opt_in', 'BOOLEAN DEFAULT TRUE'),
                    ('marketing_opt_in', 'BOOLEAN DEFAULT FALSE'),
                    ('user_preferences', 'TEXT'),
                    ('birth_date', 'TIMESTAMP'),
                    ('interests', 'TEXT')
                ]
                
                # Add missing columns
                for col_name, col_type in required_columns:
                    if col_name not in columns:
                        try:
                            logger.info(f"Adding column {col_name} to users table...")
                            db.session.execute(text(f"ALTER TABLE users ADD COLUMN IF NOT EXISTS {col_name} {col_type}"))
                            logger.info(f"Column {col_name} added successfully.")
                        except Exception as e:
                            logger.error(f"Error adding column {col_name}: {str(e)}")
                
                # Create test users for convenience
                try:
                    # Check if admin user exists
                    admin = db.session.execute(text("SELECT id FROM users WHERE email = 'admin@example.com'")).fetchone()
                    
                    if not admin:
                        from werkzeug.security import generate_password_hash
                        admin_hash = generate_password_hash('admin123')
                        
                        # Insert admin user
                        db.session.execute(text(f"""
                            INSERT INTO users (email, password_hash, is_admin, account_active, is_event_creator, is_organizer) 
                            VALUES ('admin@example.com', :password, TRUE, TRUE, TRUE, TRUE)
                        """), {"password": admin_hash})
                        
                        logger.info("Admin user created successfully")
                    
                    # Check if regular user exists
                    user = db.session.execute(text("SELECT id FROM users WHERE email = 'user@example.com'")).fetchone()
                    
                    if not user:
                        from werkzeug.security import generate_password_hash
                        user_hash = generate_password_hash('user123')
                        
                        # Insert regular user
                        db.session.execute(text(f"""
                            INSERT INTO users (email, password_hash, account_active, is_event_creator) 
                            VALUES ('user@example.com', :password, TRUE, TRUE)
                        """), {"password": user_hash})
                        
                        logger.info("Regular user created successfully")
                        
                except Exception as e:
                    logger.error(f"Error creating test users: {str(e)}")
            
            db.session.commit()
            logger.info("Database schema update completed")
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating schema: {str(e)}")
            logger.error("Schema update failed.")
            return False

if __name__ == "__main__":
    success = fix_database_schema()
    if success:
        print("Database schema fixed successfully.")
        print("You can now login with:")
        print("Admin - Email: admin@example.com, Password: admin123")
        print("User - Email: user@example.com, Password: user123")
    else:
        print("Failed to fix database schema.")
