from flask import Flask
from models import User
from db_init import db
import logging
from settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app

def add_admin_user(email, password):
    app = create_app()
    with app.app_context():
        try:
            # First make sure the schema is updated
            from update_schema import update_schema
            update_schema()

            # Now create or update the admin
            user = User.query.filter_by(email=email).first()
            if user:
                logger.info(f"User already exists: {email}")
                user.is_admin = True
                user.is_subscriber = True
                user.is_event_creator = True
                user.is_organizer = True
                user.account_active = True
                user.set_password(password)
                db.session.commit()
                logger.info(f"User updated with admin privileges: {email}")
            else:
                # Create new admin user
                user = User(
                    email=email,
                    is_admin=True,
                    is_subscriber=True,
                    is_event_creator=True,
                    is_organizer=True,
                    account_active=True
                )
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                logger.info(f"Admin user created: {email}")

            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating/updating admin user: {str(e)}")
            return False

if __name__ == "__main__":
    # Add main admin
    success1 = add_admin_user('ryan@americanmarketingalliance.com', '120M2025*v7')
    print(f"Admin user 1 created/updated: {'Successfully' if success1 else 'Failed'}")

    # Add additional admin
    success2 = add_admin_user('ryan.r.rutledge@gmail.com', '120M2025*v7')
    print(f"Admin user 2 created/updated: {'Successfully' if success2 else 'Failed'}")

    print("Admin users creation process completed.")
