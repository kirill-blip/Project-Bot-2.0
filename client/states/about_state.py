from response import Response
from states.state import State


class AboutState(State):
    def get_message(self):
        text = 'ℹ *О боте*. Бот предназначен для контроля электронной очереди в приемной коммиссии колледжа AITU.\n\nБот создан *студентами* колледжа AITU:\n\t@KirillBlip - Голубенко Кирилл\n\t@alikhan131 - Джамбул Алихан\n\t@dinishok - Азирбаев Динислам'
        return text
    
    def handle_message(self, message):
        return Response(self.get_message(), self.get_markup())
    
    def get_markup(self):
        return None