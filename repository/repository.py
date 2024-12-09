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
    def check_password(self, password : str):
        pass

    @abstractmethod
    def get_name_and_num(self, password : str):
        pass

    @abstractmethod
    def update_status_admin(self, table_number : int):
        pass

    @abstractmethod
    def check_admin_status(self, password : str):
        pass

    @abstractmethod
    def check_user_admin(self, id : int):
        pass

    @abstractmethod
    def add_user_admin(self, id : int):
        pass

    @abstractmethod
    def call_client(self):
        pass

    @abstractmethod
    def update_client(self, id : int):
        pass

    @abstractmethod
    def check_client(self):
        pass

    @abstractmethod
    def come_client(self):
        pass

    @abstractmethod
    def dont_come_client(self):
        pass