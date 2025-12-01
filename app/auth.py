from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from config import Config

bp = Blueprint('auth', __name__)

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please login to access this page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        
        if password == Config.APP_PASSWORD:
            session['logged_in'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Incorrect password', 'error')
            return redirect(url_for('auth.login'))
    
    return render_template('login.html')

@bp.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    flash('Successfully logged out', 'success')
    return redirect(url_for('auth.login'))
