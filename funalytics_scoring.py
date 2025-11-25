"""
Funalytics™ Scoring System
Comprehensive scoring logic for event frequency, audience-specific ratings, and time-based relevance filtering
"""

from datetime import datetime, time

# Frequency-based deductions for Funalytics™ Scoring
FREQUENCY_DEDUCTIONS = {
    'daily': 4.0,      # Recurring daily events lose 4 points
    'weekly': 2.5,     # Recurring weekly events lose 2.5 points
    'monthly': 1.5,    # Recurring monthly events lose 1.5 points
    'yearly': 0.5,     # Yearly events lose 0.5 points
    'once': 0.0        # One-time events lose 0 points
}

# 12 Target Audiences with time-based relevance filtering
TARGET_AUDIENCES = {
    'Kids': {
        'min_age': 0,
        'max_age': 12,
        'exclude_times': ['22:00', '23:00', '00:00', '01:00', '02:00', '03:00', '04:00', '05:00'],
        'description': 'Children ages 0-12 and their caregivers'
    },
    'Teens': {
        'min_age': 13,
        'max_age': 19,
        'exclude_times': ['02:00', '03:00', '04:00', '05:00'],
        'description': 'Teenagers ages 13-19'
    },
    'Families': {
        'min_age': 0,
        'max_age': 100,
        'exclude_times': ['23:00', '00:00', '01:00', '02:00', '03:00', '04:00', '05:00'],
        'description': 'Families with children'
    },
    'Students': {
        'min_age': 16,
        'max_age': 25,
        'exclude_times': ['02:00', '03:00', '04:00', '05:00'],
        'description': 'High school and college students'
    },
    'Adults': {
        'min_age': 18,
        'max_age': 65,
        'exclude_times': [],
        'description': 'General adult audience'
    },
    'Seniors': {
        'min_age': 55,
        'max_age': 120,
        'exclude_times': ['22:00', '23:00', '00:00', '01:00', '02:00', '03:00', '04:00'],
        'description': 'Adults 55 and older'
    },
    'Singles': {
        'min_age': 18,
        'max_age': 65,
        'exclude_times': [],
        'description': 'Single adults seeking social connections'
    },
    'Date Night': {
        'min_age': 18,
        'max_age': 65,
        'exclude_times': [],
        'description': 'Couples and romantic outings'
    },
    'Professionals': {
        'min_age': 22,
        'max_age': 65,
        'exclude_times': ['02:00', '03:00', '04:00', '05:00'],
        'description': 'Working professionals and business networking'
    },
    'Fitness & Active': {
        'min_age': 16,
        'max_age': 75,
        'exclude_times': [],
        'description': 'Sports, fitness, and outdoor enthusiasts'
    },
    'Arts & Culture': {
        'min_age': 16,
        'max_age': 120,
        'exclude_times': [],
        'description': 'Art, theater, music, and cultural events'
    },
    '21+': {
        'min_age': 21,
        'max_age': 120,
        'exclude_times': [],
        'description': 'Adults 21 and older (drinking venues, nightlife)'
    }
}


def calculate_frequency_deduction(event_frequency):
    """
    Calculate points deducted based on event frequency.
    More frequent events are deducted more points to promote unique experiences.
    
    Args:
        event_frequency: str - 'daily', 'weekly', 'monthly', 'yearly', or 'once'
    
    Returns:
        float - Points to deduct from base Funalytics™ Score
    """
    return FREQUENCY_DEDUCTIONS.get(event_frequency, 0.0)


def is_event_appropriate_for_audience(event, audience_name):
    """
    Determine if an event is appropriate for a specific audience.
    Checks both audience type and time-based restrictions.
    
    Args:
        event: Event object
        audience_name: str - Name of target audience
    
    Returns:
        bool - True if event is appropriate for audience
    """
    if audience_name not in TARGET_AUDIENCES:
        return False
    
    audience_info = TARGET_AUDIENCES[audience_name]
    
    # Check event time restrictions for this audience
    if event.start_time:
        event_hour = event.start_time[:2]  # Extract hour from HH:MM format
        excluded_times = audience_info.get('exclude_times', [])
        
        for excluded_time in excluded_times:
            if excluded_time.startswith(event_hour):
                return False
    
    # Additional logic could check event type, content, etc.
    # For now, time-based filtering is the primary constraint
    
    return True


