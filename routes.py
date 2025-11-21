import os
import logging
import requests
from flask import render_template, flash, redirect, url_for, request, session, jsonify, current_app
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from forms import (SignupForm, LoginForm, ProfileForm, EventForm,
                   ResetPasswordRequestForm, ResetPasswordForm, ContactForm, SearchForm) # Added ContactForm, SearchForm
from models import User, Event, Subscriber, Chapter, HelpArticle # Added HelpArticle
from db_init import db
# Removed direct import of geocode_address, assume it's in utils.utils now
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime, timedelta
import json
import openai # Import OpenAI library
import anthropic # Import Anthropic library - using python_anthropic integration
from google import genai # Import Google Gemini - using python_gemini integration
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
        api_base_url = os.environ.get('EXPRESS_API_URL')
        if not api_base_url:
            logger.warning("EXPRESS_API_URL not configured, skipping Funalytics")
            return {}
        
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
        try:
            funalytics_scores = get_funalytics_scores()
            logger.info(f"Fetched Funalytics scores for {len(funalytics_scores)} events")
            
            # Attach Funalytics scores to events
            for event in events:
                score_data = funalytics_scores.get(event.id)
                if score_data:
                    logger.debug(f"Event {event.id} Funalytics: {score_data}")
                event.funalytics = score_data
        except Exception as funalytics_error:
            logger.warning(f"Failed to fetch Funalytics scores: {str(funalytics_error)}")
            # Continue without Funalytics if the service is unavailable
            for event in events:
                event.funalytics = None
        
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
    
    # Check if user is a returning visitor
    is_returning_user = request.cookies.get('returning_user') == 'true'
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password_hash and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            
            # Set cookie to mark as returning user
            response = redirect(request.args.get('next') or url_for('index'))
            response.set_cookie('returning_user', 'true', max_age=31536000)  # 1 year
            return response
        flash('Invalid email or password', 'danger')
    
    return render_template('login.html', form=form, chapters=chapters, is_returning_user=is_returning_user)

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

        # Smart AI fallback handles all API key configuration internally

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

            current_app.logger.debug(f"Sending prompt to AI: {prompt}")

            # --- Smart AI Fallback System: Anthropic → OpenAI → Gemini ---
            assistant_reply = call_ai_with_fallback(
                system_message="You are Fun Assistant, helping users find fun local events.",
                user_message=prompt,
                max_tokens=300
            )

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

        # Call AI for analysis using smart fallback system
        try:
            ai_response = call_ai_with_fallback(
                system_message="You are an expert event analyst for FunList.ai. Provide accurate, helpful analysis in the requested JSON format.",
                user_message=analysis_prompt,
                max_tokens=500,
                response_format="json"
            )
            
            # Parse AI response with error handling
            try:
                analysis_result = json.loads(ai_response)
            except json.JSONDecodeError as e:
                current_app.logger.error(f"Failed to parse AI response as JSON: {str(e)}")
                return jsonify({"success": False, "error": "AI response format error"}), 500
                
            # Define event_data for contextual intelligence
            event_data = {
                'title': title,
                'description': description,
                'category': category,
                'target_audience': target_audience,
                'city': city,
                'state': state
            }
            
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
            
            # Enhance with contextual intelligence
            enhanced_analysis = enhance_with_contextual_intelligence(analysis_result, event_data)
            
            return jsonify({
                "success": True,
                "analysis": enhanced_analysis,
                "funalytics": {
                    "communityVibe": enhanced_analysis['communityVibe']['score'],
                    "familyFun": enhanced_analysis['familyFun']['score'],
                    "overallScore": enhanced_analysis['overallScore'],
                    "reasoning": f"Community: {enhanced_analysis['communityVibe']['reasoning']} | Family: {enhanced_analysis['familyFun']['reasoning']}"
                }
            })
            
        except Exception as ai_error:
            current_app.logger.error(f"AI Analysis Error: {str(ai_error)}")
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

@login_required
@admin_required
def add_venue():
    """Route for adding a new venue"""
    from forms import VenueForm  # Import if exists, or create placeholder
    chapters = Chapter.query.all()
    # TODO: Implement venue creation logic
    return render_template('add_venue.html', chapters=chapters)

@login_required
def venues():
    """Route for viewing venues"""
    chapters = Chapter.query.all()
    # TODO: Fetch venues from database
    venues = []
    return render_template('venues.html', venues=venues, chapters=chapters)

