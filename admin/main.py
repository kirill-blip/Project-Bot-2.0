import sys
import os
from admin_bot import Admin_bot
from service_collection import ServiceCollection

# Добавляем путь к папке repository
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'repository'))

# Теперь можно импортировать модули из папки repository
from psql_repository import PsqlRepository
ServiceCollection.Repository = PsqlRepository("bot_staging", "postgres", "postgres", "localhost", "5432")
try:
    bot = Admin_bot("8177585416:AAGoas6yHV8dGmH5bTxFHu3Tpcnxqe9GwPw")
except Exception as e:
    print(e)