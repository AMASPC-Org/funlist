
from flask import Flask
from db_init import db
from models import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_admin():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/funlist.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    
    with app.app_context():
        try:
            # Create admin user
            admin = User()
            admin.email = 'admin@example.com'
            admin.set_password('admin123')
            admin.account_active = True
            admin.is_admin = True
            admin.is_event_creator = True
            admin.is_organizer = True
            db.session.add(admin)
            
            # Create regular test user
            user = User()
            user.email = 'user@example.com'
            user.set_password('user123')
            user.account_active = True
            db.session.add(user)
            
            db.session.commit()
            logger.info("Test users created successfully")
            
            print("Admin user created:")
            print("Email: admin@example.com")
            print("Password: admin123")
            print("\nRegular user created:")
            print("Email: user@example.com")
            print("Password: user123")
            
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating test users: {str(e)}")
            return False

if __name__ == "__main__":
    success = create_test_admin()
    if not success:
        print("Failed to create test users.")
