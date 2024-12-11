import sys
import os
import threading

from bot import Bot
from form_repository import InMemoryFormRepository
from service_collection import ServiceCollection

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'repository'))
from psql_repository import PsqlRepository, listen
import json

app_type = "development"

psql_settings = {}    

if app_type == "development":
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    json_file_path = os.path.join(data_dir, 'psql_settings_develop.json')

    with open(json_file_path, 'r') as f:
        data = json.load(f)
        psql_settings.update(data)
elif app_type == "production":
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    json_file_path =os.path.join(data_dir, 'psql_settings.json')

    with open(json_file_path, 'r') as f:
        data = json.load(f)
        psql_settings.update(data)

print(psql_settings)

ServiceCollection.Repository = PsqlRepository(psql_settings["dbname"], psql_settings["user"], psql_settings["password"], psql_settings["host"], psql_settings["port"])
ServiceCollection.FormRepository = InMemoryFormRepository()

bot = Bot("7831619955:AAGDhO6ig-VoJDsTEKEjb0MbcgNEUaDCSho")

ServiceCollection.Repository.attach(bot)

def listen_for_notifications():
    listen(ServiceCollection.Repository)

listener_thread = threading.Thread(target=listen_for_notifications)
listener_thread.start()

bot.run()

ServiceCollection.FormRepository.dispose()
ServiceCollection.Repository.dispose()
listener_thread.join()