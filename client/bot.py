from admin import Admin
from manager import Manager
from response import Response
from service_collection import ServiceCollection
import telebot

import sys
import os

from states.about_state import AboutState
from states.first_login import FirstLogin
from states.help_state import HelpState
from status.status import Status
from status.text_getter import TextGetter
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from observer import Observer

class Bot(Observer):
    def __init__(self, token:str):
        # Инициализация бота
        ServiceCollection.LoggerService.info("Bot creating")
        self.bot = telebot.TeleBot(token)
        
        self.last_bot_message = {}
        self.last_user_message = {}
        
        self.bot.message_handler(commands=['start'])(self.handle_start_command)
        self.bot.message_handler(commands=['entry'])(self.handle_entry_command)
        self.bot.message_handler(commands=['about'])(self.handle_about_command)
        self.bot.message_handler(commands=['help'])(self.handle_help_command)
        self.bot.message_handler(content_types=['text'])(self.handle_text_command)
        
        self.bot.callback_query_handler(func=self.callback_query_filter)(self.handle_button_query)
        
    def update(self, entry_id:int):
        chat_id = ServiceCollection.Repository.get_chat_id_by_entry_id(entry_id)
        status:str= ServiceCollection.Repository.get_status_by_entry_id(entry_id)

        text = TextGetter.get_text(chat_id, entry_id, status)
        
        if status == Status.AtTheReception:
            try:
                self.bot.edit_message_reply_markup(chat_id, self.last_bot_message[chat_id], reply_markup=None)
            except telebot.apihelper.ApiException as e:
                ServiceCollection.LoggerService.error(f"Failed to edit message reply markup: {e}")
                print(f"Failed to edit message reply markup: {e}")
        
        if text is not None:
            message = self.bot.send_message(chat_id, text, parse_mode="Markdown")
            self.last_bot_message[chat_id] = message.message_id
    
    def run(self):
        ServiceCollection.LoggerService.info("Bot running")
        self.bot.polling(none_stop=True)
        
    def callback_query_filter(self, call):
        # Фильтр для обработки нажатий на кнопки
        return (call.data.startswith("entry")
                or call.data == "use"
                or call.data == "change"
                or call.data == "cancel")
        
    def handle_button_query(self, call):
        # Обработка нажатий на кнопки
        ServiceCollection.LoggerService.info(f"Button query from {call.message.chat.id}")
        
        manager = Manager(call.message.chat.id)
        response = manager.handle_message(call)
        
        self.last_user_message[call.message.chat.id] = call.message.message_id
        
        self.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        self.send_message(call.message.chat.id, response.message, response.markup)

    def handle_text_command(self, message):
        # Обработка текстовых сообщений
        ServiceCollection.LoggerService.info(f"Text command from {message.chat.id}")
        
        manager = Manager(message.chat.id)
        self.last_user_message[message.chat.id] = message.message_id
        
        if manager.is_entry_state():
            self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        elif manager.is_form():
            response = manager.handle_message(message)
            message = self.bot.send_message(message.chat.id, response.message, reply_markup=response.markup, parse_mode="HTML")
            self.last_bot_message[message.chat.id] = message.message_id
        else:
            self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    
    def handle_about_command(self, message):
        # Обработка команды /about
        ServiceCollection.LoggerService.info(f"About command from {message.chat.id}")
        manager = Manager(message.chat.id)
        
        if manager.is_form():
            self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            return
        
        self.last_user_message[message.chat.id] = message.message_id
        
        next_state = AboutState(manager)
        manager.set_next_state(next_state)
        
        response:Response = manager.handle_message(message)
        
        self.send_message(message.chat.id, response.message, response.markup)
        
    def handle_help_command(self, message):
        # Обработка команды /help
        ServiceCollection.LoggerService.info(f"Help command from {message.chat.id}")
        manager = Manager(message.chat.id)
        
        if manager.is_form():
            self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            return
        
        self.last_user_message[message.chat.id] = message.message_id
        
        next_state = HelpState(manager)
        manager.set_next_state(next_state)
        
        response:Response = manager.handle_message(message)
        
        self.send_message(message.chat.id, response.message, response.markup)
    
    def handle_entry_command(self, message):
        # Обработка команды /entry
        ServiceCollection.LoggerService.info(f"Entry command from {message.chat.id}")
        manager = Manager(message.chat.id)
        next_state = None
        
        has_entry = ServiceCollection.Repository.has_entry_by_chat_id(message.chat.id)
        is_waiting = ServiceCollection.Repository.is_user_waiting(message.chat.id)
        
        print("Is waiting: ", is_waiting)
        
        if has_entry and is_waiting:
            from states.initial_entry_state import InitialEntryState
            next_state = InitialEntryState(manager)
        
        manager.set_next_state(next_state)
        response = manager.handle_message(message)
        
        self.send_message(message.chat.id, response.message, response.markup)
    
    def handle_start_command(self, message):
        # Обработка команды /start
        ServiceCollection.LoggerService.info(f"Start command from {message.chat.id}")
        
        if self.last_user_message.get(message.chat.id):
            self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            return
        
        self.last_user_message[message.chat.id] = message.message_id
        
        manager = Manager(message.chat.id)
        next_state = FirstLogin(manager)
        manager.set_next_state(next_state)
        
        response = manager.handle_message(message)
        self.send_message(message.chat.id, response.message, response.markup)
        
    def send_message(self, chat_id, message, reply_markup=None):
        # Удаляем старое сообщение
        if chat_id in self.last_bot_message:
            try:
                self.bot.edit_message_reply_markup(chat_id, self.last_bot_message[chat_id], reply_markup=None)
            except telebot.apihelper.ApiException as e:
                print(f"Failed to edit message reply markup: {e}")
        
        parse_mode = "Markdown"
        
        if any(tag in message for tag in ["<b>", "</b>"]):
            parse_mode = "HTML"
        
        # Отправляем новое сообщение
        ServiceCollection.LoggerService.info(f"Sending message to {chat_id}: {message}")
        message = self.bot.send_message(chat_id, text=message, reply_markup=reply_markup, parse_mode=parse_mode)
        self.last_bot_message[chat_id] = message.message_id
