from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField, PasswordField, SubmitField, BooleanField, TextAreaField,
    DateField, TimeField, SelectField, FloatField, SelectMultipleField,
    IntegerField
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
    is_event_creator = BooleanField('I want to create events')
    is_organizer = BooleanField('I represent an organization or venue')
    is_vendor = BooleanField('I am a vendor')
    vendor_type = SelectField('Vendor Type', choices=[
        ('', 'Select vendor type...'),
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
    username = StringField('Username', validators=[
        Optional(),
        Length(min=3, max=50, message="Username must be between 3 and 50 characters"),
        Regexp(r'^[\w.]+$', message="Username can only contain letters, numbers, dots, and underscores")
    ])
    first_name = StringField('First Name', validators=[Optional(), Length(max=50)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=50)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])
    location = StringField('Location', validators=[Optional(), Length(max=100)])
    interests = StringField('Interests', validators=[Optional(), Length(max=255)])
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
    birth_date = DateField('Birth Date', validators=[Optional()])
    submit = SubmitField('Update Profile')

    def validate_username(self, username):
        if username.data:
            user = User.query.filter_by(username=username.data).first()
            if user and user.id != self.user_id:
                raise ValidationError('This username is already taken. Please choose another one.')

class EventForm(FlaskForm):
    prohibited_advertisers = SelectMultipleField('Prohibited Advertisers',
        validators=[Optional()],
        coerce=int
    )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        try:
            self.prohibited_advertisers.choices = [
                (cat.id, cat.name) for cat in ProhibitedAdvertiserCategory.query.all()
            ]
        except:
            self.prohibited_advertisers.choices = []
    title = StringField('Title', validators=[DataRequired(), Length(max=150, message="Title must be less than 150 characters")])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[Optional()])
    end_time = TimeField('End Time', validators=[Optional()])
    all_day = BooleanField('All Day Event')

    # Recurring event fields
    is_recurring = BooleanField('Recurring Event')
    recurring_pattern = SelectField('Repeat', choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom')
    ], validators=[Optional()])
    recurring_end_date = DateField('Repeat Until', validators=[Optional()])

    # Sub-event fields
    is_sub_event = BooleanField('This is a sub-event')
    parent_event = SelectField('Parent Event', choices=[], validators=[Optional()])
    recurrence_type = SelectField('Recurrence Pattern', choices=[
        ('none', 'One-time Event'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
        ('custom', 'Custom')
    ])
    recurrence_interval = IntegerField('Repeat Every', validators=[Optional(), NumberRange(min=1)], default=1)
    recurrence_unit = SelectField('Recurrence Unit', choices=[
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months')
    ], validators=[Optional()])
    occurrence_count = IntegerField('Number of Occurrences', validators=[Optional(), NumberRange(min=1)], default=10)
    recurrence_end_date = DateField('Recurrence End Date')
    street = StringField('Street Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('ZIP Code', validators=[DataRequired()])
    fun_meter = SelectField('Fun Rating', choices=[
        ('1', '⭐'),
        ('2', '⭐⭐'),
        ('3', '⭐⭐⭐'),
        ('4', '⭐⭐⭐⭐'),
        ('5', '⭐⭐⭐⭐⭐')
    ], validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('arts', 'Arts & Culture'),
        ('business', 'Business & Networking'),
        ('charity', 'Charity & Causes'),
        ('community', 'Community & Neighborhood'),
        ('education', 'Education & Learning'),
        ('family', 'Family & Kids'),
        ('festivals', 'Festivals & Fairs'),
        ('food', 'Food & Drink'),
        ('health', 'Health & Wellness'),
        ('holiday', 'Holiday & Seasonal'),
        ('markets', 'Markets & Shopping'),
        ('music', 'Music & Concerts'),
        ('nightlife', 'Nightlife & Entertainment'),
        ('outdoor', 'Outdoor & Adventure'),
        ('sports', 'Sports & Recreation'),
        ('tech', 'Technology & Innovation'),
        ('theatre', 'Theatre & Performing Arts'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    target_audience = SelectField('Target Audience', choices=[
        ('21plus', '21+'),
        ('adults', 'Adults'),
        ('families', 'Families'),
        ('kids', 'Kids'),
        ('parents', 'Parents'),
        ('professionals', 'Professionals'),
        ('seniors', 'Seniors'),
        ('singles', 'Singles')
    ], validators=[DataRequired()])
    website = StringField('Website', validators=[Optional(), URL()])
    facebook = StringField('Facebook')
    instagram = StringField('Instagram')
    twitter = StringField('Twitter')
    ticket_url = StringField('Purchase Tickets URL', validators=[Optional(), URL()])
    terms_accepted = BooleanField('I accept the Terms and Conditions', validators=[DataRequired()])
    submit = SubmitField('Create Event')

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