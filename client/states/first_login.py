from response import Response
from states.state import State


class FirstLogin(State):
    def get_message(self):
        return 'Добро пожаловать! Для начала работы введите команду /entry'

    def handle_message(self, message):
        return Response(self.get_message(), self.get_markup())

    def get_markup(self):
        return None
    