def calculate_audience_specific_score(base_score, audience_name, community_vibe, family_fun):
    """
    Calculate audience-specific Funalytics™ Score.
    Different audiences value different event attributes.
    
    Args:
        base_score: float - Overall Funalytics™ Score (0-10)
        audience_name: str - Target audience name
        community_vibe: float - Community connection score (0-10)
        family_fun: float - Family-friendliness score (0-10)
    
    Returns:
        float - Audience-specific score (0-10)
    """
    if audience_name not in TARGET_AUDIENCES:
        return base_score
    
    # Audience-specific weighting
    audience_weights = {
        'Kids': {'community_vibe': 0.4, 'family_fun': 0.6},
        'Teens': {'community_vibe': 0.6, 'family_fun': 0.4},
        'Families': {'community_vibe': 0.3, 'family_fun': 0.7},
        'Students': {'community_vibe': 0.7, 'family_fun': 0.3},
        'Adults': {'community_vibe': 0.5, 'family_fun': 0.5},
        'Seniors': {'community_vibe': 0.6, 'family_fun': 0.4},
        'Singles': {'community_vibe': 0.8, 'family_fun': 0.2},
        'Date Night': {'community_vibe': 0.3, 'family_fun': 0.7},
        'Professionals': {'community_vibe': 0.9, 'family_fun': 0.1},
        'Fitness & Active': {'community_vibe': 0.6, 'family_fun': 0.4},
        'Arts & Culture': {'community_vibe': 0.5, 'family_fun': 0.5},
        '21+': {'community_vibe': 0.7, 'family_fun': 0.3}
    }
    
    weights = audience_weights.get(audience_name, {'community_vibe': 0.5, 'family_fun': 0.5})
    
    audience_score = (
        community_vibe * weights['community_vibe'] +
        family_fun * weights['family_fun']
    )
    
    # Clamp to 0-10 range
    return max(0, min(10, audience_score))


def apply_frequency_deduction(base_score, event_frequency):
    """
    Apply frequency-based deduction to Funalytics™ Score.
    
    Args:
        base_score: float - Base Funalytics™ Score (0-10)
        event_frequency: str - Event frequency ('daily', 'weekly', 'monthly', 'yearly', 'once')
    
    Returns:
        float - Adjusted score after frequency deduction
    """
    deduction = calculate_frequency_deduction(event_frequency)
    adjusted_score = max(1.0, base_score - deduction)  # Minimum score of 1.0
    
    return min(10.0, adjusted_score)  # Maximum score of 10.0


def get_audience_recommendations(event):
    """
    Get list of recommended audiences for an event.
    Filters out audiences that shouldn't view this event based on time restrictions.
    
    Args:
        event: Event object
    
    Returns:
        list - Names of appropriate audiences for this event
    """
    appropriate_audiences = []
    
    for audience_name in TARGET_AUDIENCES.keys():
        if is_event_appropriate_for_audience(event, audience_name):
            appropriate_audiences.append(audience_name)
    
    return appropriate_audiences


def validate_event_exclusions(event_category, event_description, exclusion_rules):
    """
    Check if an event matches any active exclusion rules.
    
    Args:
        event_category: str - Event category
        event_description: str - Event description
        exclusion_rules: list - List of EventExclusionRule objects
    
    Returns:
        dict - {'is_excluded': bool, 'reason': str}
    """
    for rule in exclusion_rules:
        if rule.matches_event(event_category, event_description):
            return {
                'is_excluded': True,
                'reason': rule.exclusion_reason,
                'rule_id': rule.exclusion_id
            }
    
    return {'is_excluded': False, 'reason': None, 'rule_id': None}


def generate_event_disclaimer():
    """
    Generate standard disclaimer for all events about potential changes/cancellations.
    
    Returns:
        str - Disclaimer text
    """
    return (
        "Please note: Events are subject to change or cancellation. "
        "We strongly recommend checking the event host's website and social media "
        "for the latest updates before attending."
    )
