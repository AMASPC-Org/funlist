import requests
import logging
import os
from flask import url_for

logger = logging.getLogger(__name__)

def send_password_reset_email(user, token):
    """
    This is a placeholder function for sending password reset emails.
    In a production environment, you would configure an email service
    and actually send the email with the reset link.
    """
    reset_url = url_for('reset_password', token=token, _external=True)
    # Log the reset URL for development purposes
    logger.info(f"Password reset requested for {user.email}. Reset URL: {reset_url}")

    # In a real app, you would send an email here
    # For now, we'll just return True to indicate success
    return True

def geocode_address(street=None, city=None, state=None, zip_code=None, location_query=None):
    """Get coordinates from address or location query using Google Maps Geocoding API."""
    try:
        if location_query:
            address = location_query
        else:
            address_parts = []
            if street: address_parts.append(street)
            if city: address_parts.append(city)
            if state: address_parts.append(state)
            if zip_code: address_parts.append(zip_code)
            address = ", ".join(filter(None, address_parts))

        if not address:
            return None

        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={current_app.config['GOOGLE_MAPS_API_KEY']}"
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            bounds = data['results'][0].get('geometry', {}).get('viewport')
            return {
                'lat': location['lat'],
                'lng': location['lng'],
                'bounds': bounds if bounds else None
            }
        return None
    except Exception as e:
        current_app.logger.error(f"Geocoding error: {str(e)}")
        return None

def get_weekly_top_events(limit=10):
    return Event.query.order_by(func.random()).limit(limit).all()

def get_personalized_recommendations(user, limit=10):
    user_groups = [group.name for group in user.groups]
    future_events = Event.query.filter(
        Event.target_audience.in_(user_groups),
        Event.date > datetime.utcnow()
    ).all()
    return future_events[:limit]

def get_events_by_user_groups(user_groups, limit=None):
    events = Event.query.filter(
        Event.target_audience.in_(user_groups),
        Event.date > datetime.utcnow()
    ).order_by(Event.date)

    if limit:
        events = events.limit(limit)

    return events.all()

def calculate_event_similarity(event1, event2):
    # Calculate similarity between two events based on their attributes
    similarity = 0
    if event1.category == event2.category:
        similarity += 1
    if event1.target_audience == event2.target_audience:
        similarity += 1
    if abs((event1.date - event2.date).days) < 7:  # Events within a week of each other
        similarity += 1
    if event1.location == event2.location:
        similarity += 1
    return similarity

def get_similar_events(event, limit=5):
    # Find similar events to a given event
    all_events = Event.query.filter(Event.id != event.id, Event.date > datetime.utcnow()).all()
    event_similarities = [(e, calculate_event_similarity(event, e)) for e in all_events]
    sorted_events = sorted(event_similarities, key=lambda x: x[1], reverse=True)
    return [e for e, _ in sorted_events[:limit]]
