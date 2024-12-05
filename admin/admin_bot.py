import telebot

class Admin_bot():
    def __init__(self, token:str):
        self.bot = telebot.TeleBot(token)
        
        self.bot.message_handler(commands=['start'])(self.handle_start_command)
        
        self.bot.polling(none_stop=True)
        
    def handle_start_command(self, message):
        self.bot.send_message(message.chat.id, 'Hello, I am a bot!')