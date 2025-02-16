from datetime import datetime, timedelta
import random
from models import Event, User
from db_init import db
from app import app

def add_sample_events():
    with app.app_context():
        # Create a test user if not exists
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            test_user = User(email='test@example.com')
            test_user.set_password('test123')
            db.session.add(test_user)
            db.session.commit()

        # Sample events with coordinates and social media links
        events = [
            {
                "title": "Olympia Music Festival",
                "description": "A weekend of live music performances featuring local and national artists.",
                "date": datetime.now() + timedelta(days=7),
                "street": "416 Washington St SE",
                "city": "Olympia",
                "state": "WA",
                "zip_code": "98501",
                "category": "music",
                "target_audience": "adults",
                "fun_meter": 5,
                "latitude": 47.0379,
                "longitude": -122.9007,
                "website": "https://olympiamusicfest.com",
                "facebook": "https://facebook.com/olympiamusicfest",
                "instagram": "https://instagram.com/olympiamusicfest",
                "twitter": "https://twitter.com/olympiamusicfest"
            },
            {
                "title": "Thurston County Fair",
                "description": "Annual county fair with rides, games, food, and exhibitions.",
                "date": datetime.now() + timedelta(days=14),
                "street": "3054 Carpenter Rd SE",
                "city": "Lacey",
                "state": "WA",
                "zip_code": "98503",
                "category": "other",
                "target_audience": "family",
                "fun_meter": 4,
                "latitude": 47.0343,
                "longitude": -122.8815,
                "website": "https://thurstoncountyfair.com",
                "facebook": "https://facebook.com/thurstoncountyfair",
                "instagram": "https://instagram.com/thurstoncountyfair",
                "twitter": "https://twitter.com/thurstoncountyfair"
            }
        ]

        # Add events to database
        for event_data in events:
            event = Event(user_id=test_user.id, **event_data)
            db.session.add(event)

        db.session.commit()
        print("Sample events added successfully!")

if __name__ == "__main__":
    add_sample_events()