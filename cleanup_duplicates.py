#!/usr/bin/env python3
"""
Database Cleanup Script - Removes true duplicate events
Keeps only one copy of events with same title AND date
"""

from app import create_app
from apps.funlist.models import Event
from db_init import db
from sqlalchemy import func

def cleanup_duplicates():
    """Remove duplicate events keeping only the first one."""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("DATABASE DUPLICATE CLEANUP")
        print("="*60)
        
        # Find all duplicates (same title AND date)
        duplicates = db.session.query(
            Event.title, 
            Event.start_date,
            func.count(Event.id).label('count'),
            func.min(Event.id).label('keep_id')
        ).group_by(
            Event.title, 
            Event.start_date
        ).having(
            func.count(Event.id) > 1
        ).all()
        
        if not duplicates:
            print("✅ No duplicate events found!")
            return
        
        print(f"\n Found {len(duplicates)} sets of duplicate events:\n")
        
        total_removed = 0
        
        for title, start_date, count, keep_id in duplicates:
            print(f"  • '{title}' on {start_date.strftime('%Y-%m-%d')}")
            print(f"    Found {count} copies, keeping ID {keep_id}, removing {count-1}")
            
            # Delete all except the one with minimum ID
            Event.query.filter(
                Event.title == title,
                Event.start_date == start_date,
                Event.id != keep_id
            ).delete()
            
            total_removed += (count - 1)
        
        # Commit the cleanup
        db.session.commit()
        
        print(f"\n{'='*60}")
        print(f"CLEANUP COMPLETE!")
        print(f"{'='*60}")
        print(f"✅ Removed {total_removed} duplicate events")
        print(f"📊 Events remaining: {Event.query.count()}")
        print("="*60 + "\n")

if __name__ == "__main__":
    cleanup_duplicates()