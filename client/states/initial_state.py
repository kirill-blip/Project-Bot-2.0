from service_collection import ServiceCollection


from response import Response
from .state import State
from telebot import types

class InitialState(State):
    def get_message(self):
        return 'Привет. Нажмите на кнопку "Записаться", чтобы записаться на прием.'
    
    def handle_message(self, message):
        if message.data == 'entry':
            if ServiceCollection.Repository.has_entry_by_chat_id(self.manager.chat_id):
                if ServiceCollection.Repository.is_user_waiting(self.manager.chat_id):
                    from states.entry_state import EntryState
                    next_state = EntryState(self.manager)
                else:
                    from states.ask_state import AskState
                    next_state = AskState(self.manager)
            else:
                from states.first_name import FirstName
                next_state = FirstName(self.manager)
                
            self.manager.set_next_state(next_state)
            
            return Response(next_state.get_message(), next_state.get_markup())
        
    
    def get_markup(self):
        markup = types.InlineKeyboardMarkup()
        
        markup.add(types.InlineKeyboardButton('Записаться', callback_data='entry'))
        
        return markup