#imports
import sqlite3

#classes

"""class that defines a client message cache, stores the local client messages."""
class client_message_cache:
    def __init__(self,name):
        self.name = name
        #estabish connection
        conn = sqlite3.connect('client_message_cache.db')
        cursor = conn.cursor()

        #create a new table for the user, holds if name is the same (username functionality)
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {name}_client_cache (
                                id INTEGER PRIMARY KEY,
                                sender_name TEXT NOT NULL,
                                sender_id INTEGER,
                                message TEXT NOT NULL
                                time INTEGER)''')

        #commit and close
        conn.commit()
        conn.close()
    def add_message(self, sender_name, sender_id, message, time):
        conn = sqlite3.connect('client_message_cache.db')
        cursor = conn.cursor()

        #add new message to the database
        new_message = (sender_name, sender_id, message, time)
        cursor.execute(f'''INSERT INTO {self.name}_client_cache (sender_name, sender_id, message, time) VALUES (?, ?, ?, ?)''', new_message)

        conn.commit()
        conn.close()
    def get_messages_by_time(self):
        conn = sqlite3.connect('client_message_cache.db')





