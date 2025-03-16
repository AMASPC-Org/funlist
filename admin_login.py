
from flask import Flask
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import os
from db_init import db
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///instance/funlist.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app

def force_admin_login():
    """Creates or updates the admin user with known credentials"""
    app = create_app()
    with app.app_context():
        try:
            admin_email = 'ryan@funlist.ai'
            admin_password = '120M2025*v7'
            
            # Generate password hash
            password_hash = generate_password_hash(admin_password)
            
            # Check if admin exists
            admin_exists = db.session.execute(
                text(f"SELECT COUNT(*) FROM \"user\" WHERE email = '{admin_email}'")
            ).scalar()
            
            if admin_exists:
                # Update existing admin
                db.session.execute(text(f"""
                    UPDATE "user" 
                    SET password_hash = '{password_hash}',
                        is_admin = TRUE,
                        account_active = TRUE,
                        is_subscriber = TRUE
                    WHERE email = '{admin_email}'
                """))
                logger.info(f"Updated admin user: {admin_email}")
            else:
                # Create new admin
                db.session.execute(text(f"""
                    INSERT INTO "user" (
                        email, password_hash, is_admin, account_active, 
                        is_subscriber, created_at
                    ) VALUES (
                        '{admin_email}', '{password_hash}', TRUE, TRUE, 
                        TRUE, CURRENT_TIMESTAMP
                    )
                """))
                logger.info(f"Created new admin user: {admin_email}")
            
            # Commit changes
            db.session.commit()
            
            # Verify admin exists
            admin = db.session.execute(text(f"""
                SELECT id, email, is_admin, account_active 
                FROM "user" 
                WHERE email = '{admin_email}'
            """)).fetchone()
            
            if admin:
                logger.info(f"Admin user confirmed:")
                logger.info(f"  ID: {admin[0]}")
                logger.info(f"  Email: {admin[1]}")
                logger.info(f"  Is Admin: {admin[2]}")
                logger.info(f"  Active: {admin[3]}")
                return True
            else:
                logger.error("Failed to verify admin user after update/creation")
                return False
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in force_admin_login: {str(e)}")
            return False

if __name__ == "__main__":
    success = force_admin_login()
    if success:
        print("Admin account created/updated successfully.")
        print("Email: ryan@funlist.ai")
        print("Password: 120M2025*v7")
    else:
        print("Failed to create/update admin account.")
