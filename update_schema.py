from app import app, db
from models import User, UserGroup, Event, OrganizerProfile

def update_schema():
    with app.app_context():
        db.create_all()
        
        # Create default user groups if they don't exist
        default_groups = ['adult', 'parent', 'single', 'senior', 'young_adult', 'couple', '21_plus']
        for group_name in default_groups:
            group = UserGroup.query.filter_by(name=group_name).first()
            if group is None:
                new_group = UserGroup(name=group_name)
                db.session.add(new_group)
        
        db.session.commit()
    
    print("Database schema updated successfully.")

if __name__ == "__main__":
    update_schema()
