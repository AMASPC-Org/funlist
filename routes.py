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
logger.setLevel(logging.DEBUG)


def init_routes(app):
    @app.route("/about")
    def about():
        return render_template('about.html')

    @app.route("/subscribe", methods=["POST"])
    def subscribe():
        try:
            data = request.get_json()
            email = data.get("email")
            if not email:
                return jsonify({"success": False, "message": "Email is required"}), 400
            if Subscriber.query.filter_by(email=email).first():
                return (
                    jsonify({"success": False, "message": "Email already subscribed"}),
                    400,
                )
            subscriber = Subscriber(email=email)
            db.session.add(subscriber)
            db.session.commit()

            return jsonify({"success": True, "message": "Subscription successful"})
        except Exception as e:
            logger.error(f"Subscription error: {str(e)}")
            db.session.rollback()
            return jsonify({"success": False, "message": "An error occurred"}), 500

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
        events = Event.query.order_by(Event.start_date.desc()).all()
        return render_template("index.html", events=events, user=current_user)

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        form = SignupForm()
        if form.validate_on_submit():
            try:
                user = User()
                user.email = form.email.data
                user.set_password(form.password.data)
                user.account_active = True

                db.session.add(user)
                db.session.commit()

                flash("Account created successfully! You can now log in.", "success")
                return redirect(url_for("login"))
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
                user = User.query.filter_by(email=form.email.data).first()

                if user and user.check_password(form.password.data):
                    if form.remember_me.data:
                        session.permanent = True
                    session["user_id"] = user.id
                    session["login_time"] = datetime.utcnow().isoformat()
                    session["last_activity"] = datetime.utcnow().isoformat()

                    login_user(user, remember=form.remember_me.data)
                    user.last_login = db.func.now()
                    db.session.commit()

                    flash("Logged in successfully!", "success")
                    next_page = request.args.get("next")
                    return redirect(next_page or url_for("index"))
                else:
                    logger.warning(f"Failed login attempt for email: {form.email.data}")
                    flash("Invalid email or password. Please try again.", "danger")
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Database error during login: {str(e)}")
                flash(
                    "We encountered a technical issue. Please try again later.",
                    "danger",
                )
            except Exception as e:
                logger.error(f"Unexpected error during login: {str(e)}")
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
        if form.validate_on_submit():
            try:
                profile_data = {
                    "username": form.username.data,
                    "first_name": form.first_name.data,
                    "last_name": form.last_name.data,
                    "bio": form.bio.data,
                    "location": form.location.data,
                    "interests": form.interests.data,
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
                        fun_meter=form.fun_meter.data,
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
        if current_user.is_authenticated and current_user.is_admin:
            return redirect(url_for("admin_dashboard"))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data) and user.is_admin:
                login_user(user)
                return redirect(url_for("admin_dashboard"))
            flash("Invalid credentials or not an admin user.", "danger")
        return render_template("admin_login.html", form=form)

    @app.route("/admin/events")
    @login_required
    def admin_events():
        if not current_user.is_admin:
            flash("Access denied. Admin privileges required.", "danger")
            return redirect(url_for("index"))
        events = Event.query.order_by(Event.start_date.desc()).all()
        return render_template("admin_events.html", events=events)

    @app.route("/admin/users")
    @login_required
    def admin_users():
        if not current_user.is_admin:
            flash("Access denied. Admin privileges required.", "danger")
            return redirect(url_for("index"))
        users = User.query.order_by(User.created_at.desc()).all()
        return render_template("admin_users.html", users=users)

    @app.route("/api/featured-events")
    def featured_events_api():
        lat = request.args.get("lat", type=float)
        lng = request.args.get("lng", type=float)

        if not lat or not lng:
            return jsonify({"error": "Location required"}), 400
        # Get events within 15 miles radius and with high fun ratings

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
        return jsonify(sorted(featured, key=lambda x: (-x["fun_meter"], x["date"]))[:5])

    @app.route("/advertising")
    def advertising():
        return render_template("advertising.html")

    @app.route("/admin/analytics")
    @login_required
    def admin_analytics():
        if not current_user.is_admin:
            flash("Access denied. Admin privileges required.", "danger")
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
        if not current_user.is_admin:
            return jsonify({"success": False, "message": "Unauthorized"}), 403
        event = Event.query.get_or_404(event_id)

        if action == "approve":
            event.status = "approved"
        elif action == "reject":
            event.status = "rejected"
        elif action == "delete":
            db.session.delete(event)
        db.session.commit()
        return jsonify({"success": True})

    @app.route("/admin/dashboard")
    @login_required
    def admin_dashboard():
        if not current_user.is_admin:
            flash("Access denied. Admin privileges required.", "danger")
            return redirect(url_for("index"))
        tab = request.args.get("tab", "overview")
        status = request.args.get("status", "pending")

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

        # Get users for user management

        users = User.query.order_by(User.created_at.desc()).all()

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
            events_by_category=events_by_category,
            user_growth_data=user_growth_data,
        )

    @app.route("/admin/user/<int:user_id>/deactivate")
    @login_required
    def admin_deactivate_user(user_id):
        if not current_user.is_admin:
            return jsonify({"error": "Unauthorized"}), 403
        user = User.query.get_or_404(user_id)
        user.account_active = False
        db.session.commit()
        flash("User account deactivated.", "success")  # Fixed
        return redirect(url_for("admin_dashboard", tab="users"))

    @app.route("/admin/user/<int:user_id>/activate")
    @login_required
    def admin_activate_user(user_id):
        if not current_user.is_admin:
            return jsonify({"error": "Unauthorized"}), 403
        user = User.query.get_or_404(user_id)
        user.account_active = True
        db.session.commit()
        flash("User account activated.", "success")
        return redirect(url_for("admin_dashboard", tab="users"))
