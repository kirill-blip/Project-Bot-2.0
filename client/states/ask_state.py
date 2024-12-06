from response import Response
from service_collection import ServiceCollection
from states.state import State
from ticket_manager import TicketManager
from user import User
from telebot import types

class AskState(State):
    def get_message(self):
        text = "Вы уже вводили данные"
        
        user:User = ServiceCollection.Repository.get_user(self.manager.chat_id)
        
        text += f"\nИмя: {user.first_name}"
        text += f"\nФамилия: {user.last_name}"
        text += f"\nТелефон: {user.phone}"
        
        return text

    def handle_message(self, message):
        next_state = None
        
        if message.data == "use":
            from states.entry_state import EntryState
            
            TicketManager().create(self.manager.chat_id, True)
            next_state = EntryState(self.manager)
        
            self.manager.set_next_state(next_state)
            
            return Response(next_state.get_message(), next_state.get_markup())
        elif message.data == "change":
            from states.first_name import FirstName
            next_state = FirstName(self.manager)
            
            self.manager.set_next_state(next_state)
            
            return Response(next_state.get_message(), next_state.get_markup())
            
    def get_markup(self):
        markup = types.InlineKeyboardMarkup()
        
        use_button = types.InlineKeyboardButton("Использовать", callback_data="use")
        new_button = types.InlineKeyboardButton("Изменить", callback_data="change")
        
        markup.add(use_button, new_button)
        
        return markup
        