from flask import render_template, flash, redirect, url_for, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from forms import SignupForm, LoginForm, ProfileForm
from models import User, Event # Added Event import
from db_init import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

def init_routes(app):
    @app.route('/subscribe', methods=['POST'])
    def subscribe():
        try:
            data = request.get_json()
            email = data.get('email')
            if email:
                # Here you would typically save this to your database
                # For now, we'll just return success
                return jsonify({'success': True, 'message': 'Subscription successful'})
            return jsonify({'success': False, 'message': 'Email is required'}), 400
        except Exception as e:
            logger.error(f"Subscription error: {str(e)}")
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
        events = Event.query.order_by(Event.date.desc()).limit(6).all()
        if current_user.is_authenticated:
            return render_template('index.html', user=current_user, events=events)
        return render_template('home.html', events=events)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        form = SignupForm()
        if form.validate_on_submit():
            try:
                user = User()
                user.email = form.email.data
                user.set_password(form.password.data)
                user.account_active = True

                db.session.add(user)
                db.session.commit()

                flash('Account created successfully! You can now log in.', 'success')
                return redirect(url_for('login'))

            except IntegrityError as e:
                db.session.rollback()
                logger.error(f"Database integrity error during sign up: {str(e)}")
                error_msg = str(e).lower()

                if 'email' in error_msg and 'unique constraint' in error_msg:
                    flash('This email address is already registered. Please use a different email or try logging in.', 'danger')
                    form.email.errors = list(form.email.errors) + ['Email already registered']
                else:
                    flash('There was a problem with your sign up. Please verify your information and try again.', 'danger')

            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Database error during sign up: {str(e)}")
                flash('We encountered a technical issue. Our team has been notified. Please try again later.', 'danger')

            except Exception as e:
                db.session.rollback()
                logger.error(f"Unexpected error during sign up: {str(e)}")
                flash('An unexpected error occurred. Please try again. If the problem persists, contact support.', 'danger')

        return render_template('signup.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        form = LoginForm()
        if form.validate_on_submit():
            try:
                user = User.query.filter_by(email=form.email.data).first()

                if user and user.check_password(form.password.data):
                    if form.remember_me.data:
                        session.permanent = True

                    session['user_id'] = user.id
                    session['login_time'] = datetime.utcnow().isoformat()
                    session['last_activity'] = datetime.utcnow().isoformat()

                    login_user(user, remember=form.remember_me.data)
                    user.last_login = db.func.now()
                    db.session.commit()

                    flash('Logged in successfully!', 'success')
                    next_page = request.args.get('next')
                    return redirect(next_page or url_for('index'))
                else:
                    logger.warning(f"Failed login attempt for email: {form.email.data}")
                    flash('Invalid email or password. Please try again.', 'danger')

            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Database error during login: {str(e)}")
                flash('We encountered a technical issue. Please try again later.', 'danger')

            except Exception as e:
                logger.error(f"Unexpected error during login: {str(e)}")
                flash('An unexpected error occurred. Please try again.', 'danger')

        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        session.clear()
        logout_user()
        flash('You have been logged out successfully.', 'info')
        return redirect(url_for('index'))

    @app.route('/profile', methods=['GET'])
    @login_required
    def profile():
        return render_template('profile.html', user=current_user)

    @app.route('/profile/edit', methods=['GET', 'POST'])
    @login_required
    def edit_profile():
        form = ProfileForm()
        form.user_id = current_user.id

        if request.method == 'GET':
            form.username.data = current_user.username
            form.first_name.data = current_user.first_name
            form.last_name.data = current_user.last_name
            form.bio.data = current_user.bio
            form.location.data = current_user.location
            form.interests.data = current_user.interests
            form.birth_date.data = current_user.birth_date

        if form.validate_on_submit():
            try:
                profile_data = {
                    'username': form.username.data,
                    'first_name': form.first_name.data,
                    'last_name': form.last_name.data,
                    'bio': form.bio.data,
                    'location': form.location.data,
                    'interests': form.interests.data,
                    'birth_date': form.birth_date.data
                }

                current_user.update_profile(profile_data)
                db.session.commit()
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('profile'))

            except IntegrityError as e:
                db.session.rollback()
                logger.error(f"Database integrity error during profile update: {str(e)}")
                flash('There was a problem updating your profile. Please try again.', 'danger')

            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Database error during profile update: {str(e)}")
                flash('We encountered a technical issue. Please try again later.', 'danger')

            except Exception as e:
                db.session.rollback()
                logger.error(f"Unexpected error during profile update: {str(e)}")
                flash('An unexpected error occurred. Please try again.', 'danger')

        return render_template('edit_profile.html', form=form)

    @app.route('/events')
    def events():
        category = request.args.get('category')
        date = request.args.get('date')
        location = request.args.get('location')

        query = Event.query

        if category:
            query = query.filter(Event.category == category)
        if date:
            query = query.filter(db.func.date(Event.date) == date)
        if location:
            query = query.filter(Event.location.ilike(f'%{location}%'))

        events = query.order_by(Event.date).all()
        return render_template('events.html', events=events)

    @app.route('/map')
    def map():
        events = Event.query.all()
        return render_template('map.html', events=events)

    @app.route('/event/<int:event_id>')
    def event_detail(event_id):
        event = Event.query.get_or_404(event_id)
        return render_template('event_detail.html', event=event)

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500