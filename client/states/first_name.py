from .state import State

class FirstName(State):
    def get_message(self):
        return "Введите ваше имя:"
    
    def handle_message(self, message):
        pass
    
    def get_markup(self):
        return None