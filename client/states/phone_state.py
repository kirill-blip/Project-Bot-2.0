from entry import Entry
from helpers.phone_validation import validate_phone
from response import Response
from ticket_manager import TicketManager
from .entry_state import EntryState
from .state import State
from service_collection import ServiceCollection

class PhoneState(State):
    def get_message(self):
        return "Введите ваш номер телефона:"
    
    def handle_message(self, message):
        if validate_phone(message.text) == False:
            return Response("Номер телефона должен начинаться с + и содержать от 10 до 15 цифр. Попробуйте еще раз.", self.get_markup())
        
        entry:Entry = ServiceCollection.FormRepository.get_form_entry(self.manager.chat_id)
        entry.phone = message.text
        ServiceCollection.FormRepository.save_form_entry(self.manager.chat_id, entry)
        
        TicketManager().create(self.manager.chat_id)
        
        next_state = EntryState(self.manager)
        self.manager.set_next_state(next_state)
        
        return Response(next_state.get_message(), next_state.get_markup())
    
    def get_markup(self):
        return None