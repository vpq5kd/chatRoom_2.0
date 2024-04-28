#imports
import sqlite3

#classes
class message_cache:
    def __init__(self):
        self.conn = sqlite3.connect('message_cache.db')
        self.cursor = self.conn.cursor()
        #self.cursor.execute('''CREATE TABLE IF NOT EXISTS ''')