# --- Other Routes (Placeholder/Keep Existing) ---
@login_required
@admin_required
def admin_dashboard():
     # ... (Keep existing logic) ...
     chapters = Chapter.query.all()
     # Fetch necessary data for the admin dashboard
     stats = { "pending_events": 0, "total_users": 0, "todays_events": 0, "new_users_24h": 0} # Placeholder
     events = [] # Placeholder
     users = [] # Placeholder
     events_by_category = {"labels": [], "datasets": [{"data":[]}]} # Placeholder
     user_growth_data = {"labels": [], "datasets": [{"label": "New Users", "data":[]}]} # Placeholder
     return render_template('admin_dashboard.html', chapters=chapters, stats=stats, events=events, users=users, status='pending', events_by_category=events_by_category, user_growth_data=user_growth_data)

# Add other routes from your previous routes.py here, ensuring imports are correct
# ... e.g., /marketplace, /admin/users, /api/feedback, /search, etc. ...

# API Health Check Endpoint - Ultra lightweight to handle flooding
def api_health_check():
    """Ultra lightweight health check to handle monitoring floods"""
    return "", 200

def health_check():
    """
    Health check endpoint for Google Cloud Run monitoring.
    Returns JSON with application status and database connectivity.
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "funlist-app",
        "checks": {
            "application": "ok"
        }
    }
    
    # Check database connectivity
    try:
        # Execute a simple query to verify database connection
        db.session.execute('SELECT 1')
        health_status["checks"]["database"] = "ok"
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["checks"]["database"] = f"error: {str(e)[:100]}"
        logger.error(f"Database health check failed: {str(e)}")
    
    # Return appropriate status code
    status_code = 200 if health_status["status"] == "healthy" else 503
    return jsonify(health_status), status_code

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
    
    # Register OAuth blueprints
    try:
        from google_auth import google_auth
        from github_auth import github_auth
        app.register_blueprint(google_auth)
        app.register_blueprint(github_auth)
        print("✅ OAuth blueprints registered successfully (Google + GitHub)")
    except ImportError as e:
        print(f"⚠️ OAuth blueprints not available: {str(e)}")
    except Exception as e:
        print(f"⚠️ OAuth blueprints registration failed: {str(e)}")
    
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
    app.route('/api', methods=['GET', 'HEAD'])(api_health_check)
    app.route('/health', methods=['GET'])(health_check)
    app.route('/api/fun-assistant/chat', methods=['POST'])(fun_assistant_chat)
    app.route('/api/analyze-event', methods=['POST'])(analyze_event)
    app.route('/admin/dashboard')(admin_dashboard)
    app.route('/add-venue', methods=['GET', 'POST'])(add_venue)
    app.route('/venues')(venues)
    app.route("/api/feedback", methods=['POST'])(submit_feedback)
    app.route("/search", methods=["GET", "POST"])(search)

    # Return the app instance
    return app


def enhance_with_contextual_intelligence(analysis_result, event_data):
    """
    Enhance AI analysis with contextual intelligence and success predictions
    """
    try:
        # Get contextual recommendations
        contextual_recommendations = get_contextual_recommendations(event_data)
        
        # Calculate success prediction score
        success_prediction = calculate_success_prediction(event_data, analysis_result)
        
        # Add smart suggestions for missing details
        smart_suggestions = get_smart_suggestions(event_data)
        
        # Enhance the analysis with additional intelligence - ensure defaults
        analysis_result.update({
            "contextualRecommendations": contextual_recommendations or [],
            "successPrediction": success_prediction or {"score": 50, "confidence": 60, "factors": {"overallReadiness": "analyzing"}},
            "smartSuggestions": smart_suggestions or [],
            "marketingTips": generate_marketing_tips(event_data, analysis_result) or []
        })
        
        return analysis_result
        
    except Exception as e:
        current_app.logger.error(f"Error enhancing with contextual intelligence: {str(e)}")
        # Return original analysis if enhancement fails
        return analysis_result


def get_contextual_recommendations(event_data):
    """
    Generate contextual recommendations based on event type and content
    """
    recommendations = []
    
    title = event_data.get('title', '').lower()
    description = event_data.get('description', '').lower()
    
    # Time-based recommendations
    if 'evening' in title or 'night' in title:
        recommendations.append({
            "type": "timing",
            "suggestion": "Evening events often benefit from mentioning lighting or atmosphere details",
            "priority": "medium"
        })
    
    # Family-focused recommendations
    if any(word in title + description for word in ['family', 'kids', 'children']):
        recommendations.append({
            "type": "family",
            "suggestion": "Consider mentioning age ranges and safety features to boost family appeal",
            "priority": "high"
        })
    
    # Music/Entertainment recommendations
    if any(word in title + description for word in ['music', 'concert', 'band', 'performance']):
        recommendations.append({
            "type": "entertainment",
            "suggestion": "Mention the music genre or performance style to attract the right audience",
            "priority": "medium"
        })
    
    # Food-related recommendations
    if any(word in title + description for word in ['food', 'dinner', 'lunch', 'restaurant']):
        recommendations.append({
            "type": "food",
            "suggestion": "Highlight dietary options (vegetarian, gluten-free) to increase accessibility",
            "priority": "high"
        })
    
    return recommendations[:3]  # Return top 3 recommendations


def calculate_success_prediction(event_data, analysis_result):
    """
    Calculate event success prediction based on various factors
    """
    score = 50  # Base score
    confidence = 60  # Base confidence
    
    # Title quality impact
    title_length = len(event_data.get('title', ''))
    if 20 <= title_length <= 60:
        score += 15
        confidence += 10
    elif title_length < 10:
        score -= 10
        confidence -= 5
    
    # Description quality impact
    description_length = len(event_data.get('description', ''))
    if description_length > 100:
        score += 20
        confidence += 15
    elif description_length < 50:
        score -= 15
        confidence -= 10
    
    # Use AI analysis scores if available
    if analysis_result.get('overallScore'):
        ai_score = int(analysis_result['overallScore'])
        score = int(score * 0.4 + ai_score * 12)  # Weight AI score heavily
        confidence = min(95, confidence + (ai_score * 2))
    
    # Ensure realistic bounds
    score = max(10, min(95, score))
    confidence = max(30, min(95, confidence))
    
    return {
        "score": score,
        "confidence": confidence,
        "factors": {
            "contentQuality": "high" if description_length > 100 else "medium" if description_length > 50 else "low",
            "titleOptimization": "good" if 20 <= title_length <= 60 else "needs_work",
            "overallReadiness": "ready" if score >= 70 else "needs_improvement" if score >= 50 else "major_revisions_needed"
        }
    }


def get_smart_suggestions(event_data):
    """
    Generate smart suggestions for missing or incomplete event details
    """
    suggestions = []
    
    title = event_data.get('title', '')
    description = event_data.get('description', '')
    
    # Check for missing key details
    if not any(word in description.lower() for word in ['time', 'when', 'start', 'begins']):
        suggestions.append({
            "type": "timing",
            "suggestion": "Add specific start time information to help attendees plan",
            "impact": "high"
        })
    
    if not any(word in description.lower() for word in ['location', 'where', 'address', 'venue']):
        suggestions.append({
            "type": "location",
            "suggestion": "Include specific venue or location details for better discoverability",
            "impact": "high"
        })
    
    if not any(word in description.lower() for word in ['free', 'cost', 'price', 'ticket', '$']):
        suggestions.append({
            "type": "pricing",
            "suggestion": "Mention if the event is free or include pricing information",
            "impact": "medium"
        })
    
    if len(description) < 100:
        suggestions.append({
            "type": "content",
            "suggestion": "Add more descriptive details about what attendees can expect",
            "impact": "high"
        })
    
    if not any(word in description.lower() for word in ['contact', 'info', 'questions', 'email']):
        suggestions.append({
            "type": "contact",
            "suggestion": "Include contact information for questions or more details",
            "impact": "medium"
        })
    
    return suggestions[:4]  # Return top 4 suggestions


def generate_marketing_tips(event_data, analysis_result):
    """
    Generate specific marketing tips based on event analysis
    """
    tips = []
    
    # Get scores from analysis
    community_score = analysis_result.get('communityVibe', {}).get('score', 3)
    family_score = analysis_result.get('familyFun', {}).get('score', 3)
    
    if community_score < 4:
        tips.append({
            "category": "community",
            "tip": "Emphasize social aspects like networking opportunities or group activities",
            "reason": "To boost your CommunityVibe™ score"
        })
    
    if family_score < 4:
        tips.append({
            "category": "family",
            "tip": "Highlight kid-friendly features, safety measures, or educational value",
            "reason": "To increase your FamilyFun™ appeal"
        })
    
    # General marketing tips
    title_length = len(event_data.get('title', ''))
    if title_length > 50:
        tips.append({
            "category": "title",
            "tip": "Consider shortening your title for better mobile readability",
            "reason": "Shorter titles perform better on social media"
        })
    
    description = event_data.get('description', '').lower()
    if 'fun' not in description and 'enjoy' not in description:
        tips.append({
            "category": "engagement",
            "tip": "Use engaging words like 'fun', 'exciting', or 'memorable' in your description",
            "reason": "Emotional language increases event appeal"
        })
    
    return tips[:3]  # Return top 3 tips


def call_ai_with_fallback(system_message, user_message, max_tokens=500, response_format="text"):
    """
    Smart AI system: Gemini 3.0 as PRIMARY → Anthropic → OpenAI as fallbacks
    
    # Using Gemini 3.0 (gemini-3-pro-preview) as the default AI model
    # This is Google's most powerful model for agentic workflows and complex reasoning
    # Fallback order: Gemini → Anthropic → OpenAI
    """
    
    # Validate at least one API key is configured
    if not any([os.environ.get("GEMINI_API_KEY"), os.environ.get("ANTHROPIC_API_KEY"), os.environ.get("OPENAI_API_KEY")]):
        current_app.logger.error("No AI API keys configured")
        if response_format == "json":
            return '{"error": "AI service not configured", "fallback": true}'
        return "AI assistant is temporarily unavailable. Please contact support."
    
    # Try Gemini 3.0 FIRST as the primary AI service
    try:
        current_app.logger.info("Attempting Gemini 3.0 API call (PRIMARY)...")
        gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        
        # Combine system and user messages for Gemini
        combined_prompt = f"{system_message}\n\nUser: {user_message}"
        
        if response_format == "json":
            response = gemini_client.models.generate_content(
                model="gemini-3-pro-preview",  # Gemini 3.0 - most powerful model
                contents=combined_prompt + "\n\nPlease respond with valid JSON format."
            )
        else:
            response = gemini_client.models.generate_content(
                model="gemini-3-pro-preview",  # Gemini 3.0 for all responses
                contents=combined_prompt
            )
        
        result = response.text or "I'm having trouble generating a response right now."
        current_app.logger.info("✅ Gemini 3.0 API call successful")
        return result
        
    except Exception as gemini_error:
        current_app.logger.warning(f"❌ Gemini API failed: {str(gemini_error)}")
        
        # Try Anthropic as second fallback
        try:
            current_app.logger.info("Attempting Anthropic API call as fallback...")
            anthropic_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
            
            if response_format == "json":
                response = anthropic_client.messages.create(
                    model="claude-sonnet-4-20250514",  # Latest Anthropic model
                    max_tokens=max_tokens,
                    system=system_message,
                    messages=[{"role": "user", "content": user_message}]
                )
            else:
                response = anthropic_client.messages.create(
                    model="claude-sonnet-4-20250514",  # Latest Anthropic model
                    max_tokens=max_tokens,
                    system=system_message,
                    messages=[{"role": "user", "content": user_message}]
                )
            
            result = response.content[0].text
            current_app.logger.info("✅ Anthropic API call successful")
            return result
            
        except Exception as anthropic_error:
            current_app.logger.warning(f"❌ Anthropic API failed: {str(anthropic_error)}")
            
            # Try OpenAI as final fallback
            try:
                current_app.logger.info("Attempting OpenAI API call as final fallback...")
                openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
                
                if response_format == "json":
                    response = openai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": user_message}
                        ],
                        response_format={"type": "json_object"},
                        max_tokens=max_tokens
                    )
                else:
                    response = openai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": user_message}
                        ],
                        max_tokens=max_tokens
                    )
                
                result = response.choices[0].message.content
                if result:
                    result = result.strip()
                else:
                    result = "No response generated"
                current_app.logger.info("✅ OpenAI API call successful")
                return result
                
            except Exception as openai_error:
                current_app.logger.error(f"❌ All AI services failed. OpenAI error: {str(openai_error)}")
                
                # Return fallback response if all APIs fail
                if response_format == "json":
                    return '{"error": "AI services temporarily unavailable", "fallback": true}'
                else:
                    return "I'm experiencing technical difficulties with my AI services. Please try again in a few moments."