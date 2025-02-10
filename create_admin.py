
from app import app
from models import User
from db_init import db

def create_admin():
    with app.app_context():
        admin = User.query.filter_by(email='ryan@funlist.ai').first()
        if not admin:
            admin = User(
                email='ryan@funlist.ai',
                is_admin=True,
                account_active=True
            )
            admin.set_password('120M2025*')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully")
        else:
            admin.is_admin = True
            admin.set_password('120M2025*')
            db.session.commit()
            print("Admin user updated successfully")

if __name__ == '__main__':
    create_admin()
