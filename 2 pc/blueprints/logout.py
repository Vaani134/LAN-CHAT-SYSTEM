from flask import Blueprint, session, redirect, request
import sqlite3
from datetime import datetime

# Define the blueprint
logout_blueprint = Blueprint('logout', __name__)

# Function to log actions in the audit trail
def log_audit_trail(user_id, activity):
    query = "INSERT INTO audit (user_id, activity, timestamp) VALUES (?, ?, ?)"
    try:
        conn = sqlite3.connect('restart.db')
        cur = conn.cursor()
        cur.execute(query, (user_id, activity, datetime.now()))  # Store the action with current timestamp
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Route for logout
@logout_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':  # Ensure logout is triggered by POST
        user_id = session.get('user_id')  # Get user ID from session
        if user_id:
            log_audit_trail(user_id, 'logout')  # Log the logout event
        session.clear()  # Clear all session data
    return redirect('/login')  # Redirect to the login page
