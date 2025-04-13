from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField, PasswordField, SubmitField, BooleanField, TextAreaField,
    DateField, TimeField, SelectField, FloatField, SelectMultipleField,
    IntegerField, RadioField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, ValidationError, 
    Regexp, Optional, URL, NumberRange
)
from models import User, ProhibitedAdvertiserCategory

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Please enter your email address"),
        Email(message="Please enter a valid email address"),
        Length(max=120, message="Email address is too long")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Please enter your password"),
        Length(min=8, max=128, message="Password must be between 8 and 128 characters long"),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]+$',
               message="Password must contain at least one letter, one number, and one special character")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('password', message='Passwords do not match. Please try again.')
    ])
    primary_role = RadioField(
        'What is your primary reason for joining FunList.ai?', 
        validators=[DataRequired()],
        choices=[
            ('attendee', 'Find events to attend'),
            ('organizer', 'Create, list, or promote events'),
            ('venue', 'Represent an organization or venue that hosts events'),
            ('vendor', 'Offer services for events (e.g., catering, AV, entertainment)'),
            ('sponsor', 'Explore advertising or sponsorship opportunities')
        ]
    )
    terms_accepted = BooleanField('I accept the <a href="/terms" target="_blank">Terms and Conditions</a> and <a href="/privacy" target="_blank">Privacy Policy</a>', validators=[
        DataRequired(message="You must accept the Terms and Conditions and Privacy Policy to continue")
    ])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('An account with this email already exists. Please use a different email or try logging in.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Please enter your email address"),
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Please enter your password")
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ProfileForm(FlaskForm):
    # Personal Information
    first_name = StringField('First Name', validators=[Optional(), Length(max=50)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=50)])
    title = StringField('Your Title', validators=[Optional(), Length(max=100)])
    event_focus = SelectMultipleField(
        "Tell Us About Yourself", 
        choices=[
            ('single', 'Single (18+)'),
            ('senior', 'Senior'),
            ('professional', 'Professional'),
            ('parent', 'Parent'),
            ('adult', 'Adult'),
            ('family', 'Family'),
            ('21+', '21+')
        ],
        validators=[Optional()],
        description="Select all that apply to help us recommend events for you"
    )
    preferred_locations = StringField(
        "Preferred Locations",
        description="Enter up to 5 cities, separated by commas",
        validators=[Optional(), Length(max=255)]
    )
    event_interests = StringField(
        "Event Interests",
        description="Enter interests separated by commas (e.g., sports,music,outdoors)",
        validators=[Optional(), Length(max=255)]
    )

    # Social Media Links
    facebook_url = StringField('Facebook URL', validators=[Optional(), URL()])
    instagram_url = StringField('Instagram URL', validators=[Optional(), URL()])
    twitter_url = StringField('Twitter URL', validators=[Optional(), URL()])
    linkedin_url = StringField('LinkedIn URL', validators=[Optional(), URL()])
    tiktok_url = StringField('TikTok URL', validators=[Optional(), URL()])

    # Organizer Information
    company_name = StringField('Organization/Company Name', validators=[Optional(), Length(max=100)])
    organizer_description = TextAreaField('About Your Organization', validators=[Optional(), Length(max=500)])
    organizer_website = StringField('Website', validators=[Optional(), URL()])
    business_street = StringField('Street Address', validators=[Optional(), Length(max=100)])
    business_city = StringField('City', validators=[Optional(), Length(max=50)])
    business_state = StringField('State', validators=[Optional(), Length(max=50)])
    business_zip = StringField('ZIP Code', validators=[Optional(), Length(max=20)])
    business_phone = StringField('Business Phone', validators=[Optional(), Length(max=20)])
    business_email = StringField('Business Email', validators=[Optional(), Email(), Length(max=120)])
    
    # Vendor Information
    vendor_type = SelectField('Vendor Type', choices=[
        ('food', 'Food Vendor'),
        ('alcohol', 'Alcohol Vendor'),
        ('sound', 'Sound and Audio'),
        ('print', 'Printing Services'),
        ('entertainment', 'Entertainer (Magician, Clown, etc.)'),
        ('face_paint', 'Face Painter'),
        ('music', 'Live Music Performer'),
        ('photography', 'Photography/Videography'),
        ('decor', 'Decoration Services'),
        ('other', 'Other')
    ], validators=[Optional()])
    vendor_description = TextAreaField('About Your Vendor Services', validators=[Optional(), Length(max=500)])
    
    # Sponsor Information
    sponsorship_interests = TextAreaField('Sponsorship Interests', validators=[Optional(), Length(max=500)])
    sponsorship_budget = StringField('Sponsorship Budget Range', validators=[Optional(), Length(max=100)])
    
    submit = SubmitField('Update Profile')

    def validate_username(self, username):
        if username.data:
            user = User.query.filter_by(username=username.data).first()
            if user and user.id != self.user_id:
                raise ValidationError('This username is already taken. Please choose another one.')

