"""
from flask import Blueprint, render_template, request, redirect, session, flash
import sqlite3
from datetime import datetime

login_blueprint = Blueprint('login', __name__, template_folder='templates')

# Function to create a database connection
def create_connection():
    conn = sqlite3.connect('restart.db')
    conn.row_factory = sqlite3.Row  # Enable dict-like access for rows
    return conn
"""
"""
# Function to log actions in the audit trail
def log_audit_trail(user_id, activity):
    query = "INSERT INTO audit (user_id, activity, timestamp) VALUES (?, ?, ?)"
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id, activity, datetime.now()))  # Store the action with current timestamp
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        
"""
"""
# Function to log audit trail with activity and IP address
def log_audit_trail(user_id, activity):
    ip_address = request.remote_addr  # Get the user's IP address
    
    query = "INSERT INTO audit (user_id, activity, timestamp, ip_address) VALUES (?, ?, ?, ?)"
    
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id, activity, datetime.now(), ip_address))  # Include IP address
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")        

# Route for login page
@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Validate credentials against the database
        query = "SELECT id FROM user WHERE email = ? AND password = ?"
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute(query, (email, password))  # Replace with hashed password verification
            user = cur.fetchone()
            conn.close()

            if user:
                session['user_id'] = user['id']  # Store user ID in session
                log_audit_trail(user['id'], 'login')  # Log the login event
                return redirect('/chat')  # Redirect to chat page
            else:
                flash('Invalid credentials. Please try again.')
        except sqlite3.Error as e:
            flash(f"Database error: {e}")
    return render_template('login.html')  # Render login template if GET request or failed login




"""


##############################################################################
"""
from flask import Blueprint, render_template, request, redirect, session, flash
import sqlite3
from datetime import datetime

login_blueprint = Blueprint('login', __name__, template_folder='templates')

# Function to create a database connection
def create_connection():
    conn = sqlite3.connect('restart.db')
    conn.row_factory = sqlite3.Row  # Enable dict-like access for rows
    return conn

# Function to log audit trail with activity and IP address
def log_audit_trail(user_id, activity):
    ip_address = request.remote_addr  # Get the user's IP address
    query = "INSERT INTO audit (user_id, activity, timestamp, ip_address) VALUES (?, ?, ?, ?)"
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id, activity, datetime.now(), ip_address))  # Include IP address
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Admin credentials (hardcoded)
ADMIN_EMAIL = "admin@gmail.com"  # Admin email
ADMIN_PASSWORD = "admin"        # Admin password (replace with a secure hash)

# Route for login page
@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the credentials match the admin's credentials
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['user_id'] = 'admin'  # Use a special identifier for admin in the session
            log_audit_trail('admin', 'admin login')  # Log the admin login event
            return redirect('/admin')  # Redirect to admin page

        # Validate credentials against the database for normal users
        query = "SELECT id FROM user WHERE email = ? AND password = ?"
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute(query, (email, password))  # Replace with hashed password verification
            user = cur.fetchone()
            conn.close()

            if user:
                session['user_id'] = user['id']  # Store user ID in session
                log_audit_trail(user['id'], 'login')  # Log the login event
                return redirect('/chat')  # Redirect to chat page
            else:
                flash('Invalid credentials. Please try again.')
        except sqlite3.Error as e:
            flash(f"Database error: {e}")
    return render_template('login.html')  # Render login template if GET request or failed login

# Route for admin dashboard
@login_blueprint.route('/admin')
def admin_dashboard():
    if 'user_id' in session and session['user_id'] == 'admin':  # Check for admin session
        return render_template('admin.html')  # Render admin page
    else:
        flash('Unauthorized access.')
        return redirect('/login')  # Redirect to login if unauthorized

# Route for logout
@login_blueprint.route('/logout')
def logout():
    if 'user_id' in session:
        user_id = session.pop('user_id')  # Remove user_id from session
        log_audit_trail(user_id, 'logout')  # Log the logout event
    flash('You have been logged out.')
    return redirect('/login')  # Redirect to login page

"""
#################################################################
"""
from flask import Blueprint, render_template, request, redirect, session, flash, jsonify
import sqlite3
from datetime import datetime

login_blueprint = Blueprint('login', __name__, template_folder='templates')

# Function to create a database connection
def create_connection():
    conn = sqlite3.connect('restart.db')
    conn.row_factory = sqlite3.Row  # Enable dict-like access for rows
    return conn

# Function to log audit trail with activity and IP address
def log_audit_trail(user_id, activity):
    ip_address = request.remote_addr  # Get the user's IP address
    query = "INSERT INTO audit (user_id, activity, timestamp, ip_address) VALUES (?, ?, ?, ?)"
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id, activity, datetime.now(), ip_address))  # Include IP address
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Admin credentials (hardcoded)
ADMIN_EMAIL = "admin@gmail.com"  # Admin email
ADMIN_PASSWORD = "admin"        # Admin password (replace with a secure hash)

# Route for login page
@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the credentials match the admin's credentials
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['user_id'] = 'admin'  # Use a special identifier for admin in the session
            log_audit_trail('admin', 'admin login')  # Log the admin login event
            return redirect('/admin')  # Redirect to admin page

        # Validate credentials against the database for normal users
        query = "SELECT id FROM user WHERE email = ? AND password = ?"
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute(query, (email, password))  # Replace with hashed password verification
            user = cur.fetchone()
            conn.close()

            if user:
                session['user_id'] = user['id']  # Store user ID in session
                log_audit_trail(user['id'], 'login')  # Log the login event
                return redirect('/chat')  # Redirect to chat page
            else:
                flash('Invalid credentials. Please try again.')
        except sqlite3.Error as e:
            flash(f"Database error: {e}")
    return render_template('login.html')  # Render login template if GET request or failed login

# Route for admin dashboard
@login_blueprint.route('/admin')
def admin_dashboard():
    if 'user_id' in session and session['user_id'] == 'admin':  # Check for admin session
        return render_template('admin.html')  # Render admin page
    else:
        flash('Unauthorized access.')
        return redirect('/login')  # Redirect to login if unauthorized

# Route for logout
@login_blueprint.route('/admin/logout')
def logout():
    if 'user_id' in session:
        user_id = session.pop('user_id')  # Remove user_id from session
        log_audit_trail(user_id, 'logout')  # Log the logout event
    flash('You have been logged out.')
    return redirect('/login')  # Redirect to login page

# AJAX: Fetch all users for management
@login_blueprint.route('/manage_users', methods=['GET'])
def manage_users():
    if 'user_id' in session and session['user_id'] == 'admin':
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM user")  # Fetch all users
            users = cur.fetchall()
            conn.close()
            return jsonify([dict(user) for user in users])  # Return as JSON
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Unauthorized access"}), 403

# AJAX: Fetch audit logs
@login_blueprint.route('/view_audit_logs', methods=['GET'])
def view_audit_logs():
    if 'user_id' in session and session['user_id'] == 'admin':
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM audit")  # Fetch audit logs
            logs = cur.fetchall()
            conn.close()
            return jsonify([dict(log) for log in logs])  # Return as JSON
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Unauthorized access"}), 403

# AJAX: Broadcast a message
@login_blueprint.route('/broadcast', methods=['POST'])
def broadcast_message():
    if 'user_id' in session and session['user_id'] == 'admin':
        message = request.form.get('message')
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO msg (content, broadcast) VALUES (?, 1)", (message,))
            conn.commit()
            conn.close()
            return jsonify({"message": "Broadcast message sent successfully"}), 200
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Unauthorized access"}), 403
"""

