import json
import sqlite3
import os

import psycopg2

def create_db():
    db_type:str = ""
    
    with open("data/settings.json") as f:
        settings = json.load(f)
        db_type = settings["database"]
    
    print(db_type)
    
    if db_type == "sqlite":
        connection = sqlite3.connect('repository/example.db')
    
        script_path = os.path.join(os.path.dirname(__file__), 'sqlite.sql')
        with open(script_path, 'r') as sql_file:
            sql_script = sql_file.read()
        
        connection.executescript(sql_script)

        connection.commit()
        connection.close()
    
    elif db_type == "psql":
        with open("data/psql_settings.json") as f:
            settings = json.load(f)
        
        dbname = settings["dbname"]
        user = settings["user"]
        password = settings["password"]
        host = settings["host"]
        port = settings["port"]

        connection = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {dbname}")

        cursor.close()
        connection.close()

        connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cursor = connection.cursor()

        script_path = os.path.join(os.path.dirname(__file__), 'psql.sql')
        with open(script_path, 'r') as sql_file:
            sql_script = sql_file.read()

        cursor.execute(sql_script)

        connection.commit()
        connection.close()