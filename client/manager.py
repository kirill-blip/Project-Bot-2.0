from states.start_state import StartState
import response

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