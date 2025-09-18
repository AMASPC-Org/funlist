
from datetime import datetime
from urllib.parse import urlparse
import re

def generate_event_schema(event):
    """Generate structured data for events"""
    schema = {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": event.title,
        "description": event.description,
        "startDate": event.start_date.isoformat(),
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
        }
    }
    
    if event.end_date:
        schema["endDate"] = event.end_date.isoformat()
    
    if event.street:
        schema["location"]["address"]["streetAddress"] = event.street
    
    if event.zip_code:
        schema["location"]["address"]["postalCode"] = event.zip_code
    
    if event.latitude and event.longitude:
        schema["location"]["geo"] = {
            "@type": "GeoCoordinates",
            "latitude": event.latitude,
            "longitude": event.longitude
        }
    
    if event.website:
        schema["url"] = event.website
    
    if event.fun_meter:
        schema["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(event.fun_meter),
            "bestRating": "5",
            "worstRating": "1"
        }
    
    return schema

def generate_seo_meta(title, description, keywords=None, og_image=None):
    """Generate SEO meta tags"""
    meta = {
        'title': title,
        'description': description[:160],  # Limit to 160 chars
        'keywords': keywords or [],
        'og_image': og_image
    }
    return meta

def clean_url_for_seo(text):
    """Create SEO-friendly URL slugs"""
    # Convert to lowercase and replace spaces/special chars with hyphens
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def generate_local_business_schema(name, description, address=None):
    """Generate local business structured data"""
    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": name,
        "description": description
    }
    
    if address:
        schema["address"] = {
            "@type": "PostalAddress",
            "addressLocality": address.get("city", ""),
            "addressRegion": address.get("state", ""),
            "addressCountry": address.get("country", "US")
        }
    
    return schema
