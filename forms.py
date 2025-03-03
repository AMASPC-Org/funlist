from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, TimeField, SelectField, FloatField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp, Optional, NumberRange, URL
from models import User

class SignupForm(FlaskForm):
    user_intention = SelectField(
        "I'm here to...",
        choices=[
            ('', 'Select an option...'),
            ('find_events', 'Find Events'),
            ('create_events', 'Create Events'),
            ('represent_organization', 'Represent an Organization'),
            ('vendor_services', 'Offer Vendor Services')
        ],
        validators=[DataRequired()],
        render_kw={"class": "form-control", "id": "user-intention"}
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(min=6, max=120, message="Email must be between 6 and 120 characters"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters"),
            Regexp(
                "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d).+$",
                message="Password must include at least one lowercase letter, one uppercase letter, and one number",
            ),
        ],
        render_kw={"id": "password-field"}
    )
    confirm_password = PasswordField(
        "Confirm Password", 
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"id": "confirm-password-field"}
    )

    audience_type = SelectMultipleField(
        "Audience Type",
        choices=[
            ('individual', 'Individual'),
            ('family', 'Family'),
            ('professional', 'Professional'),
            ('senior', 'Senior'),
            ('student', 'Student'),
            ('parent', 'Parent'),
            ('tourist', 'Tourist')
        ],
        render_kw={"class": "form-control", "id": "audience-type", "multiple": "multiple"}
    )

    preferred_locations = StringField(
        "Preferred Locations",
        validators=[Optional(), Length(max=255)],
        render_kw={"class": "form-control", "id": "preferred-locations", "placeholder": "Enter locations separated by commas"}
    )

    event_interests = StringField(
        "Event Interests",
        validators=[Optional(), Length(max=255)],
        render_kw={"class": "form-control", "id": "event-interests", "placeholder": "Enter interests separated by commas"}
    )

    terms_accepted = BooleanField(
        "I accept the Terms and Conditions and Privacy Policy", validators=[DataRequired()]
    )
    submit = SubmitField("Sign Up")

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
    username = StringField(
        "Username",
        validators=[
            Optional(),
            Length(min=3, max=64),
            Regexp(
                "^[A-Za-z0-9_]*$",
                message="Username can only contain letters, numbers, and underscores",
            ),
        ],
    )
    first_name = StringField("First Name", validators=[Optional(), Length(max=50)])
    last_name = StringField("Last Name", validators=[Optional(), Length(max=50)])
    bio = TextAreaField("Bio", validators=[Optional(), Length(max=1000)])
    location = StringField("Location", validators=[Optional(), Length(max=100)])
    interests = StringField("Interests", validators=[Optional(), Length(max=200)])

    audience_type = SelectMultipleField(
        "Audience Type",
        choices=[
            ('individual', 'Individual'),
            ('family', 'Family'),
            ('professional', 'Professional'),
            ('senior', 'Senior'),
            ('student', 'Student'),
            ('parent', 'Parent'),
            ('tourist', 'Tourist')
        ],
        render_kw={"class": "form-control", "id": "audience-type", "multiple": "multiple"}
    )

    preferred_locations = StringField(
        "Preferred Locations",
        validators=[Optional(), Length(max=255)],
        render_kw={"class": "form-control", "id": "preferred-locations", "placeholder": "Enter locations separated by commas"}
    )

    event_interests = StringField(
        "Event Interests",
        validators=[Optional(), Length(max=255)],
        render_kw={"class": "form-control", "id": "event-interests", "placeholder": "Enter interests separated by commas"}
    )

    birth_date = DateField("Birth Date", validators=[Optional()], format="%Y-%m-%d")
    submit = SubmitField("Update Profile")

    def validate_username(self, username):
        if username.data:
            user = User.query.filter_by(username=username.data).first()
            if user and user.id != self.user_id:
                raise ValidationError('This username is already taken. Please choose another one.')

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    start_time = TimeField('Start Time')
    end_time = TimeField('End Time')
    all_day = BooleanField('All Day Event')
    recurring = BooleanField('Recurring Event')
    recurrence_type = SelectField('Recurrence Pattern', choices=[
        ('none', 'One-time Event'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually')
    ])
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
        ('music', 'Music'), 
        ('sports', 'Sports'),
        ('arts', 'Arts'),
        ('food', 'Food & Drink'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    target_audience = SelectField('Target Audience', choices=[
        ('all', 'All Ages'),
        ('adults', 'Adults'),
        ('kids', 'Kids'),
        ('seniors', 'Seniors')
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
    advertising_opportunities = TextAreaField('Advertising Opportunities', validators=[Optional(), Length(max=500)])
    sponsorship_opportunities = TextAreaField('Sponsorship Opportunities', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Profile')

class VendorProfileForm(FlaskForm):
    company_name = StringField('Company Name', validators=[Optional(), Length(max=100)])
    vendor_type = SelectField('Vendor Type', choices=[
        ('Event Planner', 'Event Planner'),
        ('Catering', 'Catering'),
        ('Photography', 'Photography'),
        ('Videography', 'Videography'),
        ('Audio/Visual', 'Audio/Visual'),
        ('Decoration', 'Decoration'),
        ('Entertainment', 'Entertainment'),
        ('Transportation', 'Transportation'),
        ('Security', 'Security'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    description = TextAreaField('About Your Services', validators=[Optional(), Length(max=500)])
    website = StringField('Website', validators=[Optional(), URL()])
    services = TextAreaField('Services Offered', validators=[Optional(), Length(max=500)])
    pricing = TextAreaField('Pricing Information', validators=[Optional(), Length(max=300)])
    submit = SubmitField('Save Profile')

class VenueProfileForm(FlaskForm):
    company_name = StringField('Venue Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('About Your Venue', validators=[Optional(), Length(max=500)])
    location = StringField('Address', validators=[Optional(), Length(max=200)])
    website = StringField('Website', validators=[Optional(), URL()])
    capacity = StringField('Venue Capacity', validators=[Optional(), Length(max=50)])
    features = TextAreaField('Venue Features', validators=[Optional(), Length(max=500)])
    advertising_opportunities = TextAreaField('Advertising Opportunities', validators=[Optional(), Length(max=500)])
    sponsorship_opportunities = TextAreaField('Sponsorship Opportunities', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Profile')ield('Save Organizer Profile')

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