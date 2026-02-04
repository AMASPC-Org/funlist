
import os
import psycopg2
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

# --- CONFIGURATION ---
PG_CONN_STRING = os.getenv('DATABASE_URL')
FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID', 'ama-ecosystem-prod')

def get_utc_now():
    """Returns current UTC time with timezone info."""
    return datetime.now(timezone.utc)

def ensure_tz(dt):
    """Ensures a datetime object is timezone-aware (UTC), assuming naive means UTC."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt

def migrate():
    print(f"🚀 Starting Local Migration to {FIREBASE_PROJECT_ID}...")
    
    # 1. Initialize Firebase
    if not firebase_admin._apps:
        firebase_admin.initialize_app(options={'projectId': FIREBASE_PROJECT_ID})
    
    db = firestore.client()
    
    # 2. Connect to PostgreSQL
    if not PG_CONN_STRING:
        print("❌ Error: DATABASE_URL not found in .env")
        return

    pg_conn = None
    try:
        pg_conn = psycopg2.connect(PG_CONN_STRING)
        cur = pg_conn.cursor()
        print("✅ Connected to PostgreSQL and Firebase!")
    except Exception as e:
        print(f"❌ PostgreSQL Connection Failed: {e}")
        return

    # --- USERS MIGRATION ---
    print("\n--- Migrating Users ---")
    try:
        cur.execute("""
            SELECT id, email, is_admin, is_organizer, first_name, last_name, 
                   account_active, created_at 
            FROM users
        """)
        users = cur.fetchall()
        batch = db.batch()
        count = 0
        for u in users:
            uid, email, is_admin, is_organizer, first_name, last_name, account_active, created_at = u
            
            role = 'attendee'
            if is_admin:
                role = 'admin'
            elif is_organizer:
                role = 'organizer'
                
            display_name = f"{first_name or ''} {last_name or ''}".strip()
            
            user_ref = db.collection("users").document(str(uid))
            batch.set(user_ref, {
                "email": email,
                "role": role,
                "display_name": display_name or email.split('@')[0],
                "first_name": first_name,
                "last_name": last_name,
                "account_active": account_active,
                "is_admin": is_admin,
                "created_at": ensure_tz(created_at) or get_utc_now(),
                "migrated_from": "postgres_live"
            }, merge=True)
            count += 1
            if count % 400 == 0:
                batch.commit()
                batch = db.batch()
        if count % 400 != 0:
            batch.commit()
        print(f"✅ Total Users Migrated: {count}")
    except Exception as e:
        print(f"⚠️ User migration error: {e}")
        pg_conn.rollback()

    # --- VENUES MIGRATION ---
    print("\n--- Migrating Venues ---")
    try:
        cur.execute("""
            SELECT id, name, street, city, state, zip_code, latitude, longitude, is_verified 
            FROM venues
        """)
        venues = cur.fetchall()
        batch = db.batch()
        count = 0
        for v in venues:
            vid, name, street, city, state, zip_code, lat, lng, is_verified = v
            venue_ref = db.collection("venues").document(str(vid))
            batch.set(venue_ref, {
                "name": name,
                "address": street,     # Mapped for protocol
                "street": street,      # Kept for compatibility
                "city": city,
                "state": state,
                "zip": zip_code,       # Mapped for protocol
                "zip_code": zip_code,  # Kept for compatibility
                "location": {"lat": lat, "lng": lng} if lat and lng else None,
                "is_verified": is_verified if is_verified is not None else False,
                "migrated_from": "postgres_live"
            }, merge=True)
            count += 1
            if count % 400 == 0:
                batch.commit()
                batch = db.batch()
        if count % 400 != 0:
            batch.commit()
        print(f"✅ Total Venues Migrated: {count}")
    except Exception as e:
        print(f"⚠️ Venue migration error: {e}")
        pg_conn.rollback()

    # --- EVENTS MIGRATION ---
    print("\n--- Migrating Events ---")
    try:
        cur.execute("""
            SELECT id, title, description, start_date, start_time, end_date, end_time, 
                   venue_id, status, created_at
            FROM events
        """)
        events = cur.fetchall()
        batch = db.batch()
        count = 0
        for e in events:
            eid, title, desc, s_date, s_time, e_date, e_time, venue_id, status, created_at = e
            
            # Combine date and time to ISO strings
            start_dt = None
            if s_date:
                if s_time:
                    start_dt = datetime.combine(s_date, s_time).isoformat()
                else:
                    start_dt = s_date.isoformat()
            
            end_dt = None
            if e_date:
                if e_time:
                    end_dt = datetime.combine(e_date, e_time).isoformat()
                else:
                    end_dt = e_date.isoformat()

            event_ref = db.collection("funlist_events").document(str(eid))
            
            batch.set(event_ref, {
                "title": title,
                "description": desc,
                "start_date": start_dt,
                "end_date": end_dt,
                "venueId": str(venue_id) if venue_id else None,
                "status": status.lower() if status else 'pending',
                "category": "Other",
                "source": "postgres_live",
                "created_at": ensure_tz(created_at) or get_utc_now(),
                "migrated_at": firestore.SERVER_TIMESTAMP
            }, merge=True)

            count += 1
            if count % 400 == 0:
                batch.commit()
                batch = db.batch()
        if count % 400 != 0:
            batch.commit()
        print(f"✅ Total Events Migrated: {count}")
    except Exception as e:
        print(f"⚠️ Event migration error: {e}")
        pg_conn.rollback()

    if pg_conn:
        pg_conn.close()
    print("\n🏁 LOCAL MIGRATION COMPLETE 🏁")

if __name__ == "__main__":
    migrate()
