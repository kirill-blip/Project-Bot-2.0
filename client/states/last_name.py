from entry import Entry
from helpers.name_validation import validate_name
from response import Response
from states.phone_state import PhoneState
from .state import State
from service_collection import ServiceCollection

class LastNameState(State):
    def get_message(self):
        return "Введите вашу фамилию:"
    
    def handle_message(self, message):
        if validate_name(message.text) == False:
            return Response("Фамилия должно содержать только буквы и быть длиной от 3 до 20 символов. Попробуйте еще раз.", self.get_markup())
        
        entry:Entry = ServiceCollection.FormRepository.get_form_entry(self.manager.chat_id)
        entry.last_name = message.text
        ServiceCollection.FormRepository.save_form_entry(self.manager.chat_id, entry)
        
        next_state = PhoneState(self.manager)
        self.manager.set_next_state(next_state)
        
        return Response(next_state.get_message(), next_state.get_markup())
    
    def get_markup(self):
        return None