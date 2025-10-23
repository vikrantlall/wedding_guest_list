"""
Main Flask application for Wedding Guest List.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
from models.database import Database
import config
import os

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['DEBUG'] = config.DEBUG_MODE

# Initialize database
db = Database(config.DATABASE_PATH)

# Ensure database is initialized
if not os.path.exists(config.DATABASE_PATH):
    db.init_db()


def login_required(f):
    """Decorator to require login for routes"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    """Redirect to login or dashboard based on session"""
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in config.USERS and config.USERS[username] == password:
            session['username'] = username
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html', app_title=config.APP_TITLE)


@app.route('/logout')
def logout():
    """Logout and clear session"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}!', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with guest list and statistics"""
    guests = db.get_all_guests()
    stats = db.get_statistics()

    return render_template('dashboard.html',
                           guests=guests,
                           stats=stats,
                           username=session.get('username'),
                           app_title=config.APP_TITLE)


@app.route('/add_guest', methods=['POST'])
@login_required
def add_guest():
    """Add a new guest"""
    try:
        name = request.form.get('name')
        count = int(request.form.get('count'))
        side = request.form.get('side')
        attendance = request.form.get('attendance')

        # Validation
        if not name or count < 1 or side not in ['groom', 'bride'] or attendance not in ['likely', 'unlikely']:
            flash('Invalid guest data. Please check your inputs.', 'danger')
            return redirect(url_for('dashboard'))

        db.add_guest(name, count, side, attendance)
        flash(f'Guest "{name}" added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding guest: {str(e)}', 'danger')

    return redirect(url_for('dashboard'))


@app.route('/update_guest/<int:guest_id>', methods=['POST'])
@login_required
def update_guest(guest_id):
    """Update an existing guest"""
    try:
        name = request.form.get('name')
        count = int(request.form.get('count'))
        side = request.form.get('side')
        attendance = request.form.get('attendance')

        # Validation
        if not name or count < 1 or side not in ['groom', 'bride'] or attendance not in ['likely', 'unlikely']:
            flash('Invalid guest data. Please check your inputs.', 'danger')
            return redirect(url_for('dashboard'))

        if db.update_guest(guest_id, name, count, side, attendance):
            flash(f'Guest "{name}" updated successfully!', 'success')
        else:
            flash('Guest not found.', 'warning')
    except Exception as e:
        flash(f'Error updating guest: {str(e)}', 'danger')

    return redirect(url_for('dashboard'))


@app.route('/delete_guest/<int:guest_id>', methods=['POST'])
@login_required
def delete_guest(guest_id):
    """Delete a guest"""
    try:
        guest = db.get_guest_by_id(guest_id)
        if guest:
            db.delete_guest(guest_id)
            flash(f'Guest "{guest["name"]}" deleted successfully!', 'success')
        else:
            flash('Guest not found.', 'warning')
    except Exception as e:
        flash(f'Error deleting guest: {str(e)}', 'danger')

    return redirect(url_for('dashboard'))


@app.route('/api/stats')
@login_required
def api_stats():
    """API endpoint for statistics (for future AJAX updates)"""
    stats = db.get_statistics()
    return jsonify(stats)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=config.DEBUG_MODE)