################################################
"""
from flask import Blueprint, render_template, request, redirect, session, flash, jsonify
import sqlite3
from datetime import datetime

login_blueprint = Blueprint('login', __name__, template_folder='templates')

# Function to create a database connection
def create_connection():
    conn = sqlite3.connect('restart.db')
    conn.row_factory = sqlite3.Row  # Enable dict-like access for rows
    return conn

# Function to log audit trail with activity and IP address
def log_audit_trail(user_id, activity):
    ip_address = request.remote_addr  # Get the user's IP address
    query = "INSERT INTO audit (user_id, activity, timestamp, ip_address) VALUES (?, ?, ?, ?)"
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id, activity, datetime.now(), ip_address))  # Include IP address
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Admin credentials (hardcoded)
ADMIN_EMAIL = "admin@gmail.com"  # Admin email
ADMIN_PASSWORD = "admin"        # Admin password (replace with a secure hash)

# Route for login page
@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the credentials match the admin's credentials
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['user_id'] = 'admin'  # Use a special identifier for admin in the session
            log_audit_trail('admin', 'admin login')  # Log the admin login event
            return redirect('/admin')  # Redirect to admin page

        # Validate credentials against the database for normal users
        query = "SELECT id FROM user WHERE email = ? AND password = ?"
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute(query, (email, password))  # Replace with hashed password verification
            user = cur.fetchone()
            conn.close()

            if user:
                session['user_id'] = user['id']  # Store user ID in session
                log_audit_trail(user['id'], 'login')  # Log the login event
                return redirect('/chat')  # Redirect to chat page
            else:
                flash('Invalid credentials. Please try again.')
        except sqlite3.Error as e:
            flash(f"Database error: {e}")
    return render_template('login.html')  # Render login template if GET request or failed login

# Route for admin dashboard
@login_blueprint.route('/admin')
def admin_dashboard():
    if 'user_id' in session and session['user_id'] == 'admin':  # Check for admin session
        return render_template('admin.html')  # Render admin page
    else:
        flash('Unauthorized access.')
        return redirect('/login')  # Redirect to login if unauthorized

# Route for logout
@login_blueprint.route('/admin/logout')
def logout():
    if 'user_id' in session:
        user_id = session.pop('user_id')  # Remove user_id from session
        log_audit_trail(user_id, 'logout')  # Log the logout event
    flash('You have been logged out.')
    return redirect('/login')  # Redirect to login page

# AJAX: Fetch all users for management
@login_blueprint.route('/manage_users', methods=['GET'])
def manage_users():
    if 'user_id' in session and session['user_id'] == 'admin':
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM user")  # Fetch all users
            users = cur.fetchall()
            conn.close()
            return jsonify([dict(user) for user in users])  # Return as JSON
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Unauthorized access"}), 403

# AJAX: Fetch audit logs
@login_blueprint.route('/view_audit_logs', methods=['GET'])
def view_audit_logs():
    if 'user_id' in session and session['user_id'] == 'admin':
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM audit")  # Fetch audit logs
            logs = cur.fetchall()
            conn.close()
            return jsonify([dict(log) for log in logs])  # Return as JSON
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Unauthorized access"}), 403

# AJAX: Broadcast a message
@login_blueprint.route('/broadcast', methods=['POST'])
def broadcast_message():
    if 'user_id' in session and session['user_id'] == 'admin':
        message = request.form.get('message')
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO msg (content, broadcast) VALUES (?, 1)", (message,))
            conn.commit()
            conn.close()
            return jsonify({"message": "Broadcast message sent successfully"}), 200
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Unauthorized access"}), 403

"""

