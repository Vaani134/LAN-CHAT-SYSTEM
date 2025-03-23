"""

from flask import Blueprint, render_template, session
import sqlite3

# Define the blueprint
chat_blueprint = Blueprint('chat', __name__, template_folder='templates')

# Function to create a database connection
def create_connection():
    conn = sqlite3.connect('restart.db')
    conn.row_factory = sqlite3.Row  # Enable dict-like access for rows
    return conn

# Function to fetch contacts and their names for a specific user
def get_user_contacts(user_id):
    query = """ """
    SELECT 
        c.contact_id,    
        u.name           
    FROM 
        contacts c
    JOIN 
        user u
    ON 
        c.contact_id = u.id
    WHERE 
        c.user_id = ?;  
    """  """
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id,))
        contacts = cur.fetchall()
        conn.close()
        return contacts
    except sqlite3.Error as e:
        print(f"Error fetching contacts: {e}")
        return []

# Route for chat interface
@chat_blueprint.route('/chat', methods=['GET'])
def chat():
    user_id = session.get('user_id', 1)  # Default to user_id 2 for testing
    contacts = get_user_contacts(user_id)  # Fetch contacts for the logged-in user
    return render_template('chat.html', contacts=contacts)



@chat_blueprint.route('/chat/<int:contact_id>', methods=['GET'])
def start_chat(contact_id):
    user_id = session.get('user_id', 1)  # Default user_id if not in session
    return render_template('chat_window.html', contact_id=contact_id)
"""

#########################################################################
"""
from flask import Blueprint, render_template, session
import sqlite3

# Define the blueprint
chat_blueprint = Blueprint('chat', __name__, template_folder='templates')

# Function to create a database connection
def create_connection():
    conn = sqlite3.connect('restart.db')
    conn.row_factory = sqlite3.Row  # Enable dict-like access for rows
    return conn

# Function to fetch contacts and their names for a specific user
def get_user_contacts(user_id):
    query = """ """
    SELECT 
        c.contact_id,    
        u.name           
    FROM 
        contacts c
    JOIN 
        user u
    ON 
        c.contact_id = u.id
    WHERE 
        c.user_id = ?;  
    """ """
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id,))
        contacts = cur.fetchall()
        conn.close()
        return contacts
    except sqlite3.Error as e:
        print(f"Error fetching contacts: {e}")
        return []

# Route for chat interface
@chat_blueprint.route('/chat', methods=['GET'])
def chat():
    user_id = session.get('user_id',)  # Default to user_id 1 for testing
    contacts = get_user_contacts(user_id)  # Fetch contacts for the logged-in user
    return render_template('chat.html', contacts=contacts)


# Route for a specific chat with a contact
@chat_blueprint.route('/chat/<int:contact_id>', methods=['GET'])
def start_chat(contact_id):
    # You can fetch the chat history or setup the interface for the given contact_id
    user_id = session.get('user_id', )  # Default user_id
    return render_template('chat_window.html', contact_id=contact_id)
"""
##############################################################################
"""
from flask import Blueprint, render_template, session, redirect, url_for, flash
import sqlite3

# Define the blueprint
chat_blueprint = Blueprint('chat', __name__, template_folder='templates')

# Function to create a database connection
def create_connection():
    conn = sqlite3.connect('restart.db')
    conn.row_factory = sqlite3.Row  # Enable dict-like access for rows
    return conn

# Function to fetch contacts and their names for a specific user
def get_user_contacts(user_id):
    query = """ """
    SELECT 
        c.contact_id,    
        u.name           
    FROM 
        contacts c
    JOIN 
        user u
    ON 
        c.contact_id = u.id
    WHERE 
        c.user_id = ?;  
    """ """
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id,))
        contacts = cur.fetchall()
        conn.close()
        return contacts
    except sqlite3.Error as e:
        print(f"Error fetching contacts: {e}")
        return []

# Route for chat interface
@chat_blueprint.route('/chat', methods=['GET'])
def chat():
    # Check if user_id is in session
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to view your contacts.")
        return redirect(url_for('login'))  # Redirect to the login page

    contacts = get_user_contacts(user_id)  # Fetch contacts for the logged-in user
    return render_template('chat.html', contacts=contacts)

# Route for a specific chat with a contact
@chat_blueprint.route('/chat/<int:contact_id>', methods=['GET'])
def start_chat(contact_id):
    # Check if user_id is in session
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to start a chat.")
        return redirect(url_for('login'))  # Redirect to the login page

    return render_template('chat_window.html', contact_id=contact_id)
"""
##############################################################
"""
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import sqlite3

# Define the blueprint
chat_blueprint = Blueprint('chat', __name__, template_folder='templates')

# Function to create a database connection
def create_connection():
    conn = sqlite3.connect('restart.db')
    conn.row_factory = sqlite3.Row  # Enable dict-like access for rows
    return conn

# Function to fetch contacts and their names for a specific user
def get_user_contacts(user_id):
    query = """ """
    SELECT 
        c.contact_id,    
        u.name           
    FROM 
        contacts c
    JOIN 
        user u
    ON 
        c.contact_id = u.id
    WHERE 
        c.user_id = ?;  
    """ """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query, (user_id,))
    contacts = cur.fetchall()
    conn.close()
    return contacts

# Function to fetch chat messages between the current user and a contact
def get_chat_messages(user_id, contact_id):
    query = """ """
    SELECT sender_id, receiver_id, message, timestamp
    FROM msg
    WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
    ORDER BY timestamp ASC;
    """ """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query, (user_id, contact_id, contact_id, user_id))
    messages = cur.fetchall()
    conn.close()
    return messages

# Function to send a message
def send_message(sender_id, receiver_id, message):
    query = """ """
    INSERT INTO msg (sender_id, receiver_id, message, timestamp)
    VALUES (?, ?, ?, datetime('now'));
    """ """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query, (sender_id, receiver_id, message))
    conn.commit()
    conn.close()

# Route for chat interface
@chat_blueprint.route('/chat', methods=['GET'])
def chat():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to view your contacts.")
        return redirect(url_for('login'))  # Redirect to the login page

    contacts = get_user_contacts(user_id)
    return render_template('chat.html', contacts=contacts)

# Route for a specific chat with a contact
@chat_blueprint.route('/chat/<int:contact_id>', methods=['GET', 'POST'])
def start_chat(contact_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to start a chat.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            send_message(user_id, contact_id, message)

    messages = get_chat_messages(user_id, contact_id)
    return render_template('chat_window.html', messages=messages, contact_id=contact_id)
"""
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import sqlite3

