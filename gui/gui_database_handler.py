#imports
import sqlite3
import datetime
import pytz

#classes

"""class that defines a client message cache, stores the local client messages."""
class credentials_handler:
    """initializes the table"""
    def __init__(self):
        #estabish connection
        conn = sqlite3.connect('server_databases\\server_database.db')
        cursor = conn.cursor()

        #create a new table for the user, holds if name is the same (username functionality)
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS credentials(
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL)''')

        #commit and close
        conn.commit()
        conn.close()
    def authenticate(self,username,password):
        conn = sqlite3.connect('server_databases\\server_database.db')
        cursor = conn.cursor()

        #search username with a given password
        cursor.execute("SELECT password FROM credentials WHERE username = ?", (username,))
        row = cursor.fetchone()

        #authenticate password
        if row:
            if password == row:
                return True
        return False















