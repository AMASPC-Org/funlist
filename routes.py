from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from forms import ProfileForm, EventForm, ContactForm, VenueForm, OrganizerApplicationForm
from models import User, Event, Subscriber, ProhibitedAdvertiserCategory, Organization
from db_init import db
from utils import geocode_address
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from datetime import datetime, timedelta
import json
from dateutil.relativedelta import relativedelta
from sqlalchemy import func, inspect
import secrets
from urllib.parse import urljoin, urlparse
from firebase_service import FirebaseAuthError, verify_firebase_token

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def init_routes(app):
    def _safe_redirect_target(target):
        """Ensure redirect targets stay within this application."""
        if not target:
            return url_for("index")
        ref_url = urlparse(request.host_url)
        test_url = urlparse(urljoin(request.host_url, target))
        if (test_url.scheme in ("http", "https") and
                test_url.netloc == ref_url.netloc):
            redirect_path = test_url.path or "/"
            if test_url.query:
                redirect_path = f"{redirect_path}?{test_url.query}"
            return redirect_path
        return url_for("index")

    def _organizer_status(user):
        organization = getattr(user, "organization", None)
        if organization and organization.status:
            return organization.status.lower()
        if user.organizer_status:
            return user.organizer_status.lower()
        return "none"

    def _ensure_organization(user):
        organization = getattr(user, "organization", None)
        if not organization:
            organization = Organization(owner=user)
            db.session.add(organization)
        return organization

    def _has_event_access(user):
        if user.is_admin or user.is_event_creator or user.is_organizer:
            return True
        organization = getattr(user, "organization", None)
        return bool(organization and organization.status == "approved")

    def _ensure_legacy_organization(user):
        organization = getattr(user, "organization", None)
        if organization:
            return organization

        legacy_fields = [
            user.company_name,
            user.organizer_description,
            user.organizer_website,
            getattr(user, "business_street", None),
            getattr(user, "business_city", None),
            getattr(user, "business_state", None),
            getattr(user, "business_zip", None),
            getattr(user, "business_phone", None),
            getattr(user, "business_email", None),
        ]

        status_value = (user.organizer_status or "none").lower()
        if status_value == "none" and not user.is_organizer:
            return None

        organization = Organization(
            owner=user,
            name=user.company_name,
            description=user.organizer_description,
            website=user.organizer_website,
            street=getattr(user, "business_street", None),
            city=getattr(user, "business_city", None),
            state=getattr(user, "business_state", None),
            zip_code=getattr(user, "business_zip", None),
            business_phone=getattr(user, "business_phone", None),
            business_email=getattr(user, "business_email", None),
            status=status_value if status_value else ("approved" if user.is_organizer else "none"),
            terms_accepted=user.organizer_terms_accepted,
            applied_at=user.organizer_applied_at,
            approved_at=user.organizer_approved_at,
            denied_at=user.organizer_denied_at,
        )
        db.session.add(organization)
        try:
            db.session.commit()
        except SQLAlchemyError as exc:
            db.session.rollback()
            logger.error("Failed to bootstrap organization for %s: %s", user.email, exc)
            return None
        return organization

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

    @app.route("/auth/session", methods=["POST"])
    def establish_session_from_firebase():
        payload = request.get_json(silent=True) or {}
        id_token = payload.get("idToken") or payload.get("id_token")
        intent = (payload.get("intent") or "user").lower()
        redirect_target = payload.get("redirect") or request.args.get("next")

        if not id_token:
            return jsonify({"success": False, "message": "Missing Firebase token."}), 400

        try:
            decoded_token = verify_firebase_token(id_token)
        except FirebaseAuthError as exc:
            logger.warning("Firebase token verification failed: %s", exc)
            return jsonify({"success": False, "message": str(exc)}), 401

        raw_email = (decoded_token.get("email") or "").strip()
        if not raw_email:
            return jsonify({"success": False, "message": "Your Firebase account is missing an email address."}), 400
        normalized_email = raw_email.lower()

        display_name = decoded_token.get("name") or ""
        first_name = decoded_token.get("given_name") or (display_name.split(" ")[0] if display_name else None)
        last_name = decoded_token.get("family_name")

        try:
            user = User.query.filter(func.lower(User.email) == normalized_email).first()
            is_new_user = False

            if not user:
                user = User(
                    email=raw_email,
                    first_name=first_name,
                    last_name=last_name,
                    account_active=True,
                )
                # Store a random password placeholder to satisfy non-null constraint
                user.set_password(secrets.token_urlsafe(32))
                is_new_user = True
                db.session.add(user)
            else:
                if first_name and not user.first_name:
                    user.first_name = first_name
                if last_name and not user.last_name:
                    user.last_name = last_name

            admin_emails = app.config.get("ADMIN_EMAILS", {"ryan@funlist.ai"})
            if intent == "admin":
                if normalized_email not in admin_emails and not user.is_admin:
                    return jsonify({"success": False, "message": "Admin access denied."}), 403
                user.is_admin = True

            user.last_login = datetime.utcnow()
            db.session.commit()
        except SQLAlchemyError as exc:
            db.session.rollback()
            logger.error("Database error establishing Firebase session: %s", exc, exc_info=True)
            return jsonify({"success": False, "message": "Unable to update your account."}), 500

        login_user(user)
        session["user_id"] = user.id
        session["login_time"] = datetime.utcnow().isoformat()
        session["last_activity"] = datetime.utcnow().isoformat()

        if is_new_user:
            session['new_registration'] = True
            flash("Welcome to FunList.ai! Let's get your profile set up.", "success")

        safe_redirect = _safe_redirect_target(redirect_target)
        return jsonify({
            "success": True,
            "redirect": safe_redirect,
            "isNewUser": is_new_user
        })

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

    @app.route("/signup", methods=["GET"])
    def signup():
        if current_user.is_authenticated:
            return redirect(url_for("index"))

        redirect_target = request.args.get("next") or request.args.get("redirect")
        safe_redirect = _safe_redirect_target(redirect_target)

        return render_template(
            "signup.html",
            auth_screen="signup",
            auth_redirect=safe_redirect,
        )

    @app.route("/login", methods=["GET"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        safe_redirect = _safe_redirect_target(request.args.get("next"))

        return render_template(
            "login.html",
            auth_screen="login",
            auth_redirect=safe_redirect,
        )

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
        organization = current_user.organization or _ensure_legacy_organization(current_user)
        return render_template("profile.html", user=current_user, organization=organization)

    @app.route("/organizer/apply", methods=["GET", "POST"])
    @login_required
    def organizer_apply():
        form = OrganizerApplicationForm()
        organization = current_user.organization or _ensure_legacy_organization(current_user)
        status = _organizer_status(current_user)

        if current_user.is_organizer and status == "approved":
            flash("You are already approved as an organizer.", "info")
            return redirect(url_for("profile"))

        if request.method == "GET":
            form.company_name.data = (
                organization.name if organization and organization.name else current_user.company_name
            )
            form.organizer_description.data = (
                organization.description if organization and organization.description else current_user.organizer_description
            )
            form.organizer_website.data = (
                organization.website if organization and organization.website else current_user.organizer_website
            )
            form.business_email.data = (
                organization.business_email
                if organization and organization.business_email
                else getattr(current_user, "business_email", None)
                or current_user.email
            )
            form.business_phone.data = (
                organization.business_phone
                if organization and organization.business_phone
                else getattr(current_user, "business_phone", "")
            )
            form.business_street.data = (
                organization.street if organization and organization.street else getattr(current_user, "business_street", "")
            )
            form.business_city.data = (
                organization.city if organization and organization.city else getattr(current_user, "business_city", "")
            )
            form.business_state.data = (
                organization.state if organization and organization.state else getattr(current_user, "business_state", "")
            )
            form.business_zip.data = (
                organization.zip_code if organization and organization.zip_code else getattr(current_user, "business_zip", "")
            )
            form.terms_accepted.data = organization.terms_accepted if organization else False

        if form.validate_on_submit():
            organization = _ensure_organization(current_user)
            organization.name = form.company_name.data
            organization.description = form.organizer_description.data
            organization.website = form.organizer_website.data
            organization.business_email = form.business_email.data
            organization.business_phone = form.business_phone.data
            organization.street = form.business_street.data
            organization.city = form.business_city.data
            organization.state = form.business_state.data
            organization.zip_code = form.business_zip.data
            organization.terms_accepted = form.terms_accepted.data
            organization.status = "pending"
            organization.applied_at = datetime.utcnow()
            organization.approved_at = None
            organization.denied_at = None

            current_user.company_name = form.company_name.data
            current_user.organizer_description = form.organizer_description.data
            current_user.organizer_website = form.organizer_website.data
            current_user.organizer_terms_accepted = form.terms_accepted.data
            current_user.organizer_status = "pending"
            current_user.organizer_applied_at = datetime.utcnow()
            current_user.organizer_denied_at = None
            current_user.organizer_approved_at = None
            current_user.is_organizer = False

            try:
                db.session.commit()
                flash("Thanks! Your organizer application is under review. We'll email you once it's approved.", "success")
                return redirect(url_for("profile"))
            except SQLAlchemyError as exc:
                db.session.rollback()
                logger.error("Organizer application failed: %s", exc, exc_info=True)
                flash("We couldn't submit your application. Please try again.", "danger")

        return render_template(
            "organizer_apply.html",
            form=form,
            status=status,
        )

    @app.route("/profile/edit", methods=["GET", "POST"])
    @login_required
    def edit_profile():
        form = ProfileForm()
        form.user_id = current_user.id

        organization = current_user.organization or _ensure_legacy_organization(current_user)

        if request.method == "GET":
            # Personal Information
            form.first_name.data = current_user.first_name
            form.last_name.data = current_user.last_name
            form.title.data = current_user.title
            if hasattr(current_user, 'phone'):
                form.phone.data = current_user.phone
            # Company name is managed in the organizer section
            
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
            if current_user.is_organizer and organization:
                form.company_name.data = organization.name
                form.organizer_description.data = organization.description or current_user.organizer_description
                form.organizer_website.data = organization.website or current_user.organizer_website
                form.business_street.data = organization.street
                form.business_city.data = organization.city
                form.business_state.data = organization.state
                form.business_zip.data = organization.zip_code
                form.business_phone.data = organization.business_phone
                form.business_email.data = organization.business_email or current_user.email
                
        if form.validate_on_submit():
            try:
                # Personal profile data
                profile_data = {
                    "first_name": form.first_name.data,
                    "last_name": form.last_name.data,
                    "title": form.title.data,
                    "phone": form.phone.data,
                    "company_name": form.company_name.data,
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
            google_maps_api_key = app.config.get("GOOGLE_MAPS_API_KEY", "")
            return render_template(
                "map.html",
                events=events,
                google_maps_api_key=google_maps_api_key
            )
        except Exception as e:
            app.logger.error(f"Error in map route: {str(e)}")
            return render_template(
                "map.html",
                events=[],
                error_message="Could not load events for the map. Please try again later.",
                google_maps_api_key=app.config.get("GOOGLE_MAPS_API_KEY", "")
            )

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
        if not _has_event_access(current_user):
            return render_template(
                "event_creator_required.html",
                organizer_status=_organizer_status(current_user)
            )

        # Create a new form instance
        form = EventForm()
        
        # Make sure we have a clean database session by rolling back any failed transactions
        try:
            db.session.rollback()
        except Exception as e:
            logger.error(f"Error rolling back session: {str(e)}")
        
        # Set default choices for parent events
        form.parent_event.choices = [('0', 'No parent events available')]
        
        # Refresh the current user to ensure we're working with a properly attached instance
        try:
            # Make sure we have a fresh user object to work with
            user = User.query.get(current_user.id)
            
            # Try to safely get the user's events for parent event selection in a new transaction
            try:
                user_events = Event.query.filter_by(user_id=user.id, parent_event_id=None).all()
                if user_events:
                    form.parent_event.choices = [(str(e.id), e.title) for e in user_events]
            except Exception as inner_e:
                logger.error(f"Error querying parent events: {str(inner_e)}")
                db.session.rollback()  # Roll back on error
                # Continue execution even if this fails
        except Exception as e:
            logger.error(f"Error refreshing user session: {str(e)}")
            db.session.rollback()  # Roll back on error
            # Don't fail the whole page if we can't get parent events
        
        # Check if venue_id is in request args (coming from venue detail page)
        venue_id = request.args.get('venue_id')
        if venue_id and request.method == 'GET':
            try:
                form.venue_id.data = int(venue_id)
            except (ValueError, TypeError):
                logger.warning(f"Invalid venue_id in request: {venue_id}")
                # Continue with default venue selection
                pass

        if form.validate_on_submit():
            try:
                # Create the event
                event = Event(
                    title=form.title.data,
                    description=form.description.data,
                    status="pending",
                    start_date=form.start_date.data,
                    end_date=form.end_date.data,
                    all_day=form.all_day.data,
                    street=form.street.data,
                    city=form.city.data,
                    state=form.state.data,
                    zip_code=form.zip_code.data,
                    category=form.category.data,
                    target_audience=form.target_audience.data,
                    fun_meter=int(form.fun_meter.data),
                    user_id=current_user.id,
                    ticket_url=form.ticket_url.data if hasattr(form, 'ticket_url') else None
                )
                
                # Handle times if not all day
                if not event.all_day:
                    event.start_time = form.start_time.data.strftime('%H:%M:%S') if form.start_time.data else None
                    event.end_time = form.end_time.data.strftime('%H:%M:%S') if form.end_time.data else None

                # Handle recurring events
                if form.is_recurring.data:
                    event.is_recurring = True
                    event.recurring_pattern = form.recurring_pattern.data
                    event.recurring_end_date = form.recurring_end_date.data
                
                # Handle sub-events
                if form.is_sub_event.data and form.parent_event.data:
                    event.parent_event_id = int(form.parent_event.data)
                
                # Handle venue selection
                if form.venue_selection_type.data == 'existing' and form.venue_id.data and form.venue_id.data != 0:
                    # Use selected venue
                    event.venue_id = form.venue_id.data
                    
                    # Get venue location for geocoding if event location fields are empty
                    venue = Venue.query.get(form.venue_id.data)
                    if venue and not event.street:
                        event.street = venue.street
                        event.city = venue.city
                        event.state = venue.state
                        event.zip_code = venue.zip_code
                        
                        # Use venue coordinates if available
                        if venue.latitude and venue.longitude:
                            event.latitude = venue.latitude
                            event.longitude = venue.longitude
                elif form.venue_selection_type.data == 'new' and form.use_new_venue.data and form.venue_name.data:
                    # Create a new venue
                    new_venue = Venue(
                        name=form.venue_name.data,
                        street=form.venue_street.data,
                        city=form.venue_city.data,
                        state=form.venue_state.data,
                        zip_code=form.venue_zip.data,
                        venue_type_id=form.venue_type_id.data if form.venue_type_id.data and form.venue_type_id.data != 0 else None,
                        created_by_user_id=current_user.id
                    )
                    
                    # If user claims to be owner/manager
                    if form.is_venue_owner.data:
                        new_venue.owner_manager_user_id = current_user.id
                        new_venue.is_verified = False  # Requires admin verification
                        new_venue.verification_notes = f"Owner/manager claim submitted during event creation by {current_user.email} on {datetime.utcnow()}"
                    
                    # Geocode the venue address
                    venue_coordinates = geocode_address(
                        form.venue_street.data,
                        form.venue_city.data,
                        form.venue_state.data,
                        form.venue_zip.data
                    )
                    
                    if venue_coordinates:
                        new_venue.latitude = venue_coordinates[0]
                        new_venue.longitude = venue_coordinates[1]
                        
                        # Use these coordinates for the event too
                        event.latitude = venue_coordinates[0]
                        event.longitude = venue_coordinates[1]
                    
                    db.session.add(new_venue)
                    db.session.flush()  # Get the ID without committing
                    event.venue_id = new_venue.id
                else:
                    # No venue selected or created, geocode the event location
                    coordinates = geocode_address(
                        form.street.data,
                        form.city.data,
                        form.state.data,
                        form.zip_code.data
                    )

                    if coordinates:
                        event.latitude = coordinates[0]
                        event.longitude = coordinates[1]
                    
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
                    if hasattr(form, 'prohibited_advertisers') and form.prohibited_advertisers.data:
                        for category_id in form.prohibited_advertisers.data:
                            category = ProhibitedAdvertiserCategory.query.get(category_id)
                            if category:
                                event.prohibited_advertisers.append(category)
                                
                    db.session.add(event)
                    db.session.commit()
                    flash("Event created successfully!", "success")
                    return redirect(url_for("events"))
                
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.exception(
                    f"Database error during event submission: {str(e)}"
                )  # Improved logging
                flash("A database error occurred. Please try again later.", "danger")
                return render_template("submit_event.html", form=form)
            except Exception as e:
                db.session.rollback()
                logger.exception(f"Error during event submission: {str(e)}")
                flash("An unexpected error occurred. Please try again later.", "danger")
                return render_template("submit_event.html", form=form)
                
        elif request.method == "POST":
            flash("Form submission failed. Please check your inputs.", "danger")
        return render_template("submit_event.html", form=form)

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("500.html"), 500

    @app.route("/admin/login", methods=["GET"])
    @app.route("/admin_login", methods=["GET"])  # Add alternative URL route
    def admin_login():
        admin_emails = app.config.get("ADMIN_EMAILS", {"ryan@funlist.ai"})
        if current_user.is_authenticated and current_user.email.lower() in admin_emails:
            return redirect(url_for("admin_dashboard"))

        redirect_target = request.args.get("next") or url_for("admin_dashboard")
        safe_redirect = _safe_redirect_target(redirect_target)

        return render_template(
            "admin_login.html",
            auth_screen="login",
            auth_redirect=safe_redirect,
            auth_intent="admin",
        )

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

    @app.route("/reset-password-request", methods=["GET"])
    @app.route("/reset_password_request", methods=["GET"])
    def reset_password_request():
        return render_template(
            'reset_password_request.html',
            auth_screen="reset-password",
        )

    @app.route("/reset-password/<token>", methods=["GET", "POST"])
    @app.route("/reset_password/<token>", methods=["GET", "POST"])
    def reset_password(token):
        flash('Password reset links are now handled directly by Firebase. Please request a new link below.', 'info')
        return redirect(url_for('reset_password_request'))
        
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
        return redirect(url_for("organizer_apply"))

    @app.route("/organizer-profile", methods=["GET", "POST"])
    @login_required
    def organizer_profile():
        # Redirect to the consolidated profile editing page
        flash("Your organizer profile can now be managed from your main profile page.", "info")
        return redirect(url_for("edit_profile"))
        
    @app.route("/change-password", methods=["GET"])
    @login_required
    def change_password():
        return render_template(
            "change_password.html",
            auth_screen="reset-password",
            prefill_email=current_user.email,
        )

    @app.route("/venues", methods=["GET"])
    def venues():
        venues = Venue.query.order_by(Venue.name).all()
        return render_template("venues.html", venues=venues)
        
    @app.route("/venues/<int:venue_id>", methods=["GET"])
    def venue_detail(venue_id):
        venue = Venue.query.get_or_404(venue_id)
        events = Event.query.filter_by(venue_id=venue.id).all()
        return render_template("venue_detail.html", venue=venue, events=events, now=datetime.utcnow())
    
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
                    created_by_user_id=current_user.id
                )
                
                # If user claims to be owner/manager
                if form.is_owner_manager.data:
                    venue.owner_manager_user_id = current_user.id
                    venue.is_verified = False  # Requires admin verification
                    venue.verification_notes = f"Owner/manager claim submitted by {current_user.email} on {datetime.utcnow()}"
                
                # Geocode the address for mapping
                try:
                    coordinates = geocode_address(
                        form.street.data,
                        form.city.data,
                        form.state.data,
                        form.zip_code.data
                    )
                    if coordinates:
                        venue.latitude = coordinates[0]
                        venue.longitude = coordinates[1]
                except Exception as e:
                    logger.error(f"Error geocoding venue address: {str(e)}")
                
                db.session.add(venue)
                db.session.commit()
                flash("Venue added successfully!", "success")
                return redirect(url_for("venue_detail", venue_id=venue.id))
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
        authorized = (
            current_user.is_admin or 
            (venue.owner_manager_user_id == current_user.id and venue.is_verified)
        )
        
        if not authorized:
            flash("You are not authorized to edit this venue. Only verified owners/managers or admins can edit venues.", "danger")
            return redirect(url_for("venue_detail", venue_id=venue.id))
        
        form = VenueForm(obj=venue)
        
        if form.validate_on_submit():
            try:
                form.populate_obj(venue)
                venue.updated_at = datetime.utcnow()
                
                # Re-geocode if address changed
                if (form.street.data != venue.street or
                    form.city.data != venue.city or
                    form.state.data != venue.state or
                    form.zip_code.data != venue.zip_code):
                    
                    try:
                        coordinates = geocode_address(
                            form.street.data,
                            form.city.data,
                            form.state.data,
                            form.zip_code.data
                        )
                        if coordinates:
                            venue.latitude = coordinates[0]
                            venue.longitude = coordinates[1]
                    except Exception as e:
                        logger.error(f"Error geocoding venue address during edit: {str(e)}")
                
                db.session.commit()
                flash("Venue updated successfully!", "success")
                return redirect(url_for("venue_detail", venue_id=venue.id))
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error updating venue: {str(e)}")
                flash("There was a problem updating the venue. Please try again.", "danger")
        
        return render_template("edit_venue.html", form=form, venue=venue)
    
    @app.route("/venues/<int:venue_id>/claim", methods=["POST"])
    @login_required
    def claim_venue(venue_id):
        venue = Venue.query.get_or_404(venue_id)
        
        try:
            # Check if venue already has a verified owner/manager
            if venue.owner_manager_user_id and venue.is_verified:
                flash("This venue already has a verified owner/manager.", "warning")
                return redirect(url_for("venue_detail", venue_id=venue.id))
            
            # Record the claim
            venue.owner_manager_user_id = current_user.id
            venue.is_verified = False  # Pending verification
            venue.verification_notes = f"Venue claim submitted by {current_user.email} ({current_user.id}) on {datetime.utcnow()}"
            
            db.session.commit()
            flash("Your claim has been submitted. An administrator will review your request.", "success")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error claiming venue: {str(e)}")
            flash("There was a problem submitting your claim. Please try again.", "danger")
        
        return redirect(url_for("venue_detail", venue_id=venue.id))
    
    @app.route("/venues/<int:venue_id>/delete", methods=["POST"])
    @login_required
    def delete_venue(venue_id):
        venue = Venue.query.get_or_404(venue_id)
        
        # Check if user is authorized to delete this venue
        authorized = (
            current_user.is_admin or
            (venue.owner_manager_user_id == current_user.id and venue.is_verified) or
            (venue.created_by_user_id == current_user.id and not venue.owner_manager_user_id)
        )
        
        if not authorized:
            flash("You are not authorized to delete this venue.", "danger")
            return redirect(url_for("venue_detail", venue_id=venue.id))
        
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
        missing_org_users = User.query.filter(
            User.is_organizer.is_(True),
            ~User.organization.has()
        ).all()
        for user in missing_org_users:
            _ensure_legacy_organization(user)

        organizers = Organization.query.filter_by(status="approved").order_by(Organization.name.asc()).all()
        return render_template("organizers.html", organizations=organizers)

    @app.route("/organizer/<int:user_id>")
    def organizer_detail(user_id):
        organizer = User.query.get_or_404(user_id)
        organization = organizer.organization or _ensure_legacy_organization(organizer)
        if not organization or organization.status != "approved":
            flash("This user is not registered as an event organizer.", "warning")
            return redirect(url_for("organizers"))

        # Get events by this organizer
        events = Event.query.filter_by(user_id=organizer.id).order_by(Event.start_date.desc()).all()
        return render_template("organizer_detail.html", organizer=organizer, organization=organization, events=events)

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
        
    @app.route("/admin/venues")
    @login_required
    def admin_venues():
        if current_user.email != 'ryan@funlist.ai':
            flash("Access denied. Only authorized administrators can access this page.", "danger")
            return redirect(url_for("index"))
            
        # Filter options
        filter_status = request.args.get('status', 'pending')
        
        venues_query = Venue.query
        
        if filter_status == 'pending':
            # Venues with owner/manager claims pending verification
            venues_query = venues_query.filter(
                Venue.owner_manager_user_id.isnot(None),
                Venue.is_verified == False
            )
        elif filter_status == 'verified':
            # Venues with verified owners/managers
            venues_query = venues_query.filter(
                Venue.owner_manager_user_id.isnot(None),
                Venue.is_verified == True
            )
        elif filter_status == 'unclaimed':
            # Venues without any ownership claims
            venues_query = venues_query.filter(
                Venue.owner_manager_user_id.is_(None)
            )
            
        venues = venues_query.order_by(Venue.created_at.desc()).all()
        
        return render_template(
            "admin_venues.html", 
            venues=venues, 
            filter_status=filter_status
        )
        
    @app.route("/admin/venue/<int:venue_id>/verify", methods=["POST"])
    @login_required
    def admin_verify_venue(venue_id):
        if current_user.email != 'ryan@funlist.ai':
            return jsonify({"success": False, "message": "Unauthorized. Only administrators can perform this action."}), 403
            
        try:
            venue = Venue.query.get_or_404(venue_id)
            venue.is_verified = True
            venue.verification_notes += f"\nVerified by admin ({current_user.email}) on {datetime.utcnow()}"
            db.session.commit()
            
            return jsonify({
                "success": True, 
                "message": f"Venue '{venue.name}' has been verified"
            })
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in admin_verify_venue: {str(e)}")
            return jsonify({
                "success": False, 
                "message": f"Error: {str(e)}"
            }), 500
            
    @app.route("/admin/venue/<int:venue_id>/reject-claim", methods=["POST"])
    @login_required
    def admin_reject_venue_claim(venue_id):
        if current_user.email != 'ryan@funlist.ai':
            return jsonify({"success": False, "message": "Unauthorized. Only administrators can perform this action."}), 403
            
        try:
            venue = Venue.query.get_or_404(venue_id)
            previously_claimed_by = venue.owner_manager_user_id
            
            venue.owner_manager_user_id = None
            venue.is_verified = False
            venue.verification_notes += f"\nClaim rejected by admin ({current_user.email}) on {datetime.utcnow()}"
            db.session.commit()
            
            return jsonify({
                "success": True, 
                "message": f"Ownership claim for venue '{venue.name}' has been rejected"
            })
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in admin_reject_venue_claim: {str(e)}")
            return jsonify({
                "success": False, 
                "message": f"Error: {str(e)}"
            }), 500
    
    @app.route('/advertiser-exclusion-info')
    def advertiser_exclusion_info():
        return render_template('advertiser_exclusion_info.html')
