from states.state import State

from response import Response


class HelpState(State):
    def get_message(self):
        return "Помощь. В разработке."
    
    def handle_message(self, message):
        return Response(self.get_message(), self.get_markup())
    
    def get_markup(self):
        return None
    