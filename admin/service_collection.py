from logging import Logger
import os
import sys


sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'repository'))
import repository

class ServiceCollection():
    Repository  : repository.Repository= None 
    LoggerService : Logger = None