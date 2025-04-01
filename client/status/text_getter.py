from admin import Admin
from service_collection import ServiceCollection
from status.status import Status


class TextGetter():
    def get_text(chat_id:int, entry_id:int, status:str):
        if status == Status.Processing:
            admin:Admin = ServiceCollection.Repository.get_admin(entry_id)
            return f"Подойдите к столику №{admin.table_number}.\nВас будет обслуживать: {admin.first_name} {admin.last_name}."
        elif status == Status.Canceled:
            return "Вашу запись отменили."
        elif status == Status.Accepted:
            return "Ваш прием окончен."
        else:
            return None