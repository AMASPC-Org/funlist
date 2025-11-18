#!/usr/bin/env python3
"""
Smart Event Import Script with Recurring Event Support
Handles recurring events properly - same name, different dates are treated as separate events
"""

import json
import os
import sys
from datetime import datetime
from app import create_app
from apps.funlist.models import Event
from db_init import db

def parse_time(time_str):
    """Parse time string to HH:MM format."""
    if not time_str:
        return None
    try:
        # Try parsing various time formats
        for fmt in ['%I:%M %p', '%H:%M', '%I:%M%p', '%H:%M:%S']:
            try:
                time_obj = datetime.strptime(time_str, fmt)
                return time_obj.strftime('%H:%M')
            except ValueError:
                continue
    except:
        pass
    return None

def import_events(json_file_path='events.json', handle_recurring=True):
    """
    Import events from JSON file with smart duplicate detection.
    
    Args:
        json_file_path: Path to JSON file containing events
        handle_recurring: If True, allows events with same name but different dates
    """
    app = create_app()
    
    with app.app_context():
        print(f"\n{'='*60}")
        print(f"SMART EVENT IMPORT SCRIPT")
        print(f"{'='*60}")
        print(f"Starting import from {json_file_path}...")
        print(f"Recurring events handling: {'ENABLED' if handle_recurring else 'DISABLED'}")
        print()

        # Load JSON data
        try:
            with open(json_file_path, 'r') as f:
                events_data = json.load(f)
        except FileNotFoundError:
            print(f"❌ ERROR: Could not find file: {json_file_path}")
            return
        except json.JSONDecodeError:
            print(f"❌ ERROR: Invalid JSON in file: {json_file_path}")
            return

        # Track import statistics
        stats = {
            'added': 0,
            'skipped_duplicates': 0,
            'skipped_invalid': 0,
            'recurring_added': 0,
            'updated': 0
        }
        
        # Track events by name for recurring detection
        events_by_name = {}

        print(f"Found {len(events_data)} events in JSON file\n")
        print(f"{'='*60}")

        for idx, event in enumerate(events_data, 1):
            event_name = event.get('eventName', 'Untitled Event')
            event_date_str = event.get('eventDate')
            
            # Parse date
            try:
                event_date_obj = datetime.strptime(event_date_str, '%Y-%m-%d')
            except (ValueError, TypeError):
                print(f"⚠️  [{idx:3}] Invalid date for '{event_name}': {event_date_str}")
                stats['skipped_invalid'] += 1
                continue

            # Check for existing event (same title AND date)
            existing_event = Event.query.filter_by(
                title=event_name,
                start_date=event_date_obj
            ).first()

            if existing_event:
                print(f"⏭️  [{idx:3}] Skipped duplicate: '{event_name}' on {event_date_str}")
                stats['skipped_duplicates'] += 1
                continue

            # Track if this is a recurring event (same name, different date)
            is_recurring = event_name in events_by_name
            if is_recurring:
                stats['recurring_added'] += 1
                recurring_marker = " 🔄 [RECURRING]"
            else:
                recurring_marker = ""
                events_by_name[event_name] = []
            
            events_by_name[event_name].append(event_date_str)

            # Parse address
            address_parts = event.get('locationAddress', '').split(', ')
            street = address_parts[0] if len(address_parts) > 0 else ''
            zip_code = address_parts[-1].split()[-1] if len(address_parts) > 2 else ''

            # Create new event with additional metadata
            new_event = Event(
                title=event_name,
                description=event.get('description'),
                start_date=event_date_obj,
                start_time=parse_time(event.get('eventTime')),
                location=event.get('locationName'),
                street=street,
                city=event.get('city', 'Olympia'),  # Default city
                state=event.get('state', 'WA'),
                zip_code=zip_code,
                website=event.get('sourceURL'),
                category=event.get('primaryEventType'),
                target_audience=', '.join(event.get('initialTags', [])),
                tags=', '.join(event.get('initialTags', [])),
                status='approved',  # Auto-approve curated events
                featured='Tree Lighting' in event_name or 'Parade' in event_name,
                is_recurring=is_recurring  # Mark as recurring if applicable
            )

            db.session.add(new_event)
            stats['added'] += 1
            print(f"✅  [{idx:3}] Added: '{event_name}' on {event_date_str}{recurring_marker}")

        # Commit all changes
        try:
            db.session.commit()
            print(f"\n{'='*60}")
            print(f"IMPORT COMPLETE!")
            print(f"{'='*60}")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR during commit: {str(e)}")
            return

        # Print summary statistics
        print(f"\n📊 IMPORT STATISTICS:")
        print(f"{'='*60}")
        print(f"✅ Successfully added:     {stats['added']} events")
        if stats['recurring_added'] > 0:
            print(f"   └─ Recurring events:    {stats['recurring_added']} events")
        print(f"⏭️  Skipped (duplicates):   {stats['skipped_duplicates']} events")
        print(f"⚠️  Skipped (invalid data): {stats['skipped_invalid']} events")
        print(f"{'='*60}")
        
        # Show recurring event series
        recurring_series = {name: dates for name, dates in events_by_name.items() if len(dates) > 1}
        if recurring_series:
            print(f"\n🔄 RECURRING EVENT SERIES DETECTED:")
            print(f"{'='*60}")
            for event_name, dates in sorted(recurring_series.items()):
                print(f"  • {event_name}")
                for date in sorted(dates):
                    print(f"      - {date}")
        
        # Final database count
        total_events = Event.query.count()
        approved_events = Event.query.filter_by(status='approved').count()
        print(f"\n📈 DATABASE STATUS:")
        print(f"{'='*60}")
        print(f"Total events in database:  {total_events}")
        print(f"Approved events:           {approved_events}")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    # Allow passing custom JSON file as argument
    json_file = sys.argv[1] if len(sys.argv) > 1 else 'events.json'
    import_events(json_file)