import sys
import os
import threading

from bot import Bot
from form_repository import InMemoryFormRepository
from service_collection import ServiceCollection

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'repository'))
from psql_repository import PsqlRepository, listen
    
ServiceCollection.Repository = PsqlRepository("bot_staging", "postgres", "postgres", "localhost", "5432")
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