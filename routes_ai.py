
import os
import logging
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Event, AIAccessLog
from db_init import db
from datetime import datetime

logger = logging.getLogger(__name__)

ai_routes = Blueprint('ai_routes', __name__)

# In production, this should be stored in environment variables or a database
VALID_API_KEYS = {
    os.environ.get('AI_FEED_API_KEY', 'demo_key_12345'): 'demo',
    # Add more keys as needed
}

@ai_routes.route('/ai-feed.json', methods=['GET'])
def ai_feed():
    """
    AI Feed endpoint - provides structured event data for AI consumers
    Requires authentication headers:
    - X-AI-Key: API authentication token
    - X-AI-Consumer: Identifies the application/service
    - X-AI-Purpose: Intended use of the data
    """
    
    # Validate required headers
    api_key = request.headers.get('X-AI-Key')
    consumer = request.headers.get('X-AI-Consumer')
    purpose = request.headers.get('X-AI-Purpose')
    
    # Get IP address (accounting for proxy)
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip_address and ',' in ip_address:
        ip_address = ip_address.split(',')[0].strip()
    
    user_agent = request.headers.get('User-Agent', '')
    
    # Check API key first
    if not api_key:
        logger.warning(f"AI Feed access attempt without API key from {ip_address}")
        # Log failed attempt
        log_entry = AIAccessLog(
            consumer=consumer or 'unknown',
            purpose=purpose or 'unknown',
            api_key='****',
            path=request.path,
            ip_address=ip_address,
            user_agent=user_agent,
            success=False,
            error_message='Missing API key'
        )
        db.session.add(log_entry)
        db.session.commit()
        
        return jsonify({
            "error": "Missing X-AI-Key header",
            "message": "API key is required for authentication"
        }), 401
    
    if api_key not in VALID_API_KEYS:
        logger.warning(f"AI Feed access attempt with invalid API key from {ip_address}")
        # Log failed attempt
        log_entry = AIAccessLog(
            consumer=consumer or 'unknown',
            purpose=purpose or 'unknown',
            api_key=api_key[-4:] if len(api_key) > 4 else '****',
            path=request.path,
            ip_address=ip_address,
            user_agent=user_agent,
            success=False,
            error_message='Invalid API key'
        )
        db.session.add(log_entry)
        db.session.commit()
        
        return jsonify({
            "error": "Invalid API key",
            "message": "The provided API key is not valid"
        }), 401
    
    # Check other required headers
    if not consumer:
        return jsonify({
            "error": "Missing X-AI-Consumer header",
            "message": "X-AI-Consumer header is required to identify your application"
        }), 400
    
    if not purpose:
        return jsonify({
            "error": "Missing X-AI-Purpose header",
            "message": "X-AI-Purpose header is required to specify data usage intent"
        }), 400
    
    # Log the access
    logger.info(f"AI Feed accessed by consumer: {consumer}, purpose: {purpose}, key: {VALID_API_KEYS.get(api_key)}")
    
    try:
        # Query upcoming approved events
        current_date = datetime.utcnow()
        events = Event.query.filter(
            Event.status == 'approved',
            Event.start_date >= current_date
        ).order_by(Event.start_date).limit(10).all()
        
        # Format events for AI consumption
        events_data = []
        for event in events:
            event_dict = {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "start_date": event.start_date.strftime('%Y-%m-%d') if event.start_date else None,
                "start_time": event.start_time,
                "end_date": event.end_date.strftime('%Y-%m-%d') if event.end_date else None,
                "end_time": event.end_time,
                "location": {
                    "venue": event.location,
                    "street": event.street,
                    "city": event.city,
                    "state": event.state,
                    "zip_code": event.zip_code,
                    "coordinates": {
                        "latitude": event.latitude,
                        "longitude": event.longitude
                    } if event.latitude and event.longitude else None
                },
                "category": event.category,
                "target_audience": event.target_audience,
                "tags": event.tags.split(',') if event.tags else [],
                "fun_meter": event.fun_meter,
                "website": event.website,
                "all_day": event.all_day
            }
            events_data.append(event_dict)
        
        # Return structured response
        response_data = {
            "success": True,
            "metadata": {
                "total_events": len(events_data),
                "consumer": consumer,
                "purpose": purpose,
                "timestamp": datetime.utcnow().isoformat(),
                "api_version": "1.0"
            },
            "events": events_data
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error generating AI feed: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "message": "Failed to generate event feed"
        }), 500
