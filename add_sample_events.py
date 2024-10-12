from app import app, db
from models import Event, User
from datetime import datetime, timedelta
import random

def add_sample_events():
    with app.app_context():
        # Create a sample user if not exists
        user = User.query.filter_by(email="sample@example.com").first()
        if not user:
            user = User(username="SampleUser", email="sample@example.com", is_organizer=True)
            user.set_password("password123")
            db.session.add(user)
            db.session.commit()

        # Sample event data
        events = [
            {
                "title": "Olympia Music Festival",
                "description": "A weekend of live music performances featuring local and national artists.",
                "category": "music",
                "target_audience": "adults",
                "fun_meter": 5
            },
            {
                "title": "Thurston County Fair",
                "description": "Annual county fair with rides, games, food, and exhibitions.",
                "category": "other",
                "target_audience": "family",
                "fun_meter": 4
            },
            {
                "title": "Lakefair Fireworks Show",
                "description": "Spectacular fireworks display over Capitol Lake.",
                "category": "other",
                "target_audience": "inclusive",
                "fun_meter": 5
            },
            {
                "title": "Olympia Farmers Market",
                "description": "Weekly market featuring local produce, crafts, and food vendors.",
                "category": "food",
                "target_audience": "inclusive",
                "fun_meter": 3
            },
            {
                "title": "Olympia Film Society Movie Night",
                "description": "Screening of independent and classic films at the historic Capitol Theater.",
                "category": "arts",
                "target_audience": "adults",
                "fun_meter": 4
            }
        ]

        # Add events to the database
        for event_data in events:
            event = Event(
                title=event_data["title"],
                description=event_data["description"],
                date=datetime.now() + timedelta(days=random.randint(1, 30)),
                location="Olympia, WA",
                category=event_data["category"],
                target_audience=event_data["target_audience"],
                fun_meter=event_data["fun_meter"],
                user_id=user.id
            )
            db.session.add(event)

        db.session.commit()
        print("Sample events added successfully.")

if __name__ == "__main__":
    add_sample_events()
