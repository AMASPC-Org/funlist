from flask import render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from app import app, db, logger
from forms import RegistrationForm
from models import User
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data)
            )
            db.session.add(user)
            db.session.commit()
            logger.info(f"Successfully registered user: {user.username}")
            flash('Registration successful! You can now log in with your credentials.', 'success')
            return redirect(url_for('login'))
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Database integrity error during registration: {str(e)}")
            if 'username' in str(e).lower():
                flash('This username is already taken. Please choose a different one.', 'danger')
            elif 'email' in str(e).lower():
                flash('This email address is already registered. Please use a different email.', 'danger')
            else:
                flash('There was a problem with your registration. Please try again.', 'danger')
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during registration: {str(e)}")
            flash('A database error occurred. Please try again later.', 'danger')
        except Exception as e:
            logger.error(f"Unexpected error during registration: {str(e)}")
            flash('An unexpected error occurred. Please try again later or contact support if the problem persists.', 'danger')
    return render_template('register.html', form=form)

@app.route('/login')
def login():
    return render_template('login.html')
