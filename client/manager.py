from states.entry_state import EntryState
from states.first_name import FirstName
from states.last_name import LastNameState
from states.phone_state import PhoneState
from states.start_state import StartState
import response

# Это класс, который обрабатывает переходы состояний и обработку сообщений для чат-бота.
class Manager():
    states = {}
    
    def __init__(self, chat_id : int):
        self.chat_id = chat_id
        print(self.states)
        
    def handle_message(self, message) -> response.Response:
        self.ensure_chat_id_has_state()
        return self.states[self.chat_id].handle_message(message)
    
    def set_next_state(self, state):
        self.states[self.chat_id] = state
    
    def ensure_chat_id_has_state(self):
        if self.states.get(self.chat_id) is None:
            self.states[self.chat_id] = StartState(self)
            
    def is_form(self):
        return isinstance(self.states[self.chat_id], (FirstName, LastNameState, PhoneState))
    
    def is_entry_state(self):
        if self.states.get(self.chat_id) is None:
            return False
        
        return isinstance(self.states[self.chat_id], EntryState)
