from admin import Admin
from manager import Manager
from service_collection import ServiceCollection
import telebot

import sys
sys.path.append('C:/Users/golub/Develop/College/Python/Project Bot 2.0')

from observer import Observer

class Bot(Observer):
    def __init__(self, token:str):
        self.bot = telebot.TeleBot(token)
        
        self.bot.message_handler(commands=['start'])(self.handle_start_command)
        self.bot.message_handler(content_types=['text'])(self.handle_text_command)
        
        self.bot.callback_query_handler(func=self.callback_query_filter)(self.handle_button_query)

    def update(self, entry_id):
        status:str= ServiceCollection.Repository.get_status_by_entry_id(entry_id)
        chat_id = ServiceCollection.Repository.get_chat_id_by_entry_id(entry_id)
        
        admin:Admin = ServiceCollection.Repository.get_admin(entry_id)
        
        if status == "AtTheReception":
            text = f"Подойдите к столику №{admin.table_number}.\nВас будет обслуживать: {admin.first_name} {admin.last_name}."
            self.bot.send_message(chat_id, text)
        
        if status == "Cancel":
            text = f"Вашу запись отменили."
            self.bot.send_message(chat_id, text)
    
    def run(self):
        self.bot.polling(none_stop=True)
        
    def callback_query_filter(self, call):
        return (call.data.startswith("entry")
                or call.data == "use"
                or call.data == "change"
                or call.data == "cancel")
    
    def handle_button_query(self, call):
        manager = Manager(call.message.chat.id)
        response = manager.handle_message(call)
        
        self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Привет. Нажмите на кнопку "Записаться", чтобы записаться на прием.', reply_markup=None)
        self.bot.send_message(call.message.chat.id, response.message, reply_markup=response.markup)
    
    def handle_text_command(self, message):
        manager = Manager(message.chat.id)
        response = manager.handle_message(message)
        
        self.bot.send_message(chat_id=message.chat.id, text=response.message, reply_markup=response.markup)    
    
    def handle_start_command(self, message):
        manager = Manager(message.chat.id)
        next_state = None
        
        has_entry = ServiceCollection.Repository.has_entry_by_chat_id(message.chat.id)
        is_waiting = ServiceCollection.Repository.is_user_waiting(message.chat.id)
        
        print("Has entry", has_entry)
        print("Is waiting", is_waiting)
        
        if has_entry and is_waiting:
            from states.initial_entry_state import InitialEntryState
            next_state = InitialEntryState(manager)
        else:
            from states.start_state import StartState
            next_state = StartState(manager)
        
        manager.set_next_state(next_state)
            
        response = manager.handle_message(message)
        
        self.bot.send_message(chat_id=message.chat.id, text=response.message, reply_markup=response.markup)
        
    def send_message(self, chat_id, message):
        self.bot.send_message(chat_id, message)