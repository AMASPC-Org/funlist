from models import Event, User
from sqlalchemy import func
from collections import Counter

def get_weekly_top_events(limit=10):
    """
    Get the top events for the current week based on some criteria.
    This is a placeholder implementation and should be improved based on actual requirements.
    """
    return Event.query.order_by(func.random()).limit(limit).all()

def get_personalized_recommendations(user, limit=10):
    """
    Generate personalized event recommendations for a user.
    """
    # Get the user's attended events
    attended_events = Event.query.filter(Event.attendees.any(id=user.id)).all()
    
    # Extract categories and target audiences from attended events
    categories = [event.category for event in attended_events]
    target_audiences = [event.target_audience for event in attended_events]
    
    # Count occurrences of categories and target audiences
    category_counter = Counter(categories)
    audience_counter = Counter(target_audiences)
    
    # Get the most common category and target audience
    preferred_category = category_counter.most_common(1)[0][0] if category_counter else None
    preferred_audience = audience_counter.most_common(1)[0][0] if audience_counter else None
    
    # Query for recommended events
    recommended_events = Event.query.filter(
        (Event.category == preferred_category) | (Event.target_audience == preferred_audience)
    ).filter(
        Event.id.notin_([event.id for event in attended_events])
    ).order_by(
        func.random()
    ).limit(limit).all()
    
    return recommended_events
