#!/usr/bin/env python
"""
Direct event import script that bypasses SQLAlchemy model conflicts
by using direct database operations.
"""

import json
import psycopg2
import os
from datetime import datetime
from urllib.parse import urlparse

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

def import_events_direct():
    """Import events directly to database, bypassing SQLAlchemy"""
    
    # Get database URL from environment
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("ERROR: DATABASE_URL not set")
        return
    
    # Parse database URL for psycopg2
    parsed = urlparse(database_url)
    
    # Connect to database
    conn = psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port,
        database=parsed.path[1:],
        user=parsed.username,
        password=parsed.password
    )
    cur = conn.cursor()
    
    print("=" * 60)
    print("DIRECT EVENT IMPORT")
    print("=" * 60)
    
    # Read JSON file
    try:
        with open('events.json', 'r') as f:
            events_data = json.load(f)
        print(f"Found {len(events_data)} events in JSON file")
    except Exception as e:
        print(f"ERROR reading events.json: {e}")
        return
    
    added_count = 0
    skipped_count = 0
    
    for event in events_data:
        try:
            # Extract and map fields
            event_name = event['eventName']
            event_date = event['eventDate']
            event_time = event.get('eventTime', '')
            location_name = event.get('locationName', '')
            location_address = event.get('locationAddress', '')
            city = event.get('city', '')
            description = event.get('description', '')
            event_type = event.get('primaryEventType', 'General')
            
            # Parse date
            event_date_obj = datetime.strptime(event_date, '%Y-%m-%d').date()
            
            # Parse time
            start_time = parse_time(event_time)
            
            # Extract street from address
            street = location_address.split(',')[0] if ',' in location_address else location_address
            
            # Check for duplicate
            cur.execute("""
                SELECT id FROM events 
                WHERE title = %s AND start_date = %s
            """, (event_name, event_date_obj))
            
            if cur.fetchone():
                print(f"  ⏭️  Skipping duplicate: {event_name} on {event_date}")
                skipped_count += 1
                continue
            
            # Insert new event
            cur.execute("""
                INSERT INTO events (
                    title, start_date, start_time, location, 
                    street, city, state, description, 
                    category, status, created_at
                ) VALUES (
                    %s, %s, %s, %s, 
                    %s, %s, %s, %s, 
                    %s, %s, CURRENT_TIMESTAMP
                )
            """, (
                event_name, event_date_obj, start_time, location_name,
                street, city, 'WA', description,
                event_type, 'approved'
            ))
            
            added_count += 1
            print(f"  ✅ Added: {event_name} on {event_date}")
            
        except Exception as e:
            print(f"  ❌ Error processing {event.get('eventName', 'unknown')}: {e}")
            continue
    
    # Commit changes
    conn.commit()
    
    print("\n" + "=" * 60)
    print(f"IMPORT COMPLETE")
    print(f"  Added: {added_count} events")
    print(f"  Skipped: {skipped_count} duplicates")
    print("=" * 60)
    
    # Close connection
    cur.close()
    conn.close()

if __name__ == "__main__":
    import_events_direct()
