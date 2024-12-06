from db_setup import create_db


class Setup():
    def __init__(self):
        self.database = None

database_type = input("Выберите базу данных (psql/sqlite): ")

if database_type == "psql":
    dbname = input("Введите имя базы данных: ")
    user = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    host = input("Введите хост: ")
    port = input("Введите порт: ")
    
    print("Создание файла конфигурации для psql...")
    with open("data/psql_settings.json", "w") as file:
        config = f'''
        "dbname": "{dbname}",
        "user": "{user}",
        "password": "{password}",
        "host": "{host}",
        "port": "{port}"'''
    
        config = "{" + config + "\n}"

        file.write(config)
    
print("Создание файла конфигурации...")
with open("data/settings.json", "w") as file:
    config = f'''
        "database": "{database_type}"'''
    
    config = "{" + config + "\n}"
    
    file.write(config)

print("Создание таблиц...")
create_db()
