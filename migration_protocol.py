# FunList.ai: PostgreSQL to Firestore Migration Protocol
# Script Version: 1.0 (PROMPT/COLAB READY)

# MISSION: Migrate FunList's PostgreSQL data to Firestore for Unified Ecosystem Architecture.
# EXECUTION: This script is designed to be run in Google Colab or by Google Jules with access to the source DB.

import os
import json
import psycopg2
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# --- CONFIGURATION (FILL IN) ---
PG_CONN_STRING = "postgresql://user:password@host:port/dbname"
FIREBASE_PROJECT_ID = "ama-ecosystem-prod"
# If running in Colab, upload your service account JSON
# CRED_PATH = "/content/service_account.json" 

def migrate():
    # 1. Initialize Firebase
    if not firebase_admin._apps:
        # cred = credentials.Certificate(CRED_PATH)
        # firebase_admin.initialize_app(cred)
        # Fallback for Jules/ADC
        firebase_admin.initialize_app(options={'projectId': FIREBASE_PROJECT_ID})
    
    db = firestore.client()
    pg_conn = psycopg2.connect(PG_CONN_STRING)
    cur = pg_conn.cursor()

    print("🚀 Starting Migration Protocol...")

    # 2. Migrate Venues (The Foundation)
    print("--- Normalizing Venues ---")
    cur.execute("SELECT id, name, address, city, state, zip, latitude, longitude FROM venues")
    venues = cur.fetchall()
    for v in venues:
        vid, name, addr, city, state, zip_code, lat, lng = v
        # Venues use their original ID or normalized name-based hash
        venue_data = {
            "name": name,
            "address": addr,
            "city": city,
            "state": state,
            "zip": zip_code,
            "lat": lat,
            "lng": lng,
            "is_verified": True,
            "updated_at": datetime.utcnow()
        }
        db.collection("venues").document(str(vid)).set(venue_data, merge=True)
    print(f"✅ Migrated {len(venues)} Venues.")

    # 3. Migrate Users (Authentication Bridge)
    print("--- Bridging Users ---")
    cur.execute("SELECT id, email, role, display_name, created_at FROM users")
    users = cur.fetchall()
    for u in users:
        uid, email, role, display_name, created_at = u
        user_data = {
            "email": email,
            "role": role,
            "display_name": display_name,
            "account_active": True,
            "is_admin": role == 'admin',
            "created_at": created_at or datetime.utcnow()
        }
        db.collection("users").document(str(uid)).set(user_data, merge=True)
    print(f"✅ Migrated {len(users)} Users.")

    # 4. Migrate Events (The Golden Records)
    print("--- Fan-out Events ---")
    cur.execute("""
        SELECT e.id, e.title, e.description, e.start_time, e.end_time, e.venue_id, e.status, e.created_at,
               f.community_vibe, f.family_fun, f.overall_score
        FROM events e
        LEFT JOIN funalytics_scores f ON e.id = f.event_id
    """)
    events = cur.fetchall()
    for e in events:
        eid, title, desc, start, end, venue_id, status, created, vibe, family, overall = e
        
        # Mapping rules to Spoke Schema
        event_data = {
            "title": title,
            "description": desc,
            "start_date": start.date().isoformat() if start else None,
            "start_time": start.time().isoformat() if start else None,
            "end_date": end.date().isoformat() if end else None,
            "venueId": str(venue_id) if venue_id else "unknown",
            "status": status.lower(),
            "category": "Other", # Default, will be updated by Taxonomy Refresher
            "metadata": {
                "fun_rating": overall or 50,
                "community_vibe": vibe or 5,
                "family_fun": family or 5
            },
            "source": "migration",
            "created_at": created or datetime.utcnow()
        }
        db.collection("funlist_events").document(str(eid)).set(event_data, merge=True)
    print(f"✅ Migrated {len(events)} Events.")

    pg_conn.close()
    print("🏁 Migration Complete.")

if __name__ == "__main__":
    migrate()
