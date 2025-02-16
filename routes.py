from flask import render_template, flash, redirect, url_for, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from forms import SignupForm, LoginForm, ProfileForm, EventForm
from models import User, Event, Subscriber
from db_init import db
from utils import geocode_address
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)
handler = logging.FileHandler('app.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('home.html')

    @app.route('/map')
    def map():
        try:
            events = Event.query.order_by(Event.start_date.desc()).all()
            return render_template('map.html', events=events)
        except Exception as e:
            logger.error(f"Error fetching events for map: {str(e)}")
            flash('Error loading events map. Please try again later.', 'danger')
            return redirect(url_for('index'))

    @app.route('/events')
    def events():
        events = Event.query.order_by(Event.start_date.desc()).all()
        return render_template('events.html', events=events)

    @app.route('/submit_event', methods=['GET', 'POST'])
    @login_required
    def submit_event():
        form = EventForm()
        if form.validate_on_submit():
            try:
                event = Event(
                    title=form.title.data,
                    description=form.description.data,
                    start_date=form.start_date.data,
                    end_date=form.end_date.data,
                    street=form.street.data,
                    city=form.city.data,
                    state=form.state.data,
                    zip_code=form.zip_code.data,
                    category=form.category.data,
                    user_id=current_user.id
                )
                db.session.add(event)
                db.session.commit()
                flash('Event submitted successfully!', 'success')
                return redirect(url_for('events'))
            except Exception as e:
                logger.error(f"Event submission error: {str(e)}")
                db.session.rollback()
                flash('Error submitting event. Please try again.', 'danger')
        return render_template('submit_event.html', form=form)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = SignupForm()
        if form.validate_on_submit():
            try:
                user = User(
                    email=form.email.data,
                    password_hash=generate_password_hash(form.password.data),
                    account_active=True
                )
                db.session.add(user)
                db.session.commit()
                flash('Account created successfully! You can now log in.', 'success')
                return redirect(url_for('login'))
            except IntegrityError:
                db.session.rollback()
                flash('Email already registered. Try logging in.', 'danger')
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Database error: {str(e)}")
                flash('Technical issue. Try again later.', 'danger')
        return render_template('signup.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            flash('Invalid email or password', 'danger')
        return render_template('login.html', form=form)

    @app.route('/subscribe', methods=['POST'])
    def subscribe():
        try:
            data = request.get_json()
            email = data.get('email')
            if not email:
                return jsonify({'success': False, 'message': 'Email is required'}), 400

            existing_subscriber = db.session.execute(db.select(Subscriber).filter_by(email=email)).scalar_one_or_none()
            if existing_subscriber:
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
            last_activity = session.get('last_activity')
            if last_activity:
                try:
                    last_activity = datetime.fromisoformat(last_activity)
                except ValueError:
                    last_activity = current_time
                if (current_time - last_activity) > timedelta(minutes=30):
                    session.pop('last_activity', None)
                    logout_user()
                    flash('Your session has expired. Please log in again.', 'info')
                    return redirect(url_for('login'))
            session['last_activity'] = current_time.isoformat()

    return app