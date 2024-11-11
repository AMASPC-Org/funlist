from flask import render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from app import app, db, logger
from forms import RegistrationForm
from models import User
from sqlalchemy.exc import SQLAlchemyError

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
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during registration: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'danger')
        except Exception as e:
            logger.error(f"Unexpected error during registration: {str(e)}")
            flash('An unexpected error occurred. Please try again.', 'danger')
    return render_template('register.html', form=form)

@app.route('/login')
def login():
    return render_template('login.html')
