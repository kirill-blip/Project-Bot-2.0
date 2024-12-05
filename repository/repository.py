from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def save_entry(self, entry):
        pass
    
    @abstractmethod
    def get_last_number(self, date):
        pass
    
    @abstractmethod
    def get_ticket_number_by_chat_id(self, chat_id):
        pass
    
    @abstractmethod
    def has_entry_by_chat_id(self, chat_id):
        pass