from response import Response
from .initial_state import InitialState
from .state import State

class StartState(State):
    def get_message(self):
        return ''
    
    def handle_message(self, message):
        next_state = InitialState(self.manager)
        self.manager.set_next_state(next_state)
        
        return Response(next_state.get_message(), next_state.get_markup())
    
    def get_markup(self):
        return None