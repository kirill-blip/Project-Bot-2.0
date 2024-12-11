import sys
import os
import threading
import logging

from bot import Bot
from form_repository import InMemoryFormRepository
from helpers import psql_loader
from service_collection import ServiceCollection

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'repository'))
from psql_repository import PsqlRepository, listen


logging.basicConfig(
    filename='client.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
ServiceCollection.LoggerService = logging.getLogger()

app_type = "development"

psql_settings = psql_loader.load_psql_settings(app_type)

ServiceCollection.Repository = PsqlRepository(psql_settings["dbname"], psql_settings["user"], psql_settings["password"], psql_settings["host"], psql_settings["port"])
ServiceCollection.FormRepository = InMemoryFormRepository()

bot = Bot("7831619955:AAGDhO6ig-VoJDsTEKEjb0MbcgNEUaDCSho")

ServiceCollection.Repository.attach(bot)

def listen_for_notifications():
    logging.info("Listening for notifications")
    listen(ServiceCollection.Repository)

listener_thread = threading.Thread(target=listen_for_notifications)
listener_thread.start()


try:
    bot.run()
except Exception as e:
    logging.error(e)

ServiceCollection.FormRepository.dispose()
ServiceCollection.Repository.dispose()

listener_thread.join()