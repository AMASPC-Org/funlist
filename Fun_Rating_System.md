
# FunList.ai Funalytics™ Scoring System

## Overview

The FunList.ai platform uses Funalytics™, a sophisticated AI-powered scoring algorithm, to help users discover and filter events based on their potential for fun. This document outlines the core logic and methodologies that power our event discovery and scoring system.

## Funalytics™ Score Basics

Events in FunList.ai are assigned a "Funalytics™ Score" on a scale of 0-10, where:

- 1-2: Low fun potential
- 3-4: Fair fun
- 5-6: Good fun
- 7-8: Great fun
- 9-10: Exceptional fun

For more details, see [Funalytics Documentation](docs/FUNALYTICS_DOCS.md).

## Score Assignment Process

1. **Initial Score**: Funalytics™ automatically computes scores based on event details, category, and keywords
2. **Score Verification**: Admin review may trigger score recomputation based on updated event details
3. **Featured Status**: Events with high Funalytics™ scores can be marked as "featured" by administrators

## Search and Discovery Algorithm

### Featured Events API

The platform includes an API endpoint (`/api/featured-events`) that leverages Funalytics™ scores to enhance event discovery:

```python
# From routes.py - Featured Events API
@app.route("/api/featured-events")
def featured_events_api():
    # Feature is now enabled
    FEATURED_EVENTS_ENABLED = True
    
    # Get user coordinates
    lat = request.args.get("lat")
    lng = request.args.get("lng")

    # Query high-fun events
    events = Event.query.filter(
        Event.latitude.isnot(None),
        Event.longitude.isnot(None),
        Event.fun_meter >= 4,       # Only events with Funalytics™ score of 4 or higher
        Event.status == "approved",
    ).all()

    # Calculate distances and filter to nearby events (15 mile radius)
    featured = []
    for event in events:
        # Convert to miles (1 degree ≈ 69 miles)
        distance = (
            (float(event.latitude) - float(lat)) ** 2 +
            (float(event.longitude) - float(lng)) ** 2
        ) ** 0.5 * 69

        if distance <= 15:  # 15 miles radius
            featured.append({
                "id": event.id,
                "title": event.title,
                "description": event.description[:100] + "..." if len(event.description) > 100 else event.description,
                "date": event.start_date.strftime("%Y-%m-%d"),
                "fun_meter": event.fun_meter,
                "distance": round(distance, 1)
            })

    # Return events sorted by Funalytics™ score (highest first) and then by date
    return jsonify({
        "success": True,
        "events": sorted(featured, key=lambda x: (-x["fun_meter"], x["date"]))[:5]
    })
```

### Event Filtering Logic

The map and events pages implement client-side filtering based on Funalytics™ scores:

1. **Map Filtering**: 
   ```javascript
   if (funRatingFilter && funRatingFilter !== 'All Fun Ratings') {
       const minRating = parseInt(funRatingFilter);
       if (funRating < minRating) {
           passesFilter = false;
       }
   }
   ```

2. **Events Page Filtering**:
   Funalytics™ score filters provide users with direct control, allowing them to find events meeting their minimum fun threshold.

## Geographic Relevance

The platform prioritizes geographic relevance in several ways:

1. **Proximity-Based Results**: Events are ranked partially based on proximity to the user's location
2. **Map Visualization**: The interactive map interface automatically updates visible events based on the current map bounds
3. **Location-Based Featured Events**: The featured events algorithm displays only events within 15 miles of the user's location

## Future Algorithm Enhancements

Based on the codebase structure, potential enhancements to the algorithm may include:

1. **Personalized Recommendations**: A recommendation engine based on user preferences and past behavior
   ```python
   # From utils.py (not yet fully implemented)
   def get_personalized_recommendations(user, limit=10):
       user_groups = [group.name for group in user.groups]
       future_events = Event.query.filter(
           Event.target_audience.in_(user_groups),
           Event.date > datetime.utcnow()
       ).all()
       return future_events[:limit]
   ```

2. **Event Similarity Scoring**: Suggesting similar events based on multiple attributes
   ```python
   # From utils.py
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
   ```

3. **Category-Based Analytics**: The admin dashboard shows events by category distribution, indicating a potential for future category-weighted algorithms.

## Admin Controls and Data Insights

The admin dashboard provides insights into event statistics and can be used to make data-driven decisions about which events should be featured. Admins have the ability to:

1. View pending events
2. Approve or reject events
3. Edit event details including fun ratings
4. Mark events as featured

## Prohibited Advertisers Feature

FunList.ai also includes the ability for event organizers to specify prohibited advertiser categories, ensuring appropriate advertising context for each event. This feature demonstrates the platform's commitment to alignment between event content and surrounding promotional material.

## Conclusion

The FunList.ai Funalytics™ Scoring System is designed to surface the most enjoyable events to users based on a combination of:

- AI-powered Funalytics™ scores (CommunityVibe™ + FamilyFun™)
- Geographic relevance
- Event attributes matching
- Administrative curation

This multi-faceted approach ensures that users can quickly discover events that match their interests and location while prioritizing those with the highest potential for enjoyment.

For complete technical documentation, see [Funalytics™ Documentation](docs/FUNALYTICS_DOCS.md).
