from response import Response
from service_collection import ServiceCollection
from .initial_state import InitialState
from .state import State

class StartState(State):
    def get_message(self):
        return ''
    
    def handle_message(self, message):
        if ServiceCollection.Repository.has_entry_by_chat_id(self.manager.chat_id):
            if ServiceCollection.Repository.is_user_waiting(self.manager.chat_id):
                from states.entry_state import EntryState
                next_state = EntryState(self.manager)
            else:
                from states.ask_state import AskState
                next_state = AskState(self.manager)
        else:              
            next_state = InitialState(self.manager)
            
        self.manager.set_next_state(next_state)
        
        return Response(next_state.get_message(), next_state.get_markup())
    
    def get_markup(self):
        return None