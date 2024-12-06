CREATE TABLE IF NOT EXISTS phone (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT NOT NULL
            );

CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                first_name TEXT NOT NULL,
                last_name INTEGER NOT NULL,
                phone_id INTEGER NOT NULL,
                FOREIGN KEY (phone_id)
                    REFERENCES phone (id));

CREATE TABLE IF NOT EXISTS admin(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                first_name TEXT NOT NULL,
                                last_name TEXT NOT NULL,
                                password TEXT NOT NULL,
                                table_number INTEGER NOT NULL
                            );

CREATE TABLE IF NOT EXISTS entry(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                ticket_number INTEGER NOT NULL,
                                user_id INTEGER NOT NULL,
                                admin_id INTEGER,
                                date TEXT NOT NULL,
                                status TEXT NOT NULL,
                                FOREIGN KEY (user_id)
                                    REFERENCES user (id));