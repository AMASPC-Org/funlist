from models import Event, User
from sqlalchemy import func
from collections import Counter
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_weekly_top_events(limit=10):
    return Event.query.order_by(func.random()).limit(limit).all()

def get_personalized_recommendations(user, limit=10):
    user_groups = [group.name for group in user.groups]
    
    # Query for events that match the user's groups and are in the future
    future_events = Event.query.filter(
        Event.target_audience.in_(user_groups),
        Event.date > datetime.utcnow()
    ).all()
    
    if not future_events:
        return []

    # Calculate user's preferred categories based on their group memberships, past attendance, and interests
    attended_categories = Counter(event.category for event in user.attended_events)
    interested_categories = Counter(event.category for event in user.interested_events)
    preferred_categories = Counter(event.category for event in future_events) + attended_categories + interested_categories
    
    # Content-based filtering: Use TF-IDF to find similar events based on descriptions
    event_descriptions = [event.description for event in future_events]
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(event_descriptions)
    
    # Collaborative filtering: Find similar users
    similar_users = User.query.filter(User.groups.any(User.groups.contains(user.groups[0]))).all()
    similar_user_events = [event for similar_user in similar_users for event in similar_user.attended_events]
    
    # Calculate event scores
    event_scores = {}
    for i, event in enumerate(future_events):
        score = 0
        # Score based on matching user groups
        score += sum(1 for group in user_groups if group == event.target_audience)
        # Score based on fun meter
        score += event.fun_meter
        # Score based on preferred categories
        score += preferred_categories[event.category] * 2  # Increased weight for preferred categories
        # Score based on popularity (number of interested users)
        score += len(event.interested_users)
        # Time-based weighting: higher score for events happening soon
        days_until_event = (event.date - datetime.utcnow()).days
        score += max(0, 30 - days_until_event) / 30  # Max boost for events within 30 days
        
        # Content-based similarity
        event_vector = tfidf_matrix[i]
        content_similarities = cosine_similarity(event_vector, tfidf_matrix).flatten()
        score += np.mean(content_similarities) * 5  # Scale similarity score
        
        # Collaborative filtering: boost score if similar users attended this event
        if event in similar_user_events:
            score += 2
        
        # Boost score if the user has expressed interest in this event
        if event in user.interested_events:
            score += 3
        
        # Penalty for events user has already attended
        if event in user.attended_events:
            score -= 5
        
        # New: Consider the user's age group (if available)
        if hasattr(user, 'age_group'):
            if user.age_group == event.target_audience:
                score += 2
        
        # New: Consider the event's location (if available)
        if hasattr(user, 'preferred_location') and event.location == user.preferred_location:
            score += 2
        
        event_scores[event] = score
    
    # Sort events by score and get top recommendations
    sorted_events = sorted(event_scores.items(), key=lambda x: x[1], reverse=True)
    recommendations = [event for event, _ in sorted_events[:limit]]
    
    return recommendations

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
