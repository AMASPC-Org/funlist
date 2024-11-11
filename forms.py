from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Please enter an email address"),
        Email(message="Please enter a valid email address (e.g., user@example.com)"),
        Length(max=120, message="Email address is too long (maximum is 120 characters)")
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
    submit = SubmitField('Register')

    def validate_email(self, email):
        from models import User
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('An account with this email already exists. Please use a different email or try logging in.')
