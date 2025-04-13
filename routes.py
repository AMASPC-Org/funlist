import os
import logging
from flask import render_template, flash, redirect, url_for, request, session, jsonify
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from forms import (SignupForm, LoginForm, ProfileForm, EventForm,
                   ResetPasswordRequestForm, ResetPasswordForm, ContactForm, SearchForm) # Added ContactForm, SearchForm
from models import User, Event, Subscriber, Chapter, HelpArticle, CharterMember # Added HelpArticle, CharterMember
from db_init import db
# Removed direct import of geocode_address, assume it's in utils.utils now
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime, timedelta
import json
import openai # Import OpenAI library
from flask_wtf.csrf import CSRFProtect # Fixed CSRF import

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# --- Helper Decorators ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need admin privileges to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def chapter_leader_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need admin privileges to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def sponsor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_sponsor:
            flash('You need sponsor privileges to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def investor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_investor:
            flash('You need investor privileges to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Core Routes ---
def index():
    # Fetch chapters for the dropdown/links if needed on index
    chapters = Chapter.query.all()
    # Check if this is a new registration to show the wizard
    new_registration = session.pop('new_registration', False)
    return render_template("index.html", user=current_user, chapters=chapters, new_registration=new_registration)

def map():
    try:
        # Fetch events with valid coordinates for the map
        events = Event.query.filter(Event.latitude.isnot(None), Event.longitude.isnot(None)).all()
        chapters = Chapter.query.all() # Pass chapters if needed in base.html
        return render_template("map.html", events=events, chapters=chapters)
    except Exception as e:
        print(f"Error in map route: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"An error occurred: {str(e)}", 500

def events():
    app.logger.debug("Starting events route")
    try:
        # Implement filtering logic here later based on request args
        events = Event.query.order_by(Event.start_date.desc()).all()
        chapters = Chapter.query.all() # Pass chapters if needed in base.html
        return render_template("events.html", events=events, chapters=chapters)
    except Exception as e:
        app.logger.error(f"Error in events route: {str(e)}")
        app.logger.exception("Exception details:")
        return f"An error occurred: {str(e)}", 500

@login_required
def submit_event():
    if not current_user.is_event_creator: # Check the flag
        flash("You need to enable the 'Event Creator' role in your profile to add events.", "warning")
        return redirect(url_for('edit_profile')) # Redirect to profile to enable

    form = EventForm()
    # Populate venue choices (assuming Venue model exists)
    # form.existing_venue_id.query = Venue.query.order_by(Venue.name) # Example

    if form.validate_on_submit():
        # ... (existing logic for processing event and venue data) ...
        # Make sure to import and use geocode_address from utils
        # from utils.utils import geocode_address
        # coordinates = geocode_address(...)
        # ... create Event object ...
        # db.session.add(event)
        # db.session.commit()
        flash("Event submitted successfully!", "success")
        return redirect(url_for('events'))
    chapters = Chapter.query.all()
    return render_template("submit_event.html", form=form, chapters=chapters)

# --- Authentication Routes ---
def login():
    # ... (Keep existing login logic) ...
    chapters = Chapter.query.all()
    form = LoginForm() # Ensure form is initialized
    return render_template('auth/login.html', form=form, chapters=chapters)

@login_required
def logout():
   # ... (Keep existing logout logic) ...
   return redirect(url_for('login'))


def register():
    # ... (Keep existing registration logic using primary_role radio buttons) ...
    # Ensure you import MembershipTier, Chapter, Role, generate_password_hash
    form = SignupForm() # Ensure form is initialized
    # Populate choices dynamically if needed
    # form.membership_tier.choices = [...]
    # form.chapter_id.choices = [...]
    chapters = Chapter.query.all()
    return render_template('auth/register.html', form=form, chapters=chapters)

def reset_password_request():
     # ... (Keep existing logic) ...
     form = ResetPasswordRequestForm() # Ensure form is initialized
     chapters = Chapter.query.all()
     return render_template('reset_password_request.html', form=form, chapters=chapters)


def reset_password(token):
    # ... (Keep existing logic) ...
    form = ResetPasswordForm() # Ensure form is initialized
    chapters = Chapter.query.all()
    return render_template('reset_password.html', form=form, token=token, chapters=chapters)


# --- User Profile & Settings ---
@login_required
def profile():
     # Simple profile view page
     chapters = Chapter.query.all()
     return render_template('profile.html', user=current_user, chapters=chapters)

@login_required
def edit_profile():
     form = ProfileForm(obj=current_user) # Pre-populate form

     if request.method == 'POST':
         # Handle role activation
         role_to_activate = request.form.get('activate_role')
         if role_to_activate:
             if role_to_activate == 'organizer':
                 current_user.is_organizer = True
                 current_user.is_event_creator = True # Organizers can also create
             elif role_to_activate == 'vendor':
                 current_user.is_vendor = True
             elif role_to_activate == 'event_creator':
                  current_user.is_event_creator = True
             # Add other roles if needed (e.g., sponsor)

             try:
                 db.session.commit()
                 flash(f"Your {role_to_activate.capitalize()} features are now active! Please complete the relevant profile section below.", "success")
                 # Re-render the form to show new sections immediately
                 return render_template('edit_profile.html', form=form, chapters=Chapter.query.all())
             except Exception as e:
                 db.session.rollback()
                 logger.error(f"Error activating role: {str(e)}")
                 flash("Could not activate role. Please try again.", "danger")

         # Handle profile data submission if not activating role
         elif form.validate_on_submit():
             # Update standard profile fields
             current_user.username = form.username.data
             current_user.first_name = form.first_name.data
             current_user.last_name = form.last_name.data
             # ... (update other personal/social fields) ...

             # Update role flags based on checkboxes
             current_user.is_event_creator = form.enable_event_creator.data
             current_user.is_organizer = form.enable_organizer.data
             current_user.is_vendor = form.enable_vendor.data
             if current_user.is_organizer: # Ensure organizers can create events
                current_user.is_event_creator = True

             # Update organizer/vendor fields *if* role is enabled
             if current_user.is_organizer:
                 current_user.business_name = form.business_name.data
                 # ... (update other organizer fields) ...
             if current_user.is_vendor:
                  # current_user.vendor_type = form.vendor_type.data # Assuming vendor_type is added back later
                  pass # Add vendor field updates here

             try:
                 db.session.commit()
                 flash('Profile updated successfully!', 'success')
                 return redirect(url_for('profile')) # Redirect to view profile page
             except Exception as e:
                 db.session.rollback()
                 logger.error(f"Error updating profile: {str(e)}")
                 flash("Could not update profile. Please try again.", "danger")

     # Pre-populate checkboxes on GET request
     elif request.method == "GET":
         form.enable_event_creator.data = current_user.is_event_creator
         form.enable_organizer.data = current_user.is_organizer
         form.enable_vendor.data = current_user.is_vendor

     chapters = Chapter.query.all()
     return render_template('edit_profile.html', form=form, chapters=chapters)

# --- Static Pages & Other ---
def about():
    chapters = Chapter.query.all()
    return render_template('about.html', chapters=chapters)

def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # ... (Handle contact form submission - e.g., send email) ...
        flash('Thank you for your message!', 'success')
        return redirect(url_for('contact'))
    chapters = Chapter.query.all()
    return render_template('contact.html', form=form, chapters=chapters)

def help():
    chapters = Chapter.query.all()
    # Fetch FAQ articles if needed for the help template
    help_articles = HelpArticle.query.all()
    return render_template('help_center.html', chapters=chapters, help_articles=help_articles)

def terms():
    chapters = Chapter.query.all()
    return render_template('terms.html', chapters=chapters)

def privacy():
    chapters = Chapter.query.all()
    return render_template('privacy.html', chapters=chapters)

def definitions():
    chapters = Chapter.query.all()
    return render_template('definitions.html', chapters=chapters)

def chapters_page():
     chapters = Chapter.query.all()
     return render_template('chapters.html', chapters=chapters)

# --- DYNAMIC CHAPTER ROUTE ---
def chapter(slug):
    chapter = Chapter.query.filter_by(slug=slug).first_or_404()
    all_chapters = Chapter.query.all() # Needed for base template potentially

    # --- Placeholder for Trial Access Logic ---
    can_view_full_content = False
    if current_user.is_authenticated:
        # Option 1: Paid members get full access
        if current_user.membership_tier_id and current_user.membership_tier.price > 0:
             can_view_full_content = True
        # Option 2: Check for active trial pass (implement fully later)
        # elif user_has_active_trial(current_user):
        #    can_view_full_content = True
        pass # Add trial logic here

    # Pass can_view_full_content to the template
    return render_template('chapter.html', chapter=chapter, chapters=all_chapters, can_view_full_content=can_view_full_content)
    # ------------------------------------------

# --- Fun Assistant Routes ---
def fun_assistant_page():
    """Renders the dedicated Fun Assistant chat page."""
    chapters = Chapter.query.all() # Pass chapters if needed in base.html
    return render_template('partials/fun_assistant.html', chapters=chapters)

def fun_assistant_chat():
    app.logger.debug("Starting Fun Assistant chat processing")
    try:
        # Check if the user is logged in or track usage for anonymous users
        if not current_user.is_authenticated:
            # Initialize session counter if it doesn't exist
            if 'fun_assistant_uses' not in session:
                session['fun_assistant_uses'] = 0
                session['fun_assistant_reset_date'] = datetime.utcnow().strftime("%Y-%m")

            # Check if we need to reset the counter (new month)
            current_month = datetime.utcnow().strftime("%Y-%m")
            if session.get('fun_assistant_reset_date') != current_month:
                session['fun_assistant_uses'] = 0
                session['fun_assistant_reset_date'] = current_month

            # Increment the usage counter
            session['fun_assistant_uses'] += 1

            # Check if usage limit exceeded
            if session['fun_assistant_uses'] > 5:
                return jsonify({
                    "limit_exceeded": True,
                    "reply": "You've reached your free usage limit for the Fun Assistant this month. Sign up for a free account to continue using this feature and get personalized recommendations!"
                }), 200

        openai.api_key = os.environ.get("OPENAI_API_KEY")
        if not openai.api_key:
             logger.error("OpenAI API Key not found in environment variables.")
             return jsonify({"error": "AI Assistant configuration error."}), 500

        try:
            data = request.get_json()
            user_message = data.get('message')

            if not user_message:
                return jsonify({"error": "No message provided."}), 400

            # --- Gather Context for OpenAI ---
            # 1. User Info
            user_context = "Anonymous visitor (limited to 5 queries per month)"

            if current_user.is_authenticated:
                # Get detailed user profile information
                user_preferences = current_user.get_preferences()

                user_context = f"""
                Logged in user: {current_user.first_name or current_user.email}
                Interests: {current_user.event_interests or 'Not specified'}
                Location: {current_user.business_city or 'Not specified'}, {current_user.business_state or 'Not specified'}
                """

                # Add any additional preference info if available
                if user_preferences:
                    if 'preferred_locations' in user_preferences:
                        user_context += f"\nPreferred locations: {user_preferences.get('preferred_locations')}"
                    if 'event_focus' in user_preferences:
                        user_context += f"\nEvent focus: {user_preferences.get('event_focus')}"

                # Add user role information
                roles = []
                if current_user.is_event_creator:
                    roles.append("Event Creator")
                if current_user.is_organizer:
                    roles.append("Organizer")
                if current_user.is_vendor:
                    roles.append("Vendor")
                if roles:
                    user_context += f"\nUser roles: {', '.join(roles)}"

            # For non-logged in users, we'll use basic info
            user_interests = current_user.event_interests if current_user.is_authenticated else "general fun"
            user_location = current_user.business_city if current_user.is_authenticated and current_user.business_city else "their current area"

            # 2. Relevant Events - Fetch upcoming events
            current_date = datetime.utcnow().date()
            relevant_events = Event.query.filter(
                Event.start_date >= current_date
            ).order_by(Event.start_date).limit(15).all()

            # 3. Events with highest fun ratings
            top_rated_events = Event.query.filter(
                Event.start_date >= current_date,
                Event.fun_meter >= 4
            ).order_by(Event.fun_meter.desc()).limit(5).all()

            # Build event context for the prompt
            event_context = "\nUpcoming events:\n"
            if relevant_events:
                for event in relevant_events:
                     event_context += f"- {event.title} on {event.start_date.strftime('%Y-%m-%d')} at {event.location or 'Venue TBA'} (Fun Score: {event.fun_meter}/5): {event.description[:100]}...\n"
            else:
                event_context = "\nNo specific upcoming events found in the database right now.\n"

            if top_rated_events:
                event_context += "\nTop-rated events:\n"
                for event in top_rated_events:
                    if event not in relevant_events:  # Avoid duplicates
                        event_context += f"- {event.title} on {event.start_date.strftime('%Y-%m-%d')} at {event.location or 'Venue TBA'} (Fun Score: {event.fun_meter}/5): {event.description[:100]}...\n"

            # --- Construct Prompt ---
            prompt = f"""You are Fun Assistant, a friendly and helpful AI guide for the FunList.ai platform. Your goal is to help users discover fun local events based on their preferences.

            User Profile:
            {user_context}
            - Interests: {user_interests}
            - Location: {user_location}

            {event_context}

            User Query: "{user_message}"

            Based ONLY on the provided user profile and event context, answer the user's query. Recommend events from the list if they match the user's interests or location. If no listed events match, suggest general types of fun activities relevant to their interests. Mention the Fun Score when recommending specific events.

            If the user is not logged in, gently encourage them to create an account for more personalized recommendations while still providing useful information. 

            Your responses should be:
            1. Concise (about 2-3 short paragraphs)
            2. Friendly and enthusiastic 
            3. Focused on actual events in the database
            4. Personalized based on user interests if available
            5. Include specific event details when recommending (date, fun score)

            Do not invent events not listed above. If you don't have enough information, politely ask for clarification.
            """

            logger.debug(f"Sending prompt to OpenAI: {prompt}")

            # --- Call OpenAI API ---
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4", # Or your chosen model
                    messages=[
                        {"role": "system", "content": "You are Fun Assistant, helping users find fun local events."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300,  # Increased token limit for better responses
                    temperature=0.7  # Slightly more creative but still factual
                )
                assistant_reply = response.choices[0].message['content'].strip()
                logger.debug(f"Received reply from OpenAI: {assistant_reply}")

            except Exception as openai_error:
                 logger.error(f"OpenAI API Error: {str(openai_error)}")
                 assistant_reply = "Sorry, I encountered an issue connecting to my knowledge base. Please try again later."

            return jsonify({"reply": assistant_reply})

        except Exception as e:
            logger.error(f"Error in /api/fun-assistant/chat: {str(e)}", exc_info=True)
            return jsonify({"error": "An internal error occurred."}), 500
    except Exception as e:
        app.logger.error(f"Error in Fun Assistant chat: {str(e)}")
        app.logger.exception("Exception details:")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# --- Other Routes (Placeholder/Keep Existing) ---
@login_required
#@admin_required # Add decorator back once roles are solid
def admin_dashboard():
     # ... (Keep existing logic) ...
     chapters = Chapter.query.all()
     # Fetch necessary data for the admin dashboard
     stats = { "pending_events": 0, "total_users": 0, "todays_events": 0, "new_users_24h": 0} # Placeholder
     events = [] # Placeholder
     users = [] # Placeholder
     events_by_category = {"labels": [], "datasets": [{"data":[]}]} # Placeholder
     user_growth_data = {"labels": [], "datasets": [{"label": "New Users", "data":[]}]} # Placeholder
     return render_template('admin/dashboard.html', chapters=chapters, stats=stats, events=events, users=users, status='pending', events_by_category=events_by_category, user_growth_data=user_growth_data)

# Add other routes from your previous routes.py here, ensuring imports are correct
# ... e.g., /marketplace, /admin/users, /api/feedback, /search, etc. ...

def submit_feedback():
     # Implement feedback submission logic
     return jsonify({"status": "success"}), 200

def search():
     # ... (Keep existing logic, ensure HelpArticle is imported) ...
     form = SearchForm() # Ensure form is initialized
     chapters = Chapter.query.all()
     return render_template("search.html", form=form, results=[], query=None, chapters=chapters)

# Ensure all template paths use the 'main/' prefix where appropriate
# Example: render_template('main/about.html') instead of render_template('about.html')

def init_routes(app):
    """Initialize all routes with the Flask app instance"""
    csrf = CSRFProtect(app) #Initialize CSRF protection
    # Register all routes with the app instance
    app.route("/")(index)
    app.route("/map")(map)
    app.route("/events")(events)
    app.route("/submit-event", methods=["GET", "POST"])(submit_event)
    app.route('/login', methods=['GET', 'POST'])(login)
    app.route('/logout')(logout)
    app.route('/register', methods=['GET', 'POST'])(register)
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
    app.route('/fun-assistant')(fun_assistant_page)
    app.route('/api/fun-assistant/chat', methods=['POST'])(fun_assistant_chat)
    app.route('/admin/dashboard')(admin_dashboard)
    app.route("/api/feedback", methods=['POST'])(submit_feedback)
    app.route("/search", methods=["GET", "POST"])(search)

    # Return the app instance
    return app