from manager import Manager
import telebot

class Bot():
    def __init__(self, token:str):
        self.bot = telebot.TeleBot(token)
        
        self.bot.message_handler(commands=['start'])(self.handle_start_command)
        self.bot.message_handler(content_types=['text'])(self.handle_text_command)
        
        self.bot.callback_query_handler(func=self.callback_query_filter)(self.handle_button_query)
        
        self.bot.polling(none_stop=True)
        
    def callback_query_filter(self, call):
        return (call.data.startswith("entry"))
    
    def handle_button_query(self, call):
        manager = Manager(call.message.chat.id)
        response = manager.handle_message(call)
        
        self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Привет. Нажмите на кнопку "Записаться", чтобы записаться на прием.', reply_markup=None)
        self.bot.send_message(call.message.chat.id, response.text, reply_markup=response.markup)
    
    def handle_text_command(self, message):
        manager = Manager(message.chat.id)
        response = manager.handle_message(message)
        
        self.bot.send_message(chat_id=message.chat.id, text=response.message, reply_markup=response.markup)    
    
    def handle_start_command(self, message):
        manager = Manager(message.chat.id)
        response = manager.handle_message(message)
        
        print(response)
        
        self.bot.send_message(chat_id=message.chat.id, text=response.message, reply_markup=response.markup)