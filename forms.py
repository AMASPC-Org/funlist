from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField, SelectField, IntegerField, FloatField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, URL, Optional, NumberRange

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    user_groups = SelectMultipleField('User Groups', choices=[
        ('adult', 'Adult'),
        ('parent', 'Parent'),
        ('single', 'Single'),
        ('senior', 'Senior'),
        ('young_adult', 'Young Adult'),
        ('couple', 'Couple'),
        ('21_plus', '21+')
    ], validators=[DataRequired()])
    is_organizer = BooleanField('Register as Event Organizer')
    opt_in_email = BooleanField('I would like to receive the Weekly Fun List Email for events in my area')
    submit = SubmitField('Register')

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateTimeField('Date and Time', validators=[DataRequired()], format='%Y-%m-%d %H:%M')
    location = StringField('Location', validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[Optional(), NumberRange(min=-90, max=90)])
    longitude = FloatField('Longitude', validators=[Optional(), NumberRange(min=-180, max=180)])
    category = SelectField('Category', choices=[
        ('music', 'Music'),
        ('sports', 'Sports'),
        ('arts', 'Arts'),
        ('food', 'Food'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    target_audience = SelectField('Target Audience', choices=[
        ('adults', 'Adults'),
        ('singles', 'Singles'),
        ('inclusive', 'Inclusive')
    ], validators=[DataRequired()])
    fun_meter = IntegerField('Fun Meter (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit Event')

class OrganizerProfileForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    website = StringField('Website', validators=[Optional(), URL()])
    advertising_opportunities = TextAreaField('Advertising Opportunities')
    sponsorship_opportunities = TextAreaField('Sponsorship Opportunities')
    submit = SubmitField('Update Profile')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
