from app import app, db
from models import User, UserGroup
from werkzeug.security import generate_password_hash

def create_test_user():
    with app.app_context():
        # Check if the test user already exists
        test_user = User.query.filter_by(email='testuser@example.com').first()
        if not test_user:
            # Create a new test user
            test_user = User(email='testuser@example.com', is_organizer=False, opt_in_email=True)
            test_user.set_password('testpassword')
            
            # Add user groups
            groups = ['adult', 'single']
            for group_name in groups:
                group = UserGroup.query.filter_by(name=group_name).first()
                if group is None:
                    group = UserGroup(name=group_name)
                    db.session.add(group)
                test_user.groups.append(group)
            
            db.session.add(test_user)
            db.session.commit()
            print("Test user created successfully.")
        else:
            print("Test user already exists.")

    print("Test user email: testuser@example.com")
    print("Test user password: testpassword")

if __name__ == "__main__":
    create_test_user()
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
