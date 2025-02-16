from flask import render_template, flash, redirect, url_for, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from forms import SignupForm, LoginForm, ProfileForm, EventForm
from models import User, Event, Subscriber  # Ensure all models are imported
from db_init import db
from utils import geocode_address
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def init_routes(app):

    @app.route('/subscribe', methods=['POST'])
    def subscribe():
        try:
            data = request.get_json()
            email = data.get('email')
            if not email:
                return jsonify({'success': False, 'message': 'Email is required'}), 400

            if Subscriber.query.filter_by(email=email).first():
                return jsonify({'success': False, 'message': 'Email already subscribed'}), 400

            subscriber = Subscriber(email=email)
            db.session.add(subscriber)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Subscription successful'})
        except Exception as e:
            logger.error(f"Subscription error: {str(e)}")
            db.session.rollback()
            return jsonify({'success': False, 'message': 'An error occurred'}), 500

    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            current_time = datetime.utcnow()
            if 'last_activity' not in session:
                session['last_activity'] = current_time
                return
            last_activity = session.get('last_activity')
            if isinstance(last_activity, str):
                try:
                    last_activity = datetime.fromisoformat(last_activity)
                except ValueError:
                    last_activity = current_time
            if (current_time - last_activity) > timedelta(minutes=30):
                session.clear()
                logout_user()
                flash('Your session has expired. Please log in again.', 'info')
                return redirect(url_for('login'))
            session['last_activity'] = current_time

    @app.route('/')
    def index():
        events = Event.query.order_by(Event.start_date.desc()).all()
        events_json = json.dumps([
            {
                'id': event.id,
                'title': event.title,
                'date': event.start_date.strftime('%B %d, %Y'),
                'category': event.category,
                'latitude': event.latitude,
                'longitude': event.longitude,
                'description': event.description[:100],
                'funMeter': event.fun_meter,
                'url': url_for('event_detail', event_id=event.id)
            } for event in events
        ])
        return render_template('home.html', events=events, events_json=events_json, user=current_user)

    @app.route('/events')
    def events():
        category = request.args.get('category')
        date = request.args.get('date')
        location = request.args.get('location')

        query = Event.query

        if category:
            query = query.filter(Event.category == category)
        if date:
            query = query.filter(db.func.date(Event.start_date) == date)
        if location:
            query = query.filter(Event.location.ilike(f'%{location}%'))

        events = query.order_by(Event.start_date).all()
        return render_template('events.html', events=events)

    @app.route('/map')
    def map_view():
        events = Event.query.all()
        events_json = json.dumps([
            {
                'id': event.id,
                'title': event.title,
                'date': event.start_date.strftime('%B %d, %Y'),
                'category': event.category,
                'latitude': event.latitude,
                'longitude': event.longitude,
                'description': event.description[:100],
                'funMeter': event.fun_meter,
                'url': url_for('event_detail', event_id=event.id)
            } for event in events
        ])
        return render_template('map.html', events=events, events_json=events_json, user=current_user)

    @app.route('/event/<int:event_id>')
    def event_detail(event_id):
        event = Event.query.get_or_404(event_id)
        return render_template('event_detail.html', event=event)

    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('index'))

        status = request.args.get('status', 'pending')

        stats = {
            'pending_events': Event.query.filter_by(status='pending').count(),
            'total_users': User.query.count(),
            'todays_events': Event.query.filter(
                Event.start_date >= datetime.now().date(),
                Event.start_date < datetime.now().date() + timedelta(days=1)
            ).count(),
        }

        events = Event.query.filter_by(status=status).order_by(Event.start_date).all()

        return render_template('admin_dashboard.html', stats=stats, events=events, status=status)

    @app.route('/admin/event/<int:event_id>/<action>', methods=['POST'])
    @login_required
    def admin_event_action(event_id, action):
        if not current_user.is_admin:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403

        event = Event.query.get_or_404(event_id)

        if action == 'approve':
            event.status = 'approved'
        elif action == 'reject':
            event.status = 'rejected'
        elif action == 'delete':
            db.session.delete(event)

        db.session.commit()
        return jsonify({'success': True})

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
