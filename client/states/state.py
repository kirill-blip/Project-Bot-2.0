from abc import ABC, abstractmethod
import sys

sys.path.append("../..")

class State(ABC):
    def __init__(self, manager):
        from manager import Manager
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