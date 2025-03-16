from flask import Flask
from db_init import db
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_database_schema():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/funlist'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        try:
            with db.engine.connect() as conn:
                # Update admin user credentials
                conn.execute(text("""
                    INSERT INTO users (email, password_hash, is_admin, account_active) 
                    VALUES ('ryan@funlist.ai', 
                           'pbkdf2:sha256:600000$jEvAVRjlYYYSbtQb$9c2a7da5e79cb28ed9ec2308a2f0d2a4d0b268694fbb4e4ab6c1c6f9939ac2ae', 
                           TRUE, TRUE)
                    ON CONFLICT (email) DO UPDATE SET 
                    is_admin = TRUE, 
                    account_active = TRUE,
                    password_hash = 'pbkdf2:sha256:600000$jEvAVRjlYYYSbtQb$9c2a7da5e79cb28ed9ec2308a2f0d2a4d0b268694fbb4e4ab6c1c6f9939ac2ae'
                """))
                conn.commit()

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