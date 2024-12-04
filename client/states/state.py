from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def get_message(self):
        pass
    
    @abstractmethod
    def handle_message(self):
        pass
    
    @abstractmethod
    def get_markup(self):
        pass