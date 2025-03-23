"""
from flask import Blueprint, request, render_template, flash
from conn2 import create_connection, insert_user

register_blueprint = Blueprint('register', __name__)

@register_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Create a connection to the SQLite database
        conn = create_connection()
        user_id = insert_user(conn, name, email, password)
        
        
        conn.close()

    return render_template('register.html') """

from flask import Blueprint, request, render_template, flash, redirect, url_for
from conn2 import create_connection, insert_user, check_email_exists

register_blueprint = Blueprint('register', __name__)

@register_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if the email already exists
        conn = create_connection()
        if check_email_exists(conn, email):  # Check if email exists in the database
            flash('Email already exists. Please use a different email.', 'danger')
            conn.close()
            return render_template('register.html')  # Return to the same page with error message
        
        # Insert user into the database
        user_id = insert_user(conn, name, email, password)
        conn.close()

        if user_id:
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login.login'))  # Redirect to the login page after successful registration
        else:
            flash('Registration failed. Please try again.', 'danger')

    return render_template('register.html')
