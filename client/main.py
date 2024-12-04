import sys
import os
from bot import Bot
from service_collection import ServiceCollection

# Добавляем путь к папке repository
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'repository'))

# Теперь можно импортировать модули из папки repository
from sqliterepository import SQLiteRepository
ServiceCollection.Repository = SQLiteRepository()
try:
    bot = Bot("7831619955:AAGDhO6ig-VoJDsTEKEjb0MbcgNEUaDCSho")
except Exception as e:
    print(e)