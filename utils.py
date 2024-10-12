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
    preferred categories, event ratings, past attendance, and event popularity.
    """
    user_groups = [group.name for group in user.groups]
    
    # Query for events that match the user's groups
    recommended_events = Event.query.filter(
        Event.target_audience.in_(user_groups)
    ).order_by(
        Event.fun_meter.desc(),  # Prioritize events with higher fun meter ratings
        func.random()
    ).limit(limit * 3).all()  # Get more events than needed for further filtering
    
    # Calculate user's preferred categories based on their group memberships and past attendance
    preferred_categories = Counter(event.category for event in recommended_events)
    
    # Factor in past attendance (assuming we have a way to track this)
    # This is a placeholder and should be replaced with actual past attendance data
    past_attended_categories = Counter(event.category for event in user.attended_events) if hasattr(user, 'attended_events') else Counter()
    
    # Combine preferences from group memberships and past attendance
    for category, count in past_attended_categories.items():
        preferred_categories[category] += count * 2  # Give more weight to past attendance
    
    top_categories = [category for category, _ in preferred_categories.most_common(5)]
    
    # Calculate event popularity (this is a placeholder and should be replaced with actual data)
    event_popularity = {event.id: len(event.interested_users) for event in recommended_events} if hasattr(Event, 'interested_users') else {}
    
    # Filter and sort the events based on preferred categories, fun meter, and popularity
    sorted_events = sorted(
        recommended_events,
        key=lambda e: (
            e.category in top_categories,
            e.fun_meter,
            event_popularity.get(e.id, 0)
        ),
        reverse=True
    )
    
    # Ensure category diversity
    final_recommendations = []
    category_count = Counter()
    for event in sorted_events:
        if len(final_recommendations) >= limit:
            break
        if category_count[event.category] < 3:  # Limit to 3 events per category
            final_recommendations.append(event)
            category_count[event.category] += 1
    
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
