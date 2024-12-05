import datetime
from entry import Entry
from response import Response
from .entry_state import EntryState
from .state import State
from service_collection import ServiceCollection

class PhoneState(State):
    def get_message(self):
        return "Введите ваш номер телефона:"
    
    def handle_message(self, message):
        entry:Entry = ServiceCollection.FormRepository.get_form_entry(self.manager.chat_id)
        
        entry.chat_id = self.manager.chat_id
        entry.date = datetime.datetime.now().strftime("%Y-%m-%d")
        entry.ticket_number = ServiceCollection.Repository.get_last_number(entry.date) + 1
        
        entry.phone = message.text
        
        ServiceCollection.FormRepository.save_form_entry(self.manager.chat_id, entry)
        
        ServiceCollection.Repository.save_entry(entry)
        
        next_state = EntryState(self.manager)
        self.manager.set_next_state(next_state)
        
        return Response(next_state.get_message(), next_state.get_markup())
    
    def get_markup(self):
        return None