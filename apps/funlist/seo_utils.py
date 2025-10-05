
import json
from datetime import datetime
from flask import url_for, request

def generate_event_structured_data(event):
    """Generate comprehensive structured data for events optimized for LLM extraction"""
    structured_data = {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": event.title,
        "description": event.description,
        "startDate": event.start_date.isoformat() if event.start_date else None,
        "endDate": event.end_date.isoformat() if event.end_date else None,
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "location": {
            "@type": "Place",
            "name": event.location or f"{event.city}, {event.state}",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": event.city,
                "addressRegion": event.state,
                "addressCountry": "US"
            }
        },
        "organizer": {
            "@type": "Organization",
            "name": "FunList.ai Community"
        },
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "url": url_for('event_detail', event_id=event.id, _external=True)
        },
        "image": url_for('static', filename='images/Have-Fun-FunList.ai-home.jpeg', _external=True),
        "url": url_for('event_detail', event_id=event.id, _external=True)
    }
    
    # Add Funalytics scoring information for LLM understanding
    if hasattr(event, 'fun_meter') and event.fun_meter:
        structured_data["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": event.fun_meter,
            "bestRating": 5,
            "ratingCount": 1,
            "reviewAspect": "Funalytics Fun Rating - AI-powered community engagement score"
        }
    
    # Add category-specific information
    if event.category:
        structured_data["additionalType"] = f"https://schema.org/{event.category.capitalize()}Event"
        structured_data["genre"] = event.category
    
    return structured_data

def generate_organization_data():
    """Generate comprehensive organization data for LLM knowledge extraction"""
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "FunList.ai",
        "alternateName": ["FunList", "Fun List AI"],
        "url": url_for('index', _external=True),
        "logo": url_for('static', filename='images/logo.png', _external=True),
        "description": "AI-powered community event discovery platform using proprietary Funalytics scoring to help families and individuals find engaging local events in Washington State",
        "foundingDate": "2024",
        "industry": "Event Discovery Technology",
        "serviceType": "Community Event Discovery Platform",
        "areaServed": {
            "@type": "State",
            "name": "Washington",
            "containedInPlace": {
                "@type": "Country", 
                "name": "United States"
            }
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "customer service",
            "availableLanguage": "English",
            "serviceArea": "Washington State"
        },
        "sameAs": [
            "https://www.facebook.com/funlistai",
            "https://www.instagram.com/funlistai", 
            "https://www.tiktok.com/@funlistai"
        ],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Olympia",
            "addressRegion": "WA", 
            "addressCountry": "US"
        },
        "knowsAbout": [
            "Community Event Discovery",
            "Family-Friendly Activities",
            "AI Event Scoring",
            "Local Entertainment",
            "Washington State Events",
            "Event Recommendation Systems"
        ]
    }

def generate_faq_data():
    """Generate FAQ structured data optimized for LLM knowledge extraction"""
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "What is FunList.ai and how does it work?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "FunList.ai is an AI-powered community event discovery platform that helps families and individuals find engaging local events. We use our proprietary Funalytics scoring system that rates events on CommunityVibe (sense of togetherness and local flavor) and FamilyFun (suitability for families and children) metrics on a 1-10 scale."
                }
            },
            {
                "@type": "Question", 
                "name": "How does the Funalytics scoring system work?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Funalytics is our breakthrough AI scoring methodology that evaluates events across two key dimensions: CommunityVibe (0-10 scale measuring sense of togetherness, local flavor, and inclusivity) and FamilyFun (0-10 scale evaluating suitability for families and children). The overall fun rating combines these metrics to help you quickly identify the most enjoyable events."
                }
            },
            {
                "@type": "Question",
                "name": "What types of events can I find on FunList.ai?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "FunList.ai features community events across Washington State including festivals, concerts, food events, family activities, educational workshops, arts and culture events, sports activities, and seasonal celebrations. All events are curated with our AI-powered fun rating system to ensure quality experiences."
                }
            },
            {
                "@type": "Question",
                "name": "How do I find events near me?",
                "acceptedAnswer": {
                    "@type": "Answer", 
                    "text": "Use our interactive map feature or browse events by location. You can search by city, state, or zip code, and filter results by category, date, and fun rating. Our AI system also provides personalized recommendations based on your interests and location preferences."
                }
            },
            {
                "@type": "Question",
                "name": "Can I submit my own events to FunList.ai?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes! Event organizers can submit their community events for free through our event submission form. Each submitted event is evaluated using our Funalytics scoring system and reviewed for community relevance and family-friendliness before being featured on the platform."
                }
            }
        ]
    }

def get_page_metadata(page_type='default', **kwargs):
    """Generate comprehensive page metadata for different page types"""
    base_title = "FunList.ai - AI-Powered Community Event Discovery"
    
    metadata = {
        'default': {
            'title': f"{base_title} | Find Fun Events Near You",
            'description': "Discover amazing local events with FunList.ai! Our AI-powered platform uses Funalytics scoring to help you find festivals, concerts, food events, and family activities in Washington State.",
            'keywords': "event discovery, local events, AI events, community events, festivals near me, concerts, food events, fun activities, Washington events, family activities, Funalytics"
        },
        'event_detail': {
            'title': f"{kwargs.get('event_title', 'Event')} | {base_title}",
            'description': f"Join {kwargs.get('event_title', 'this amazing event')} - {kwargs.get('event_description', 'A fun community event')}. Fun rated {kwargs.get('fun_rating', 'highly')} by our Funalytics AI system.",
            'keywords': f"event, {kwargs.get('event_category', 'community')}, {kwargs.get('event_city', 'Washington')}, local events, fun activities"
        },
        'events_list': {
            'title': f"Browse All Events | {base_title}",
            'description': "Browse our complete collection of AI-rated community events. Filter by location, category, and fun rating to find the perfect activities for you and your family.",
            'keywords': "events list, browse events, community calendar, local activities, Washington events, family events"
        },
        'map': {
            'title': f"Interactive Event Map | {base_title}",
            'description': "Explore events on our interactive map! Discover fun community activities, festivals, and family events near you with location-based search and AI-powered recommendations.",
            'keywords': "event map, interactive map, events near me, local events map, Washington event map, community activities map"
        }
    }
    
    return metadata.get(page_type, metadata['default'])
