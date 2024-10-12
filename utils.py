from models import Event, User
from sqlalchemy import func
from collections import Counter
from datetime import datetime, timedelta

def get_weekly_top_events(limit=10):
    """
    Get the top events for the current week based on some criteria.
    This is a placeholder implementation and should be improved based on actual requirements.
    """
    return Event.query.order_by(func.random()).limit(limit).all()

def get_personalized_recommendations(user, limit=10):
    """
    Generate personalized event recommendations for a user based on their groups,
    preferred categories, event ratings, past attendance, and event popularity.
    """
    user_groups = [group.name for group in user.groups]
    
    # Query for events that match the user's groups and are in the future
    future_events = Event.query.filter(
        Event.target_audience.in_(user_groups),
        Event.date > datetime.utcnow()
    ).all()
    
    # Calculate user's preferred categories based on their group memberships and past attendance
    attended_categories = Counter(event.category for event in user.attended_events)
    preferred_categories = Counter(event.category for event in future_events) + attended_categories
    
    # Calculate event scores
    event_scores = {}
    for event in future_events:
        score = 0
        # Score based on matching user groups
        score += sum(1 for group in user_groups if group == event.target_audience)
        # Score based on fun meter
        score += event.fun_meter
        # Score based on preferred categories
        score += preferred_categories[event.category]
        # Score based on popularity (number of interested users)
        score += len(event.interested_users)
        # Penalty for events user has already expressed interest in
        if event in user.interested_events:
            score -= 2
        event_scores[event] = score
    
    # Sort events by score and get top recommendations
    sorted_events = sorted(event_scores.items(), key=lambda x: x[1], reverse=True)
    recommendations = [event for event, _ in sorted_events[:limit]]
    
    return recommendations

def get_events_by_user_groups(user_groups, limit=None):
    """
    Generate a list of events based on user groups.
    """
    events = Event.query.filter(
        Event.target_audience.in_(user_groups),
        Event.date > datetime.utcnow()
    ).order_by(Event.date)
    
    if limit:
        events = events.limit(limit)
    
    return events.all()
