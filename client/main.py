import sys
import os
import threading
import logging

from bot import Bot
from form_repository import InMemoryFormRepository
from helpers import psql_loader
from service_collection import ServiceCollection

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'repository'))
from psql_repository import PsqlRepository

# Настройка логгера
logging.basicConfig(
    filename='client.log',
    filemode='a',
    level=logging.DEBUG
)

ServiceCollection.LoggerService = logging.getLogger()

app_type = "production" # development or production

psql_settings = psql_loader.load_psql_settings(app_type)

# Ининциализация репозиториев
ServiceCollection.Repository = PsqlRepository(psql_settings["dbname"], psql_settings["user"], psql_settings["password"], psql_settings["host"], psql_settings["port"])
ServiceCollection.FormRepository = InMemoryFormRepository()

bot = Bot("7831619955:AAGDhO6ig-VoJDsTEKEjb0MbcgNEUaDCSho")

ServiceCollection.Repository.attach(bot)

def listen_for_notifications():
    logging.info("Listening for notifications")
    ServiceCollection.Repository.listen()

try:
    # Запуск бота и слушателя
    
    listener_thread = threading.Thread(target=listen_for_notifications)
    listener_thread.start()
    bot.run()
except Exception as e:
    ServiceCollection.LoggerService.error(e)
    print(e)

# Отключение репозиториев
ServiceCollection.FormRepository.dispose()
ServiceCollection.Repository.dispose()

listener_thread.join()
