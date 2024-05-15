#imports
import sqlite3
import datetime
import pytz

#classes

db_file = 'C:\\Users\\Smspaner\\PycharmProjects\\chatRoom_2.0\\server_databases\\server_database.db'

"""class that defines a table for the credentials"""
class credentials_handler:
    """initializes the table"""
    def __init__(self):
        self.db_file = db_file
        #estabish connection
        conn = sqlite3.connect(self.db_file)
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
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        #search username with a given password
        cursor.execute("SELECT password FROM credentials WHERE username = ?", (username,))
        row = cursor.fetchone()

        #authenticate password
        if row:
            if password == row[0]:
                return True
        return False
    def add_user(self,username,password):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute("SELECT username FROM credentials where username=? ",(username,))
        user = cursor.fetchone()

        if user:
            return False
        #add user if not exists
        elif not user:
            cursor.execute("INSERT INTO credentials (username, password) VALUES (?,?)", (username,password))
            conn.commit()
            return True
"""class that persists messages and has appropriate functions"""
class message_handler():
    def __init__(self):
        self.db_file = db_file
        # estabish connection
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # create a new table for the user, holds if name is the same (username functionality)
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS messages(
                                        id INTEGER PRIMARY KEY,
                                        senderUsername TEXT NOT NULL,
                                        recipientUsername TEXT NOT NULL,
                                        messageType TEXT NOT NULL,
                                        message TEXT NOT NULL,
                                        time BIGINT NOT NULL)''')

        # commit and close
        conn.commit()
        conn.close()


def deleteRecords(table):
    ch = credentials_handler()
    conn = sqlite3.connect(ch.db_file)
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM {table}")

    conn.commit()















