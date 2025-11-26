import os
import sys
import logging
from werkzeug.security import generate_password_hash
from sqlalchemy import text
import psycopg2
from psycopg2 import sql

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

def fix_admin_login():
    """Creates or updates the admin user with expected credentials"""
    try:
        # Get database connection string from environment
        db_url = os.environ.get('DATABASE_URL')
        
        if not db_url:
            logger.error("DATABASE_URL environment variable not set")
            return False
        
        # Connect to the database
        conn = psycopg2.connect(db_url)
        conn.autocommit = False
        cursor = conn.cursor()
        
        # First ensure all columns exist to avoid transaction errors
        columns_to_check = [
            ('is_subscriber', 'BOOLEAN DEFAULT TRUE'),
            ('is_sponsor', 'BOOLEAN DEFAULT FALSE'),
            ('roles_last_updated', 'TIMESTAMP'),
            ('is_event_creator_last_known', 'BOOLEAN DEFAULT FALSE'),
            ('is_organizer_last_known', 'BOOLEAN DEFAULT FALSE'),
            ('is_vendor_last_known', 'BOOLEAN DEFAULT FALSE'),
            ('is_sponsor_last_known', 'BOOLEAN DEFAULT FALSE'),
            ('facebook_url', 'VARCHAR(255)'),
            ('instagram_url', 'VARCHAR(255)'),
            ('twitter_url', 'VARCHAR(255)'),
            ('linkedin_url', 'VARCHAR(255)'),
            ('tiktok_url', 'VARCHAR(255)'),
            ('business_phone', 'VARCHAR(20)'),
            ('business_email', 'VARCHAR(120)')
        ]
        
        for column_name, column_type in columns_to_check:
            add_column(conn, cursor, 'users', column_name, column_type)
        
        # Hash the password
        password_hash = generate_password_hash("120M2025*v7")
        
        # Check if the user already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", ("ryan@funlist.ai",))
        user = cursor.fetchone()
        
        # Start a new transaction for the user creation/update
        conn.commit()
        
        if user:
            # Update the existing admin user
            user_id = user[0]
            logger.info(f"Updating existing admin user with ID: {user_id}")
            
            # Use parameterized query to update
            cursor.execute(
                """
                UPDATE users 
                SET password_hash = %s, 
                    is_admin = TRUE, 
                    account_active = TRUE, 
                    first_name = 'Ryan', 
                    last_name = 'Admin',
                    is_subscriber = TRUE
                WHERE id = %s
                """,
                (password_hash, user_id)
            )
            logger.info("Admin user updated successfully")
        else:
            # Create a new admin user
            logger.info("Creating new admin user")
            
            # Use parameterized query for insertion
            cursor.execute(
                """
                INSERT INTO users (
                    email, password_hash, first_name, last_name, 
                    is_admin, account_active, created_at, is_subscriber
                ) VALUES (%s, %s, %s, %s, %s, %s, NOW(), TRUE)
                """,
                ("ryan@funlist.ai", password_hash, "Ryan", "Admin", True, True)
            )
            logger.info("Admin user created successfully")
        
        # Commit changes
        conn.commit()
        
        # Verify the user was created/updated
        cursor.execute("SELECT id, email, is_admin FROM users WHERE email = %s", ("ryan@funlist.ai",))
        admin_user = cursor.fetchone()
        if admin_user:
            logger.info(f"Verified admin user: ID={admin_user[0]}, Email={admin_user[1]}, IsAdmin={admin_user[2]}")
        else:
            logger.error("Failed to verify admin user after creation/update")
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        logger.error(f"Error fixing admin login: {str(e)}")
        if 'conn' in locals() and conn:
            try:
                conn.rollback()
                if 'cursor' in locals() and cursor:
                    cursor.close()
                conn.close()
            except:
                pass
        return False

if __name__ == "__main__":
    # Run the function directly
    fix_admin_login()
