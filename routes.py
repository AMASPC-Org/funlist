from flask import render_template, flash, redirect, url_for, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from forms import SignupForm, LoginForm, ProfileForm, EventForm, ResetPasswordRequestForm, ResetPasswordForm, ContactForm
from models import User, Event, Subscriber, ProhibitedAdvertiserCategory
from db_init import db
from utils import geocode_address, send_password_reset_email
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from datetime import datetime, timedelta
import json
from dateutil.relativedelta import relativedelta
from sqlalchemy import func, inspect

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def init_routes(app):
    # Add CSP report endpoint (exempt from CSRF protection)
    @app.route('/csp-report', methods=['POST'])
    def csp_report():
        """Endpoint for CSP violation reports."""
        report = request.get_json() or request.get_data() or {}
        app.logger.warning(f"CSP violation: {report}")
        return '', 204  # No content response

    # Add global error handler for application context errors
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return render_template('500.html'), 500

    @app.route("/about")
    def about():
        return render_template('about.html')

    @app.route("/subscribe", methods=["POST"])
    def subscribe():
        data = request.get_json()
        email = data.get('email')
        preferences = data.get('preferences', {})

        if not email:
            return jsonify({'success': False, 'message': 'Email is required'})

        # Here you would typically add the email to your database or newsletter service
        # This is a placeholder implementation

        # Log the subscription for demo purposes
        app.logger.info(f"New subscription: {email} with preferences: {preferences}")

        return jsonify({'success': True, 'message': 'Subscription successful'})

    @app.route('/submit-feedback', methods=['POST'])
    def submit_feedback():
        data = request.get_json()
        feedback_type = data.get('type')
        message = data.get('message')
        email = data.get('email', 'Anonymous')

        if not feedback_type or not message:
            return jsonify({'success': False, 'message': 'Feedback type and message are required'})

        # Here you would typically store the feedback in your database
        # This is a placeholder implementation

        # Log the feedback for demo purposes
        app.logger.info(f"New feedback from {email} - Type: {feedback_type} - Message: {message}")

        return jsonify({'success': True, 'message': 'Feedback submitted successfully'})

    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            current_time = datetime.utcnow()
            if "last_activity" not in session:
                session["last_activity"] = current_time
                return
            last_activity = session.get("last_activity")
            if isinstance(last_activity, str):
                try:
                    last_activity = datetime.fromisoformat(last_activity)
                except ValueError:
                    last_activity = current_time
            if (current_time - last_activity) > timedelta(minutes=30):
                session.clear()
                logout_user()
                flash("Your session has expired. Please log in again.", "info")
                return redirect(url_for("login"))
            session["last_activity"] = current_time

    @app.route("/")
    def index():
        try:
            events = Event.query.order_by(Event.start_date.desc()).all()
            # Check if this is a new registration to show the wizard
            new_registration = session.pop('new_registration', False)
            return render_template("index.html", events=events, user=current_user, new_registration=new_registration)
        except Exception as e:
            app.logger.error(f"Error in index route: {str(e)}")
            return render_template("index.html", events=[], user=current_user, new_registration=False)

    @app.route("/save-preferences", methods=["POST"])
    @login_required
    def save_preferences():
        try:
            data = request.get_json()

            # Update user profile with preferences
            profile_data = {}

            if 'location' in data and data['location']:
                profile_data['location'] = data['location']

            if 'interests' in data and data['interests']:
                profile_data['interests'] = ','.join(data['interests'])

            # Update organizer profile if applicable
            if current_user.is_organizer:
                organizer_data = {}

                if 'organizationName' in data and data['organizationName']:
                    organizer_data['company_name'] = data['organizationName']

                if 'organizationWebsite' in data and data['organizationWebsite']:
                    organizer_data['organizer_website'] = data['organizationWebsite']

                if organizer_data:
                    current_user.update_organizer_profile(organizer_data)

            # Update user profile
            if profile_data:
                current_user.update_profile(profile_data)

            db.session.commit()

            return jsonify({"success": True, "message": "Preferences saved successfully"})
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving preferences: {str(e)}")
            return jsonify({"success": False, "message": str(e)}), 500

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        form = SignupForm()

        # Pre-select organizer option if specified in URL
        if request.args.get('as') == 'organizer':
            form.is_organizer.data = True
            form.is_event_creator.data = True

        if form.validate_on_submit():
            try:
                # Check if user already exists
                existing_user = User.query.filter_by(email=form.email.data).first()
                if existing_user:
                    flash("This email address is already registered. Please use a different email or try logging in.", "danger")
                    form.email.errors = list(form.email.errors) + ["Email already registered"]
                    return render_template("signup.html", form=form)

                user = User()
                user.email = form.email.data
                user.set_password(form.password.data)
                user.account_active = True

                # Process user intentions (can select multiple)
                try:
                    user_intentions = request.form.getlist('user_intention[]')
                    if not user_intentions:
                        user_intentions = ['find_events']  # Default

                    if 'create_events' in user_intentions:
                        user.is_event_creator = True
                    if 'represent_organization' in user_intentions:
                        user.is_organizer = True
                        user.is_event_creator = True  # Organizers can also create events
                except Exception as e:
                    logger.warning(f"Error processing user intentions: {str(e)}")
                    # Fallback to form fields if available
                    if hasattr(form, 'is_event_creator') and form.is_event_creator.data:
                        user.is_event_creator = True
                    if hasattr(form, 'is_organizer') and form.is_organizer.data:
                        user.is_organizer = True
                        user.is_event_creator = True  # Organizers can also create events
                    if hasattr(form, 'is_vendor') and form.is_vendor.data:
                        user.is_vendor = True
                        if hasattr(form, 'vendor_type') and form.vendor_type.data:
                            user.vendor_type = form.vendor_type.data

                # Store user preferences from registration
                profile_data = {}
                if hasattr(form, 'event_focus') and request.form.getlist('event_focus'):
                    event_focus = request.form.getlist('event_focus')
                    preferences = user.get_preferences()
                    preferences['event_focus'] = event_focus
                    user.set_preferences(preferences)

                if hasattr(form, 'preferred_locations') and form.preferred_locations.data:
                    profile_data['location'] = form.preferred_locations.data

                if hasattr(form, 'event_interests') and form.event_interests.data:
                    profile_data['interests'] = form.event_interests.data

                if profile_data:
                    for key, value in profile_data.items():
                        setattr(user, key, value)


                db.session.add(user)
                db.session.commit()

                # Auto-login the user
                login_user(user)
                session["user_id"] = user.id
                session["login_time"] = datetime.utcnow().isoformat()
                session["last_activity"] = datetime.utcnow().isoformat()

                # Verify terms acceptance
                if not form.terms_accepted.data:
                    flash("You must accept the Terms and Conditions and Privacy Policy to register.", "danger")
                    return render_template("signup.html", form=form)

                # Set welcome message and indicate this is a new registration
                flash("Welcome to FunList.ai! Let's set up your profile.", "success")

                # Set session flag for new registration to trigger wizard
                session['new_registration'] = True

                # Redirect to index which will show the wizard
                return redirect(url_for("index"))
            except IntegrityError as e:
                db.session.rollback()
                logger.error(f"Database integrity error during sign up: {str(e)}")
                error_msg = str(e).lower()

                if "email" in error_msg and "unique constraint" in error_msg:
                    flash(
                        "This email address is already registered. Please use a different email or try logging in.",
                        "danger",
                    )
                    form.email.errors = list(form.email.errors) + [
                        "Email already registered"
                    ]
                else:
                    flash(
                        "There was a problem with your sign up. Please verify your information and try again.",
                        "danger",
                    )
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Database error during sign up: {str(e)}")
                flash(
                    "We encountered a technical issue. Please try again later.",
                    "danger",
                )
            except Exception as e:
                db.session.rollback()
                logger.error(f"Unexpected error during sign up: {str(e)}")
                flash(
                    "An unexpected error occurred. Please try again. If the problem persists, contact support.",
                    "danger",
                )
        return render_template("signup.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        form = LoginForm()
        if form.validate_on_submit():
            try:
                email = form.email.data
                logger.info(f"Attempting login for: {email}")

                user = User.query.filter_by(email=email).first()

                if user and user.check_password(form.password.data):
                    if form.remember_me.data:
                        session.permanent = True
                    session["user_id"] = user.id
                    session["login_time"] = datetime.utcnow().isoformat()
                    session["last_activity"] = datetime.utcnow().isoformat()

                    login_user(user, remember=form.remember_me.data)
                    user.last_login = datetime.utcnow()
                    db.session.commit()

                    logger.info(f"Login successful for user: {user.id}")
                    flash("Logged in successfully!", "success")
                    next_page = request.args.get("next")
                    return redirect(next_page or url_for("index"))
                else:
                    logger.warning(f"Failed login attempt for email: {email}")
                    flash("Invalid email or password. Please try again.", "danger")
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Database error during login: {str(e)}", exc_info=True)
                flash(
                    "We encountered a technical issue. Please try again later.",
                    "danger",
                )
            except Exception as e:
                logger.error(f"Unexpected error during login: {str(e)}", exc_info=True)
                flash("An unexpected error occurred. Please try again.", "danger")
        return render_template("login.html", form=form)

    @app.route("/logout")
    @login_required
    def logout():
        session.clear()
        logout_user()
        flash("You have been logged out successfully.", "info")
        return redirect(url_for("index"))

    @app.route("/profile", methods=["GET"])
    @login_required
    def profile():
        return render_template("profile.html", user=current_user)

    @app.route("/profile/edit", methods=["GET", "POST"])
    @login_required
    def edit_profile():
        form = ProfileForm()
        form.user_id = current_user.id

        if request.method == "GET":
            # Personal Information
            form.first_name.data = current_user.first_name
            form.last_name.data = current_user.last_name
            form.title.data = current_user.title
            
            # Social Media Links (if these fields exist in the User model)
            if hasattr(current_user, 'facebook_url'):
                form.facebook_url.data = current_user.facebook_url
            if hasattr(current_user, 'instagram_url'):
                form.instagram_url.data = current_user.instagram_url
            if hasattr(current_user, 'twitter_url'):
                form.twitter_url.data = current_user.twitter_url
            if hasattr(current_user, 'linkedin_url'):
                form.linkedin_url.data = current_user.linkedin_url
            if hasattr(current_user, 'tiktok_url'):
                form.tiktok_url.data = current_user.tiktok_url
            
            # Organizer Information (if user is an organizer)
            if current_user.is_organizer:
                form.company_name.data = current_user.company_name
                form.organizer_description.data = current_user.organizer_description
                form.organizer_website.data = current_user.organizer_website
                # Fill additional organizer fields if they exist in the database
                # organizer_title removed, now using title field in personal info
                # Handle the split business location fields
                if hasattr(current_user, 'business_street'):
                    form.business_street.data = current_user.business_street
                if hasattr(current_user, 'business_city'):
                    form.business_city.data = current_user.business_city
                if hasattr(current_user, 'business_state'):
                    form.business_state.data = current_user.business_state
                if hasattr(current_user, 'business_zip'):
                    form.business_zip.data = current_user.business_zip
                if hasattr(current_user, 'business_phone'):
                    form.business_phone.data = current_user.business_phone
                if hasattr(current_user, 'business_email'):
                    form.business_email.data = current_user.business_email
                
        if form.validate_on_submit():
            try:
                # Personal profile data
                profile_data = {
                    "first_name": form.first_name.data,
                    "last_name": form.last_name.data,
                    "title": form.title.data,
                }
                
                # Handle social media fields if they exist in the User model
                if hasattr(current_user, 'facebook_url'):
                    profile_data["facebook_url"] = form.facebook_url.data
                if hasattr(current_user, 'instagram_url'):
                    profile_data["instagram_url"] = form.instagram_url.data
                if hasattr(current_user, 'twitter_url'):
                    profile_data["twitter_url"] = form.twitter_url.data
                if hasattr(current_user, 'linkedin_url'):
                    profile_data["linkedin_url"] = form.linkedin_url.data
                if hasattr(current_user, 'tiktok_url'):
                    profile_data["tiktok_url"] = form.tiktok_url.data

                # Update profile with basic information
                current_user.update_profile(profile_data)
                
                # If user is an organizer, also update organizer information
                if current_user.is_organizer:
                    organizer_data = {
                        "company_name": form.company_name.data,
                        "organizer_description": form.organizer_description.data,
                        "organizer_website": form.organizer_website.data,
                    }
                    
                    # organizer_title removed, now using title field in personal info
                    if hasattr(form, 'business_street') and form.business_street.data:
                        organizer_data["business_street"] = form.business_street.data
                    if hasattr(form, 'business_city') and form.business_city.data:
                        organizer_data["business_city"] = form.business_city.data
                    if hasattr(form, 'business_state') and form.business_state.data:
                        organizer_data["business_state"] = form.business_state.data
                    if hasattr(form, 'business_zip') and form.business_zip.data:
                        organizer_data["business_zip"] = form.business_zip.data
                    if hasattr(form, 'business_phone') and form.business_phone.data:
                        organizer_data["business_phone"] = form.business_phone.data
                    if hasattr(form, 'business_email') and form.business_email.data:
                        organizer_data["business_email"] = form.business_email.data
                    
                    current_user.update_organizer_profile(organizer_data)
                
                db.session.commit()
                flash("Profile updated successfully!", "success")
                return redirect(url_for("profile"))
            except IntegrityError as e:
                db.session.rollback()
                logger.error(
                    f"Database integrity error during profile update: {str(e)}"
                )
                flash(
                    "There was a problem updating your profile. Please try again.",
                    "danger",
                )
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Database error during profile update: {str(e)}")
                flash(
                    "We encountered a technical issue. Please try again later.",
                    "danger",
                )
            except Exception as e:
                db.session.rollback()
                logger.error(f"Unexpected error during profile update: {str(e)}")
                flash("An unexpected error occurred. Please try again.", "danger")
        return render_template("edit_profile.html", form=form)

    @app.route("/events")
    def events():
        try:
            category = request.args.get("category")
            date_range = request.args.get("date_range")
            specific_date = request.args.get("specific_date")
            location = request.args.get("search_location")
            fun_rating = request.args.get("fun_rating")

            query = Event.query

            if category:
                query = query.filter(Event.category == category)
            if location:
                query = query.filter(Event.location.ilike(f"%{location}%"))
            if fun_rating:
                query = query.filter(Event.fun_meter >= int(fun_rating))
            today = datetime.now().date()
            if date_range:
                if date_range == "today":
                    query = query.filter(db.func.date(Event.start_date) == today)
                elif date_range == "tomorrow":
                    query = query.filter(
                        db.func.date(Event.start_date) == today + timedelta(days=1)
                    )
                elif date_range == "weekend":
                    saturday = today + timedelta(days=(5 - today.weekday()))
                    sunday = saturday + timedelta(days=1)
                    query = query.filter(
                        db.func.date(Event.start_date).between(saturday, sunday)
                    )
                elif date_range == "week":
                    week_end = today + timedelta(days=7)
                    query = query.filter(
                        db.func.date(Event.start_date).between(today, week_end)
                    )
                elif date_range == "specific" and specific_date:
                    query = query.filter(db.func.date(Event.start_date) == specific_date)
            events = query.order_by(Event.start_date).all()
            return render_template("events.html", events=events)
        except Exception as e:
            app.logger.error(f"Error in events route: {str(e)}")
            return render_template("events.html", events=[], error_message="Could not load events. Please try again later.")

    @app.route("/map")
    def map():
        try:
            # Get only approved events that have lat/long coordinates
            events = Event.query.filter(
                Event.status == 'approved',
                Event.latitude.isnot(None),
                Event.longitude.isnot(None)
            ).all()

            # Log the number of events found for debugging
            app.logger.info(f"Map page loaded with {len(events)} events")
            return render_template("map.html", events=events)
        except Exception as e:
            app.logger.error(f"Error in map route: {str(e)}")
            return render_template("map.html", events=[], error_message="Could not load events for the map. Please try again later.")

    @app.route("/event/<int:event_id>")
    def event_detail(event_id):
        event = Event.query.get_or_404(event_id)
        return render_template("event_detail.html", event=event)

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("404.html"), 404

    @app.route("/submit-event", methods=["GET", "POST"])
    @login_required
    def submit_event():
        # Verify user has proper permissions
        if not (current_user.is_event_creator or current_user.is_admin):
            return render_template("event_creator_required.html")

        form = EventForm()

        # Populate parent event choices
        user_events = Event.query.filter_by(user_id=current_user.id, parent_event_id=None).all()
        form.parent_event.choices = [(str(e.id), e.title) for e in user_events]

        if request.method == "POST":
            if form.validate_on_submit():
                event = Event()
                event.title = form.title.data
                event.description = form.description.data
                event.start_date = form.start_date.data
                event.end_date = form.end_date.data
                event.all_day = form.all_day.data

                if not event.all_day:
                    event.start_time = form.start_time.data.strftime('%H:%M:%S') if form.start_time.data else None
                    event.end_time = form.end_time.data.strftime('%H:%M:%S') if form.end_time.data else None

                if form.is_sub_event.data and form.parent_event.data:
                    event.parent_event_id = int(form.parent_event.data)

                if form.is_recurring.data:
                    event.is_recurring = True
                    event.recurring_pattern = form.recurring_pattern.data
                    event.recurring_end_date = form.recurring_end_date.data
            try:
                if form.validate_on_submit():
                    is_draft = request.form.get("is_draft", "false") == "true"
                    coordinates = geocode_address(
                        form.street.data,
                        form.city.data,
                        form.state.data,
                        form.zip_code.data,
                    )

                    if not coordinates:
                        flash(
                            "Could not geocode address. Please verify the address is correct.",
                            "danger",
                        )
                        return render_template("submit_event.html", form=form)
                    event = Event(
                        title=form.title.data,
                        description=form.description.data,
                        status="draft" if is_draft else "pending",
                        start_date=form.date.data,
                        end_date=form.date.data,
                        street=form.street.data,
                        city=form.city.data,
                        state=form.state.data,
                        zip_code=form.zip_code.data,
                        latitude=coordinates[0],
                        longitude=coordinates[1],
                        category=form.category.data,
                        target_audience=form.target_audience.data,
                        fun_meter=form.fun_meter.data,
                        user_id=current_user.id,
                        ticket_url=form.ticket_url.data
                    )
                    
                    # Add network_opt_out if the form has it and the column exists
                    if hasattr(form, 'network_opt_out'):
                        try:
                            # Check if the column exists in the database
                            inspector = inspect(db.engine)
                            columns = [column['name'] for column in inspector.get_columns('events')]
                            
                            if 'network_opt_out' in columns:
                                event.network_opt_out = form.network_opt_out.data
                            else:
                                logger.warning("network_opt_out column does not exist in the database")
                        except Exception as e:
                            logger.warning(f"Could not set network_opt_out: {str(e)}")

                    # Handle prohibited advertisers
                    if form.prohibited_advertisers.data:
                        for category_id in form.prohibited_advertisers.data:
                            category = ProhibitedAdvertiserCategory.query.get(category_id)
                            if category:
                                event.prohibited_advertisers.append(category)
                    db.session.add(event)
                    db.session.commit()
                    flash("Event created successfully!", "success")
                    return redirect(url_for("events"))
                else:
                    flash(
                        "Form submission failed. Please check your inputs.", "danger"
                    )  # Added flash message for form validation errors
                    return render_template("submit_event.html", form=form)
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.exception(
                    f"Database error during event submission: {str(e)}"
                )  # Improved logging
                flash("A database error occurred. Please try again later.", "danger")
                return render_template("submit_event.html", form=form)
            except Exception as e:
                db.session.rollback()
                logger.exception(
                    f"Unexpected error during event submission: {str(e)}"
                )  # Improved logging
                flash("An unexpected error occurred. Please try again later.", "danger")
                return render_template("submit_event.html", form=form)
        return render_template("submit_event.html", form=form)

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("500.html"), 500

    @app.route("/admin/login", methods=["GET", "POST"])
    @app.route("/admin_login", methods=["GET", "POST"])  # Add alternative URL route
    def admin_login():
        if current_user.is_authenticated and current_user.email == 'ryan@funlist.ai':
            return redirect(url_for("admin_dashboard"))
        form = LoginForm()
        if form.validate_on_submit():
            try:
                email = form.email.data
                password = form.password.data
                logger.info(f"Admin login attempt: {email}")

                # Only ryan@funlist.ai should have admin access
                admin_email = 'ryan@funlist.ai'

                # Standard login check
                try:
                    user = User.query.filter_by(email=email).first()
                    if user and user.check_password(password) and user.email == admin_email:
                        # Ensure admin privileges for the correct admin
                        user.is_admin = True
                        db.session.commit()

                        # Login the user
                        login_user(user)
                        session["user_id"] = user.id
                        session["login_time"] = datetime.utcnow().isoformat()
                        session["last_activity"] = datetime.utcnow().isoformat()

                        logger.info(f"Admin login successful: {admin_email}")
                        return redirect(url_for("admin_dashboard"))
                    else:
                        flash("Invalid credentials or insufficient privileges.", "danger")
                except Exception as e:
                    logger.error(f"Standard login check failed: {str(e)}")
                    flash("Login check failed. Database may need maintenance.", "danger")

            except Exception as e:
                logger.error(f"Unexpected error in admin login: {str(e)}", exc_info=True)
                flash("We encountered a technical issue. Please try again later.", "danger")

        return render_template("admin_login.html", form=form)

    @app.route("/admin/events")
    @login_required
    def admin_events():
        if current_user.email != 'ryan@funlist.ai':
            flash("Access denied. Only authorized administrators can access this page.", "danger")
            return redirect(url_for("index"))
        events = Event.query.order_by(Event.created_at.desc()).all()
        return render_template("admin_events.html", events=events)

    @app.route("/admin/events/<int:event_id>/edit", methods=['GET', 'POST'])
    @login_required
    def admin_edit_event(event_id):
        if current_user.email != 'ryan@funlist.ai':
            flash("Access denied. Admin privileges required.", "danger")
            return redirect(url_for("index"))
        event = Event.query.get_or_404(event_id)

        if request.method == 'POST':
            # Update event details from form
            event.title = request.form.get('title')
            event.description = request.form.get('description')
            event.location = request.form.get('location')
            # address field removed
            event.city = request.form.get('city')
            event.state = request.form.get('state')
            event.zip_code = request.form.get('zip_code')
            event.start_time = datetime.strptime(request.form.get('start_time'), '%Y-%m-%dT%H:%M')
            event.end_time = datetime.strptime(request.form.get('end_time'), '%Y-%m-%dT%H:%M')
            event.website = request.form.get('website')
            event.organizer_name = request.form.get('organizer_name')
            event.organizer_email = request.form.get('organizer_email')
            event.organizer_phone = request.form.get('organizer_phone')
            event.category = request.form.get('category')
            event.tags = request.form.get('target_market') # Store target market in tags field
            event.featured = True if request.form.get('is_featured') else False
            event.status = request.form.get('status')

            db.session.commit()
            flash('Event updated successfully', 'success')
            return redirect(url_for('admin_events'))

        return render_template('edit_event.html', event=event, is_admin=True)


    @app.route("/admin/users")
    @login_required
    def admin_users():
        if current_user.email != 'ryan@funlist.ai':
            flash("Access denied. Only authorized administrators can access this page.", "danger")
            return redirect(url_for("index"))
        users = User.query.order_by(User.created_at.desc()).all()
        return render_template("admin_users.html", users=users)

    @app.route("/api/featured-events")
    def featured_events_api():
        # Feature is now enabled
        FEATURED_EVENTS_ENABLED = True
        if not FEATURED_EVENTS_ENABLED:
            return jsonify({"success": True, "events": [], "message": "Feature not yet available"}), 200

        try:
            lat = request.args.get("lat")
            lng = request.args.get("lng")

            if not lat or not lng:
                return jsonify({"success": True, "events": [], "message": "No coordinates provided"}), 200

            try:
                lat = float(lat)
                lng = float(lng)
            except (ValueError, TypeError):
                return jsonify({"success": False, "error": "Invalid coordinates"}), 400

            try:
                lat = float(lat)
                lng = float(lng)
            except (TypeError, ValueError):
                return jsonify({"success": True, "events": []}), 200

            events = Event.query.filter(
                Event.latitude.isnot(None),
                Event.longitude.isnot(None),
                Event.fun_meter >= 4,
                Event.status == "approved",
            ).all()

            featured = []
            for event in events:
                try:
                    # Convert to miles (1 degree ≈ 69 miles)
                    distance = (
                        (float(event.latitude) - float(lat)) ** 2 +
                        (float(event.longitude) - float(lng)) ** 2
                    ) ** 0.5 * 69

                    if distance <= 15:  # 15 miles radius
                        featured.append({
                            "id": event.id,
                            "title": event.title,
                            "description": event.description[:100] + "..." if len(event.description) > 100 else event.description,
                            "date": event.start_date.strftime("%Y-%m-%d"),
                            "fun_meter": event.fun_meter,
                            "distance": round(distance, 1)
                        })
                except (TypeError, ValueError) as e:
                    logger.error(f"Error calculating distance for event {event.id}: {str(e)}")
                    continue

            if not featured:
                return jsonify({
                    "success": True,
                    "events": []
                })
            return jsonify({
                "success": True,
                "events": sorted(featured, key=lambda x: (-x["fun_meter"], x["date"]))[:5]
            })
        except Exception as e:
            logger.error(f"Featured events API error: {str(e)}")
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/advertising")
    def advertising():
        return render_template("advertising.html")

    @app.route("/privacy")
    def privacy():
        return render_template('privacy.html')

    @app.route("/terms")
    def terms():
        return render_template("terms.html")

    @app.route("/help")
    def help_center():
        return render_template("help_center.html")

    @app.route("/reset-password-request", methods=["GET", "POST"])
    def reset_password_request():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        form = ResetPasswordRequestForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                token = user.get_reset_token()
                # In a real production environment, you'd send an email with a reset link
                # For development, we'll just redirect to the reset page with the token
                flash(f'Password reset link has been sent to {form.email.data}. Please check your email.', 'info')

                # For demo purposes, we'll provide a direct link as well
                reset_url = url_for('reset_password', token=token, _external=True)
                flash(f'For demo purposes, you can also <a href="{reset_url}">click here</a> to reset your password.', 'info')

                return redirect(url_for('login'))
            else:
                # Don't reveal that the user doesn't exist
                flash('If an account with this email exists, a password reset link has been sent.', 'info')
                return redirect(url_for('login'))
        return render_template('reset_password_request.html', form=form)

    @app.route("/reset-password/<token>", methods=["GET", "POST"])
    def reset_password(token):
        if current_user.is_authenticated:
            return redirect(url_for("index"))

        user = User.verify_reset_token(token)
        if not user:
            flash('Invalid or expired reset token. Please try again.', 'danger')
            return redirect(url_for('reset_password_request'))

        form = ResetPasswordForm()
        if form.validate_on_submit():
            user.set_password(form.password.data)
            user.clear_reset_token()
            db.session.commit()
            flash('Your password has been reset successfully. You can now log in with your new password.', 'success')
            return redirect(url_for('login'))

        return render_template('reset_password.html', form=form, token=token)
        
    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            try:
                # Log the contact submission
                app.logger.info(f"Contact form submission from {form.name.data} ({form.email.data}): {form.subject.data} - Category: {form.category.data}")
                
                # Here you would typically save the contact form to database or send email
                # For now, we'll just show a success message
                flash("Thank you for your message! We'll respond to you shortly.", "success")
                return redirect(url_for('contact'))
            except Exception as e:
                app.logger.error(f"Error processing contact form: {str(e)}")
                flash("Sorry, we encountered an error processing your request. Please try again later.", "danger")
        
        return render_template("contact.html", form=form)

    @app.route("/admin/analytics")
    @login_required
    def admin_analytics():
        if current_user.email != 'ryan@funlist.ai':
            flash("Access denied. Only authorized administrators can access this page.", "danger")
            return redirect(url_for("index"))
        # Get events by category data

        events_by_category = {
            "labels": ["Sports", "Music", "Arts", "Food", "Other"],
            "datasets": [
                {
                    "data": [
                        Event.query.filter_by(category="Sports").count(),
                        Event.query.filter_by(category="Music").count(),
                        Event.query.filter_by(category="Arts").count(),
                        Event.query.filter_by(category="Food").count(),
                        Event.query.filter_by(category="Other").count(),
                    ]
                }
            ],
        }

        # Get user growth data (last 7 days)

        from datetime import datetime, timedelta

        user_growth_data = {
            "labels": [
                (datetime.now() - timedelta(days=x)).strftime("%Y-%m-%d")
                for x in range(7)
            ],
            "datasets": [
                {
                    "label": "New Users",
                    "data": [
                        User.query.filter(
                            User.created_at
                            >= datetime.now().date() - timedelta(days=x),
                            User.created_at
                            < datetime.now().date() - timedelta(days=x - 1),
                        ).count()
                        for x in range(7)
                    ],
                }
            ],
        }

        return render_template(
            "admin_analytics.html",
            events_by_category=events_by_category,
            user_growth_data=user_growth_data,
        )

    @app.route("/admin/event/<int:event_id>/<action>", methods=["POST"])
    @login_required
    def admin_event_action(event_id, action):
        if current_user.email != 'ryan@funlist.ai':
            return jsonify({"success": False, "message": "Unauthorized. Only administrators can perform this action."}), 403

        # Exempt this route from CSRF protection for API calls
        try:
            event = Event.query.get_or_404(event_id)

            if action == "approve":
                event.status= "approved"
                message = f"Event '{event.title}' has been approved"
            elif action == "reject":
                event.status = "rejected"
                message = f"Event '{event.title}' has been rejected"
            elif action == "delete":
                title = event.title
                db.session.delete(event)
                message = f"Event '{title}' has been deleted"
            else:
                return jsonify({"success": False, "message": "Invalid action"}), 400

            db.session.commit()
            return jsonify({"success": True, "message": message})
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in admin_event_action: {str(e)}")
            return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

    @app.route("/admin/event/<int:event_id>/toggle-feature", methods=["POST"])
    @login_required
    def toggle_event_feature(event_id):
        if current_user.email != 'ryan@funlist.ai':
            return jsonify({"success": False, "message": "Unauthorized. Only administrators can perform this action."}), 403

        try:
            data = request.get_json()
            featured = data.get('featured', False)

            event = Event.query.get_or_404(event_id)
            event.featured = featured

            action = "featured" if featured else "unfeatured"
            message = f"Event '{event.title}' has been {action}"

            db.session.commit()
            return jsonify({"success": True, "message": message})
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in toggle_event_feature: {str(e)}")
            return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

    @app.route("/admin/event/<int:event_id>/delete", methods=["POST"])
    @login_required
    def admin_delete_event(event_id):
        if current_user.email != 'ryan@funlist.ai':
            return jsonify({"success": False, "message": "Unauthorized. Only administrators can perform this action."}), 403

        try:
            event = Event.query.get_or_404(event_id)
            title = event.title
            db.session.delete(event)
            db.session.commit()
            return jsonify({"success": True, "message": f"Event '{title}' has been deleted"})
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in admin_delete_event: {str(e)}")
            return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

    @app.route("/become-organizer")
    @login_required
    def become_organizer():
        # Redirect user to the organizer profile page to set up their organizer account
        return redirect(url_for("organizer_profile"))

    @app.route("/organizer-profile", methods=["GET", "POST"])
    @login_required
    def organizer_profile():
        # Redirect to the consolidated profile editing page
        flash("Your organizer profile can now be managed from your main profile page.", "info")
        return redirect(url_for("edit_profile"))
        
    @app.route("/change-password", methods=["GET", "POST"])
    @login_required
    def change_password():
        from forms import ResetPasswordForm
        form = ResetPasswordForm()
        if form.validate_on_submit():
            current_user.set_password(form.password.data)
            db.session.commit()
            flash("Your password has been updated successfully!", "success")
            return redirect(url_for("profile"))
        return render_template("change_password.html", form=form)

    @app.route("/venues", methods=["GET"])
    def venues():
        venues = Venue.query.order_by(Venue.name).all()
        return render_template("venues.html", venues=venues)
        
    @app.route("/venues/<int:venue_id>", methods=["GET"])
    def venue_detail(venue_id):
        venue = Venue.query.get_or_404(venue_id)
        events = Event.query.filter_by(venue_id=venue.id).all()
        return render_template("venue_detail.html", venue=venue, events=events)
    
    @app.route("/venues/add", methods=["GET", "POST"])
    @login_required
    def add_venue():
        form = VenueForm()
        
        if form.validate_on_submit():
            try:
                venue = Venue(
                    name=form.name.data,
                    street=form.street.data,
                    city=form.city.data,
                    state=form.state.data,
                    zip_code=form.zip_code.data,
                    country=form.country.data,
                    phone=form.phone.data,
                    email=form.email.data,
                    website=form.website.data,
                    venue_type_id=form.venue_type_id.data,
                    contact_name=form.contact_name.data,
                    contact_phone=form.contact_phone.data,
                    contact_email=form.contact_email.data,
                    user_id=current_user.id
                )
                db.session.add(venue)
                db.session.commit()
                flash("Venue added successfully!", "success")
                return redirect(url_for("venues"))
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error adding venue: {str(e)}")
                flash("There was a problem adding the venue. Please try again.", "danger")
        
        return render_template("add_venue.html", form=form)
    
    @app.route("/venues/<int:venue_id>/edit", methods=["GET", "POST"])
    @login_required
    def edit_venue(venue_id):
        venue = Venue.query.get_or_404(venue_id)
        
        # Check if user is authorized to edit this venue
        if venue.user_id != current_user.id and not current_user.is_admin:
            flash("You are not authorized to edit this venue.", "danger")
            return redirect(url_for("venues"))
        
        form = VenueForm(obj=venue)
        
        if form.validate_on_submit():
            try:
                form.populate_obj(venue)
                venue.updated_at = datetime.utcnow()
                db.session.commit()
                flash("Venue updated successfully!", "success")
                return redirect(url_for("venue_detail", venue_id=venue.id))
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error updating venue: {str(e)}")
                flash("There was a problem updating the venue. Please try again.", "danger")
        
        return render_template("edit_venue.html", form=form, venue=venue)
    
    @app.route("/venues/<int:venue_id>/delete", methods=["POST"])
    @login_required
    def delete_venue(venue_id):
        venue = Venue.query.get_or_404(venue_id)
        
        # Check if user is authorized to delete this venue
        if venue.user_id != current_user.id and not current_user.is_admin:
            flash("You are not authorized to delete this venue.", "danger")
            return redirect(url_for("venues"))
        
        try:
            # Check if venue is used in any events
            events_count = Event.query.filter_by(venue_id=venue.id).count()
            if events_count > 0:
                flash(f"Cannot delete venue because it is associated with {events_count} events.", "danger")
                return redirect(url_for("venue_detail", venue_id=venue.id))
            
            name = venue.name
            db.session.delete(venue)
            db.session.commit()
            flash(f"Venue '{name}' deleted successfully!", "success")
            return redirect(url_for("venues"))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting venue: {str(e)}")
            flash("There was a problem deleting the venue. Please try again.", "danger")
            return redirect(url_for("venue_detail", venue_id=venue.id))
            
    @app.route("/my-venues")
    @login_required
    def my_venues():
        venues = Venue.query.filter_by(user_id=current_user.id).all()
        return render_template("my_venues.html", venues=venues)

    @app.route("/vendor-profile", methods=["GET", "POST"])
    @login_required
    def vendor_profile():
        # Import the form
        from forms import VendorProfileForm

        form = VendorProfileForm()

        if request.method == "GET":
            # Pre-populate form with existing data if available
            form.vendor_type.data = current_user.vendor_type
            form.description.data = current_user.vendor_description
            form.website.data = current_user.organizer_website  # Reuse the organizer_website field

        if form.validate_on_submit():
            try:
                current_user.is_vendor = True
                current_user.vendor_type = form.vendor_type.data
                current_user.vendor_description = form.description.data
                current_user.organizer_website = form.website.data  # Reuse the organizer_website field
                current_user.vendor_profile_updated_at = datetime.utcnow()

                db.session.commit()
                flash("Vendor profile updated successfully!", "success")
                return redirect(url_for("profile"))
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error updating vendor profile: {str(e)}")
                flash("There was a problem updating your vendor profile. Please try again.", "danger")

        return render_template("vendor_profile.html", form=form)

    @app.route("/organizers")
    def organizers():
        # Get all users who are organizers
        organizers = User.query.filter_by(is_organizer=True).all()
        return render_template("organizers.html", organizers=organizers)

    @app.route("/organizer/<int:user_id>")
    def organizer_detail(user_id):
        organizer = User.query.get_or_404(user_id)
        if not organizer.is_organizer:
            flash("This user is not registered as an event organizer.", "warning")
            return redirect(url_for("organizers"))

        # Get events by this organizer
        events = Event.query.filter_by(user_id=organizer.id).order_by(Event.start_date.desc()).all()
        return render_template("organizer_detail.html", organizer=organizer, events=events)

    @app.route("/admin/dashboard")
    @login_required
    def admin_dashboard():
        if current_user.email != 'ryan@funlist.ai':
            flash("Access denied. Only authorized administrators can access this page.", "danger")
            return redirect(url_for("index"))

        active_tab = request.args.get('tab', 'overview')
        status = request.args.get('status', 'pending')

        # Prepare default statistics
        stats = {
            'total_users': User.query.count(),
            'pending_events': Event.query.filter_by(status='pending').count(),
            'todays_events': Event.query.filter(
                Event.start_date >= datetime.now().replace(hour=0, minute=0, second=0),
                Event.start_date < (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0)
            ).count(),
            'new_users_24h': User.query.filter(
                User.created_at >= (datetime.now() - timedelta(days=1))
            ).count(),
            'featured_events': Event.query.filter_by(featured=True).count()
        }

        events = []
        users = []

        if active_tab == 'events':
            # For the Events tab, include the status filter
            query = Event.query
            if status != 'all':
                query = query.filter_by(status=status)
            events = query.all()
        elif active_tab == 'featured_events':
            # For the Featured Events tab, only show featured events
            events = Event.query.filter_by(featured=True).all()
        elif active_tab == 'users':
            users = User.query.all()
        elif active_tab == 'analytics':
            # Analytics data
            categories = Event.query.with_entities(Event.category, func.count(Event.id).label('count')).group_by(Event.category).all()
            events_by_category = {
                'labels': [c[0] or 'Uncategorized' for c in categories],
                'datasets': [{
                    'label': 'Events by Category',
                    'data': [c[1] for c in categories],
                    'backgroundColor': [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#8AC054'
                    ]
                }]
            }

            # User growth data (monthly for the past year)
            months = 12
            now = datetime.now()
            user_growth_data = {
                'labels': [],
                'datasets': [{
                    'label': 'New Users',
                    'data': [],
                    'fill': False,
                    'borderColor': '#36A2EB',
                    'tension': 0.1
                }]
            }

            for i in range(months-1, -1, -1):
                start_date = (now - relativedelta(months=i)).replace(day=1, hour=0, minute=0, second=0)
                end_date = (start_date + relativedelta(months=1))

                user_count = User.query.filter(
                    User.created_at >= start_date,
                    User.created_at < end_date
                ).count()

                month_name = start_date.strftime('%b %Y')
                user_growth_data['labels'].append(month_name)
                user_growth_data['datasets'][0]['data'].append(user_count)

            return render_template(
                'admin_dashboard.html', 
                active_tab=active_tab,
                stats=stats,
                events_by_category=events_by_category,
                user_growth_data=user_growth_data
            )

        return render_template(
            'admin_dashboard.html', 
            active_tab=active_tab,
            status=status,
            stats=stats,
            events=events,
            users=users
        )

    @app.route("/admin/user/<int:user_id>/deactivate")
    @login_required
    def admin_deactivate_user(user_id):
        if current_user.email != 'ryan@funlist.ai':
            return jsonify({"error": "Unauthorized. Only administrators can perform this action."}), 403
        user = User.query.get_or_404(user_id)
        user.account_active = False
        db.session.commit()
        flash("User account deactivated.", "success")  # Fixed
        return redirect(url_for("admin_dashboard", tab="users"))

    @app.route("/admin/user/<int:user_id>/activate")
    @login_required
    def admin_activate_user(user_id):
        if current_user.email != 'ryan@funlist.ai':
            return jsonify({"error": "Unauthorized. Only administrators can perform this action."}), 403
        user = User.query.get_or_404(user_id)
        user.account_active = True
        db.session.commit()
        flash("User account activated.", "success")
        return redirect(url_for("admin_dashboard", tab="users"))
    @app.route('/advertiser-exclusion-info')
    def advertiser_exclusion_info():
        return render_template('advertiser_exclusion_info.html')