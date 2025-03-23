from flask import Blueprint, request, redirect, session
from conn2 import create_connection  # Assuming you have a function to create a DB connection

# Define the blueprint
add_blueprint = Blueprint('add', __name__)

# Function to get the user ID by the contact name from the user table
def get_user_id_by_name(conn, contact_name):
    query = "SELECT id FROM user WHERE name = ?"
    cur = conn.cursor()
    cur.execute(query, (contact_name,))
    result = cur.fetchone()
    return result[0] if result else None

# Function to check if a contact already exists in the contacts table
def is_contact_exists(conn, user_id, contact_id):
    query = "SELECT 1 FROM contacts WHERE user_id = ? AND contact_id = ?"
    cur = conn.cursor()
    cur.execute(query, (user_id, contact_id))
    return cur.fetchone() is not None

# Function to insert a contact into the contacts table
def insert_contact(conn, user_id, contact_id):
    query = "INSERT INTO contacts (user_id, contact_id, status) VALUES (?, ?, ?)"
    cur = conn.cursor()
    cur.execute(query, (user_id, contact_id, 'accepted'))
    conn.commit()

# Route for adding a new contact
@add_blueprint.route('/add_contact', methods=['POST'])
def add_contact():
    contact_name = request.form['name']  # Get the contact name from the form
    user_id = session.get('user_id')  # Get the logged-in user's ID from the session

    if not user_id:
        return redirect('/login')  # Redirect to login if the user is not logged in

    # Establish a database connection
    conn = create_connection()

    # Get the ID of the contact user from the `user` table
    contact_id = get_user_id_by_name(conn, contact_name)

    if contact_id:
        # Check if the contact already exists in the `contacts` table
        if not is_contact_exists(conn, user_id, contact_id):
            insert_contact(conn, user_id, contact_id)  # Add the contact
            conn.close()
            return redirect('/chat')  # Redirect to the chat page
        else:
            conn.close()
            return redirect('/chat')  # Redirect to chat if contact already exists
    else:
        conn.close()
        return redirect('/chat')  # Redirect if contact does not exist
