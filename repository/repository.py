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
    
    @abstractmethod
    def get_status_by_entry_id(self, entry_id):
        pass
    
    @abstractmethod
    def get_chat_id_by_entry_id(self, entry_id):
        pass
    
    @abstractmethod
    def is_user_waiting(self, chat_id):
        pass
    
    @abstractmethod
    def get_user(self, chat_id):
        pass
    
    @abstractmethod
    def add_user(self, user):
        pass
    
    @abstractmethod
    def update_user(self, user):
        pass
    
    @abstractmethod
    def add_entry(self, entry):
        pass
    
    @abstractmethod
    def has_user(self, chat_id):
        pass
    
    @abstractmethod
    def update_status(self, chat_id):
        pass
    
    @abstractmethod
    def dispose(self):
        pass
    