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
    Generate personalized event recommendations for a user based on their groups,
    preferred categories, and event ratings.
    """
    user_groups = [group.name for group in user.groups]
    
    # Query for events that match the user's groups
    recommended_events = Event.query.filter(
        Event.target_audience.in_(user_groups)
    ).order_by(
        Event.fun_meter.desc(),  # Prioritize events with higher fun meter ratings
        func.random()
    ).limit(limit * 2).all()  # Get more events than needed for further filtering
    
    # Calculate user's preferred categories based on their group memberships
    preferred_categories = Counter(event.category for event in recommended_events)
    top_categories = [category for category, _ in preferred_categories.most_common(3)]
    
    # Filter and sort the events based on preferred categories and fun meter
    sorted_events = sorted(
        recommended_events,
        key=lambda e: (e.category in top_categories, e.fun_meter),
        reverse=True
    )
    
    # Select the top 'limit' events
    final_recommendations = sorted_events[:limit]
    
    # If we don't have enough events, add some random events to fill the limit
    if len(final_recommendations) < limit:
        additional_events = Event.query.filter(
            ~Event.id.in_([e.id for e in final_recommendations])
        ).order_by(
            func.random()
        ).limit(limit - len(final_recommendations)).all()
        final_recommendations.extend(additional_events)
    
    return final_recommendations

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
