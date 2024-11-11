from flask import render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_required
from forms import RegistrationForm
from models import User
from db_init import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from typing import List

logger = logging.getLogger(__name__)

def init_routes(app):
    @app.route('/')
    def index():
        return redirect(url_for('register'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            flash('You are already registered and logged in.', 'info')
            return redirect(url_for('index'))
            
        form = RegistrationForm()
        if form.validate_on_submit():
            try:
                if not form.password.data:
                    flash('Password is required. Please enter a secure password.', 'danger')
                    return render_template('register.html', form=form)

                # Create new user instance
                user = User()
                user.email = form.email.data
                user.password_hash = generate_password_hash(form.password.data)
                
                # Add user to database
                db.session.add(user)
                db.session.commit()
                
                logger.info(f"Successfully registered user: {user.email}")
                flash('Registration successful! You can now log in with your email and password.', 'success')
                return redirect(url_for('login'))
                
            except IntegrityError as e:
                db.session.rollback()
                logger.error(f"Database integrity error during registration: {str(e)}")
                error_msg = str(e).lower()
                
                if 'email' in error_msg and 'unique constraint' in error_msg:
                    flash('This email address is already registered. Please use a different email or try logging in.', 'danger')
                    form.email.errors = list(form.email.errors) + ['Email already registered']
                else:
                    flash('There was a problem with your registration. Please verify your information and try again.', 'danger')
                    
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Database error during registration: {str(e)}")
                flash('We encountered a technical issue. Our team has been notified. Please try again later.', 'danger')
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"Unexpected error during registration: {str(e)}")
                flash('An unexpected error occurred. Please try again. If the problem persists, contact support.', 'danger')
        
        # If form validation failed, errors will be shown in the template
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('login.html')

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
