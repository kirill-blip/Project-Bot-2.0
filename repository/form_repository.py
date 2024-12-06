from abc import ABC, abstractmethod

from entry import Entry


class FormRepository(ABC):
    @abstractmethod
    def get_form_entry(self, user_id):
        pass

    @abstractmethod
    def save_form_entry(self, chat_id: int, form_data: Entry):
        pass
    
    @abstractmethod
    def dispose(self):
        pass


class InMemoryFormRepository(FormRepository):
    entries = {}

    def get_form_entry(self, user_id):
        if user_id in self.entries:
            return self.entries[user_id]
        else:
            return Entry()

    def save_form_entry(self, chat_id: int, form_data: Entry):
        self.entries[chat_id] = form_data
        
    def dispose(self):
        self.entries.clear()
