import os
import logging
import requests
from flask import render_template, flash, redirect, url_for, request, session, jsonify, current_app, Response
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from forms import (SignupForm, LoginForm, ProfileForm, EventForm,
                   ResetPasswordRequestForm, ResetPasswordForm, ChangePasswordForm,
                   VenueForm, ContactForm, SearchForm)
from models import User, Event, Subscriber, Chapter, HelpArticle, Venue, ProhibitedAdvertiserCategory, EventExclusionRule, OrganizerMaster, VenueMaster
from db_init import db
from sqlalchemy import func, text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime, timedelta, date, time
import json
import openai
import anthropic
from google import genai
from flask_wtf.csrf import CSRFProtect
from funalytics_scoring import (
    calculate_frequency_deduction, 
    is_event_appropriate_for_audience,
    calculate_audience_specific_score,
    apply_frequency_deduction,
    get_audience_recommendations,
    validate_event_exclusions,
    generate_event_disclaimer,
    TARGET_AUDIENCES
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def combine_date_with_time(date_value, time_value=None, fallback_time=None):
    if not date_value: return None
    if time_value: return datetime.combine(date_value, time_value)
    if fallback_time: return datetime.combine(date_value, fallback_time)
    return datetime.combine(date_value, time.min)

def build_location_details(selected_venue, form):
    location_label = selected_venue.name if selected_venue else (form.venue_name.data or None)
    street = form.street.data or None
    city = form.city.data or None
    state = form.state.data or None
    zip_code = form.zip_code.data or None
    if not street: street = (selected_venue.street if selected_venue else form.venue_street.data) or None
    if not city: city = (selected_venue.city if selected_venue else form.venue_city.data) or None
    if not state: state = (selected_venue.state if selected_venue else form.venue_state.data) or None
    if not zip_code: zip_code = (selected_venue.zip_code if selected_venue else form.venue_zip.data) or None
    if not location_label: location_label = ", ".join([segment for segment in [street, city, state] if segment])
    return location_label or "Location TBA", street, city, state, zip_code

def coerce_form_date(value):
    if not value: return None
    if isinstance(value, datetime): return value.date()
    if isinstance(value, date): return value
    if isinstance(value, str):
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
            try: return datetime.strptime(value, fmt).date()
            except ValueError: continue
    return None

def coerce_form_time(value):
    if not value: return None
    if isinstance(value, time): return value
    if hasattr(value, 'strftime'): return value
    if isinstance(value, str):
        for fmt in ('%H:%M:%S', '%H:%M'):
            try: return datetime.strptime(value, fmt).time()
            except ValueError: continue
    return None

def populate_event_form_from_model(form, event):
    form.title.data = event.title
    form.description.data = event.description
    form.start_date.data = coerce_form_date(event.start_date)
    form.end_date.data = coerce_form_date(event.end_date)
    form.start_time.data = coerce_form_time(event.start_time)
    form.end_time.data = coerce_form_time(event.end_time)
    form.all_day.data = event.all_day
    form.category.data = event.category or ''
    form.target_audience.data = event.target_audience or ''
    form.fun_meter.data = str(event.fun_meter or event.fun_rating or 3)
    form.is_recurring.data = event.is_recurring
    form.recurrence_type.data = event.recurring_pattern or ''
    form.recurring_pattern.data = event.recurring_pattern or ''
    form.recurring_end_date.data = coerce_form_date(event.recurring_end_date)
    form.street.data = event.street
    form.city.data = event.city
    form.state.data = event.state
    form.zip_code.data = event.zip_code
    form.ticket_url.data = event.website
    form.network_opt_out.data = event.network_opt_out
    form.parent_event.data = event.parent_event_id or 0
    form.is_sub_event.data = bool(event.parent_event_id)
    form.prohibited_advertisers.data = event.get_prohibited_category_ids()
    form.venue_selection_type.data = 'existing' if event.venue_id else 'new'
    form.venue_id.data = event.venue_id or 0
    if event.venue:
        form.venue_name.data = event.venue.name
        form.venue_street.data = event.venue.street
        form.venue_city.data = event.venue.city
        form.venue_state.data = event.venue.state
        form.venue_zip.data = event.venue.zip_code

def get_funalytics_scores(event_ids=None):
    try:
        api_base_url = os.environ.get('EXPRESS_API_URL')
        if not api_base_url: return {}
        url = f"{api_base_url}/events"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('events'):
                scores = {}
                for event in data['events']:
                    if not event_ids or event['id'] in event_ids:
                        if 'funalytics' in event: scores[event['id']] = event['funalytics']
                return scores
    except requests.RequestException as e:
        logger.warning(f"Failed to fetch Funalytics scores: {e}")
    return {}

def recompute_funalytics_score(event_id):
    try:
        api_base_url = os.environ.get('EXPRESS_API_URL', 'http://localhost:3001')
        response = requests.post(f"{api_base_url}/funalytics/recompute/{event_id}", timeout=10)
        return response.status_code == 201
    except requests.RequestException as e:
        logger.error(f"Failed to recompute Funalytics for event {event_id}: {e}")
        return False

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need admin privileges to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def index():
    chapters = Chapter.query.all()
    new_signup = session.pop('new_signup', False)
    return render_template("index.html", user=current_user, chapters=chapters, new_signup=new_signup)

def map():
    try:
        events = Event.query.all()
        chapters = Chapter.query.all()
        events_for_map = []
        for event in events:
            event_data = event.to_dict()
            event_data["fun_rating"] = event.fun_rating if event.fun_rating is not None else event.fun_meter
            event_data["detail_url"] = url_for("event_detail", event_id=event.id)
            events_for_map.append(event_data)
        return render_template("map.html", events=events, events_json=events_for_map, chapters=chapters)
    except Exception as e:
        logger.error(f"Error in map route: {str(e)}")
        return render_template("500.html", error=str(e)), 500

def events():
    try:
        events = Event.query.order_by(Event.start_date.desc()).all()
        chapters = Chapter.query.all()
        try:
            funalytics_scores = get_funalytics_scores()
            for event in events:
                event.funalytics = funalytics_scores.get(event.id)
        except Exception:
            for event in events: event.funalytics = None
        return render_template("events.html", events=events, chapters=chapters)
    except Exception as e:
        logger.error(f"Error in events route: {str(e)}")
        return render_template("500.html", error=str(e)), 500

def event_detail(event_id):
    try:
        event = Event.query.get_or_404(event_id)
        chapters = Chapter.query.all()
        funalytics_scores = get_funalytics_scores([event_id])
        event.funalytics = funalytics_scores.get(event_id, None)
        return render_template("event_detail.html", event=event, chapters=chapters)
    except Exception as e:
        logger.error(f"Error in event_detail route: {str(e)}")
        return render_template("500.html", error=str(e)), 500

def venues():
    chapters = Chapter.query.all()
    all_venues = Venue.query.order_by(Venue.created_at.desc()).all()
    return render_template("venues.html", venues=all_venues, chapters=chapters)

@login_required
def my_venues():
    chapters = Chapter.query.all()
    user_venues = Venue.query.filter_by(created_by_user_id=current_user.id).order_by(Venue.created_at.desc()).all()
    return render_template("my_venues.html", venues=user_venues, chapters=chapters)

@login_required
def add_venue():
    form = VenueForm()
    chapters = Chapter.query.all()
    if form.validate_on_submit():
        venue = Venue(
            name=form.name.data, street=form.street.data, city=form.city.data,
            state=form.state.data, zip_code=form.zip_code.data, country=form.country.data,
            phone=form.phone.data, email=form.email.data, website=form.website.data,
            venue_type_id=form.venue_type_id.data or None, contact_name=form.contact_name.data,
            contact_phone=form.contact_phone.data, contact_email=form.contact_email.data,
            description=form.description.data, created_by_user_id=current_user.id,
            owner_manager_user_id=current_user.id if form.is_owner_manager.data else None
        )
        try:
            db.session.add(venue)
            db.session.commit()
            flash("Venue added successfully.", "success")
            return redirect(url_for('my_venues'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error adding venue: {str(e)}")
            flash("Failed to add venue.", "danger")
    return render_template("add_venue.html", form=form, chapters=chapters)

def venue_detail(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    chapters = Chapter.query.all()
    venue_events = Event.query.filter_by(venue_id=venue.id).order_by(Event.start_date.desc()).all()
    return render_template("venue_detail.html", venue=venue, events=venue_events, now=datetime.utcnow(), chapters=chapters)

@login_required
def edit_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    if venue.created_by_user_id != current_user.id and not current_user.is_admin:
        flash("Permission denied.", "warning")
        return redirect(url_for('venue_detail', venue_id=venue.id))
    form = VenueForm(obj=venue)
    chapters = Chapter.query.all()
    if request.method == "GET":
        form.venue_type_id.data = venue.venue_type_id or 0
        form.is_owner_manager.data = venue.owner_manager_user_id == current_user.id
    if form.validate_on_submit():
        venue.name = form.name.data
        venue.street = form.street.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.zip_code = form.zip_code.data
        venue.country = form.country.data
        venue.phone = form.phone.data
        venue.email = form.email.data
        venue.website = form.website.data
        venue.venue_type_id = form.venue_type_id.data or None
        venue.contact_name = form.contact_name.data
        venue.contact_phone = form.contact_phone.data
        venue.contact_email = form.contact_email.data
        venue.description = form.description.data
        venue.owner_manager_user_id = current_user.id if form.is_owner_manager.data else venue.owner_manager_user_id
        try:
            db.session.commit()
            flash("Venue updated.", "success")
            return redirect(url_for('venue_detail', venue_id=venue.id))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating venue: {str(e)}")
            flash("Update failed.", "danger")
    return render_template("edit_venue.html", form=form, venue=venue, chapters=chapters)

@login_required
def claim_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    if venue.owner_manager_user_id and venue.owner_manager_user_id != current_user.id and venue.is_verified:
        flash("Venue already verified.", "info")
        return redirect(url_for('venue_detail', venue_id=venue.id))
    venue.owner_manager_user_id = current_user.id
    venue.is_verified = False
    try:
        db.session.commit()
        flash("Claim submitted.", "success")
    except Exception:
        db.session.rollback()
        flash("Claim failed.", "danger")
    return redirect(url_for('venue_detail', venue_id=venue.id))

@login_required
@admin_required
def admin_recompute_funalytics(event_id):
    try:
        if recompute_funalytics_score(event_id):
            flash(f"Score recomputed.", "success")
        else:
            flash("Failed to recompute.", "error")
    except Exception as e:
        logger.error(f"Error recomputing: {str(e)}")
        flash("Error occurred.", "error")
    return redirect(url_for('event_detail', event_id=event_id))

@login_required
def submit_event():
    if not current_user.is_event_creator:
        flash("Enable Event Creator role.", "warning")
        return redirect(url_for('edit_profile'))
    form = EventForm()
    chapters = Chapter.query.all()
    if request.method == 'GET':
        if request.args.get('venue_id'):
            form.venue_selection_type.data = 'existing'
            form.venue_id.data = request.args.get('venue_id', type=int)
        today = date.today()
        if not form.start_date.data: form.start_date.data = today
        if not form.end_date.data: form.end_date.data = today
    if form.validate_on_submit():
        is_draft = request.form.get('is_draft') == 'true'
        start_dt = combine_date_with_time(form.start_date.data, form.start_time.data)
        end_dt = combine_date_with_time(form.end_date.data or form.start_date.data, form.end_time.data, form.start_time.data or time.min)
        selected_venue = None
        if form.venue_selection_type.data == 'existing' and form.venue_id.data:
            selected_venue = Venue.query.get(form.venue_id.data)
        if form.venue_selection_type.data == 'new' and form.venue_name.data and form.use_new_venue.data:
            selected_venue = Venue(
                name=form.venue_name.data, street=form.venue_street.data, city=form.venue_city.data,
                state=form.venue_state.data, zip_code=form.venue_zip.data,
                venue_type_id=form.venue_type_id.data or None, created_by_user_id=current_user.id,
                owner_manager_user_id=current_user.id if form.is_venue_owner.data else None
            )
            db.session.add(selected_venue)
            db.session.flush()
        location_label, street, city, state, zip_code = build_location_details(selected_venue, form)

        event = Event(
            title=form.title.data, description=form.description.data, start_date=start_dt, end_date=end_dt,
            all_day=form.all_day.data, location=location_label, street=street, city=city, state=state, zip_code=zip_code,
            is_recurring=form.is_recurring.data, recurring_pattern=form.recurring_pattern.data,
            user_id=current_user.id, venue=selected_venue, category=form.category.data,
            target_audience=form.target_audience.data, fun_meter=int(form.fun_meter.data or 50),
            fun_rating=int(form.fun_meter.data or 50), status='draft' if is_draft else 'pending',
            network_opt_out=form.network_opt_out.data, website=form.ticket_url.data
        )
        if form.prohibited_advertisers.data:
            event.prohibited_advertisers = ProhibitedAdvertiserCategory.query.filter(
                ProhibitedAdvertiserCategory.id.in_(form.prohibited_advertisers.data)).all()
        db.session.add(event)
        db.session.commit()
        if is_draft: return jsonify({"status": "saved", "event_id": event.id}), 200
        flash("Event submitted!", "success")
        return redirect(url_for('events'))
    return render_template("submit_event.html", form=form, chapters=chapters)

@login_required
def my_events():
    if not (current_user.is_event_creator or current_user.is_admin):
        return redirect(url_for('edit_profile'))
    chapters = Chapter.query.all()
    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.start_date.desc()).all()
    return render_template("my_events.html", events=events, chapters=chapters, status_counts={})

@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id and not current_user.is_admin:
        return redirect(url_for('my_events'))
    form = EventForm(obj=event)
    chapters = Chapter.query.all()
    if request.method == 'GET': populate_event_form_from_model(form, event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.fun_meter = int(form.fun_meter.data or 50)
        event.fun_rating = event.fun_meter
        db.session.commit()
        flash("Event updated.", "success")
        return redirect(url_for('my_events'))
    return render_template("submit_event.html", form=form, chapters=chapters, is_edit=True, event=event)

def login():
    chapters = Chapter.query.all()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form, chapters=chapters)

@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        if form.primary_role.data == 'organizer': user.is_organizer = True
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            session['new_signup'] = True
            flash("Account created.", "success")
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            flash("Error creating account.", "danger")
    return render_template('signup.html', form=form, chapters=Chapter.query.all())

def reset_password_request():
    form = ResetPasswordRequestForm()
    return render_template('reset_password_request.html', form=form, chapters=Chapter.query.all())

def reset_password(token):
    form = ResetPasswordForm()
    return render_template('reset_password.html', form=form, token=token, chapters=Chapter.query.all())

@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash("Password updated.", "success")
        return redirect(url_for('profile'))
    return render_template('change_password.html', form=form, chapters=Chapter.query.all())

@login_required
def profile():
    return render_template('profile.html', user=current_user, chapters=Chapter.query.all(), preferences=current_user.get_preferences())

@login_required
def edit_profile():
    form = ProfileForm(obj=current_user, user_id=current_user.id)
    chapters = Chapter.query.all()
    try:
        preferences = current_user.get_preferences() or {}
    except Exception as exc:  # noqa: BLE001
        logger.warning("Corrupt preferences JSON for user %s: %s", current_user.id, exc)
        preferences = {}

    def _coerce_list(value):
        if not value:
            return []
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    # Quick role activation buttons (kept for convenience, but now persist correctly)
    if request.method == "POST" and request.form.get("activate_role"):
        role_to_activate = request.form.get("activate_role")
        role_applied = False

        if role_to_activate == "organizer":
            if not current_user.is_organizer:
                current_user.is_organizer = True
                role_applied = True
            if not current_user.is_event_creator:
                current_user.is_event_creator = True
                role_applied = True
        elif role_to_activate == "event_creator" and not current_user.is_event_creator:
            current_user.is_event_creator = True
            role_applied = True
        elif role_to_activate == "vendor" and not current_user.is_vendor:
            current_user.is_vendor = True
            role_applied = True
        elif role_to_activate == "sponsor" and not current_user.is_sponsor:
            current_user.is_sponsor = True
            role_applied = True

        if role_applied:
            current_user.roles_last_updated = datetime.utcnow()
            db.session.add(current_user)
            db.session.commit()
            flash(
                f"{role_to_activate.replace('_', ' ').title()} enabled. Complete the details below and save your profile.",
                "success",
            )
        else:
            flash("That capability is already enabled on your account.", "info")

        form.enable_event_creator.data = current_user.is_event_creator
        form.enable_organizer.data = current_user.is_organizer
        form.enable_vendor.data = current_user.is_vendor
        form.enable_sponsor.data = current_user.is_sponsor
        form.event_focus.data = _coerce_list(preferences.get("event_focus", []))
        form.preferred_locations.data = preferences.get("preferred_locations", "")
        form.event_interests.data = preferences.get("event_interests", "")
        return render_template("edit_profile.html", form=form, chapters=chapters)

    if request.method == "GET":
        form.event_focus.data = _coerce_list(preferences.get("event_focus", []))
        form.preferred_locations.data = preferences.get("preferred_locations", "")
        form.event_interests.data = preferences.get("event_interests", "")
        form.enable_event_creator.data = current_user.is_event_creator
        form.enable_organizer.data = current_user.is_organizer
        form.enable_vendor.data = current_user.is_vendor
        form.enable_sponsor.data = current_user.is_sponsor

    previous_roles = {
        "event_creator": current_user.is_event_creator,
        "organizer": current_user.is_organizer,
        "vendor": current_user.is_vendor,
        "sponsor": current_user.is_sponsor,
    }

    if form.validate_on_submit():
        current_user.username = form.username.data or None
        current_user.first_name = form.first_name.data or None
        current_user.last_name = form.last_name.data or None
        current_user.title = form.title.data or None
        current_user.phone = form.phone.data or None
        current_user.newsletter_opt_in = bool(form.newsletter_opt_in.data)
        current_user.marketing_opt_in = bool(form.marketing_opt_in.data)

        # Save preference-style fields in the JSON column
        preferences.update(
            {
                "event_focus": form.event_focus.data or [],
                "preferred_locations": form.preferred_locations.data or "",
                "event_interests": form.event_interests.data or "",
            }
        )
        current_user.set_preferences(preferences)

        # Role toggles
        current_user.is_event_creator = bool(form.enable_event_creator.data)
        current_user.is_organizer = bool(form.enable_organizer.data)
        current_user.is_vendor = bool(form.enable_vendor.data)
        current_user.is_sponsor = bool(form.enable_sponsor.data)

        # Organizers can always create events
        if current_user.is_organizer and not current_user.is_event_creator:
            current_user.is_event_creator = True

        # Social links
        current_user.facebook_url = form.facebook_url.data or None
        current_user.instagram_url = form.instagram_url.data or None
        current_user.twitter_url = form.twitter_url.data or None
        current_user.linkedin_url = form.linkedin_url.data or None
        current_user.tiktok_url = form.tiktok_url.data or None

        # Organizer profile (only update when organizer is enabled)
        if current_user.is_organizer:
            current_user.company_name = form.company_name.data or None
            current_user.organizer_description = form.organizer_description.data or None
            current_user.organizer_website = form.organizer_website.data or None
            current_user.business_street = form.business_street.data or None
            current_user.business_city = form.business_city.data or None
            current_user.business_state = form.business_state.data or None
            current_user.business_zip = form.business_zip.data or None
            current_user.business_phone = form.business_phone.data or None
            current_user.business_email = form.business_email.data or None
            current_user.advertising_opportunities = (
                form.advertising_opportunities.data or None
            )

        # Vendor profile
        if current_user.is_vendor:
            current_user.vendor_type = form.vendor_type.data or None
            current_user.vendor_description = form.vendor_description.data or None

        # Sponsorship preferences (shared between organizer + sponsor views)
        if current_user.is_sponsor or current_user.is_organizer:
            current_user.sponsorship_opportunities = (
                form.sponsorship_opportunities.data or None
            )

        if any(
            previous_roles[key] != getattr(current_user, f"is_{key}")
            for key in previous_roles
        ):
            current_user.roles_last_updated = datetime.utcnow()

        try:
            db.session.add(current_user)
            db.session.commit()
            flash("Profile updated successfully.", "success")
            return redirect(url_for("profile"))
        except Exception as exc:  # noqa: BLE001
            logger.error(f"Error updating profile: {exc}", exc_info=True)
            db.session.rollback()
            flash("Could not update profile. Please try again.", "danger")

    if form.errors:
        flash("Please fix the highlighted fields before saving.", "warning")

    return render_template("edit_profile.html", form=form, chapters=chapters)

def about(): return render_template('about.html', chapters=Chapter.query.all())
def contact(): return render_template('contact.html', form=ContactForm(), chapters=Chapter.query.all())
def help(): return render_template('help_center.html', chapters=Chapter.query.all(), help_articles=HelpArticle.query.all())
def terms(): return render_template('terms.html', chapters=Chapter.query.all())
def privacy(): return render_template('privacy.html', chapters=Chapter.query.all())
def definitions(): return render_template('definitions.html', chapters=Chapter.query.all())
def chapters_page(): return render_template('chapters.html', chapters=Chapter.query.all())
def chapter(slug): return render_template('chapter.html', chapter=Chapter.query.filter_by(slug=slug).first_or_404(), chapters=Chapter.query.all())
def fun_assistant_page(): return render_template('partials/fun_assistant.html', chapters=Chapter.query.all())

def fun_assistant_chat():
    data = request.get_json()
    return jsonify({"reply": "AI Chat is currently in maintenance mode while we upgrade the engines."})

def analyze_event():
    # ... (Analysis logic using call_ai_with_fallback)
    return jsonify({"success": False, "error": "Endpoint in maintenance"})

def admin_dashboard():
    return render_template('admin_dashboard.html', chapters=Chapter.query.all(), stats={}, events=[], recent_activity=[])


@login_required
@admin_required
def run_seed_script():
    """Trigger the seed script from an authenticated admin session."""
    try:
        from seed import seed as run_seed  # Imported here to avoid circular imports during app setup

        result = run_seed(current_app._get_current_object()) or {}
        return jsonify({
            "status": "success",
            "seeded_events": result.get("events"),
            "seeded_chapters": result.get("chapters"),
        }), 200
    except Exception as exc:  # noqa: BLE001
        logger.error(f"Error running seed script: {exc}", exc_info=True)
        db.session.rollback()
        return jsonify({"status": "error", "message": "Failed to run seed script"}), 500

def api_health_check(): return "", 200
def health_check(): return jsonify({"status": "healthy"}), 200
def submit_feedback(): return jsonify({"status": "success"}), 200
def search(): return render_template("search.html", form=SearchForm(), chapters=Chapter.query.all())

def sitemap():
    """Generate an XML sitemap for search engines."""
    today = datetime.utcnow().date().isoformat()

    static_pages = [
        {"loc": url_for('index', _external=True), "changefreq": "daily", "priority": 1.0, "lastmod": today},
        {"loc": url_for('map', _external=True), "changefreq": "daily", "priority": 0.9, "lastmod": today},
        {"loc": url_for('events', _external=True), "changefreq": "daily", "priority": 0.9, "lastmod": today},
        {"loc": url_for('chapters_page', _external=True), "changefreq": "weekly", "priority": 0.7, "lastmod": today},
        {"loc": url_for('venues', _external=True), "changefreq": "weekly", "priority": 0.7, "lastmod": today},
        {"loc": url_for('about', _external=True), "changefreq": "monthly", "priority": 0.5, "lastmod": today},
        {"loc": url_for('contact', _external=True), "changefreq": "monthly", "priority": 0.5, "lastmod": today},
        {"loc": url_for('help', _external=True), "changefreq": "monthly", "priority": 0.5, "lastmod": today},
        {"loc": url_for('fun_assistant_page', _external=True), "changefreq": "weekly", "priority": 0.6, "lastmod": today},
        {"loc": url_for('terms', _external=True), "changefreq": "yearly", "priority": 0.3, "lastmod": today},
        {"loc": url_for('privacy', _external=True), "changefreq": "yearly", "priority": 0.3, "lastmod": today},
        {"loc": url_for('definitions', _external=True), "changefreq": "yearly", "priority": 0.3, "lastmod": today},
    ]

    chapter_urls = []
    for chapter in Chapter.query.filter_by(is_active=True).order_by(Chapter.name.asc()).all():
        chapter_lastmod = chapter.created_at.date().isoformat() if chapter.created_at else today
        chapter_urls.append({
            "loc": url_for('chapter', slug=chapter.slug, _external=True),
            "changefreq": "weekly",
            "priority": 0.6,
            "lastmod": chapter_lastmod
        })

    event_urls = []
    approved_events = (
        Event.query.filter(func.lower(Event.status) == 'approved', Event.is_public_event.is_(True))
        .order_by(Event.start_date.desc())
        .limit(2000)
        .all()
    )
    for event in approved_events:
        lastmod_source = event.end_date or event.start_date or event.created_at
        lastmod = lastmod_source.date().isoformat() if lastmod_source else None
        event_urls.append({
            "loc": url_for('event_detail', event_id=event.id, _external=True),
            "changefreq": "weekly",
            "priority": 0.5,
            "lastmod": lastmod
        })

    sitemap_xml = render_template("sitemap.xml", pages=static_pages, chapter_urls=chapter_urls, event_urls=event_urls)
    return Response(sitemap_xml, mimetype="application/xml")

def register_ai_governance_routes(app):
    pass

def init_routes(app):
    csrf = CSRFProtect(app)
    csrf.exempt(run_seed_script)
    app.route("/")(index)
    app.route("/map")(map)
    app.route("/events")(events)
    app.route("/events/mine")(my_events)
    app.route("/events/<int:event_id>")(event_detail)
    app.route("/events/<int:event_id>/edit", methods=["GET", "POST"])(edit_event)
    app.route("/admin/recompute-funalytics/<int:event_id>", methods=["POST"])(admin_recompute_funalytics)
    app.route("/submit-event", methods=["GET", "POST"])(submit_event)
    app.route('/login', methods=['GET', 'POST'])(login)
    app.route('/logout')(logout)
    app.route('/signup', methods=['GET', 'POST'])(signup)
    app.route("/reset-password-request", methods=["GET", "POST"])(reset_password_request)
    app.route("/reset-password/<token>", methods=["GET", "POST"])(reset_password)
    app.route('/profile')(profile)
    app.route('/profile/edit', methods=['GET', 'POST'])(edit_profile)
    app.route('/about')(about)
    app.route('/contact', methods=['GET', 'POST'])(contact)
    app.route('/help')(help)
    app.route('/terms')(terms)
    app.route('/privacy')(privacy)
    app.route('/definitions')(definitions)
    app.route('/chapters')(chapters_page)
    app.route('/chapter/<string:slug>')(chapter)
    app.route('/change-password', methods=['GET', 'POST'])(change_password)
    app.route('/venues')(venues)
    app.route('/venues/add', methods=['GET', 'POST'])(add_venue)
    app.route('/venues/my')(my_venues)
    app.route('/venues/<int:venue_id>')(venue_detail)
    app.route('/venues/<int:venue_id>/edit', methods=['GET', 'POST'])(edit_venue)
    app.route('/venues/<int:venue_id>/claim', methods=['POST'])(claim_venue)
    app.route('/fun-assistant')(fun_assistant_page)
    app.route('/api', methods=['GET', 'HEAD'])(api_health_check)
    app.route('/health', methods=['GET'])(health_check)
    app.route('/api/fun-assistant/chat', methods=['POST'])(fun_assistant_chat)
    app.route('/api/analyze-event', methods=['POST'])(analyze_event)
    app.route('/sitemap.xml')(sitemap)
    app.route('/admin/seed', methods=['POST'])(run_seed_script)
    app.route('/admin/dashboard')(admin_dashboard)
    app.route("/api/feedback", methods=['POST'])(submit_feedback)
    app.route("/search", methods=["GET", "POST"])(search)
    return app
