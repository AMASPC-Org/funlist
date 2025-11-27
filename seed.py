"""Seed script to insert a small set of sample events and related data.

Usage:
    python seed.py

This script is idempotent: running it multiple times will update existing
records (matched by unique keys) and only insert new ones when needed.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, Iterable, List

from app import create_app
from db_init import db
from models import Chapter, Event


def ensure_chapters(chapters: Iterable[Dict]) -> List[Chapter]:
    """Create chapters if they do not already exist."""
    created_or_existing = []
    for data in chapters:
        chapter = Chapter.query.filter_by(slug=data["slug"]).first()
        if chapter:
            # Update any changed fields to keep the record fresh.
            chapter.name = data["name"]
            chapter.city = data.get("city")
            chapter.state = data.get("state")
            chapter.description = data.get("description")
        else:
            chapter = Chapter(**data)
            db.session.add(chapter)
        created_or_existing.append(chapter)
    return created_or_existing


def upsert_events(events: Iterable[Dict]) -> List[Event]:
    """Insert or update events, matching by title + start_date for idempotency."""
    persisted = []
    for data in events:
        match = Event.query.filter_by(
            title=data["title"], start_date=data["start_date"]
        ).first()
        if match:
            for key, value in data.items():
                setattr(match, key, value)
            event = match
        else:
            event = Event(**data)
            db.session.add(event)
        persisted.append(event)
    return persisted


def seed(app=None):
    flask_app = app or create_app()
    with flask_app.app_context():
        # Ensure a couple of chapters for navigation/dropdowns.
        chapter_payload = [
            {
                "name": "Olympia",
                "slug": "olympia-wa",
                "city": "Olympia",
                "state": "WA",
                "description": "Olympia metro events",
            },
            {
                "name": "Tacoma",
                "slug": "tacoma-wa",
                "city": "Tacoma",
                "state": "WA",
                "description": "Tacoma & South Sound events",
            },
        ]

        ensure_chapters(chapter_payload)

        # Base dates for sample events.
        now = datetime.utcnow()
        tomorrow = now + timedelta(days=1)
        weekend = now + timedelta(days=(5 - now.weekday()) % 7)
        next_week = now + timedelta(days=7)

        sample_events = [
            {
                "title": "Capitol Lake Sunset Concert",
                "description": "Live music by local bands with food trucks and craft vendors.",
                "start_date": tomorrow.replace(hour=18, minute=0, second=0, microsecond=0),
                "end_date": tomorrow.replace(hour=21, minute=0, second=0, microsecond=0),
                "location": "Capitol Lake Park",
                "city": "Olympia",
                "state": "WA",
                "latitude": 47.0405,
                "longitude": -122.9075,
                "category": "Music",
                "fun_rating": 5,
                "fun_meter": 5,
                "status": "approved",
            },
            {
                "title": "Downtown Art Walk",
                "description": "Gallery hop with artist meetups, pop-up exhibits, and family art stations.",
                "start_date": weekend.replace(hour=11, minute=0, second=0, microsecond=0),
                "end_date": weekend.replace(hour=16, minute=0, second=0, microsecond=0),
                "location": "Downtown Olympia",
                "city": "Olympia",
                "state": "WA",
                "latitude": 47.0452,
                "longitude": -122.9016,
                "category": "Arts",
                "fun_rating": 4,
                "fun_meter": 4,
                "status": "approved",
            },
            {
                "title": "Farmers Market Brunch Bash",
                "description": "Seasonal produce, live acoustic sets, and kids' cooking demos.",
                "start_date": weekend.replace(hour=9, minute=0, second=0, microsecond=0),
                "end_date": weekend.replace(hour=13, minute=0, second=0, microsecond=0),
                "location": "Olympia Farmers Market",
                "city": "Olympia",
                "state": "WA",
                "latitude": 47.0480,
                "longitude": -122.8958,
                "category": "Food",
                "fun_rating": 4,
                "fun_meter": 4,
                "status": "approved",
            },
            {
                "title": "Tacoma Waterfront Fun Run",
                "description": "5K/10K along Ruston Way with ocean views, finisher medals, and snacks.",
                "start_date": next_week.replace(hour=8, minute=30, second=0, microsecond=0),
                "end_date": next_week.replace(hour=11, minute=0, second=0, microsecond=0),
                "location": "Ruston Way Waterfront",
                "city": "Tacoma",
                "state": "WA",
                "latitude": 47.2852,
                "longitude": -122.4765,
                "category": "Sports",
                "fun_rating": 5,
                "fun_meter": 5,
                "status": "approved",
            },
            {
                "title": "Lakefair Family Movie Night",
                "description": "Outdoor screening with picnic spots, lawn games, and dessert trucks.",
                "start_date": next_week.replace(hour=19, minute=30, second=0, microsecond=0),
                "end_date": next_week.replace(hour=22, minute=0, second=0, microsecond=0),
                "location": "Heritage Park",
                "city": "Olympia",
                "state": "WA",
                "latitude": 47.0415,
                "longitude": -122.9020,
                "category": "Family",
                "fun_rating": 4,
                "fun_meter": 4,
                "status": "approved",
            },
        ]

        upsert_events(sample_events)
        db.session.commit()

        summary = {"chapters": len(chapter_payload), "events": len(sample_events)}
        print(f"Seed complete: {summary['events']} events ensured.")
        return summary


if __name__ == "__main__":
    seed()
