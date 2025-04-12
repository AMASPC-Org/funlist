
from app import create_app
from db_init import db
from models import VenueType
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def populate_venue_types():
    app = create_app()
    with app.app_context():
        try:
            # Check if venue types already exist
            existing_count = VenueType.query.count()
            if existing_count > 0:
                logger.info(f"Venue types already exist ({existing_count} records). Skipping population.")
                return True
                
            # Traditional & Purpose-Built Venues
            traditional_venues = [
                {"name": "Hotel/Resort", "category": "Traditional & Purpose-Built"},
                {"name": "Conference Center", "category": "Traditional & Purpose-Built"},
                {"name": "Convention Center", "category": "Traditional & Purpose-Built"},
                {"name": "Banquet Hall", "category": "Traditional & Purpose-Built"}
            ]
            
            # Hospitality Venues
            hospitality_venues = [
                {"name": "Restaurant", "category": "Hospitality"},
                {"name": "Bar/Pub/Nightclub", "category": "Hospitality"},
                {"name": "Brewery/Winery/Distillery", "category": "Hospitality"}
            ]
            
            # Cultural & Unique Venues
            cultural_venues = [
                {"name": "Museum/Art Gallery", "category": "Cultural & Unique"},
                {"name": "Historic Home/Estate", "category": "Cultural & Unique"},
                {"name": "Theater/Concert Hall", "category": "Cultural & Unique"},
                {"name": "Stadium/Arena", "category": "Cultural & Unique"},
                {"name": "Aquarium/Zoo", "category": "Cultural & Unique"},
                {"name": "Warehouse/Industrial Space", "category": "Cultural & Unique"},
                {"name": "Boat/Yacht", "category": "Cultural & Unique"}
            ]
            
            # Outdoor & Recreational Venues
            outdoor_venues = [
                {"name": "Park/Garden", "category": "Outdoor & Recreational"},
                {"name": "Beach", "category": "Outdoor & Recreational"},
                {"name": "Country Club/Golf Course", "category": "Outdoor & Recreational"}
            ]
            
            # Create a list of all venue types
            all_venues = traditional_venues + hospitality_venues + cultural_venues + outdoor_venues
            
            # Add each venue type to the database
            for venue_data in all_venues:
                venue_type = VenueType(
                    name=venue_data["name"],
                    category=venue_data["category"]
                )
                db.session.add(venue_type)
                
            db.session.commit()
            logger.info(f"Successfully added {len(all_venues)} venue types to the database")
            return True
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error populating venue types: {str(e)}")
            return False

if __name__ == "__main__":
    success = populate_venue_types()
    if success:
        print("Venue types populated successfully.")
    else:
        print("Failed to populate venue types.")
