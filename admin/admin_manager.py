class AdminManager():
    admins = {}
    
    def set_is_busy_admin(self, chat_id:int, is_busy:bool):
        self.admins[chat_id] = is_busy
    
    def is_busy(self, chat_id:int):
        return chat_id in self.admins