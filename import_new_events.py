
#!/usr/bin/env python3
"""
Import events directly into the database
"""

import os
from datetime import datetime
from app import create_app
from db_init import db
from models import Event

def parse_time(time_str):
    """Parse time string to HH:MM format."""
    if not time_str or time_str == "N/A":
        return None
    
    # Handle time ranges like "3:30 PM - 9:00 PM"
    if ' - ' in time_str:
        start_time = time_str.split(' - ')[0].strip()
    else:
        start_time = time_str.strip()
    
    try:
        time_obj = datetime.strptime(start_time, '%I:%M %p')
        return time_obj.strftime('%H:%M')
    except:
        return None

def import_events_to_db():
    """Import the new events directly to database"""
    
    events_data = [
        {
            "eventName": "Oly on Ice Opening Weekend",
            "eventDate": "2025-11-21",
            "eventTime": "3:30 PM - 9:00 PM",
            "locationName": "Isthmus Park",
            "locationAddress": "529 4th Ave W, Olympia, WA 98501",
            "city": "Olympia",
            "county": "Thurston",
            "cost": "$12 - $15",
            "sourceURL": "https://www.olyonice.com",
            "description": "Skate into the season at this pop-up outdoor ice rink featuring special opening weekend performances and hot cocoa.",
            "primaryEventType": "Sports / Fitness Event",
            "venueType": "Park / Outdoor Space",
            "initialTags": ["Families", "Kids", "Teens", "Date Night", "Fitness & Active"]
        },
        {
            "eventName": "Live Music: The Fabulous Roof Shakers",
            "eventDate": "2025-11-21",
            "eventTime": "7:00 PM - 10:00 PM",
            "locationName": "Nicole's Bar",
            "locationAddress": "109 Legion Way SW, Olympia, WA 98501",
            "city": "Olympia",
            "county": "Thurston",
            "cost": "Free",
            "sourceURL": "https://www.nicolesbar.com/events",
            "description": "Enjoy an evening of high-energy R&B, blues, and classic rock covers in a lively downtown bar setting.",
            "primaryEventType": "Live Music",
            "venueType": "Bar / Pub / Tavern",
            "initialTags": ["Adults", "Date Night", "Singles", "21+"]
        },
        {
            "eventName": "Olympia Farmers Market: Holiday Season",
            "eventDate": "2025-11-22",
            "eventTime": "10:00 AM - 3:00 PM",
            "locationName": "Olympia Farmers Market",
            "locationAddress": "700 Capitol Way N, Olympia, WA 98501",
            "city": "Olympia",
            "county": "Thurston",
            "cost": "Free",
            "sourceURL": "https://www.olympiafarmersmarket.com",
            "description": "Shop for fresh seasonal produce, artisan crafts, and holiday gifts while enjoying live daily entertainment and hot food vendors.",
            "primaryEventType": "Market / Bazaar",
            "venueType": "Park / Outdoor Space",
            "initialTags": ["Families", "Adults", "Seniors", "Food & Drink"]
        },
        {
            "eventName": "Family Storytime & Craft",
            "eventDate": "2025-11-22",
            "eventTime": "10:30 AM - 11:30 AM",
            "locationName": "Tumwater Timberland Library",
            "locationAddress": "7023 New Market St SW, Tumwater, WA 98501",
            "city": "Tumwater",
            "county": "Thurston",
            "cost": "Free",
            "sourceURL": "https://www.trl.org/events",
            "description": "A special Saturday morning storytime featuring interactive songs, stories, and a simple hands-on craft for children and caregivers.",
            "primaryEventType": "Kids & Family Activity",
            "venueType": "Library",
            "initialTags": ["Kids", "Families"]
        },
        {
            "eventName": "Olympia Farmers Market: Holiday Season",
            "eventDate": "2025-11-23",
            "eventTime": "10:00 AM - 3:00 PM",
            "locationName": "Olympia Farmers Market",
            "locationAddress": "700 Capitol Way N, Olympia, WA 98501",
            "city": "Olympia",
            "county": "Thurston",
            "cost": "Free",
            "sourceURL": "https://www.olympiafarmersmarket.com",
            "description": "Shop for fresh seasonal produce, artisan crafts, and holiday gifts while enjoying live daily entertainment and hot food vendors.",
            "primaryEventType": "Market / Bazaar",
            "venueType": "Park / Outdoor Space",
            "initialTags": ["Families", "Adults", "Seniors", "Food & Drink"]
        }
    ]
    
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("DIRECT DATABASE EVENT IMPORT")
        print("="*60 + "\n")
        
        added = 0
        skipped = 0
        
        for event_data in events_data:
            event_name = event_data['eventName']
            event_date_str = event_data['eventDate']
            
            # Parse date
            try:
                event_date_obj = datetime.strptime(event_date_str, '%Y-%m-%d')
            except (ValueError, TypeError):
                print(f"❌ Invalid date for '{event_name}': {event_date_str}")
                continue
            
            # Check for duplicate
            existing = Event.query.filter_by(
                title=event_name,
                start_date=event_date_obj
            ).first()
            
            if existing:
                print(f"⏭️  Skipped duplicate: {event_name} on {event_date_str}")
                skipped += 1
                continue
            
            # Parse address
            address = event_data.get('locationAddress', '')
            address_parts = address.split(', ')
            street = address_parts[0] if len(address_parts) > 0 else ''
            zip_code = address_parts[-1].split()[-1] if len(address_parts) >= 3 else ''
            
            # Create new event
            new_event = Event(
                title=event_name,
                description=event_data.get('description'),
                start_date=event_date_obj,
                start_time=parse_time(event_data.get('eventTime')),
                location=event_data.get('locationName'),
                street=street,
                city=event_data.get('city', 'Olympia'),
                state='WA',
                zip_code=zip_code,
                website=event_data.get('sourceURL'),
                category=event_data.get('primaryEventType'),
                target_audience=', '.join(event_data.get('initialTags', [])),
                tags=', '.join(event_data.get('initialTags', [])),
                status='approved',
                fun_meter=4  # Default rating
            )
            
            db.session.add(new_event)
            added += 1
            print(f"✅ Added: {event_name} on {event_date_str}")
        
        # Commit all changes
        db.session.commit()
        
        print("\n" + "="*60)
        print(f"IMPORT COMPLETE")
        print(f"  Added: {added} events")
        print(f"  Skipped: {skipped} duplicates")
        print("="*60 + "\n")

if __name__ == "__main__":
    import_events_to_db()
