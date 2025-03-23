import sqlite3

conn = sqlite3.connect('restart.db')
cursor = conn.cursor()


cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

tables = cursor.fetchall()
for i in tables:
    print(i[0]) 

"""   
#query = f"INSERT INTO 'user' (id,name,email,password) VALUES (2,'Harsh','harsh@gmail.com' ,'harsh@123')"

query = f"INSERT INTO 'contacts' (id,user_id,contact_id,status) VALUES (1,2,1,'accepted')"

cursor.execute(query)
"""

conn.commit()

conn.close()