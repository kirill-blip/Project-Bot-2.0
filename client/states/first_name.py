from entry import Entry
from helpers.name_validation import validate_name
from response import Response
from states.last_name import LastNameState
from .state import State
from service_collection import ServiceCollection

class FirstName(State):
    def get_message(self):
        return "Введите ваше имя:"
    
    def handle_message(self, message):
        if validate_name(message.text) == False:
            return Response("Имя должно содержать только буквы и быть длиной от 3 до 20 символов. Попробуйте еще раз.", self.get_markup())
        
        entry:Entry = ServiceCollection.FormRepository.get_form_entry(self.manager.chat_id)
        entry.first_name = message.text
        ServiceCollection.FormRepository.save_form_entry(self.manager.chat_id, entry)
        
        next_state = LastNameState(self.manager)
        self.manager.set_next_state(next_state)
        
        return Response(next_state.get_message(), next_state.get_markup())
    
    def get_markup(self):
        return None