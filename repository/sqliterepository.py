import sqlite3
from repository import Repository


class SQLiteRepository(Repository):
    def __init__(self):
        self.connection = sqlite3.connect("bot_staging.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

        # self.cursor.execute("DROP TABLE IF EXISTS phone")
        # self.cursor.execute("DROP TABLE IF EXISTS user")
        # self.cursor.execute("DROP TABLE IF EXISTS admin")
        # self.cursor.execute("DROP TABLE IF EXISTS entry")

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS phone (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT NOT NULL
            )
        """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                first_name TEXT NOT NULL,
                last_name INTEGER NOT NULL,
                phone_id INTEGER NOT NULL,
                FOREIGN KEY (phone_id)
                    REFERENCES phone (id)
            )
        """
        )

        self.cursor.execute(
            """
                            CREATE TABLE IF NOT EXISTS admin(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                first_name TEXT NOT NULL,
                                last_name TEXT NOT NULL,
                                password TEXT NOT NULL,
                                table_number INTEGER NOT NULL
                            )
                            """
        )

        self.cursor.execute(
            """
                            CREATE TABLE IF NOT EXISTS entry(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                ticket_number INTEGER NOT NULL,
                                user_id INTEGER NOT NULL,
                                admin_id INTEGER,
                                date TEXT NOT NULL,
                                status TEXT NOT NULL,
                                FOREIGN KEY (user_id)
                                    REFERENCES user (id)
                            )"""
        )

    def save_entry(self, entry):
        self.cursor.execute(
            """
            INSERT INTO phone (phone_number) VALUES (?)
        """,
            (entry.phone,),
        )

        phone_id = self.cursor.lastrowid

        self.cursor.execute(
            """
            INSERT INTO user (chat_id, first_name, last_name, phone_id) VALUES (?, ?, ?, ?)
        """,
            (entry.chat_id, entry.first_name, entry.last_name, phone_id),
        )

        user_id = self.cursor.lastrowid

        self.cursor.execute(
            """
            INSERT INTO entry (ticket_number, user_id, date, status) VALUES (?, ?, ?, ?)
        """,
            (entry.ticket_number, user_id, entry.date, "Waiting"),
        )

        self.connection.commit()

        return user_id

    def get_last_number(self, date):
        self.cursor.execute(
            """
            SELECT MAX(ticket_number) FROM entry WHERE date = ?
        """,
            (date,),
        )

        result = self.cursor.fetchone()

        if result[0] is None:
            return 0

        return result[0]

    def get_ticket_number_by_chat_id(self, chat_id):
        self.cursor.execute(
            """
            SELECT ticket_number FROM entry WHERE user_id = (
                SELECT id FROM user WHERE chat_id = ?
            )
        """,
            (chat_id,),
        )

        result = self.cursor.fetchone()

        return result[0]
    
    def has_entry_by_chat_id(self, chat_id):
        self.cursor.execute(
            """
            SELECT * 
            FROM entry 
            WHERE user_id = (SELECT id FROM user WHERE chat_id = ?) AND
                  status = 'Waiting'
        """,
            (chat_id,),
        )

        result = self.cursor.fetchone()

        return result[0] > 0