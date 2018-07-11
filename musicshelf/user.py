import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from musicshelf.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    The login view. No DB functions are needed since info is stored locally.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        if username != current_app.config['OWNER_USER']:
            error = 'Incorrect username.'
        elif not check_password_hash(current_app.config['OWNER_PASS'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user'] = username
            return redirect(url_for('index'))

        flash(error)

    # if called with GET
    return render_template('user/login.html')

@bp.before_app_request
def load_logged_in_user():
    """
    Get user information at the start of each request,
    if a user is logged in.
    """
    user = session.get('user')
    # whether this is None or not, it doesn't matter.
    g.user = user

@bp.route('/logout')
def logout():
    """
    Log the user out.
    """
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    """
    Decorator to mark views as needing authentication.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user.login'))

        return view(**kwargs)

    return wrapped_view
