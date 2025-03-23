"""
from conn2 import create_connection, insert_user, insert_contact, insert_audit, insert_message

# Establish connection
conn = create_connection()

# Insert data into `user` table
#user_id = insert_user(conn, "John Doe", "john@example.com", "hashed_password")

# Insert data into `contacts` table
contact_id = insert_contact(conn, 3,2, "accepted")


# Insert data into `msg` table
#msg_id = insert_message(conn, user_id, 2, "Hello, this is a message!")

# Insert data into `audit` table
#audit_id = insert_audit(conn, 3, "login")

# Close the connection
conn.close()
"""



from conn2 import create_connection, insert_contact

# Establish connection
conn = create_connection()

# Check if the contact relationship already exists
def is_contact_exists(conn, user_id, contact_id):
    query = "SELECT 1 FROM contacts WHERE user_id = ? AND contact_id = ?"
    cur = conn.cursor()
    cur.execute(query, (user_id, contact_id))
    return cur.fetchone() is not None

user_id = 13
contact_id = 3

# Insert data into `contacts` table if not already present
if not is_contact_exists(conn, user_id, contact_id):
    contact_id = insert_contact(conn, user_id, contact_id, "accepted")
    print("Contact added successfully!")
else:
    print("Contact already exists. Skipping insertion.")

# Close the connection
conn.close()
