from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import redirect, url_for, flash, session

def hashPassword(password):
    return generate_password_hash(password)

def comparePasswords(hashed_password, password):
    return check_password_hash(hashed_password, password)

def sendVerificationEmail(email):
    # Placeholder for email verification
    pass

def sendPasswordResetEmail(email):
    # Placeholder for password reset
    pass

def requireAuth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def requireAdmin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin', False):
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
