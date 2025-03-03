from flask import render_template, flash, redirect, url_for, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from forms import SignupForm, LoginForm, ProfileForm, EventForm, ResetPasswordRequestForm, ResetPasswordForm, OrganizerProfileForm, VendorProfileForm, VenueProfileForm
from models import User, Event, Subscriber
from db_init import db
from utils import geocode_address, send_password_reset_email
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def init_routes(app):
    # Add CSP report endpoint
    @app.route('/csp-report', methods=['POST'])
    def csp_report():
        try:
            report = request.get_json(force=True).get('csp-report', {})
            app.logger.warning(f"CSP Violation: {report}")
            return '', 204
        except Exception as e:
            app.logger.error(f"Error handling CSP report: {str(e)}")
            return '', 400
    
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
            
            # Simplified session tracking that avoids encoding issues
            if "last_activity" not in session:
                session["last_activity"] = current_time.isoformat()
                return
                
            # Only check for timeout if we're not on static resources
            if not request.path.startswith('/static/'):
                try:
                    # Use a simpler approach to time tracking
                    session["last_activity"] = current_time.isoformat()
                except Exception as e:
                    app.logger.error(f"Session error: {str(e)}")
                    # Don't interrupt the user experience if session tracking fails

    @app.route("/")
    def index():
        events = Event.query.order_by(Event.start_date.desc()).all()
        # Check if this is a new registration to show the wizard
        new_registration = session.pop('new_registration', False)
        return render_template("index.html", events=events, user=current_user, new_registration=new_registration)

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

                # Set default role as subscriber
                user.is_subscriber = True
                
                # Process user intention from the form
                user_intention = form.user_intention.data
                
                # Set user roles based on intention
                if user_intention == 'find_events':
                    # Default role is already subscriber
                    pass
                elif user_intention == 'create_events':
                    user.is_event_creator = True
                elif user_intention == 'represent_organization':
                    user.is_organizer = True
                    user.is_event_creator = True  # Organizers can also create events
                elif user_intention == 'vendor_services':
                    user.is_vendor = True
                
                # Store profile information if provided
                # Convert the multiselect audience_type to a comma-separated string
                if form.audience_type.data:
                    user.audience_type = ','.join(form.audience_type.data)
                
                if form.preferred_locations.data:
                    user.preferred_locations = form.preferred_locations.data
                    
                if form.event_interests.data:
                    user.event_interests = form.event_interests.data

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
                    "We encountered a technical issue. Our team has been notified. Please try again later.",
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
                # Use a simpler query to avoid column issues
                email = form.email.data
                logger.info(f"Attempting login for: {email}")

                # Direct query to improve reliability
                user = User.query.filter_by(email=email).first()

                if user:
                    logger.info(f"User found: {user.id}")
                    if user.check_password(form.password.data):
                        if form.remember_me.data:
                            session.permanent = True
                        
                        # Login the user first
                        login_user(user, remember=form.remember_me.data)
                        
                        # Then set session data with simplified strings
                        # Use native Python types that will serialize properly
                        session["user_id"] = user.id
                        session["login_time"] = datetime.utcnow().isoformat()
                        session["last_activity"] = datetime.utcnow().isoformat()

                        # Update last login time
                        user.last_login = datetime.utcnow()
                        db.session.commit()

                        logger.info(f"Login successful for user: {user.id}")
                        flash("Logged in successfully!", "success")
                        next_page = request.args.get("next")
                        return redirect(next_page or url_for("index"))
                    else:
                        logger.warning(f"Failed login attempt - wrong password for email: {email}")
                        flash("Invalid email or password. Please try again.", "danger")
                else:
                    logger.warning(f"Failed login attempt - user not found for email: {email}")
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
            form.username.data = current_user.username
            form.first_name.data = current_user.first_name
            form.last_name.data = current_user.last_name
            form.bio.data = current_user.bio
            form.location.data = current_user.location
            form.interests.data = current_user.interests
            form.birth_date.data = current_user.birth_date
            
            # Handle the new fields
            if current_user.audience_type:
                form.audience_type.data = current_user.audience_type.split(',')
            if current_user.preferred_locations:
                form.preferred_locations.data = current_user.preferred_locations
            if current_user.event_interests:
                form.event_interests.data = current_user.event_interests
                
        if form.validate_on_submit():
            try:
                # Convert audience_type from list to comma-separated string
                audience_type_value = ','.join(form.audience_type.data) if form.audience_type.data else None
                
                profile_data = {
                    "username": form.username.data,
                    "first_name": form.first_name.data,
                    "last_name": form.last_name.data,
                    "bio": form.bio.data,
                    "location": form.location.data,
                    "interests": form.interests.data,
                    "audience_type": audience_type_value,
                    "preferred_locations": form.preferred_locations.data,
                    "event_interests": form.event_interests.data,
                    "birth_date": form.birth_date.data,
                }

                current_user.update_profile(profile_data)
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

    @app.route("/map")
    def map():
        events = Event.query.all()
        return render_template("map.html", events=events)

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
        # Check if user has event creation permissions
        if not (current_user.is_event_creator or current_user.is_organizer or current_user.is_admin):
            # Allow them to request event creation access
            current_user.is_event_creator = True
            db.session.commit()
            flash("You have been granted event creation permissions.", "success")

        form = EventForm()
        if request.method == "POST":
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
                        target_audience_description=form.target_audience_description.data,
                        fun_meter=form.fun_meter.data,
                        fun_rating_justification=form.fun_rating_justification.data,
                        user_id=current_user.id,
                    )
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
                    # Use a simpler query to avoid column issues
                    user = User.query.filter(User.email == email).first()
                    
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
                except SQLAlchemyError as e:
                    db.session.rollback()
                    logger.error(f"Database error during admin login: {str(e)}", exc_info=True)
                    flash("Login check failed. Running database maintenance...", "warning")
                    
                    # Try to fix the schema on the fly
                    try:
                        from update_schema import update_schema
                        if update_schema():
                            flash("Database maintenance completed. Please try logging in again.", "info")
                        else:
                            flash("Database maintenance failed. Please contact support.", "danger")
                    except Exception as schema_error:
                        logger.error(f"Schema update failed: {str(schema_error)}", exc_info=True)
                        flash("Database maintenance failed. Please contact support.", "danger")
                except Exception as e:
                    logger.error(f"Standard login check failed: {str(e)}", exc_info=True)
                    flash("Login check failed. Please try again later.", "danger")

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
            event.address = request.form.get('address')
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
            event.is_featured = True if request.form.get('is_featured') else False
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
        # Feature flag check
        FEATURED_EVENTS_ENABLED = False
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
                event.status = "approved"
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

    @app.route("/become-organizer")
    @login_required
    def become_organizer():
        # Redirect user to the organizer profile page to set up their organizer account
        return redirect(url_for("organizer_profile"))
        
    @app.route("/become-venue")
    @login_required
    def become_venue():
        # Redirect user to the venue profile page to set up their venue
        return redirect(url_for("venue_profile"))
        
    @app.route("/become-vendor")
    @login_required
    def become_vendor():
        # Redirect user to the vendor profile page to set up their vendor services
        return redirect(url_for("vendor_profile"))

    @app.route("/organizer-profile", methods=["GET", "POST"])
    @login_required
    def organizer_profile():
        # Import the form
        from forms import OrganizerProfileForm

        form = OrganizerProfileForm()

        if request.method == "GET":
            # Pre-populate form with existing data if available            form.company_name.data = current_user.company_name
            form.description.data = current_user.organizer_description
            form.website.data = current_user.organizer_website
            form.advertising_opportunities.data = current_user.advertising_opportunities
            form.sponsorship_opportunities.data = current_user.sponsorship_opportunities

        if form.validate_on_submit():
            try:
                organizer_data = {
                    "company_name": form.company_name.data,
                    "organizer_description": form.description.data,
                    "organizer_website": form.website.data,
                    "advertising_opportunities": form.advertising_opportunities.data,
                    "sponsorship_opportunities": form.sponsorship_opportunities.data,
                }

                current_user.update_organizer_profile(organizer_data)
                db.session.commit()
                flash("Organizer profile updated successfully!", "success")
                return redirect(url_for("profile"))
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error updating organizer profile: {str(e)}")
                flash("There was a problem updating your organizer profile. Please try again.", "danger")

        return render_template("organizer_profile.html", form=form)

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
            
            # For vendors that are also organizers, pre-populate company name
            if current_user.is_organizer and current_user.company_name:
                form.company_name.data = current_user.company_name
            
            if form.services:
                form.services.data = current_user.services
            if form.pricing:
                form.pricing.data = current_user.pricing

        if form.validate_on_submit():
            try:
                # Create a combined profile that respects existing roles
                current_user.is_vendor = True
                current_user.vendor_type = form.vendor_type.data
                current_user.vendor_description = form.description.data
                
                # Always update the website field, shared across roles
                current_user.organizer_website = form.website.data
                
                # Update company name only if provided and not already set from organizer profile
                if form.company_name and form.company_name.data:
                    current_user.company_name = form.company_name.data
                
                # Additional vendor-specific fields
                if hasattr(form, 'services') and form.services.data:
                    current_user.services = form.services.data
                if hasattr(form, 'pricing') and form.pricing.data:
                    current_user.pricing = form.pricing.data
                
                current_user.vendor_profile_updated_at = datetime.utcnow()

                db.session.commit()
                flash("Vendor profile updated successfully!", "success")
                return redirect(url_for("profile"))
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error updating vendor profile: {str(e)}")
                flash("There was a problem updating your vendor profile. Please try again.", "danger")

        # Pass additional context about user's other roles
        multi_role_context = {
            'is_also_organizer': current_user.is_organizer,
            'is_also_venue': current_user.is_venue
        }
        return render_template("vendor_profile.html", form=form, multi_role=multi_role_context)

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
        
    @app.route("/vendors")
    def vendors():
        # Get all users who are vendors
        vendors = User.query.filter_by(is_vendor=True).all()
        return render_template("vendors.html", vendors=vendors)

    @app.route("/vendor/<int:user_id>")
    def vendor_detail(user_id):
        vendor = User.query.get_or_404(user_id)
        if not vendor.is_vendor:
            flash("This user is not registered as an event vendor.", "warning")
            return redirect(url_for("vendors"))

        return render_template("vendor_detail.html", vendor=vendor)
        
    @app.route("/venues")
    def venues():
        # For this implementation, we're treating venues as a subset of organizers
        # who have marked themselves specifically as venues
        venues = User.query.filter_by(is_organizer=True).filter(User.is_venue==True).all()
        return render_template("venues.html", venues=venues)

    @app.route("/venue/<int:user_id>")
    def venue_detail(user_id):
        venue = User.query.get_or_404(user_id)
        if not venue.is_venue:
            flash("This user is not registered as a venue.", "warning")
            return redirect(url_for("venues"))

        # Get events at this venue
        events = Event.query.filter_by(venue_id=venue.id).order_by(Event.start_date.desc()).all()
        return render_template("venue_detail.html", venue=venue, events=events)
        
    @app.route("/venue-profile", methods=["GET", "POST"])
    @login_required
    def venue_profile():
        # Import the form
        form = VenueProfileForm()

        if request.method == "GET":
            # Pre-populate form with existing data if available
            form.company_name.data = current_user.company_name
            form.description.data = current_user.organizer_description
            form.location.data = current_user.location
            form.website.data = current_user.organizer_website
            form.capacity.data = current_user.venue_capacity
            form.features.data = current_user.venue_features
            form.advertising_opportunities.data = current_user.advertising_opportunities
            form.sponsorship_opportunities.data = current_user.sponsorship_opportunities

        if form.validate_on_submit():
            try:
                venue_data = {
                    "company_name": form.company_name.data,
                    "organizer_description": form.description.data,
                    "location": form.location.data,
                    "organizer_website": form.website.data,
                    "venue_capacity": form.capacity.data,
                    "venue_features": form.features.data,
                    "advertising_opportunities": form.advertising_opportunities.data,
                    "sponsorship_opportunities": form.sponsorship_opportunities.data,
                }

                # Mark as venue (but only mark as organizer if not already a vendor)
                current_user.is_venue = True
                
                # If user was previously just a vendor (not an organizer), 
                # this makes them an organizer too. Otherwise, preserve existing organizer status
                if not current_user.is_organizer:
                    current_user.is_organizer = True
                
                # Update the venue profile fields
                current_user.update_organizer_profile(venue_data)
                
                # Set venue-specific update timestamp
                current_user.venue_profile_updated_at = datetime.utcnow()
                
                db.session.commit()
                flash("Venue profile updated successfully!", "success")
                return redirect(url_for("profile"))
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error updating venue profile: {str(e)}")
                flash("There was a problem updating your venue profile. Please try again.", "danger")

        # Pass additional context about user's other roles
        multi_role_context = {
            'is_also_organizer': current_user.is_organizer,
            'is_also_vendor': current_user.is_vendor
        }
        return render_template("venue_profile.html", form=form, multi_role=multi_role_context)

    @app.route("/admin/dashboard")
    @login_required
    def admin_dashboard():
        if current_user.email != 'ryan@funlist.ai':
            flash("Access denied. Only authorized administrators can access this page.", "danger")
            return redirect(url_for("index"))
        tab = request.args.get("tab", "overview")
        status = request.args.get("status", "pending")
        user_type = request.args.get("user_type", "all")

        # Get statistics for overview
        stats = {
            "pending_events": Event.query.filter_by(status="pending").count(),
            "total_users": User.query.count(),
            "todays_events": Event.query.filter(
                Event.start_date >= datetime.now().date(),
                Event.start_date < datetime.now().date() + timedelta(days=1),
            ).count(),
            "new_users_24h": User.query.filter(
                User.created_at >= datetime.now() - timedelta(hours=24)
            ).count(),
        }

        # Get events for event management
        events = Event.query.filter_by(status=status).order_by(Event.start_date).all()

        # Get users for user management with filtering by type
        user_query = User.query
        
        if user_type == 'subscribers':
            user_query = user_query.filter_by(is_subscriber=True)
        elif user_type == 'event_creators':
            user_query = user_query.filter_by(is_event_creator=True)
        elif user_type == 'organizers':
            user_query = user_query.filter_by(is_organizer=True)
        elif user_type == 'vendors':
            user_query = user_query.filter_by(is_vendor=True)
        elif user_type == 'venues':
            user_query = user_query.filter_by(is_venue=True)
        # 'all' doesn't need a filter
        
        users = user_query.order_by(User.created_at.desc()).all()

        # Get analytics data
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

        # User growth data (last 7 days)
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
            "admin_dashboard.html",
            active_tab=tab,
            stats=stats,
            events=events,
            users=users,
            status=status,
            user_type=user_type,
            events_by_category=events_by_category,
            user_growth_data=user_growth_data,
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