####################################################################
"""
from flask import Blueprint, render_template, request, redirect, session, flash, jsonify
import sqlite3
from datetime import datetime

# Define the blueprint
login_blueprint = Blueprint('login', __name__, template_folder='templates')

# Function to create a database connection
def create_connection():
    conn = sqlite3.connect('restart.db')
    conn.row_factory = sqlite3.Row  # Enable dict-like access for rows
    return conn

# Function to log actions in the audit trail
def log_audit_trail(user_id, activity):
    ip_address = request.remote_addr  # Get the user's IP address
    query = "INSERT INTO audit (user_id, activity, timestamp, ip_address) VALUES (?, ?, ?, ?)"
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id, activity, datetime.now(), ip_address))  # Include IP address
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Admin credentials (hardcoded)
ADMIN_EMAIL = "admin@gmail.com"  # Admin email
ADMIN_PASSWORD = "admin"        # Admin password (replace with a secure hash)

# Route for login page
@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the credentials match the admin's credentials
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['user_id'] = 'admin'  # Use a special identifier for admin in the session
            log_audit_trail('admin', 'admin login')  # Log the admin login event
            return redirect('/admin')  # Redirect to admin page

        # Validate credentials against the database for normal users
        query = "SELECT id FROM user WHERE email = ? AND password = ?"
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute(query, (email, password))  # Replace with hashed password verification
            user = cur.fetchone()
            conn.close()

            if user:
                session['user_id'] = user['id']  # Store user ID in session
                log_audit_trail(user['id'], 'login')  # Log the login event
                return redirect('/chat')  # Redirect to chat page
            else:
                flash('Invalid credentials. Please try again.')
        except sqlite3.Error as e:
            flash(f"Database error: {e}")
    return render_template('login.html')  # Render login template if GET request or failed login

# Route for admin dashboard
@login_blueprint.route('/admin')
def admin_dashboard():
    if 'user_id' in session and session['user_id'] == 'admin':  # Check for admin session
        return render_template('admin.html')  # Render admin page
    else:
        flash('Unauthorized access.')
        return redirect('/login')  # Redirect to login if unauthorized

# Route for logout
@login_blueprint.route('/admin/logout')
def logout():
    if 'user_id' in session:
        user_id = session.pop('user_id')  # Remove user_id from session
        log_audit_trail(user_id, 'logout')  # Log the logout event
    flash('You have been logged out.')
    return redirect('/login')  # Redirect to login page

# AJAX: Fetch all users for management
@login_blueprint.route('/manage_users', methods=['GET'])
def manage_users():
    if 'user_id' in session and session['user_id'] == 'admin':
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM user")  # Fetch all users
            users = cur.fetchall()
            conn.close()
            return jsonify([dict(user) for user in users])  # Return as JSON
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Unauthorized access"}), 403

# AJAX: Fetch audit logs
@login_blueprint.route('/view_audit_logs', methods=['GET'])
def view_audit_logs():
    if 'user_id' in session and session['user_id'] == 'admin':
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM audit")  # Fetch audit logs
            logs = cur.fetchall()
            conn.close()
            return jsonify([dict(log) for log in logs])  # Return as JSON
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Unauthorized access"}), 403

# AJAX: Broadcast a message
@login_blueprint.route('/broadcast', methods=['POST'])
def broadcast_message():
    if 'user_id' in session and session['user_id'] == 'admin':
        message = request.form.get('message')
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO msg (content, broadcast) VALUES (?, 1)", (message,))  # Insert the broadcast message
            conn.commit()
            conn.close()
            return jsonify({"message": "Broadcast message sent successfully"}), 200
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Unauthorized access"}), 403
"""


