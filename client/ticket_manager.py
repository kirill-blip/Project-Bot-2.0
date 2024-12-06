import datetime
from entry import Entry
from service_collection import ServiceCollection
from user import User

class TicketManager():
    def create(self, chat_id:int, use_old:bool = False):
        entry:Entry = ServiceCollection.FormRepository.get_form_entry(chat_id)
        entry.chat_id = chat_id
        
        last_number = ServiceCollection.Repository.get_last_number()
        entry.date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        if last_number is None:
            entry.ticket_number = 1
        else:
            entry.ticket_number = last_number + 1
            
        ServiceCollection.FormRepository.save_form_entry(chat_id, entry)
        
        if use_old:
            user:User = ServiceCollection.Repository.get_user(chat_id)
            
            entry.first_name = user.first_name
            entry.last_name = user.last_name
            entry.phone = user.phone
            
            ServiceCollection.Repository.add_entry(entry)
        else:
            entry = ServiceCollection.FormRepository.get_form_entry(chat_id)
            
            user:User = User()
            
            user.chat_id = chat_id
            user.first_name = entry.first_name
            user.last_name = entry.last_name
            user.phone = entry.phone
            
            print("User:", entry.first_name)
            print("User:", entry.last_name)
            print("User:", entry.phone)
            
            if ServiceCollection.Repository.has_user(chat_id):
                ServiceCollection.Repository.update_user(user)
            else:
                ServiceCollection.Repository.add_user(user)
                
            print("Ticket Number:", entry.ticket_number)
            print("Date:", entry.date)    
            
            ServiceCollection.Repository.add_entry(entry)
            