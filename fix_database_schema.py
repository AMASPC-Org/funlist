
from flask import Flask
from db_init import db
import os
import logging
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///instance/funlist.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app

def fix_database_schema():
    app = create_app()
    with app.app_context():
        try:
            # Check existing columns
            inspector = db.inspect(db.engine)
            columns = [c['name'] for c in inspector.get_columns('user')]
            
            # Add new columns if they don't exist
            with db.engine.connect() as conn:
                # Add missing columns from User model
                if 'reset_token' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN reset_token VARCHAR(100)'))
                    conn.commit()
                    logger.info("Added reset_token column")
                
                if 'reset_token_expiry' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN reset_token_expiry TIMESTAMP'))
                    conn.commit()
                    logger.info("Added reset_token_expiry column")

                # Make sure admin user exists and has proper credentials
                conn.execute(text("""
                    INSERT INTO "user" (email, password_hash, is_admin, account_active, is_subscriber) 
                    VALUES ('ryan@americanmarketingalliance.com', 
                           'pbkdf2:sha256:600000$jEvAVRjlYYYSbtQb$9c2a7da5e79cb28ed9ec2308a2f0d2a4d0b268694fbb4e4ab6c1c6f9939ac2ae', 
                           TRUE, TRUE, TRUE)
                    ON CONFLICT (email) DO UPDATE SET 
                    is_admin = TRUE, 
                    account_active = TRUE,
                    password_hash = 'pbkdf2:sha256:600000$jEvAVRjlYYYSbtQb$9c2a7da5e79cb28ed9ec2308a2f0d2a4d0b268694fbb4e4ab6c1c6f9939ac2ae'
                """))
                conn.commit()

                logger.info("Admin user ensured with correct password")
            
            logger.info("Schema update completed successfully")
            return True
        except Exception as e:
            logger.error(f"Error updating schema: {str(e)}")
            return False

if __name__ == "__main__":
    success = fix_database_schema()
    if success:
        print("Schema updated successfully.")
    else:
        print("Failed to update schema.")
