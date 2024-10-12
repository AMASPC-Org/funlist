from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager
from models import User, Event, OrganizerProfile
from forms import LoginForm, RegistrationForm, EventForm, OrganizerProfileForm
from utils import get_weekly_top_events
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    top_events = get_weekly_top_events()
    return render_template('index.html', top_events=top_events)

@app.route('/events')
def events():
    category = request.args.get('category')
    date = request.args.get('date')
    location = request.args.get('location')
    target_audience = request.args.get('target_audience')

    query = Event.query

    if category:
        query = query.filter_by(category=category)
    if date:
        query = query.filter(Event.date >= datetime.strptime(date, '%Y-%m-%d'))
    if location:
        query = query.filter(Event.location.ilike(f'%{location}%'))
    if target_audience:
        query = query.filter_by(target_audience=target_audience)

    events = query.order_by(Event.date).all()
    return render_template('events.html', events=events)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)

@app.route('/submit_event', methods=['GET', 'POST'])
@login_required
def submit_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            location=form.location.data,
            category=form.category.data,
            target_audience=form.target_audience.data,
            fun_meter=form.fun_meter.data,
            user_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        flash('Your event has been submitted successfully!', 'success')
        return redirect(url_for('events'))
    return render_template('submit_event.html', form=form)

@app.route('/organizer_profile', methods=['GET', 'POST'])
@login_required
def organizer_profile():
    if not current_user.is_organizer:
        flash('You must be an organizer to access this page.', 'error')
        return redirect(url_for('index'))

    profile = OrganizerProfile.query.filter_by(user_id=current_user.id).first()
    form = OrganizerProfileForm(obj=profile)

    if form.validate_on_submit():
        if not profile:
            profile = OrganizerProfile(user_id=current_user.id)
        
        form.populate_obj(profile)
        db.session.add(profile)
        db.session.commit()
        flash('Your organizer profile has been updated.', 'success')
        return redirect(url_for('organizer_profile'))

    return render_template('organizer_profile.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, is_organizer=form.is_organizer.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/weekly_top_10')
def weekly_top_10():
    top_events = get_weekly_top_events(limit=10)
    return render_template('weekly_top_10.html', top_events=top_events)
