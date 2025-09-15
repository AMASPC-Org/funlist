
import logging
import os
from sqlalchemy import inspect, text
from flask import Flask
from db_init import db
import models  # Import to register models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_database():
    """Create or fix the database tables to match current models"""
    # Create Flask app
    app = Flask(__name__)
    
    # Ensure the instance directory exists
    os.makedirs('instance', exist_ok=True)
    
    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/funlist.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            logger.info("Database tables created successfully.")
            
            # Create test user and admin accounts
            from werkzeug.security import generate_password_hash
            from models import User
            
            # Check if admin exists
            admin = User.query.filter_by(email='admin@example.com').first()
            if not admin:
                admin = User(
                    email='admin@example.com',
                    password_hash=generate_password_hash('admin123'),
                    is_admin=True,
                    account_active=True
                )
                db.session.add(admin)
                logger.info("Admin user created.")
            
            # Check if test user exists
            user = User.query.filter_by(email='user@example.com').first()
            if not user:
                user = User(
                    email='user@example.com',
                    password_hash=generate_password_hash('user123'),
                    account_active=True
                )
                db.session.add(user)
                logger.info("Test user created.")
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error fixing database: {str(e)}")
            return False

if __name__ == "__main__":
    success = fix_database()
    if success:
        print("Database fixed successfully.")
        print("You can log in with:")
        print("Admin - Email: admin@example.com, Password: admin123")
        print("User - Email: user@example.com, Password: user123")
    else:
        print("Failed to fix database.")
