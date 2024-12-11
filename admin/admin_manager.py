class AdminManager():
    admins = {}
    
    def set_is_busy_admin(self, chat_id:int, is_busy:bool):
        self.admins[chat_id] = is_busy
    
    def is_busy(self, chat_id:int):
        if chat_id not in self.admins:
            return False
        
        return self.admins[chat_id]