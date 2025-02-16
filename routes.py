                from flask import render_template, flash, redirect, url_for, request, session, jsonify
                from werkzeug.security import generate_password_hash, check_password_hash
                # from flask_login import current_user, login_required, login_user, logout_user # Removed: Not using Flask-Login
                from forms import SignupForm, LoginForm, ProfileForm, EventForm
                #from models import User, Event  # Import from your Drizzle schema, NOT SQLAlchemy
                from db import db # Import your Drizzle DB instance
                from schema import users, events #, subscribers  # Import your Drizzle schema definitions
                from utils.auth import hashPassword, comparePasswords, sendVerificationEmail, sendPasswordResetEmail, requireAuth, requireAdmin # Import from utils
                # from utils import geocode_address # Removed until geocode_address is fully fixed
                from sqlalchemy.exc import SQLAlchemyError, IntegrityError # Not used with Drizzle
                import logging
                from datetime import datetime, timedelta, timezone # Add timezone
                import json
                from drizzle_zod import parse_params
                from drizzle_zod.schemas import params

                # Configure logging
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
                            #You need to define the subscribers table in your Drizzle schema
                            #existing_subscriber = db.select(subscribers).from_(subscribers).where(eq(subscribers.c.email, email)).first()
                            #if existing_subscriber:
                            #    return jsonify({'success': False, 'message': 'Email already subscribed'}), 400

                            #subscriber = Subscriber(email=email) # Assuming you have a Subscriber model/table
                            #db.insert(subscribers).values(email=email) # Use Drizzle syntax
                            #db.commit() # Drizzle doesn't use commit

                            return jsonify({'success': True, 'message': 'Subscription successful'})  # Placeholder
                        except Exception as e:
                            logger.error(f"Subscription error: {str(e)}")
                            # db.session.rollback()  # Drizzle doesn't use rollback in this way
                            return jsonify({'success': False, 'message': 'An error occurred'}), 500


                    # I'm commenting out the before_request handler for now, because it relies on
                    # Flask-Login, which we're not using.  We'll reimplement session management
                    # later, using a Drizzle-compatible approach.
                    # @app.before_request
                    # def before_request():
                    #     if current_user.is_authenticated:
                    #         current_time = datetime.utcnow()
                    #         if 'last_activity' not in session:
                    #             session['last_activity'] = current_time
                    #             return
                    #         last_activity = session.get('last_activity')
                    #         if isinstance(last_activity, str):
                    #             try:
                    #                 last_activity = datetime.fromisoformat(last_activity)
                    #             except ValueError:
                    #                 last_activity = current_time
                    #         if (current_time - last_activity) > timedelta(minutes=30):
                    #             session.clear()
                    #             logout_user()
                    #             flash('Your session has expired. Please log in again.', 'info')
                    #             return redirect(url_for('login'))
                    #         session['last_activity'] = current_time


                    @app.route('/')
                    def index():
                      #No longer returning mockData
                        # events = Event.query.order_by(Event.start_date.desc()).all()
                        # events_json = [{
                        #     'id': event.id,
                        #     'title': event.title,
                        #     'date': event.start_date.strftime('%B %d, %Y'),
                        #     'category': event.category,
                        #     'latitude': event.latitude,
                        #     'longitude': event.longitude,
                        #     'description': event.description[:100],
                        #     'funMeter': event.fun_meter,
                        #     'url': url_for('event_detail', event_id=event.id)
                        # } for event in events]
                        return render_template('home.html', user=None) #, events=events, events_json=json.dumps(events_json))

                    @app.route('/signup', methods=['GET', 'POST'])
                    def signup():
                        # if current_user.is_authenticated:  # We're not using Flask-Login
                        #     return redirect(url_for('index'))

                        # form = SignupForm() # Where is this form coming from?  You'll need a similar form for Drizzle
                        # if form.validate_on_submit():
                        #     try:
                        #         user = User() # This needs to use your Drizzle User model
                        #         user.email = form.email.data
                        #         user.set_password(form.password.data) # You need a password hashing function!
                        #         user.account_active = True

                        #         db.session.add(user)  # This is SQLAlchemy syntax. Use Drizzle.
                        #         db.session.commit()

                        #         flash('Account created successfully! You can now log in.', 'success')
                        #         return redirect(url_for('login'))

                        # ... (rest of the error handling - adapt to Drizzle as needed) ...

                        return render_template('signup.html') #, form=form)  # You'll need to create a form

                    @app.route('/login', methods=['GET', 'POST'])
                    def login():
                        # ... (Similar changes as signup - use Drizzle, remove Flask-Login) ...
                         return render_template('login.html')

                    # @app.route('/logout') # Removed because it was causing navigation issues, can add back later.
                    # @login_required
                    # def logout():
                    #     session.clear()
                    #     logout_user()
                    #     flash('You have been logged out successfully.', 'info')
                    #     return redirect(url_for('index'))

                    @app.route('/profile', methods=['GET'])
                    #@login_required # Removed
                    def profile():
                        return render_template('profile.html')#, user=current_user)

                    @app.route('/profile/edit', methods=['GET', 'POST'])
                    # @login_required # Removed
                    def edit_profile():
                      return render_template('profile.html')
                        # form = ProfileForm()
                        # form.user_id = current_user.id

                        # if request.method == 'GET':
                        #     form.username.data = current_user.username
                        #     form.first_name.data = current_user.first_name
                        #     form.last_name.data = current_user.last_name
                        #     form.bio.data = current_user.bio
                        #     form.location.data = current_user.location
                        #     form.interests.data = current_user.interests
                        #     form.birth_date.data = current_user.birth_date

                        # if form.validate_on_submit():
                        #     try:
                        #         profile_data = {
                        #             'username': form.username.data,
                        #             'first_name': form.first_name.data,
                        #             'last_name': form.last_name.data,
                        #             'bio': form.bio.data,
                        #             'location': form.location.data,
                        #             'interests': form.interests.data,
                        #             'birth_date': form.birth_date.data
                        #         }

                        #         current_user.update_profile(profile_data)
                        #         db.session.commit()
                        #         flash('Profile updated successfully!', 'success')
                        #         return redirect(url_for('profile'))

                            # except IntegrityError as e:
                            #     db.session.rollback()
                            #     logger.error(f"Database integrity error during profile update: {str(e)}")
                            #     flash('There was a problem updating your profile. Please try again.', 'danger')

                            # except SQLAlchemyError as e:
                            #     db.session.rollback()
                            #     logger.error(f"Database error during profile update: {str(e)}")
                            #     flash('We encountered a technical issue. Please try again later.', 'danger')

                            # except Exception as e:
                            #     db.session.rollback()
                            #     logger.error(f"Unexpected error during profile update: {str(e)}")
                            #     flash('An unexpected error occurred. Please try again.', 'danger')

                        # return render_template('edit_profile.html', form=form) # Removed form

                    @app.route('/events')
                    def events_list():
                        # category = request.args.get('category') #Filter by category later
                        # date = request.args.get('date')
                        # location = request.args.get('location')

                        # query = Event.query #Need to change

                        # if category:
                        #     query = query.filter(Event.category == category)
                        # if date:
                        #     query = query.filter(db.func.date(Event.start_date) == date)
                        # if location:
                        #     query = query.filter(Event.location.ilike(f'%{location}%'))

                        # events = query.order_by(Event.start_date).all()
                        # return render_template('events.html', events=events)
                        return render_template('events.html') #Keep simple to start

                    @app.route('/map')
                    def map_view():
                        # Fetch events from the database using Drizzle ORM
                        event_list = db.select().from_(events).all()

                        # Convert events to a list of dictionaries, handling dates correctly
                        events_json = []
                        for event in event_list:
                          event_dict = {
                              'id': event.id,
                              'title': event.title,
                              'description': event.description[:100] + '...' if event.description else '',
                              'start_date': event.start_date.isoformat() if event.start_date else None,  # Use isoformat for dates
                              'category': event.category,
                              'latitude': float(event.latitude) if event.latitude else None,
                              'longitude': float(event.longitude) if event.longitude else None,
                              'fun_meter': event.fun_meter
                              # Add other fields as necessary
                          }
                          events_json.append(event_dict)

                        # Pass events_json to the template
                        return render_template('map.html', events_json=events_json)

                    @app.route('/event/<int:event_id>')
                    def event_detail(event_id):
                        # event = Event.query.get_or_404(event_id) #Need to update
                        return render_template('event_detail.html') #, event=event)

                    @app.errorhandler(404)
                    def not_found_error(error):
                        return render_template('404.html'), 404

                    @app.route('/submit-event', methods=['GET', 'POST'])
                    # @login_required # Removed
                    def submit_event():
                      return render_template('submit.html')
                        # form = EventForm()
                        # if form.validate_on_submit():
                        #     coordinates = geocode_address(
                        #         form.street.data,
                        #         form.city.data,
                        #         form.state.data,
                        #         form.zip_code.data
                        #     )

                        #     if not coordinates:
                        #         flash('Could not geocode address. Please verify the address is correct.', 'danger')
                        #         return render_template('submit_event.html', form=form)

                        #     event = Event(
                        #         title=form.title.data,
                        #         description=form.description.data,
                        #         start_date=form.date.data,
                        #         end_date=form.date.data,
                        #         street=form.street.data,
                        #         city=form.city.data,
                        #         state=form.state.data,
                        #         zip_code=form.zip_code.data,
                        #         latitude=coordinates[0],
                        #         longitude=coordinates[1],
                        #         category=form.category.data,
                        #         target_audience=form.target_audience.data,
                        #         fun_meter=form.fun_meter.data,
                        #         user_id=current_user.id,
                        #         status='pending' #Added status field
                        #     )
                        #     db.session.add(event)
                        #     db.session.commit()
                        #     flash('Event created successfully!', 'success')
                        #     return redirect(url_for('events'))
                        # return render_template('submit_event.html', form=form) # Removed form

                    @app.errorhandler(500)
                    def internal_error(error):
                        # db.session.rollback()  # Not needed with Drizzle
                        return render_template('500.html'), 500

                    @app.route('/admin/login', methods=['GET', 'POST'])
                    def admin_login():
                      return render_template('admin.html')
                        # if current_user.is_authenticated and current_user.is_admin:  # Not using Flask-Login
                        #     return redirect(url_for('admin_dashboard'))

                        # form = LoginForm()
                        # if form.validate_on_submit():
                        #     user = User.query.filter_by(email=form.email.data).first()
                        #     if user and user.check_password(form.password.data) and user.is_admin:
                        #         login_user(user)
                        #         return redirect(url_for('admin_dashboard'))
                        #     flash('Invalid credentials or not an admin user.', 'danger')
                        # return render_template('admin_login.html', form=form) #Removed form

                    @app.route('/admin/events')
                    # @login_required # Removed
                    def admin_events():
                      return render_template('admin.html')
                        # if not current_user.is_admin:  # Not using Flask-Login
                        #     flash('Access denied. Admin privileges required.', 'danger')
                        #     return redirect(url_for('index'))
                        # events = Event.query.order_by(Event.start_date.desc()).all()
                        # return render_template('admin_events.html', events=events) #removed events

                    @app.route('/admin/users')
                    # @login_required # Removed
                    def admin_users():
                      return render_template('admin.html')
                        # if not current_user.is_admin:
                        #     flash('Access denied. Admin privileges required.', 'danger')
                        #     return redirect(url_for('index'))
                        # users = User.query.order_by(User.created_at.desc()).all()
                        # return render_template('admin_users.html', users=users) # Removed users

                    @app.route('/admin/analytics')
                    # @login_required # Removed
                    def admin_analytics():
                      return render_template('admin.html')
                        # if not current_user.is_admin:
                        #     flash('Access denied. Admin privileges required.', 'danger')
                        #     return redirect(url_for('index'))
                        # return render_template('admin_analytics.html')

                    @app.route('/admin/event/<int:event_id>/<action>', methods=['POST'])
                    # @login_required # Removed
                    def admin_event_action(event_id, action):
                      return render_template('admin.html')
                        # if not current_user.is_admin:
                        #     return jsonify({'success': False, 'message': 'Unauthorized'}), 403

                        # event = Event.query.get_or_404(event_id) # Need to update this

                        # if action == 'approve':
                        #     event.status = 'approved'
                        # elif action == 'reject':
                        #     event.status = 'rejected'
                        # elif action == 'delete':
                        #     db.session.delete(event)

                        # db.session.commit()
                        # return jsonify({'success': True})

                    @app.route('/admin/dashboard')
                    # @login_required # Removed
                    def admin_dashboard():
                      return render_template('admin.html')
                        # if not current_user.is_admin:
                        #     flash('Access denied. Admin privileges required.', 'danger')
                        #     return redirect(url_for('index'))

                        # tab = request.args.get('tab', 'overview')
                        # status = request.args.get('status', 'pending')

                        # # Get statistics for overview
                        # stats = {
                        #     'pending_events': Event.query.filter_by(status='pending').count(),
                        #     'total_users': User.query.count(),
                        #     'todays_events': Event.query.filter(
                        #         Event.start_date >= datetime.now().date(),
                        #         Event.start_date < datetime.now().date() + timedelta(days=1)
                        #     ).count(),
                        #     'new_users_24h': User.query.filter(
                        #         User.created_at >= datetime.now() - timedelta(hours=24)
                        #     ).count()
                        # }

                        # # Get events for event management
                        # events = Event.query.filter_by(status=status).order_by(Event.start_date).all()

                        # # Get users for user management
                        # users = User.query.order_by(User.created_at.desc()).all()

                        # # Get analytics data
                        # events_by_category = {
                        #     'labels': ['Sports', 'Music', 'Arts', 'Food', 'Other'],
                        #     'datasets': [{
                        #         'data': [
                        #             Event.query.filter_by(category='Sports').count(),
                        #             Event.query.filter_by(category='Music').count(),
                        #             Event.query.filter_by(category='Arts').count(),
                        #             Event.query.filter_by(category='Food').count(),
                        #             Event.query.filter_by(category='Other').count()
                        #         ]
                        #     }]
                        # }

                        # # User growth data (last 7 days)
                        # user_growth_data = {
                        #     'labels': [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(7)],
                        #     'datasets': [{
                        #         'label': 'New Users',
                        #         'data': [
                        #             User.query.filter(
                        #                 User.created_at >= datetime.now().date() - timedelta(days=x),
                        #                 User.created_at < datetime.now().date() - timedelta(days=x-1)
                        #             ).count() for x in range(7)
                        #         ]
                        #     }]
                        # }

                        # return render_template('admin_dashboard.html',
                        #                      active_tab=tab,
                        #                      stats=stats,
                        #                      events=events,
                        #                      users=users,
                        #                      status=status,
                        #                      events_by_category=events_by_category,
                        #                      user_growth_data=user_growth_data) # Removed, not using

                    @app.route('/admin/user/<int:user_id>/deactivate')
                    # @login_required # Removed
                    def admin_deactivate_user(user_id):
                      return
                        # if not current_user.is_admin:
                        #     return jsonify({'error': 'Unauthorized'}), 403

                        # user = User.query.get_or_404(user_id)
                        # user.account_active = False
                        # db.session.commit()
                        # flash('User account deactivated.', 'success')
                        # return redirect(url_for('admin_dashboard', tab='users'))

                    @app.route('/admin/user/<int:user_id>/activate')
                    # @login_required
                    def admin_activate_user(user_id):
                      return
                        # if not current_user.is_admin:
                        #     return jsonify({'error': 'Unauthorized'}), 403

                        # user = User.query.get_or_404(user_id)
                        # user.account_active = True
                        # db.session.commit()
                        # flash('User account activated.', 'success')
                        # return redirect(url_for('admin_dashboard', tab='users'))