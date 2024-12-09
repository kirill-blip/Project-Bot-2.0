import sqlite3
from repository import Repository


class SQLiteRepository(Repository):
    def __init__(self):
        self.connection = sqlite3.connect("bot_staging.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

        self.cursor.execute("DROP TABLE IF EXISTS phone")
        self.cursor.execute("DROP TABLE IF EXISTS user")
        self.cursor.execute("DROP TABLE IF EXISTS admin")
        self.cursor.execute("DROP TABLE IF EXISTS entry")
        self.cursor.execute("DROP TABLE IF EXISTS user_admin")

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
                status text default 'waiting'
            )
        """
        )

                    #     FOREIGN KEY (phone_id)
                    # REFERENCES phone (id)

        self.cursor.execute(
            """
                            CREATE TABLE IF NOT EXISTS admin(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                first_name TEXT NOT NULL,
                                last_name TEXT NOT NULL,
                                password TEXT NOT NULL,
                                table_number INTEGER NOT NULL,
                                status BOOLEAN DEFAULT False
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

        self.cursor.execute(
            """
                            CREATE TABLE IF NOT EXISTS user_admin(
                                user_id INTEGER PRIMARY KEY
                            )"""
        )

        self.cursor.execute("""
            INSERT INTO admin(first_name, last_name, password, table_number) VALUES
            ('Alikhan', 'Jambul', 'admin2021', 1),
            ('Kirill', 'Golubenko', 'admin2022', 2),
            ('Dinislam', 'Azirbaev', 'admin2023', 3),
            ('Cktoto', 'Kakto', 'admin2024', 4);
""")    
        self.cursor.executemany(
    """
            INSERT INTO user (chat_id, first_name, last_name, phone_id, status)
             VALUES (?, ?, ?, ?, ?)
            """, [
                (123456, 'Иван', 'Иванов', 9876543210, 'waiting'),
                (234567, 'Мария', 'Петрова', 9876543211, 'waiting'),
                (345678, 'Алексей', 'Сидоров', 9876543212, 'waiting')
    ]
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
    

    def check_password(self, password : str):
        self.cursor.execute(f'''
            SELECT EXISTS (
                SELECT 1
                FROM admin
                WHERE password = '{password}'
            );
        ''')
        exists = self.cursor.fetchone()[0]
        return exists
    
    def get_name_and_num(self, password: str):
        self.cursor.execute(f'''
            select
                last_name || ' ' || first_name as "full name",
                table_number
            from admin
            where password = '{password}';
        ''')
        result = self.cursor.fetchall()[:]
        return result
    
    def update_status_admin(self, table_number: int):
        self.cursor.execute(f'''
            UPDATE admin
            SET status = TRUE
            WHERE table_number = {table_number};
        ''')

    def check_admin_status(self, password: str):
        self.cursor.execute(f'''
            SELECT status FROM admin
            WHERE password = '{password}';
        ''')
        result = self.cursor.fetchall()[0][0]
        if result:  
            return False
        return True
    
    def check_user_admin(self, id : int):
        self.cursor.execute(f'''
            SELECT 
                1 
            FROM
                user_admin
            WHERE user_id = {id};
        ''')
        exists = self.cursor.fetchone()
        return exists is not None
    
    def add_user_admin(self, id : int):
        self.cursor.execute(f'''
            insert into user_admin(user_id) values
            ({id});
        ''')

        self.connection.commit

    def call_client(self):
        self.cursor.execute('''
            SELECT 
                id,
                last_name || ' ' || first_name AS full_name
            FROM
                user
            WHERE
                status = 'waiting'
            ORDER BY id
            LIMIT 1;
        ''')
        client = self.cursor.fetchone()
        return client
    
    def update_client(self, id: int):
        self.cursor.execute(f'''
            update user
            set status = 'AtTheReception'
            where id = {id}
        ''')
        self.connection.commit

    def check_client(self):
        self.cursor.execute('''
            SELECT 
                count(status)
            FROM user
            WHERE status = 'waiting'
        ''')

        result = self.cursor.fetchone()  
        if result:
            return result[0]
        return 0  
    
    def dont_come_client(self, id):
        self.cursor.execute(f'''
            update user
            set status = 'Fail'
            where id = {id}
        ''')
        self.connection.commit

    def come_client(self, id):
        self.cursor.execute(f'''
            update user
            set status = 'Accept'
            where id = {id}
        ''')
        self.connection.commit