
#!/usr/bin/env python3

from datetime import datetime, timedelta, time
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

        # Sample events with coordinates
        events = [
            {
                "title": "Olympia Music Festival",
                "description": "A weekend of live music performances featuring local and national artists.",
                "date": datetime.now() + timedelta(days=7),
                "street": "416 Washington St SE",
                "city": "Olympia",
                "state": "WA",
                "zip_code": "98501",
                "category": "Music",
                "target_audience": "Adults",
                "fun_meter": 5,
                "latitude": 47.0379,
                "longitude": -122.9007
            },
            {
                "title": "Thurston County Fair",
                "description": "Annual county fair with rides, games, food, and exhibitions.",
                "date": datetime.now() + timedelta(days=14),
                "street": "3054 Carpenter Rd SE",
                "city": "Lacey",
                "state": "WA",
                "zip_code": "98503",
                "category": "Other",
                "target_audience": "Family",
                "fun_meter": 4,
                "latitude": 47.0343,
                "longitude": -122.8815
            },
            {
                "title": "Downtown Art Walk",
                "description": "Explore local art galleries and meet artists.",
                "date": datetime.now() + timedelta(days=3),
                "street": "205 4th Ave E",
                "city": "Olympia",
                "state": "WA",
                "zip_code": "98501",
                "category": "Arts",
                "target_audience": "Adults",
                "fun_meter": 4,
                "latitude": 47.0448,
                "longitude": -122.8982
            },
            {
                "title": "Food Truck Festival",
                "description": "Sample diverse cuisines from local food trucks.",
                "date": datetime.now() + timedelta(days=5),
                "street": "700 Capitol Way N",
                "city": "Olympia",
                "state": "WA",
                "zip_code": "98501",
                "category": "Food",
                "target_audience": "Everyone",
                "fun_meter": 5,
                "latitude": 47.0478,
                "longitude": -122.9020
            }
        ]

        # Add events to database
        time_slots = [
            (time(10, 0), time(18, 0)),  # 10 AM - 6 PM
            (time(14, 0), time(22, 0)),  # 2 PM - 10 PM
            (time(9, 0), time(17, 0)),   # 9 AM - 5 PM
            (time(11, 0), time(20, 0))   # 11 AM - 8 PM
        ]
        
        for idx, event_data in enumerate(events):
            start_time, end_time = time_slots[idx % len(time_slots)]
            event = Event(
                title=event_data["title"],
                description=event_data["description"],
                start_date=event_data["date"],
                end_date=event_data["date"],
                start_time=start_time,
                end_time=end_time,
                street=event_data["street"],
                city=event_data["city"],
                state=event_data["state"],
                zip_code=event_data["zip_code"],
                category=event_data["category"],
                target_audience=event_data["target_audience"],
                fun_meter=event_data["fun_meter"],
                latitude=event_data["latitude"],
                longitude=event_data["longitude"],
                user_id=test_user.id,
                status='approved'  # Set status to approved so events show up immediately
            )
            db.session.add(event)

        try:
            db.session.commit()
            print("Sample events added successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding events: {str(e)}")

if __name__ == "__main__":
    add_sample_events()
