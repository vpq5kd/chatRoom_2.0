#imports
import sqlite3
import datetime
import pytz

#classes

"""class that defines a client message cache, stores the local client messages."""
class client_message_cache:
    """initializes the table"""
    def __init__(self,name):
        self.name = name
        #estabish connection
        conn = sqlite3.connect('client_databases\\client_message_cache.db')
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

    """adds a new message to the database"""
    def add_message(self, sender_name, sender_id, message, time):
        conn = sqlite3.connect('client_databases\\client_message_cache.db')
        cursor = conn.cursor()

        #add new message to the database
        new_message = (sender_name, sender_id, message, time)
        cursor.execute(f'''INSERT INTO {self.name}_client_cache (sender_name, sender_id, message, time) VALUES (?, ?, ?, ?)''', new_message)

        conn.commit()
        conn.close()

    """gets all the messages in the database by time"""
    def get_all_messages(self):
        conn = sqlite3.connect('client_databases\\client_message_cache.db')
        cursor = conn.cursor()

        #get messages (by most recent time)
        cursor.execute(f'''SELECT sender_name, sender_id, message, time FROM {self.name}_client_cache ORDER BY time DESC''')
        messages = cursor.fetchall()

        formatted_messages = self._format_messages(messages)
        for formatted_message in formatted_messages:
            print(formatted_message)

        conn.commit()
        conn.close()

    """formats the database messages for printing to the terminal"""
    def _format_messages(self, messages):
        message_string_array = []
        for message in messages:
            message_string = ""
            sender_name = message[0]
            sender_id = message[1]
            chat_message = message[2]
            time = self._translate_epoch_time(message[3])

            message_string+=f"{sender_name} ({sender_id}) sent: {chat_message} at {time}\n"
            message_delimiter = "-"*50+"\n"

            message_string_array.append(message_string)
            message_string_array.append(message_delimiter)
        return message_string_array

    """translates the epoch time to est"""
    def _translate_epoch_time(self,epoch_time):
        utc_time = datetime.datetime.utcfromtimestamp(epoch_time)
        utc_time = utc_time.replace(tzinfo=pytz.utc)
        est_time = utc_time.astimezone(pytz.timezone('US/Eastern'))

        return est_time

    """gets the messages of a particular sender"""
    def get_senders_messages(self,sender_name):
        conn = sqlite3.connect('client_databases\\client_message_cache.db')
        cursor = conn.cursor()

        cursor.execute(f'''SELECT sender_name, sender_id, message, time FROM {self.name}_client_cache WHERE sender_name=? ORDER BY time DESC''', (sender_name,))
        messages = cursor.fetchall()

        formatted_messages = self._format_messages(messages)
        for formatted_message in formatted_messages:
            print(formatted_message)

        conn.commit()
        conn.close()












