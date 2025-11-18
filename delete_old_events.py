
#!/usr/bin/env python3
"""
Delete events from November 14th, 2025 or earlier
"""

from app import create_app
from models import Event
from db_init import db
from datetime import datetime

def delete_old_events():
    """Remove all events on or before November 14th, 2025."""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("DELETING OLD EVENTS")
        print("="*60)
        
        # Set the cutoff date (Nov 14, 2025 at end of day)
        cutoff_date = datetime(2025, 11, 14, 23, 59, 59)
        
        # Find all events on or before the cutoff date
        old_events = Event.query.filter(
            Event.start_date <= cutoff_date
        ).all()
        
        if not old_events:
            print("✅ No events found from November 14th, 2025 or earlier!")
            return
        
        print(f"\nFound {len(old_events)} events to delete:\n")
        
        for event in old_events:
            print(f"  • '{event.title}' on {event.start_date.strftime('%Y-%m-%d')}")
        
        # Delete the events
        Event.query.filter(
            Event.start_date <= cutoff_date
        ).delete()
        
        # Commit the deletion
        db.session.commit()
        
        print(f"\n{'='*60}")
        print(f"✅ DELETION COMPLETE!")
        print(f"Removed {len(old_events)} events from Nov 14, 2025 or earlier")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    delete_old_events()