# Define the blueprint
chat_blueprint = Blueprint('chat', __name__, template_folder='templates')

# Function to create a database connection
def create_connection():
    conn = sqlite3.connect('restart.db')
    conn.row_factory = sqlite3.Row  # Enable dict-like access for rows
    return conn

# Function to fetch contacts and their names for a specific user
def get_user_contacts(user_id):
    query = """
    SELECT 
        c.contact_id,    
        u.name           
    FROM 
        contacts c
    JOIN 
        user u
    ON 
        c.contact_id = u.id
    WHERE 
        c.user_id = ?;  
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query, (user_id,))
    contacts = cur.fetchall()
    conn.close()
    return contacts

# Function to fetch chat messages between the current user and a contact
def get_chat_messages(user_id, contact_id):
    query = """
    SELECT sender_id, receiver_id, message, timestamp
    FROM msg
    WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
    ORDER BY timestamp ASC;
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query, (user_id, contact_id, contact_id, user_id))
    messages = cur.fetchall()
    conn.close()
    return messages

# Function to send a message
def send_message(sender_id, receiver_id, message):
    query = """
    INSERT INTO msg (sender_id, receiver_id, message, timestamp)
    VALUES (?, ?, ?, datetime('now'));
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query, (sender_id, receiver_id, message))
    conn.commit()
    conn.close()

# Function to fetch contact's name
def get_contact_name(contact_id):
    query = """
    SELECT name FROM user WHERE id = ?;
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query, (contact_id,))
    contact = cur.fetchone()
    conn.close()
    return contact['name'] if contact else "Unknown"

# Route for chat interface
@chat_blueprint.route('/chat', methods=['GET'])
def chat():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to view your contacts.")
        return redirect(url_for('login'))  # Redirect to the login page

    contacts = get_user_contacts(user_id)
    return render_template('chat.html', contacts=contacts)

# Route for a specific chat with a contact
@chat_blueprint.route('/chat/<int:contact_id>', methods=['GET', 'POST'])
def start_chat(contact_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to start a chat.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            send_message(user_id, contact_id, message)

    messages = get_chat_messages(user_id, contact_id)
    contact_name = get_contact_name(contact_id)  # Fetch the contact's name

    return render_template('chat_window.html', messages=messages, contact_name=contact_name)

