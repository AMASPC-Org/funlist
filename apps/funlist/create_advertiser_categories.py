
from app import create_app
from models import ProhibitedAdvertiserCategory
from db_init import db

def create_advertiser_categories():
    app = create_app()
    with app.app_context():
        categories = [
            ('alcohol', 'Alcohol and Tobacco Products'),
            ('cannabis', 'Marijuana and Cannabis Dispensaries'),
            ('gambling', 'Gambling and Betting Services'),
            ('adult', 'Adult Entertainment and Products'),
            ('junk_food', 'Junk Food and Sugary Beverages'),
            ('energy_drinks', 'Energy Drinks'),
            ('political', 'Political and Religious Organizations')
        ]
        
        for code, name in categories:
            if not ProhibitedAdvertiserCategory.query.filter_by(name=name).first():
                category = ProhibitedAdvertiserCategory(name=name)
                db.session.add(category)
        
        db.session.commit()

if __name__ == '__main__':
    create_advertiser_categories()
