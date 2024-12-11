from states.state import State


class IncorrectCommandState(State):
    def get_message(self):
        return "Некорректная команда"
    
    def handle_message(self, message):
        pass
    
    def get_markup(self):
        return None