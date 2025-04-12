
import os
import sys
import logging
from app import create_app
from db_init import db
from models import VenueType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

def populate_venue_types():
    try:
        app = create_app()
        with app.app_context():
            # Check if venue types already exist
            if VenueType.query.count() > 0:
                logger.info("Venue types already exist in the database")
                return
                
            # Define venue types with their categories
            venue_types = [
                # Traditional & Purpose-Built Venues
                {'name': 'Hotel or Resort', 'category': 'Traditional & Purpose-Built'},
                {'name': 'Conference Center', 'category': 'Traditional & Purpose-Built'},
                {'name': 'Convention Center', 'category': 'Traditional & Purpose-Built'},
                {'name': 'Banquet Hall', 'category': 'Traditional & Purpose-Built'},
                
                # Hospitality Venues
                {'name': 'Restaurant', 'category': 'Hospitality'},
                {'name': 'Bar or Pub', 'category': 'Hospitality'},
                {'name': 'Nightclub', 'category': 'Hospitality'},
                {'name': 'Brewery', 'category': 'Hospitality'},
                {'name': 'Winery', 'category': 'Hospitality'},
                {'name': 'Distillery', 'category': 'Hospitality'},
                
                # Cultural & Unique Venues
                {'name': 'Museum', 'category': 'Cultural & Unique'},
                {'name': 'Art Gallery', 'category': 'Cultural & Unique'},
                {'name': 'Historic Home or Estate', 'category': 'Cultural & Unique'},
                {'name': 'Theater or Concert Hall', 'category': 'Cultural & Unique'},
                {'name': 'Sports Stadium or Arena', 'category': 'Cultural & Unique'},
                {'name': 'Aquarium or Zoo', 'category': 'Cultural & Unique'},
                {'name': 'Warehouse or Industrial Space', 'category': 'Cultural & Unique'},
                {'name': 'Boat or Yacht', 'category': 'Cultural & Unique'},
                
                # Outdoor & Recreational Venues
                {'name': 'Park or Garden', 'category': 'Outdoor & Recreational'},
                {'name': 'Beach', 'category': 'Outdoor & Recreational'},
                {'name': 'Country Club or Golf Course', 'category': 'Outdoor & Recreational'},
                {'name': 'Campground or Retreat Center', 'category': 'Outdoor & Recreational'},
                
                # Community & Other Venues
                {'name': 'Community Center', 'category': 'Community & Other'},
                {'name': 'Local Hall', 'category': 'Community & Other'},
                {'name': 'Academic Institution', 'category': 'Community & Other'},
                {'name': 'Coworking Space', 'category': 'Community & Other'},
                {'name': 'Other', 'category': 'Other'}
            ]
            
            # Add venue types to the database
            for venue_type in venue_types:
                vt = VenueType(name=venue_type['name'], category=venue_type['category'])
                db.session.add(vt)
            
            db.session.commit()
            logger.info(f"Successfully added {len(venue_types)} venue types to the database")
    except Exception as e:
        logger.error(f"Error populating venue types: {str(e)}")

if __name__ == "__main__":
    populate_venue_types()
    print("Done!")
