from app import app, db
from models import User

def create_test_user():
    with app.app_context():
        # Check if test user already exists
        if not User.query.filter_by(email='test@example.com').first():
            user = User()
            user.email = 'test@example.com'
            user.set_password('testpass123')
            user.account_active = True
            db.session.add(user)
            db.session.commit()
            print("Test user created successfully")
        else:
            print("Test user already exists")

if __name__ == '__main__':
    create_test_user()