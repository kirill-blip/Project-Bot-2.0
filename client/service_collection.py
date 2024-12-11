import os
import sys
from logging import Logger

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'repository'))
import repository
import form_repository

class ServiceCollection():
    Repository  : repository.Repository= None 
    FormRepository : form_repository.FormRepository = None
    LoggerService : Logger = None