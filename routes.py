import os
import logging
import requests
from flask import render_template, flash, redirect, url_for, request, session, jsonify, current_app
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
from flask_wtf.csrf import CSRFProtect # Use only CSRFProtect

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# --- Funalytics API Helper ---
def get_funalytics_scores(event_ids=None):
    """
    Fetch Funalytics scores from Express API.
    Returns a dictionary mapping event_id to funalytics data.
    """
    try:
        api_base_url = os.environ.get('EXPRESS_API_URL', 'http://localhost:3001')
        
        if event_ids:
            # For specific events, fetch all and filter
            response = requests.get(f"{api_base_url}/events", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('events'):
                    scores = {}
                    for event in data['events']:
                        if event['id'] in event_ids and 'funalytics' in event:
                            scores[event['id']] = event['funalytics']
                    return scores
            return {}
        else:
            # For all events, get from events endpoint
            response = requests.get(f"{api_base_url}/events", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('events'):
                    scores = {}
                    for event in data['events']:
                        if 'funalytics' in event:
                            scores[event['id']] = event['funalytics']
                    return scores
    except requests.RequestException as e:
        logger.warning(f"Failed to fetch Funalytics scores: {e}")
    
    return {}

def recompute_funalytics_score(event_id):
    """
    Call Express API to recompute Funalytics score for a specific event.
    Returns True if successful, False otherwise.
    """
    try:
        api_base_url = os.environ.get('EXPRESS_API_URL', 'http://localhost:3001')
        response = requests.post(f"{api_base_url}/funalytics/recompute/{event_id}", timeout=10)
        return response.status_code == 201
    except requests.RequestException as e:
        logger.error(f"Failed to recompute Funalytics for event {event_id}: {e}")
        return False

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
    # Check if this is a new signup to show the wizard
    new_signup = session.pop('new_signup', False)
    return render_template("index.html", user=current_user, chapters=chapters, new_signup=new_signup)

def map():
    logger.debug("Starting map route")
    try:
        # Implement filtering logic here later based on request args
        events = Event.query.all()
        chapters = Chapter.query.all() # Pass chapters if needed in base.html
        
        # Convert events to dictionary format for JavaScript
        events_for_map = [event.to_dict() for event in events]
        
        return render_template("map.html", events=events, events_json=events_for_map, chapters=chapters)
    except Exception as e:
        logger.error(f"Error in map route: {str(e)}")
        import traceback
        traceback.print_exc()
        return render_template("500.html", error=str(e)), 500

def events():
    logger.debug("Starting events route")
    try:
        # Implement filtering logic here later based on request args
        events = Event.query.order_by(Event.start_date.desc()).all()
        chapters = Chapter.query.all() # Pass chapters if needed in base.html
        
        # Fetch Funalytics scores for all events
        funalytics_scores = get_funalytics_scores()
        
        # Attach Funalytics scores to events
        for event in events:
            event.funalytics = funalytics_scores.get(event.id, None)
        
        return render_template("events.html", events=events, chapters=chapters)
    except Exception as e:
        logger.error(f"Error in events route: {str(e)}")
        logger.exception("Exception details:")
        return render_template("500.html", error=str(e)), 500
        
def event_detail(event_id):
    """Display details for a specific event."""
    try:
        event = Event.query.get_or_404(event_id)
        chapters = Chapter.query.all() # Pass chapters for base template
        
        # Fetch Funalytics scores for this specific event
        funalytics_scores = get_funalytics_scores([event_id])
        event.funalytics = funalytics_scores.get(event_id, None)
        
        return render_template("event_detail.html", event=event, chapters=chapters)
    except Exception as e:
        logger.error(f"Error in event_detail route: {str(e)}")
        return render_template("500.html", error=str(e)), 500

@login_required
@admin_required
def admin_recompute_funalytics(event_id):
    """Admin action to recompute Funalytics score for an event."""
    try:
        # Verify event exists
        event = Event.query.get_or_404(event_id)
        
        # Call Express API to recompute score
        success = recompute_funalytics_score(event_id)
        
        if success:
            flash(f"Funalytics score recomputed successfully for '{event.title}'!", "success")
        else:
            flash("Failed to recompute Funalytics score. Please try again.", "error")
            
    except Exception as e:
        logger.error(f"Error recomputing Funalytics for event {event_id}: {str(e)}")
        flash("An error occurred while recomputing the score.", "error")
    
    return redirect(url_for('event_detail', event_id=event_id))

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
    chapters = Chapter.query.all()
    form = LoginForm() # Ensure form is initialized
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password_hash and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Invalid email or password', 'danger')
    
    return render_template('login.html', form=form, chapters=chapters)

@login_required
def logout():
   # ... (Keep existing logout logic) ...
   return redirect(url_for('login'))


def signup():
    # Signup logic using primary_role radio buttons
    form = SignupForm()
    
    if form.validate_on_submit():
        # Create user with form data
        password_data = form.password.data
        if password_data:
            user = User(
                email=form.email.data,
                password_hash=generate_password_hash(password_data)
            )
        
        # Set roles based on primary_role selection
        if form.primary_role.data == 'organizer':
            user.is_organizer = True
            user.is_event_creator = True  # Organizers can also create events
        elif form.primary_role.data == 'event_creator':
            user.is_event_creator = True
        elif form.primary_role.data == 'vendor':
            user.is_vendor = True
            
        try:
            db.session.add(user)
            db.session.commit()
            
            # Log the user in
            login_user(user)
            
            # Set session flag to show onboarding wizard
            session['new_signup'] = True
            
            flash("Welcome to FunList.ai! Your account has been created.", "success")
            return redirect(url_for('index'))
        except IntegrityError:
            db.session.rollback()
            flash("An account with that email already exists.", "danger")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error during user signup: {str(e)}")
            flash("An error occurred during signup. Please try again.", "danger")
    
    chapters = Chapter.query.all()
    return render_template('signup.html', form=form, chapters=chapters)

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
    current_app.logger.debug("Starting Fun Assistant chat processing")
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
             current_app.logger.error("OpenAI API Key not found in environment variables.")
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

            current_app.logger.debug(f"Sending prompt to OpenAI: {prompt}")

            # --- Call OpenAI API ---
            try:
                openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
                response = openai_client.chat.completions.create(
                    model="gpt-4o-mini", # Using supported OpenAI model
                    messages=[
                        {"role": "system", "content": "You are Fun Assistant, helping users find fun local events."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300  # Correct parameter name
                )
                assistant_reply = response.choices[0].message.content.strip()
                current_app.logger.debug(f"Received reply from OpenAI: {assistant_reply}")

            except Exception as openai_error:
                 current_app.logger.error(f"OpenAI API Error: {str(openai_error)}")
                 assistant_reply = "Sorry, I encountered an issue connecting to my knowledge base. Please try again later."

            return jsonify({"reply": assistant_reply})

        except Exception as e:
            current_app.logger.error(f"Error in /api/fun-assistant/chat: {str(e)}", exc_info=True)
            return jsonify({"error": "An internal error occurred."}), 500
    except Exception as e:
        current_app.logger.error(f"Error in Fun Assistant chat: {str(e)}")
        current_app.logger.exception("Exception details:")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# --- Real-time Event Analysis API ---
def analyze_event():
    """
    Real-time AI analysis endpoint for event submissions.
    Analyzes event details and provides Funalytics scores with coaching suggestions.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No event data provided"}), 400
        
        # Extract event data
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        category = data.get('category', '').strip()
        target_audience = data.get('target_audience', '').strip()
        city = data.get('city', '').strip()
        state = data.get('state', '').strip()
        
        # Basic validation
        if not title or not description:
            return jsonify({
                "error": "Title and description are required for analysis",
                "success": False
            }), 400
        
        # Prepare analysis prompt for AI
        analysis_prompt = f"""
Analyze this event for FunList.ai and provide scoring and recommendations:

EVENT DETAILS:
Title: {title}
Description: {description}
Category: {category}
Target Audience: {target_audience}
Location: {city}, {state}

Please provide a JSON response with the following structure:
{{
    "communityVibe": {{
        "score": [0-10 integer],
        "reasoning": "Brief explanation for the score"
    }},
    "familyFun": {{
        "score": [0-10 integer], 
        "reasoning": "Brief explanation for the score"
    }},
    "overallScore": [0-10 integer],
    "suggestions": [
        "Specific actionable suggestion 1",
        "Specific actionable suggestion 2", 
        "Specific actionable suggestion 3"
    ],
    "missingDetails": [
        "Detail that would improve discoverability"
    ],
    "confidenceLevel": [0-100 integer]
}}

SCORING CRITERIA:
- CommunityVibe (0-10): Local flavor, community engagement, inclusivity, togetherness
- FamilyFun (0-10): Family-friendliness, kid activities, all-ages appeal
- Overall: Average of the two facets

Focus on actionable, specific suggestions that would improve the event's appeal and discoverability.
"""

        # Call OpenAI for analysis
        try:
            openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert event analyst for FunList.ai. Provide accurate, helpful analysis in the requested JSON format."},
                    {"role": "user", "content": analysis_prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=500
            )
            
            # Parse AI response
            analysis_result = json.loads(response.choices[0].message.content)
            
            # Ensure required fields exist and add defaults if missing
            analysis_result.setdefault('communityVibe', {'score': 5, 'reasoning': 'Analysis pending'})
            analysis_result.setdefault('familyFun', {'score': 5, 'reasoning': 'Analysis pending'})
            analysis_result.setdefault('overallScore', 5)
            analysis_result.setdefault('suggestions', [])
            analysis_result.setdefault('missingDetails', [])
            analysis_result.setdefault('confidenceLevel', 50)
            
            # Calculate overall score if not provided
            if 'overallScore' not in analysis_result:
                community_score = analysis_result['communityVibe'].get('score', 5)
                family_score = analysis_result['familyFun'].get('score', 5)
                analysis_result['overallScore'] = round((community_score + family_score) / 2)
            
            return jsonify({
                "success": True,
                "analysis": analysis_result,
                "funalytics": {
                    "communityVibe": analysis_result['communityVibe']['score'],
                    "familyFun": analysis_result['familyFun']['score'],
                    "overallScore": analysis_result['overallScore'],
                    "reasoning": f"Community: {analysis_result['communityVibe']['reasoning']} | Family: {analysis_result['familyFun']['reasoning']}"
                }
            })
            
        except Exception as ai_error:
            current_app.logger.error(f"OpenAI Analysis Error: {str(ai_error)}")
            # Provide fallback analysis
            return jsonify({
                "success": True,
                "analysis": {
                    "communityVibe": {"score": 6, "reasoning": "Standard community event"},
                    "familyFun": {"score": 5, "reasoning": "General audience appeal"},
                    "overallScore": 6,
                    "suggestions": [
                        "Add more specific details about activities",
                        "Mention any family-friendly elements",
                        "Include local community benefits"
                    ],
                    "missingDetails": ["Specific activities", "Target demographics"],
                    "confidenceLevel": 30
                },
                "funalytics": {
                    "communityVibe": 6,
                    "familyFun": 5, 
                    "overallScore": 6,
                    "reasoning": "AI analysis temporarily unavailable - using default scoring"
                }
            })
            
    except Exception as e:
        current_app.logger.error(f"Error in event analysis: {str(e)}")
        return jsonify({"error": "Analysis service temporarily unavailable", "success": False}), 500

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
    app.route("/events/<int:event_id>")(event_detail)
    app.route("/admin/recompute-funalytics/<int:event_id>", methods=["POST"])(admin_recompute_funalytics)
    app.route("/submit-event", methods=["GET", "POST"])(submit_event)
    app.route('/login', methods=['GET', 'POST'])(login)
    app.route('/logout')(logout)
    app.route('/register', methods=['GET', 'POST'])(signup)
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
    app.route('/fun-assistant')(fun_assistant_page)
    app.route('/api/fun-assistant/chat', methods=['POST'])(fun_assistant_chat)
    app.route('/api/analyze-event', methods=['POST'])(analyze_event)
    app.route('/admin/dashboard')(admin_dashboard)
    app.route("/api/feedback", methods=['POST'])(submit_feedback)
    app.route("/search", methods=["GET", "POST"])(search)

    # Return the app instance
    return app