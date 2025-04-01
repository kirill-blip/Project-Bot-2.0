from response import Response
from service_collection import ServiceCollection
from states.state import State

from telebot import types

from status.status import Status

class EntryState(State):
    def get_message(self):
        ticket_number = ServiceCollection.Repository.get_ticket_number_by_chat_id(self.manager.chat_id)
        print("Ticket number from method: ", ticket_number)
        return f"<b>Талон №{ticket_number:03d}</b>\nВам придет уведомление, когда ваша очередь подойдет."
    
    def handle_message(self, message):
        if message.data == "cancel":
            ServiceCollection.Repository.update_status(self.manager.chat_id, Status.CanceledByUser)
            return Response("Вы отменили запись", None)
    
    def get_markup(self):
        markup = types.InlineKeyboardMarkup()
        
        button = types.InlineKeyboardButton(text="Отменить запись", callback_data="cancel")
        markup.add(button)
        
        return markup