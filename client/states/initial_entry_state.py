from response import Response
from service_collection import ServiceCollection
from states.entry_state import EntryState
from states.state import State

from telebot import types

class InitialEntryState(State):
    def get_message(self):
        return None
    
    def handle_message(self, message):
        next_state = EntryState(self.manager)
        self.manager.set_next_state(next_state)
        
        return Response(next_state.get_message(), next_state.get_markup())
    
    def get_markup(self):
        None