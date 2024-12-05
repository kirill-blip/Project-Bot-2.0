import sys
import os
from bot import Bot
from form_repository import InMemoryFormRepository
from service_collection import ServiceCollection

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'repository'))

from sqliterepository import SQLiteRepository

ServiceCollection.Repository = SQLiteRepository()
ServiceCollection.FormRepository = InMemoryFormRepository()

bot = Bot("7831619955:AAGDhO6ig-VoJDsTEKEjb0MbcgNEUaDCSho")
