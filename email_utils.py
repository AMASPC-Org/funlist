from flask_mail import Mail, Message
from flask import current_app, url_for
from datetime import datetime
from models import User

mail = Mail()

def send_verification_email(user):
    token = User.generate_verification_token(user.email, current_app.config['SECRET_KEY'])
    verify_url = url_for('verify_email', token=token, _external=True)
    
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
