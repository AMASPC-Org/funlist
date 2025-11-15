
import json
from datetime import datetime
from app import create_app
from db_init import db
from apps.funlist.models import Event

# --- Configuration ---
JSON_FILE_PATH = 'events.json'
# ---------------------

def parse_time(time_str):
    """Parse time string and return start time in HH:MM format"""
    if not time_str or time_str == "N/A":
        return None
    
    if ' - ' in time_str:
        start_time = time_str.split(' - ')[0].strip()
    else:
        start_time = time_str.strip()
    
    try:
        time_obj = datetime.strptime(start_time, '%I:%M %p')
        return time_obj.strftime('%H:%M')
    except:
        return None

def import_events():
    """
    Reads events from a JSON file and adds them to the database.
    Checks for duplicates before adding.
    """
    app = create_app()
    with app.app_context():
        print(f"Starting import from {JSON_FILE_PATH}...")

        try:
            with open(JSON_FILE_PATH, 'r') as f:
                events_data = json.load(f)
        except FileNotFoundError:
            print(f"--- ERROR ---")
            print(f"Could not find the file: {JSON_FILE_PATH}")
            print(f"Make sure you created 'events.json' in the root of your Repl.")
            print(f"-----------------")
            return
        except json.JSONDecodeError:
            print(f"--- ERROR ---")
            print(f"Could not read the file: {JSON_FILE_PATH}")
            print(f"It seems to be invalid JSON. Make sure you copied everything correctly.")
            print(f"-----------------")
            return

        added_count = 0
        skipped_count = 0

        for event in events_data:
            event_name = event.get('eventName')
            event_date_str = event.get('eventDate')

            # Convert string date to a Python date object
            try:
                event_date_obj = datetime.strptime(event_date_str, '%Y-%m-%d')
            except (ValueError, TypeError):
                print(f"Skipping event with invalid date: {event_name}")
                continue

            # --- Duplicate Check ---
            existing_event = db.session.query(Event).filter_by(
                title=event_name,
                start_date=event_date_obj
            ).first()

            if existing_event:
                print(f"Skipping duplicate: {event_name} on {event_date_str}")
                skipped_count += 1
                continue

            # --- Parse Address ---
            address_parts = event.get('locationAddress', '').split(', ')
            street = address_parts[0] if len(address_parts) > 0 else ''
            zip_code = address_parts[-1].split()[-1] if len(address_parts) > 2 else ''

            # --- Create New Event ---
            new_event = Event(
                title=event_name,
                description=event.get('description'),
                start_date=event_date_obj,
                start_time=parse_time(event.get('eventTime')),
                location=event.get('locationName'),
                street=street,
                city=event.get('city'),
                state='WA',
                zip_code=zip_code,
                website=event.get('sourceURL'),
                category=event.get('primaryEventType'),
                target_audience=', '.join(event.get('initialTags', [])),
                tags=', '.join(event.get('initialTags', [])),
                status='approved',  # Auto-approve curated events
                featured='Tree Lighting' in event_name or 'Parade' in event_name
            )

            db.session.add(new_event)
            added_count += 1
            print(f"Added: {event_name} on {event_date_str}")

        # Commit all new events to the database
        db.session.commit()

        print(f"\n--- Import Complete ---")
        print(f"Successfully added: {added_count} new events")
        print(f"Skipped (duplicates): {skipped_count} events")
        print(f"-----------------------")

if __name__ == "__main__":
    import_events()
