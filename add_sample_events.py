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
        start_date = datetime.now() + timedelta(days=7)
        events = [
            {
                "title": "Olympia Music Festival",
                "description": "A weekend of live music performances featuring local and national artists.",
                "start_date": start_date.date(),
                "end_date": (start_date + timedelta(days=2)).date(),
                "start_time": datetime.strptime('10:00', '%H:%M').time(),
                "end_time": datetime.strptime('22:00', '%H:%M').time(),
                "all_day": False,
                "recurring": False,
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
                "twitter": "https://twitter.com/olympiamusicfest",
                "status": "approved"
            },
            {
                "title": "Thurston County Fair",
                "description": "Annual county fair with rides, games, food, and exhibitions.",
                "start_date": (datetime.now() + timedelta(days=14)).date(),
                "end_date": (datetime.now() + timedelta(days=19)).date(),
                "start_time": datetime.strptime('09:00', '%H:%M').time(),
                "end_time": datetime.strptime('21:00', '%H:%M').time(),
                "all_day": False,
                "recurring": False,
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
                "twitter": "https://twitter.com/thurstoncountyfair",
                "status": "approved"
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