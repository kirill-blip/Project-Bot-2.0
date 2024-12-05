from response import Response
from service_collection import ServiceCollection
from states.state import State

class EntryState(State):
    def get_message(self):
        ticket_number = ServiceCollection.Repository.get_ticket_number_by_chat_id(self.manager.chat_id)
        
        return f"Запись №{ticket_number:04d}\nВам придет уведомление, когда очередь подойдет"
    
    def handle_message(self, message):
        return Response(self.get_message(), None)
    
    def get_markup(self):
        pass