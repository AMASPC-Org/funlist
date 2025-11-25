"""
Funalytics™ Scoring System
Comprehensive scoring logic for event frequency, audience-specific ratings, and time-based relevance filtering.
Translates qualitative features into a 1-100 scale.
"""

from datetime import datetime, time

# Frequency-based deductions (1-100 scale impact)
# Logic: Frequent events are less "special"
FREQUENCY_DEDUCTIONS = {
    'daily': 40.0,      # High deduction
    'weekly': 25.0,
    'monthly': 15.0,
    'yearly': 5.0,
    'once': 0.0
}

# 12 Target Audiences
TARGET_AUDIENCES = {
    'Kids': {
        'min_age': 0, 'max_age': 12,
        'exclude_times': ['22:00', '23:00', '00:00', '01:00', '02:00', '03:00', '04:00', '05:00'],
        'description': 'Children ages 0-12 and their caregivers'
    },
    'Teens': {
        'min_age': 13, 'max_age': 19,
        'exclude_times': ['02:00', '03:00', '04:00', '05:00'],
        'description': 'Teenagers ages 13-19'
    },
    'Families': {
        'min_age': 0, 'max_age': 100,
        'exclude_times': ['23:00', '00:00', '01:00', '02:00', '03:00', '04:00', '05:00'],
        'description': 'Families with children'
    },
    'Students': {
        'min_age': 16, 'max_age': 25,
        'exclude_times': ['02:00', '03:00', '04:00', '05:00'],
        'description': 'High school and college students'
    },
    'Adults': {
        'min_age': 18, 'max_age': 65, 'exclude_times': [],
        'description': 'General adult audience'
    },
    'Seniors': {
        'min_age': 55, 'max_age': 120,
        'exclude_times': ['22:00', '23:00', '00:00', '01:00', '02:00', '03:00', '04:00'],
        'description': 'Adults 55 and older'
    },
    'Singles': {
        'min_age': 18, 'max_age': 65, 'exclude_times': [],
        'description': 'Single adults seeking social connections'
    },
    'Date Night': {
        'min_age': 18, 'max_age': 65, 'exclude_times': [],
        'description': 'Couples and romantic outings'
    },
    'Professionals': {
        'min_age': 22, 'max_age': 65,
        'exclude_times': ['02:00', '03:00', '04:00', '05:00'],
        'description': 'Working professionals and business networking'
    },
    'Fitness & Active': {
        'min_age': 16, 'max_age': 75, 'exclude_times': [],
        'description': 'Sports, fitness, and outdoor enthusiasts'
    },
    'Arts & Culture': {
        'min_age': 16, 'max_age': 120, 'exclude_times': [],
        'description': 'Art, theater, music, and cultural events'
    },
    '21+': {
        'min_age': 21, 'max_age': 120, 'exclude_times': [],
        'description': 'Adults 21 and older'
    }
}

# Scoring Ladder: Translating Features to Points (1-100 Scale)
# Based on "Event Fun Rating System" methodology
SCORING_LADDER = {
    'Adults': {
        'live music': 10, 'car show': 10, 'beer garden': 10, 'food tasting': 10,
        'hot air balloon': 10, 'wine tasting': 10, 'vip': 10, 'art exhibit': 10,
        'cooking demo': 10, 'fireworks': 10, 'exclusive': 10, 'luxury': 10
    },
    'Singles': {
        'live dj': 10, 'beer garden': 10, 'limbo': 10, 'beer pong': 10,
        'karaoke': 10, 'speed dating': 20, 'food trucks': 10, 'dance': 10,
        'mixology': 10, 'rooftop': 10, 'social': 5
    },
    'Families': {
        'fireworks': 10, 'live music': 10, 'petting zoo': 10, 'sack race': 10,
        'contest': 10, 'movie': 10, 'face painting': 10, 'relay race': 10,
        'food trucks': 10, 'carnival': 10, 'welcoming': 5
    },
    'Kids': {
        'bounce house': 10, 'dunk tank': 10, 'science': 10, 'balloon': 10,
        'face painter': 10, 'scavenger hunt': 10, 'magic': 10, 'talent show': 10,
        'games': 10, 'ice cream': 10, 'playful': 5
    }
}

