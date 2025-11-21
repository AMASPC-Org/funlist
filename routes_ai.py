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

        # Log failed attempt to database
        log_entry = AIAccessLog(  # type: ignore
            consumer=consumer or 'unknown',
            purpose=purpose or 'unknown',
            api_key='****',  # Don't log missing key
            path=request.path,
            ip_address=ip_address,
            user_agent=user_agent,
            success=False,
            error_message='Missing X-AI-Key header'
        )
        db.session.add(log_entry)
        db.session.commit()

        return jsonify({
            "error": "Missing X-AI-Key header",
            "message": "API key is required for authentication"
        }), 401

    if api_key not in VALID_API_KEYS:
        logger.warning(f"AI Feed access attempt with invalid API key from {ip_address}")

        # Log failed attempt to database
        log_entry = AIAccessLog(  # type: ignore
            consumer=consumer or 'unknown',
            purpose=purpose or 'unknown',
            api_key=api_key[-4:] if len(api_key) > 4 else '****',  # Store only last 4 chars
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
        # Log failed attempt to database
        log_entry = AIAccessLog(  # type: ignore
            consumer='unknown',
            purpose=purpose or 'unknown',
            api_key=api_key[-4:] if len(api_key) > 4 else '****',
            path=request.path,
            ip_address=ip_address,
            user_agent=user_agent,
            success=False,
            error_message='Missing X-AI-Consumer header'
        )
        db.session.add(log_entry)
        db.session.commit()

        return jsonify({
            "error": "Missing X-AI-Consumer header",
            "message": "X-AI-Consumer header is required to identify your application"
        }), 400

    if not purpose:
        # Log failed attempt to database
        log_entry = AIAccessLog(  # type: ignore
            consumer=consumer,
            purpose='unknown',
            api_key=api_key[-4:] if len(api_key) > 4 else '****',
            path=request.path,
            ip_address=ip_address,
            user_agent=user_agent,
            success=False,
            error_message='Missing X-AI-Purpose header'
        )
        db.session.add(log_entry)
        db.session.commit()

        return jsonify({
            "error": "Missing X-AI-Purpose header",
            "message": "X-AI-Purpose header is required to specify data usage intent"
        }), 400

    # Log successful access to database BEFORE processing request
    log_entry = AIAccessLog(  # type: ignore
        consumer=consumer,
        purpose=purpose,
        api_key=api_key[-4:] if len(api_key) > 4 else '****',  # Store only last 4 chars for security
        path=request.path,
        ip_address=ip_address,
        user_agent=user_agent,
        success=True,
        error_message=None
    )
    db.session.add(log_entry)
    db.session.commit()

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
                "start_time": str(event.start_time) if event.start_time else None,
                "end_date": event.end_date.strftime('%Y-%m-%d') if event.end_date else None,
                "end_time": str(event.end_time) if event.end_time else None,
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
        # Log the error in the database as well
        error_log_entry = AIAccessLog(  # type: ignore
            consumer=consumer or 'unknown',
            purpose=purpose or 'unknown',
            api_key=api_key[-4:] if len(api_key) > 4 else '****',
            path=request.path,
            ip_address=ip_address,
            user_agent=user_agent,
            success=False,
            error_message=f'Internal server error: {str(e)}'
        )
        db.session.add(error_log_entry)
        db.session.commit()

        return jsonify({
            "error": "Internal server error",
            "message": "Failed to generate event feed"
        }), 500


@ai_routes.route('/ai-report')
@login_required
def ai_access_report():
    """Admin-only dashboard for monitoring AI access"""

    # Check if user is admin
    if not current_user.is_admin:
        flash('You do not have permission to view this page.', 'danger')
        return redirect(url_for('index'))

    # Query recent access logs
    recent_logs = AIAccessLog.query.order_by(
        AIAccessLog.created_at.desc()
    ).limit(50).all()

    # Calculate statistics
    total_requests = AIAccessLog.query.count()
    successful_requests = AIAccessLog.query.filter_by(success=True).count()
    failed_requests = AIAccessLog.query.filter_by(success=False).count()

    # Get unique consumers
    unique_consumers = db.session.query(
        AIAccessLog.consumer
    ).distinct().count()

    stats = {
        'total_requests': total_requests,
        'successful_requests': successful_requests,
        'failed_requests': failed_requests,
        'success_rate': round((successful_requests / total_requests * 100) if total_requests > 0 else 0, 1),
        'unique_consumers': unique_consumers
    }

    return render_template('ai/report.html', logs=recent_logs, stats=stats)


@ai_routes.route('/ai-gateway')
def ai_gateway():
    """Main AI Gateway landing page"""
    return render_template('ai/gateway.html')


@ai_routes.route('/ai-policy')
def ai_policy():
    """AI Access Policy page - human-readable rules and restrictions"""
    return render_template('ai/policy.html')


@ai_routes.route('/ai-data-license')
def ai_data_license():
    """AI Data License page - legal terms governing data usage"""
    return render_template('ai/license.html')


@ai_routes.route('/ai-feed-guide')
def ai_feed_guide():
    """AI Feed Guide - technical documentation for using the AI feed"""
    return render_template('ai/feed_guide.html')


@ai_routes.route('/.well-known/ai-policy.json')
def ai_policy_json():
    """Machine-readable AI policy JSON document"""
    policy = {
        "version": "1.0",
        "lastUpdated": "2025-11-21",
        "provider": "FunList.ai",
        "dataTypes": ["events", "venues", "organizers"],
        "allowedUses": [
            "search",
            "citation",
            "analysis",
            "summarization"
        ],
        "prohibitedUses": [
            "training",
            "model_development",
            "commercial_redistribution"
        ],
        "attribution": {
            "required": True,
            "format": "Data provided by FunList.ai"
        },
        "rateLimits": {
            "perMinute": 60,
            "perHour": 1000,
            "perDay": 10000
        },
        "authentication": {
            "required": True,
            "type": "api_key",
            "headers": ["X-AI-Key", "X-AI-Consumer", "X-AI-Purpose"]
        },
        "contact": "legal@funlist.ai",
        "licenseUrl": "https://funlist.ai/ai-data-license"
    }
    return jsonify(policy)