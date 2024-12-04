import sqlite3
from repository import Repository


class SQLiteRepository(Repository):
    def __init__(self):
        self.connection = sqlite3.connect('bot_staging.db')
        self.cursor = self.connection.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS phone (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT NOT NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name INTEGER NOT NULL,
                phone_id INTEGER NOT NULL,
                FOREIGN KEY (phone_id)
                    REFERENCES phone (id)
            )
        ''')
        
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS admin(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                first_name TEXT NOT NULL,
                                last_name TEXT NOT NULL,
                                password TEXT NOT NULL,
                                table_number INTEGER NOT NULL
                            )
                            ''')
        
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS entry(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER NOT NULL,
                                admin_id INTEGER NOT NULL,
                                date TEXT NOT NULL,
                                status TEXT NOT NULL,
                                FOREIGN KEY (user_id)
                                    REFERENCES user (id)
                            )''')
        
