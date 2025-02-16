from flask import render_template, flash, redirect, url_for, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, login_user, logout_user
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

    @app.route('/')
    def index():
        events = Event.query.order_by(Event.start_date.desc()).all()
        return render_template('home.html', events=events, user=current_user)

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
            except IntegrityError as e:
                db.session.rollback()
                logger.error(f"Database integrity error: {str(e)}")
                flash('Email already registered. Try logging in.', 'danger')
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Database error: {str(e)}")
                flash('Technical issue. Try again later.', 'danger')
        return render_template('signup.html', form=form)

    return app