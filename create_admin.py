
from app import app
from models import User
from db_init import db

def create_admin():
    with app.app_context():
        admin = User.query.filter_by(email='ryan@americanmarketingalliance.com').first()
        if not admin:
            admin = User(
                email='ryan@americanmarketingalliance.com',
                is_admin=True,
                account_active=True
            )
            admin.set_password('120M2025*v7')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully")
        else:
            # Update existing admin
            admin.is_admin = True  # Ensure admin flag is set
            admin.account_active = True  # Ensure account is active
            admin.set_password('120M2025*v7')  # Reset password to ensure it's correct
            db.session.commit()
            print("Admin user updated successfully")
            
        # Verify admin was created/updated properly
        verify = User.query.filter_by(email='ryan@americanmarketingalliance.com').first()
        if verify and verify.is_admin:
            print(f"Verified admin user exists with ID: {verify.id}")
            test_pw = verify.check_password('120M2025*v7')
            print(f"Password check result: {test_pw}")
        else:
            print("ERROR: Admin verification failed!")

if __name__ == '__main__':
    create_admin()
