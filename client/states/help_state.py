from states.state import State

from response import Response


class HelpState(State):
    def get_message(self):
        text = "📋 *Помощь*.\n\n\tСписок доступных команд:\n\t/entry - запись\n\t/help - помощь\n\t/about - информация о боте\n\n📌 Чтобы получить талон на прием, введите команду /entry и следуйте дальнейшим инструкциям."
        return text
    
    def handle_message(self, message):
        return Response(self.get_message(), self.get_markup())
    
    def get_markup(self):
        return None
    