import select
import psycopg2
import psycopg2.extensions
from repository import Repository

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from client.entry import Entry
from client.user import User
from client.admin import Admin
from observer import Subject


class PsqlRepository(Repository, Subject):
    def __init__(self, dbname, user, password, host, port):
        super().__init__()

        self.connection = None
        self.cursor = None

        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.connection = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )

        self.connection.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
        )
        self.cursor = self.connection.cursor()
        self.connection.autocommit = True

    def get_cursor(self):
        return self.cursor

    def get_status_by_entry_id(self, entry_id):
        self.get_cursor().execute(
            """
            SELECT status 
            FROM entry 
            WHERE id = %s
        """,
            (entry_id,),
        )

        result = self.get_cursor().fetchone()

        return result[0]

    def get_admin(self, entry: str):
        self.get_cursor().execute(
            """
            SELECT first_name, last_name, table_number
            FROM "admin"
            WHERE id = (
                SELECT admin_id 
                FROM entry 
                WHERE id = %s
            )
        """,
            (entry,),
        )

        result = self.get_cursor().fetchone()
        print(result)
        admin: Admin = Admin()

        admin.first_name = result[0]
        admin.last_name = result[1]
        admin.table_number = result[2]

        return admin

    def get_chat_id_by_entry_id(self, entry_id):
        self.get_cursor().execute(
            """
            SELECT chat_id 
            FROM "user" 
            WHERE id = (
                SELECT user_id 
                FROM entry 
                WHERE id = %s
            )
        """,
            (entry_id,),
        )

        result = self.get_cursor().fetchone()

        return result[0]

    def save_entry(self, entry):
        self.get_cursor().execute(
            """
        CALL add_entry(%s, %s, %s, %s, %s, %s);
        """,
            (
                entry.chat_id,
                entry.first_name,
                entry.last_name,
                entry.phone,
                entry.ticket_number,
                entry.date,
            ),
        )
        self.connection.commit()

    def get_last_number(self):
        self.get_cursor().execute(
            """
            SELECT MAX(ticket_number) FROM entry;
            """
        )

        result = self.get_cursor().fetchone()

        if result is None:
            return 0

        return result[0]

    def get_ticket_number_by_chat_id(self, chat_id):
        self.get_cursor().execute(
            """
            SELECT ticket_number 
            FROM entry 
            WHERE user_id = (SELECT id FROM "user" WHERE chat_id = %s)
                AND status = 'Waiting';
            """,
            (chat_id,),
        )

        result = self.get_cursor().fetchone()
        print(result[0])
        print(result)

        return result[0]

    def is_user_waiting(self, chat_id):
        self.get_cursor().execute("SELECT check_status(%s)", (chat_id,))
        return self.get_cursor().fetchone()[0]

    def has_entry_by_chat_id(self, chat_id):
        self.get_cursor().execute("select has_entry_by_chat_id(%s)", (chat_id,))
        result = self.get_cursor().fetchone()

        if result is None:
            return False

        return result[0]

    def get_user(self, chat_id):
        self.get_cursor().execute(
            """
            SELECT chat_id, first_name, last_name, phone
            FROM "user" 
            WHERE chat_id = %s
        """,
            (chat_id,),
        )

        result = self.get_cursor().fetchone()

        user = User()
        user.chat_id = result[0]
        user.first_name = result[1]
        user.last_name = result[2]
        user.phone = result[3]

        return user

    def add_user(self, user: User):
        self.get_cursor().execute(
            """
            CALL add_user(%s, %s, %s, %s);
            """,
            (user.chat_id, user.first_name, user.last_name, user.phone),
        )
        self.connection.commit()

    def add_entry(self, entry: Entry):
        self.get_cursor().execute(
            """
            CALL add_entry(%s, %s, %s);
            """,
            (entry.chat_id, entry.ticket_number, entry.date),
        )

        self.connection.commit()

    def update_user(self, user: User):
        self.get_cursor().execute(
            """
            CALL update_user(%s, %s, %s, %s);
            """,
            (user.chat_id, user.first_name, user.last_name, user.phone),
        )

        self.connection.commit()

    def has_user(self, chat_id):
        self.get_cursor().execute(
            """
            SELECT has_user(%s);
            """,
            (chat_id,),
        )

        return self.get_cursor().fetchone()[0]

    def update_status(self, chat_id, new_status):
        self.get_cursor().execute(
            f"""
                                  UPDATE entry
                                  SET status = '{new_status}'
                                  WHERE user_id = (SELECT id FROM "user" WHERE chat_id = {chat_id}
                                        AND status = 'Waiting')
                                  """
        )

        self.connection.commit()

    def update_status_by_ticket_number(self, ticket_number, new_status):
        self.get_cursor().execute(
            f"""
                                  UPDATE entry
                                  SET status = '{new_status}'
                                  WHERE ticket_number = {ticket_number}
                                        AND status = 'Waiting'
                                  """
        )

        self.connection.commit()

    def dispose(self):
        self.get_cursor().close()

        self.connection.commit()
        self.connection.close()

    def check_password(self, password: str):
        self.cursor.execute(
            f"""
            SELECT EXISTS (
                SELECT 1
                FROM admin
                WHERE password = '{password}'
            );
        """
        )
        exists = self.cursor.fetchone()[0]
        return exists

    def get_name_and_table_number(self, password: str):
        self.cursor.execute(
            f"""
            select
                last_name || ' ' || first_name as "full name",
                table_number
            from admin
            where password = '{password}';
        """
        )
        result = self.cursor.fetchall()[:]
        return result

    def update_status_admin(self, chat_id : int, table_number: int):
        self.cursor.execute(
            f"""
            UPDATE admin
            SET status = TRUE,
                chat_id = {chat_id}            
            WHERE table_number = {table_number};
        """
        )
        
        self.connection.commit()

    def check_admin_status(self, password: str):
        self.cursor.execute(
            f"""
            SELECT status FROM admin
            WHERE password = '{password}';
        """
        )
        result = self.cursor.fetchall()[0][0]
        if result:
            return False
        return True

    def check_user_admin(self, id: int):
        self.cursor.execute(
            f"""
            SELECT 
                1 
            FROM
                user_admin
            WHERE user_id = {id};
        """
        )
        exists = self.cursor.fetchone()
        return exists is not None

    def add_user_admin(self, id: int):
        self.cursor.execute(
            f"""
            insert into user_admin(user_id) values
            ({id});
        """
        )

        self.connection.commit()

    def update_admin(self, admin_id: int, ticket_number: int):
        self.cursor.execute(
            f"""
                        update entry 
                        set admin_id = {admin_id}
                        where ticket_number = {ticket_number};
                            """
        )

    def call_client(self):
        self.cursor.execute(
            """
            SELECT 
	            ticket_number,
	            first_name || ' ' || last_name AS full_name
            FROM entry
            JOIN "user" ON user_id = "user".id
            WHERE status = 'Waiting'
            ORDER BY entry.id
            LIMIT 1;
        """
        )
        client = self.cursor.fetchone()
        return client

    def update_client(self, admin_id: int, ticket_id: int):
        self.cursor.execute(
            f"""
            update entry
            set status = 'AtTheReception',
                admin_id = {admin_id}
            where ticket_number = {ticket_id}
        """
        )
        self.connection.commit()

    def check_client(self):
        self.cursor.execute(
            """
            SELECT 
                count(status)
            FROM entry
            WHERE status = 'Waiting'
        """
        )

        result = self.cursor.fetchone()
      
        if result:
            return result[0]
        
        return 0

    def dont_come_client(self, id):
        self.cursor.execute(
            f"""
            update entry
            set status = 'Cancel'
            where ticket_number = {id}
        """
        )
        self.connection.commit()

    def come_client(self, id):
        self.cursor.execute(
            f"""
            update entry
            set status = 'Accept'
            where ticket_number = {id}
        """
        )
        self.connection.commit()
        
    def get_table_number(self, chat_id):
        self.get_cursor().execute('''
                                SELECT table_number
                                FROM admin
                                WHERE chat_id = %s
                                  ''', (chat_id,))
        
        result = self.get_cursor().fetchone()
        return result[0]


def listen(repository: PsqlRepository):
    connection = psycopg2.connect(
        dbname=repository.dbname,
        user=repository.user,
        password=repository.password,
        host=repository.host,
        port=repository.port,
    )

    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute("LISTEN value_change;")

    while True:
        if select.select([cursor.connection], [], [], 5) == ([], [], []):
            pass
        else:
            connection.poll()
            while connection.notifies:
                notify = connection.notifies.pop(0)
                print("Got NOTIFY:", notify.pid, notify.channel, notify.payload)
                repository.notify(notify.payload)
