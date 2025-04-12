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

# Define event categories
EVENT_CATEGORIES = [
    ('', 'Select category...'),
    ('Music', 'Music & Concerts'),
    ('Food', 'Food & Drink'),
    ('Arts', 'Arts & Culture'),
    ('Sports', 'Sports & Recreation'),
    ('Community', 'Community & Networking'),
    ('Education', 'Education & Workshops'),
    ('Family', 'Family & Kids'),
    ('Festival', 'Festivals & Fairs'),
    ('Other', 'Other')
]

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
    prohibited_advertisers = SelectMultipleField('Prohibited Advertisers', choices=[
        ('alcohol_tobacco', 'Alcohol and Tobacco Products'),
        ('marijuana_cannabis', 'Marijuana and Cannabis Dispensaries'),
        ('gambling_betting', 'Gambling and Betting Services'),
        ('adult_entertainment', 'Adult Entertainment and Products'),
        ('junk_food', 'Junk Food and Sugary Beverages'),
        ('energy_drinks', 'Energy Drinks'),
        ('political_religious', 'Political and Religious Organizations')
    ], validators=[Optional()])
    title = StringField('Event Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Event Description', validators=[DataRequired(), Length(max=1500)])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[Optional()])
    end_time = TimeField('End Time', validators=[Optional()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[Optional()])
    location = StringField('Location', validators=[DataRequired(), Length(max=100)])
    address = StringField('Street Address', validators=[DataRequired(), Length(max=200)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State', validators=[DataRequired(), Length(max=2)])
    zip_code = StringField('ZIP Code', validators=[DataRequired(), Length(max=10)])
    category = SelectField('Category', choices=EVENT_CATEGORIES, validators=[DataRequired()])
    website = StringField('Website', validators=[Optional(), URL()])
    is_free = BooleanField('This is a free event')
    price = StringField('Price (if not free)', validators=[Optional(), Length(max=100)])
    contact_email = StringField('Contact Email', validators=[Optional(), Email(), Length(max=100)])
    contact_phone = StringField('Contact Phone', validators=[Optional(), Length(max=20)])
    image_url = StringField('Image URL', validators=[Optional(), URL(), Length(max=200)])
    is_featured = BooleanField('Feature this event')
    submit = SubmitField('Submit Event')

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