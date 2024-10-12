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
    Generate personalized event recommendations for a user based on their groups.
    """
    user_groups = [group.name for group in user.groups]
    
    # Query for events that match the user's groups
    recommended_events = Event.query.filter(
        Event.target_audience.in_(user_groups)
    ).order_by(
        func.random()
    ).limit(limit).all()
    
    # If we don't have enough events, add some random events to fill the limit
    if len(recommended_events) < limit:
        additional_events = Event.query.filter(
            ~Event.id.in_([e.id for e in recommended_events])
        ).order_by(
            func.random()
        ).limit(limit - len(recommended_events)).all()
        recommended_events.extend(additional_events)
    
    return recommended_events

def get_events_by_user_groups(user_groups, limit=None):
    """
    Generate a list of events based on user groups.
    """
    events = Event.query.filter(
        Event.target_audience.in_(user_groups)
    ).order_by(
        Event.date
    )
    
    if limit:
        events = events.limit(limit)
    
    return events.all()
