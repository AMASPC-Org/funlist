from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, TimeField, SelectField, FloatField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp, Optional, NumberRange, URL
from models import User

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
    interests = StringField('Interests', validators=[Optional(), Length(max=200)])
    birth_date = DateField('Birth Date', validators=[Optional()])
    submit = SubmitField('Update Profile')

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