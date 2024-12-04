from states.first_name import FirstName

from response import Response
from .state import State
from telebot import types

class InitialState(State):
    def get_message(self):
        return 'Привет. Нажмите на кнопку "Записаться", чтобы записаться на прием.'
    
    def handle_message(self, message):
        if message.data == 'entry':
            next_state = FirstName()
            self.manager.set_next_state(next_state)
            
            return Response(next_state.get_message(), next_state.get_markup())
        
    
    def get_markup(self):
        markup = types.InlineKeyboardMarkup()
        
        markup.add(types.InlineKeyboardButton('Записаться', callback_data='entry'))
        
        return markup