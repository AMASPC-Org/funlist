from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, DateTimeLocalField, SelectField, FloatField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp, Optional, NumberRange

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Please enter your email address"),
        Email(message="Please enter a valid email address"),
        Length(max=120, message="Email address is too long")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Please enter a password"),
        Length(min=8, message="Password must be at least 8 characters long"),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]+$',
               message="Password must contain at least one letter, one number, and one special character")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('password', message='Passwords do not match. Please try again.')
    ])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        from models import User
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
    submit = SubmitField('Log In')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[
        Optional(),
        Length(min=3, max=50, message="Username must be between 3 and 50 characters"),
        Regexp(r'^[\w.]+$', message="Username can only contain letters, numbers, dots and underscores")
    ])
    first_name = StringField('First Name', validators=[
        Optional(),
        Length(max=50, message="First name cannot exceed 50 characters")
    ])
    last_name = StringField('Last Name', validators=[
        Optional(),
        Length(max=50, message="Last name cannot exceed 50 characters")
    ])
    bio = TextAreaField('Bio', validators=[
        Optional(),
        Length(max=500, message="Bio cannot exceed 500 characters")
    ])
    location = StringField('Location', validators=[
        Optional(),
        Length(max=100, message="Location cannot exceed 100 characters")
    ])
    interests = StringField('Interests', validators=[
        Optional(),
        Length(max=200, message="Interests cannot exceed 200 characters")
    ])
    birth_date = DateField('Birth Date', validators=[Optional()])
    submit = SubmitField('Update Profile')

    def validate_username(self, username):
        from models import User
        if username.data:
            user = User.query.filter_by(username=username.data).first()
            if user and user.id != self.user_id:
                raise ValidationError('This username is already taken. Please choose another one.')

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateTimeLocalField('Date and Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[DataRequired(), NumberRange(min=-90, max=90)])
    longitude = FloatField('Longitude', validators=[DataRequired(), NumberRange(min=-180, max=180)])
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
    website = StringField('Website')
    facebook = StringField('Facebook')
    instagram = StringField('Instagram')
    twitter = StringField('Twitter')
    submit = SubmitField('Create Event')