from flask import Blueprint, render_template, request, redirect, session, flash, jsonify
import sqlite3
from datetime import datetime

# Define the blueprint
login_blueprint = Blueprint('login', __name__, template_folder='templates')

# Function to create a database connection
def create_connection():
    conn = sqlite3.connect('restart.db')
    conn.row_factory = sqlite3.Row  # Enable dict-like access for rows
    return conn

# Function to log actions in the audit trail
def log_audit_trail(user_id, activity):
    ip_address = request.remote_addr  # Get the user's IP address
    query = "INSERT INTO audit (user_id, activity, timestamp, ip_address) VALUES (?, ?, ?, ?)"
    conn = None
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id, activity, datetime.now(), ip_address))  # Include IP address
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        flash(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

# Admin credentials (hardcoded)
ADMIN_EMAIL = "admin@gmail.com"  # Admin email
ADMIN_PASSWORD = "admin"        # Admin password (replace with a secure hash)

# Route for login page
@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the credentials match the admin's credentials
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['user_id'] = 'admin'  # Use a special identifier for admin in the session
            log_audit_trail('admin', 'admin login')  # Log the admin login event
            return redirect('/admin')  # Redirect to admin page

        # Validate credentials against the database for normal users
        query = "SELECT id FROM user WHERE email = ? AND password = ?"
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute(query, (email, password))  # Replace with hashed password verification
            user = cur.fetchone()
            conn.close()

            if user:
                session['user_id'] = user['id']  # Store user ID in session
                log_audit_trail(user['id'], 'login')  # Log the login event
                return redirect('/chat')  # Redirect to chat page
            else:
                flash('Invalid credentials. Please try again.')
        except sqlite3.Error as e:
            flash(f"Database error: {e}")
    return render_template('login.html')  # Render login template if GET request or failed login

# Route for admin dashboard
@login_blueprint.route('/admin')
def admin_dashboard():
    if 'user_id' in session and session['user_id'] == 'admin':  # Check for admin session
        return render_template('admin.html')  # Render admin page
    else:
        flash('Unauthorized access.')
        return redirect('/login')  # Redirect to login if unauthorized

# Route for logout
@login_blueprint.route('/admin/logout')
def logout():
    if 'user_id' in session:
        user_id = session.pop('user_id')  # Remove user_id from session
        log_audit_trail(user_id, 'logout')  # Log the logout event
    flash('You have been logged out.')
    return redirect('/login')  # Redirect to login page

# AJAX: Fetch all users for management
@login_blueprint.route('/manage_users', methods=['GET'])
def manage_users():
    if 'user_id' in session and session['user_id'] == 'admin':
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM user")  # Fetch all users
            users = cur.fetchall()
            conn.close()
            return jsonify([dict(user) for user in users])  # Return as JSON
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Unauthorized access"}), 403

# AJAX: Fetch audit logs
@login_blueprint.route('/view_audit_logs', methods=['GET'])
def view_audit_logs():
    if 'user_id' in session and session['user_id'] == 'admin':
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM audit")  # Fetch audit logs
            logs = cur.fetchall()
            conn.close()
            return jsonify([dict(log) for log in logs])  # Return as JSON
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Unauthorized access"}), 403

# AJAX: Broadcast a message
@login_blueprint.route('/broadcast', methods=['POST'])
def broadcast_message():
    if 'user_id' in session and session['user_id'] == 'admin':
        message = request.form.get('message')
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO msg (content, broadcast) VALUES (?, 1)", (message,))  # Insert the broadcast message
            conn.commit()
            conn.close()
            return jsonify({"message": "Broadcast message sent successfully"}), 200
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Unauthorized access"}), 403

