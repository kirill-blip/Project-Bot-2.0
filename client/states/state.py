from abc import ABC, abstractmethod
from manager import Manager

class State(ABC):
    def __init__(self, manager):
        self.manager:Manager = manager
        
    @abstractmethod
    def get_message(self):
        pass
    
    @abstractmethod
    def handle_message(self, message):
        pass
    
    @abstractmethod
    def get_markup(self):
        pass