class VenueForm(FlaskForm):
    name = StringField('Venue Name', validators=[DataRequired()])
    street = StringField('Street Address')
    city = StringField('City')
    state = StringField('State')
    zip_code = StringField('ZIP Code')
    country = StringField('Country', default='United States')
    phone = StringField('Phone Number', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    website = StringField('Website URL', validators=[Optional(), URL()])
    venue_type_id = SelectField('Venue Type', coerce=int, validators=[Optional()])
    contact_name = StringField('Contact Person Name')
    contact_phone = StringField('Contact Phone')
    contact_email = StringField('Contact Email', validators=[Optional(), Email()])
    description = TextAreaField('Description')
    is_owner_manager = BooleanField('I am an owner, manager, or authorized representative of this venue')
    submit = SubmitField('Save Venue')

    def __init__(self, *args, **kwargs):
        super(VenueForm, self).__init__(*args, **kwargs)
        try:
            from models import VenueType
            self.venue_type_id.choices = [(0, 'Select Venue Type')] + [
                (vt.id, vt.name) for vt in VenueType.query.order_by(VenueType.name).all()
            ]
        except:
            self.venue_type_id.choices = []

class EventForm(FlaskForm):
    title = StringField('Event Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[Optional()])
    all_day = BooleanField('All Day Event')
    start_time = TimeField('Start Time', format='%H:%M', validators=[Optional()])
    end_time = TimeField('End Time', format='%H:%M', validators=[Optional()])

    venue_selection_type = RadioField('Venue', choices=[
        ('existing', 'Select Existing Venue'),
        ('new', 'Add New Venue')
    ], default='existing')

    venue_id = SelectField('Select Venue', coerce=int, validators=[Optional()], default=0)

    venue_name = StringField('Venue Name', validators=[Optional()])
    venue_street = StringField('Venue Street Address', validators=[Optional()])
    venue_city = StringField('Venue City', validators=[Optional()])
    venue_state = StringField('Venue State', validators=[Optional()])
    venue_zip = StringField('Venue ZIP Code', validators=[Optional()])
    venue_type_id = SelectField('Venue Type', coerce=int, validators=[Optional()])
    use_new_venue = BooleanField('Add this as a new venue')
    is_venue_owner = BooleanField('I am an owner, manager, or authorized representative of this venue')

    street = StringField('Street Address', validators=[Optional()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('ZIP Code', validators=[DataRequired()])

    category = SelectField('Event Category', choices=[
        ('', 'Select Category'),
        ('Sports', 'Sports'),
        ('Music', 'Music'),
        ('Arts & Theater', 'Arts & Theater'),
        ('Food & Drink', 'Food & Drink'),
        ('Family & Kids', 'Family & Kids'),
        ('Community', 'Community'),
        ('Business', 'Business'),
        ('Education', 'Education'),
        ('Other', 'Other')
    ], validators=[DataRequired()])

    target_audience = StringField('Target Audience', validators=[Optional()])
    fun_meter = RadioField('Fun Meter (1-5)', choices=[
        ('1', '1 - Not Fun'),
        ('2', '2 - Somewhat Fun'),
        ('3', '3 - Fun'),
        ('4', '4 - Very Fun'),
        ('5', '5 - Extremely Fun')
    ], validators=[DataRequired()], default='3')

    is_recurring = BooleanField('This is a recurring event')
    recurrence_type = SelectField('Recurrence Type', choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom')
    ], validators=[Optional()])
    recurring_pattern = SelectField('Recurring Pattern', choices=[
        ('', 'Select Pattern'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    ], validators=[Optional()])
    recurring_end_date = DateField('Recurring Until', format='%Y-%m-%d', validators=[Optional()])
    recurrence_end_date = DateField('Recurring Until', format='%Y-%m-%d', validators=[Optional()])

    is_sub_event = BooleanField('This is a sub-event of another event')
    parent_event = SelectField('Parent Event', choices=[], validators=[Optional()])

    ticket_url = StringField('Ticket URL', validators=[Optional(), URL()])
    network_opt_out = BooleanField('Opt out of the event network')

    prohibited_advertisers = SelectMultipleField('Prohibited Advertiser Categories', coerce=int)
    
    terms_accepted = BooleanField('I accept the Terms and Conditions')
    
    submit = SubmitField('Submit Event')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        try:
            from models import ProhibitedAdvertiserCategory
            categories = ProhibitedAdvertiserCategory.query.all()
            self.prohibited_advertisers.choices = [(c.id, c.name) for c in categories]
        except Exception as e:
            self.prohibited_advertisers.choices = []

        try:
            from models import Venue
            venues = Venue.query.order_by(Venue.name).all()
            self.venue_id.choices = [(0, 'Select a Venue')] + [(v.id, v.name) for v in venues]
        except Exception as e:
            self.venue_id.choices = [(0, 'Select a Venue')]

        try:
            from models import VenueType
            venue_types = VenueType.query.order_by(VenueType.name).all()
            self.venue_type_id.choices = [(0, 'Select Venue Type')] + [(vt.id, vt.name) for vt in venue_types]
        except Exception as e:
            self.venue_type_id.choices = [(0, 'Select Venue Type')]


class OrganizerProfileForm(FlaskForm):
    company_name = StringField('Organization/Company Name', validators=[Optional(), Length(max=100)])
    description = TextAreaField('About Your Organization', validators=[Optional(), Length(max=500)])
    website = StringField('Website', validators=[Optional(), URL()])
    submit = SubmitField('Save Organizer Profile')

class VendorProfileForm(FlaskForm):
    vendor_type = SelectField('Vendor Type', choices=[
        ('food', 'Food Vendor'),
        ('alcohol', 'Alcohol Vendor'),
        ('sound', 'Sound and Audio'),
        ('print', 'Printing Services'),
        ('entertainment', 'Entertainer (Magician, Clown, etc.)'),
        ('face_paint', 'Face Painter'),
        ('music', 'Live Music Performer'),
        ('photography', 'Photography/Videography'),
        ('decor', 'Decoration Services'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    description = TextAreaField('About Your Vendor Services', validators=[Optional(), Length(max=500)])
    website = StringField('Website', validators=[Optional(), URL()])
    services = TextAreaField('Services Offered', validators=[Optional(), Length(max=500)])
    pricing = TextAreaField('Pricing Information', validators=[Optional(), Length(max=300)])
    submit = SubmitField('Save Vendor Profile')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Please enter your email address"),
        Email(message="Please enter a valid email address")
    ])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(message="Please enter your new password"),
        Length(min=8, max=128, message="Password must be between 8 and 128 characters long"),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]+$',
               message="Password must contain at least one letter, one number, and one special character")
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message="Please confirm your new password"),
        EqualTo('password', message='Passwords do not match. Please try again.')
    ])
    submit = SubmitField('Reset Password')

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[
        DataRequired(message="Please enter your name"),
        Length(max=100, message="Name must be less than 100 characters")
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message="Please enter your email address"),
        Email(message="Please enter a valid email address"),
        Length(max=120, message="Email address is too long")
    ])
    subject = StringField('Subject', validators=[
        DataRequired(message="Please enter a subject"),
        Length(max=100, message="Subject must be less than 100 characters")
    ])
    category = SelectField('Inquiry Category', choices=[
        ('general', 'General Inquiry'),
        ('technical', 'Technical Support'),
        ('billing', 'Billing'),
        ('partnership', 'Partnership'),
        ('privacy', 'Privacy')
    ], validators=[DataRequired(message="Please select a category")])
    message = TextAreaField('Message', validators=[
        DataRequired(message="Please enter your message"),
        Length(min=10, max=2000, message="Message must be between 10 and 2000 characters")
    ])
    submit = SubmitField('Send Message')