def calculate_frequency_deduction(event_frequency):
    return FREQUENCY_DEDUCTIONS.get(event_frequency, 0.0)

def is_event_appropriate_for_audience(event, audience_name):
    if audience_name not in TARGET_AUDIENCES:
        return False

    audience_info = TARGET_AUDIENCES[audience_name]
    if event.start_time:
        event_hour = event.start_time[:2]
        excluded_times = audience_info.get('exclude_times', [])
        for excluded_time in excluded_times:
            if excluded_time.startswith(event_hour):
                return False
    return True

def calculate_keyword_score(text_content, audience_name):
    """
    Scan text for keywords relevant to the audience and sum points.
    Returns a score between 0 and 100.
    """
    if audience_name not in SCORING_LADDER:
        return 50.0 # Default middle score if no specific ladder

    ladder = SCORING_LADDER[audience_name]
    score = 0.0
    text_lower = text_content.lower()

    for keyword, points in ladder.items():
        if keyword in text_lower:
            score += points

    return min(100.0, score)

def calculate_audience_specific_score(base_score, audience_name, community_vibe, family_fun, event_description=""):
    """
    Calculate audience-specific Funalytics™ Score (0-100 Scale).
    Combines base AI assessment with deterministic keyword bonuses.
    """
    if audience_name not in TARGET_AUDIENCES:
        return base_score

    # Get the deterministic keyword score
    keyword_score = calculate_keyword_score(event_description, audience_name)

    # Base weighting logic (retained from original but scaled to 100)
    audience_weights = {
        'Kids': {'community': 0.4, 'family': 0.6},
        'Teens': {'community': 0.6, 'family': 0.4},
        'Families': {'community': 0.3, 'family': 0.7},
        'Adults': {'community': 0.5, 'family': 0.5},
        # ... (Defaults to 0.5/0.5)
    }

    weights = audience_weights.get(audience_name, {'community': 0.5, 'family': 0.5})

    # Normalize inputs if they are 0-10 (convert to 0-100)
    c_score = community_vibe * 10 if community_vibe <= 10 else community_vibe
    f_score = family_fun * 10 if family_fun <= 10 else family_fun
    b_score = base_score * 10 if base_score <= 10 else base_score

    weighted_ai_score = (c_score * weights['community'] + f_score * weights['family'])

    # Blend: 60% AI Score, 40% Keyword Score (Feature Detection)
    final_score = (weighted_ai_score * 0.6) + (keyword_score * 0.4)

    return max(0, min(100, final_score))

def apply_frequency_deduction(base_score, event_frequency):
    """
    Apply deduction to 0-100 score.
    """
    # Ensure base_score is on 100 scale
    score = base_score * 10 if base_score <= 10 else base_score

    deduction = calculate_frequency_deduction(event_frequency)
    adjusted_score = max(10.0, score - deduction) # Min score 10
    return min(100.0, adjusted_score)

def get_audience_recommendations(event):
    appropriate_audiences = []
    for audience_name in TARGET_AUDIENCES.keys():
        if is_event_appropriate_for_audience(event, audience_name):
            appropriate_audiences.append(audience_name)
    return appropriate_audiences

def validate_event_exclusions(event_category, event_description, exclusion_rules):
    for rule in exclusion_rules:
        if rule.matches_event(event_category, event_description):
            return {'is_excluded': True, 'reason': rule.exclusion_reason, 'rule_id': rule.exclusion_id}
    return {'is_excluded': False, 'reason': None, 'rule_id': None}

def generate_event_disclaimer():
    return "Please note: Events are subject to change or cancellation. We strongly recommend checking the event host's website and social media for the latest updates before attending."
