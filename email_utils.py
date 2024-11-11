from flask_mail import Mail, Message
from flask import current_app, url_for
from datetime import datetime
from models import User
import logging
from urllib.parse import quote
import re

logger = logging.getLogger(__name__)
mail = Mail()

def is_valid_email_domain(email):
    """Validate email domain length."""
    try:
        domain = email.split('@')[1]
        return len(domain) <= 255 and all(len(part) <= 63 for part in domain.split('.'))
    except IndexError:
        return False

def send_verification_email(user):
    try:
        # Validate email domain
        if not is_valid_email_domain(user.email):
            raise ValueError("Invalid email domain length")

        # Generate token
        token = User.generate_verification_token(user.email, current_app.config['SECRET_KEY'])
        if not token:
            raise ValueError("Failed to generate verification token")

        # URL encode the token
        encoded_token = quote(token)
        verify_url = url_for('verify_email', token=encoded_token, _external=True)

        msg = Message('Verify Your Email Address',
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients=[user.email])
        
        msg.body = f'''Please click the following link to verify your email address:
{verify_url}

If you did not create an account, please ignore this email.

This link will expire in 1 hour.
'''
        
        msg.html = f'''
        <h1>Verify Your Email Address</h1>
        <p>Please click the following link to verify your email address:</p>
        <p><a href="{verify_url}">Verify Email</a></p>
        <p>If you did not create an account, please ignore this email.</p>
        <p><small>This link will expire in 1 hour.</small></p>
        '''
        
        mail.send(msg)
        user.email_verification_sent_at = datetime.utcnow()
    except ValueError as e:
        logger.error(f"Validation error in send_verification_email: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error sending verification email: {str(e)}")
        raise
