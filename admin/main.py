import logging
import sys
import os
from admin_bot import AdminBot
from helpers import psql_loader
from service_collection import ServiceCollection

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'repository'))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data'))

from psql_repository import PsqlRepository
from token_loader import TryParseToken
from token_loader import ParseToken

logging.basicConfig(
    filename='admin.log',
    filemode='a',
    level=logging.DEBUG
)

ServiceCollection.LoggerService = logging.getLogger()

app_type = "production" # development or production

if TryParseToken() == True:
    token = ParseToken("admin")
    ServiceCollection.LoggerService.info("Token found")
else:
    print('Token not found')
    exit()

# Загрузка настроек для подключения к БД
psql_settings = psql_loader.load_psql_settings(app_type)

print(psql_settings)

# Ининциализация репозиториев
ServiceCollection.Repository = PsqlRepository(psql_settings["dbname"], psql_settings["user"], psql_settings["password"], psql_settings["host"], psql_settings["port"])

try:
    # Запуск бота
    ServiceCollection.LoggerService.info("Starting bot")
    bot = AdminBot(token)
except Exception as e:
    ServiceCollection.LoggerService.error(e)
    print(e)