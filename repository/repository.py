from abc import ABC, abstractmethod

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from client.entry import Entry
from client.user import User

class Repository(ABC):
    @abstractmethod
    def save_entry(self, entry: Entry):
        pass

    @abstractmethod
    def get_last_number(self, date):
        pass

    @abstractmethod
    def get_ticket_number_by_chat_id(self, chat_id: int):
        pass

    @abstractmethod
    def has_entry_by_chat_id(self, chat_id: int):
        pass

    @abstractmethod
    def get_status_by_entry_id(self, entry_id: int):
        pass

    @abstractmethod
    def get_chat_id_by_entry_id(self, entry_id: int):
        pass

    @abstractmethod
    def is_user_waiting(self, chat_id: int):
        pass

    @abstractmethod
    def get_user(self, chat_id: int):
        pass

    @abstractmethod
    def add_user(self, user: User):
        pass

    @abstractmethod
    def update_user(self, user: User):
        pass

    @abstractmethod
    def add_entry(self, entry: Entry):
        pass

    @abstractmethod
    def has_user(self, chat_id: int):
        pass

    @abstractmethod
    def update_status(self, chat_id: int):
        pass

    @abstractmethod
    def has_entry_by_chat_id(self, chat_id: int):
        pass

    @abstractmethod
    def check_password(self, password: str):
        pass

    @abstractmethod
    def get_name_and_table_number(self, password: str):
        pass

    @abstractmethod
    def update_status_admin(self, chat_id, table_number: int):
        pass

    @abstractmethod
    def check_admin_status(self, password: str):
        pass

    @abstractmethod
    def check_user_admin(self, id: int):
        pass

    @abstractmethod
    def add_user_admin(self, id: int):
        pass

    @abstractmethod
    def call_client(self):
        pass

    @abstractmethod
    def get_admin(self, entry: int):
        pass

    @abstractmethod
    def get_admin_by_chat_id(self, admin_id: int):
        pass

    @abstractmethod
    def get_admin_id_by_chat_id(self, chat_id:int):
        pass

    @abstractmethod
    def update_client(self, admin_id: int, ticket_id: int):
        pass

    @abstractmethod
    def is_client_waiting(self):
        pass

    @abstractmethod
    def accept_entry(self):
        pass

    @abstractmethod
    def cancel_entry(self):
        pass

    @abstractmethod
    def update_status_by_ticket_number(self, ticket_number: int, new_status: str):
        pass

    @abstractmethod
    def get_table_number(self, chat_id: int):
        pass

    @abstractmethod
    def get_last_date(self, chat_id: int):
        pass

    @abstractmethod
    def update_table_info(
        self, table_number: int, name: str, last_name: str, password: str
    ):
        pass

    @abstractmethod
    def check_table_number(self, table_number: int):
        pass

    @abstractmethod
    def add_admin(self, table_number: int, name: str, last_name: str, password: str):
        pass

    @abstractmethod
    def check_password_admin(self, password: str):
        pass
    
    @abstractmethod
    def remove_admin(self, chat_id: int):
        pass

    @abstractmethod
    def listen(self):
        pass

    @abstractmethod
    def dispose(self):
        pass
