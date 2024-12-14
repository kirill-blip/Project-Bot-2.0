import json
import sys
import os
from admin_bot import AdminBot
from service_collection import ServiceCollection

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'repository'))

from psql_repository import PsqlRepository

app_type = "development" # development or production

psql_settings = {}    

if app_type == "development":
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    json_file_path = os.path.join(data_dir, 'psql_settings_develop.json')

    with open(json_file_path, 'r') as file:
        data = json.load(file)
        psql_settings.update(data)
elif app_type == "production":
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    json_file_path =os.path.join(data_dir, 'psql_settings.json')

    with open(json_file_path, 'r') as file:
        data = json.load(file)
        psql_settings.update(data)

print(psql_settings)

ServiceCollection.Repository = PsqlRepository(psql_settings["dbname"], psql_settings["user"], psql_settings["password"], psql_settings["host"], psql_settings["port"])

bot = AdminBot("8177585416:AAGoas6yHV8dGmH5bTxFHu3Tpcnxqe9GwPw")

try:
    pass
except Exception as e:
    print(e)