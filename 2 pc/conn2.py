import sqlite3
from sqlite3 import Error

# Database connection
def create_connection(db_file="restart.db"):
   
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to SQLite database")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return None


# Function to execute an INSERT query
def insert_data(conn, query, data):
   
    try:
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        print("Data inserted successfully")
        return cur.lastrowid
    except Error as e:
        print(f"Error inserting data: {e}")
        return None




# Insert functions for each table
def insert_user(conn, name, email, password):
    query = """
    INSERT INTO user (name, email, password) 
    VALUES (?, ?, ?);
    """
    return insert_data(conn, query, (name, email, password))


def insert_contact(conn, user_id,contact_id, status):
    query = """
    INSERT INTO contacts (user_id,contact_id, status) 
    VALUES (?, ?, ?);
    """
    return insert_data(conn, query, (user_id,contact_id, status))


def insert_audit(conn, user_id, activity):
    query = """
    INSERT INTO audit (user_id, activity) 
    VALUES (?, ?);
    """
    return insert_data(conn, query, (user_id, activity))


def insert_message(conn, sender_id, receiver_id, message):
    query = """
    INSERT INTO msg (sender_id, receiver_id, message) 
    VALUES (?, ?, ?);
    """
    return insert_data(conn, query, (sender_id, receiver_id, message))

def check_email_exists(conn, email):
    query = "SELECT 1 FROM user WHERE email = ?"
    cur = conn.cursor()
    cur.execute(query, (email,))
    result = cur.fetchone()
    return result is not None  # Returns True if email exists, False otherwise

