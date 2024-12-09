import telebot
from service_collection import ServiceCollection
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

class Admin_bot():
    def __init__(self, token:str):
        self.bot = telebot.TeleBot(token)
        self.attempts = {}
        self.information = []
        self.no_admin = 0
        self.info_user = ""
        

        self.bot.message_handler(commands=['start'])(self.handle_start_command)
        self.bot.message_handler(func=self.handle_password_input)(self.process_message)
        self.bot.message_handler(func=self.handle_button_press)(self.handle_button_action)

        self.bot.callback_query_handler(func=lambda call: call.data in ["no", "yes"])(self.handle_inline_button_action)

        self.bot.polling(none_stop=True)
    
    def handle_inline_button_action(self, call):
        if call.data == "no":
            self.handle_no_action(self.info_user)
        elif call.data == "yes":
            self.handle_yes_action(self.info_user)
        
        self.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        self.bot.answer_callback_query(call.id)
        self.waiting_for_button = False
        
    def handle_start_command(self, message):
        user_id = message.chat.id
        
        
        user_exists = ServiceCollection.Repository.check_user_admin(user_id)

        if user_exists:
            self.bot.send_message(user_id, "Вас уже пробили!")
            return False
        else:
            ServiceCollection.Repository.add_user_admin(user_id)
            self.bot.send_message(user_id, "Вас пробили")
            
        self.attempts[user_id] = 3
        self.bot.send_message(message.chat.id, 'Введите пароль для входа. Ваше количество попыток 3')

    def handle_password_input(self, message):
        user_id = message.chat.id

        if user_id not in self.attempts:
            return   

        if self.attempts[user_id] <= 0:   
            self.bot.send_message(user_id, "Вы больше не сможете войти!")
            self.no_admin = 1

            return False
        
        password = message.text
        if ServiceCollection.Repository.check_password(password):
            if ServiceCollection.Repository.check_admin_status(password) == False:
                self.bot.send_message(user_id, "Этот стол уже занят")
            else:    
                result = ServiceCollection.Repository.get_name_and_num(password)
                ServiceCollection.Repository.update_status_admin(result[0][1])
                self.information.append(result[0][1])
                self.bot.send_message(user_id, f"Пароль верный! Добро пожаловать {result[0][0]}.")
                self.send_button(user_id)
                del self.attempts[user_id]
                self.no_admin += 2
                return True
        else:
            self.attempts[user_id] -= 1  
            if self.attempts[user_id] > 0:
                self.bot.send_message(user_id, f"Неверный пароль. Осталось попыток: {self.attempts[user_id]}.")
            else:
                self.bot.send_message(user_id, "Вы исчерпали количество попыток.")
                self.no_admin = 1
                return False
    
    def send_button(self, user_id):
        if self.no_admin != 2:
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            button = KeyboardButton("Вызвать клиента")
            markup.add(button)
        
            self.bot.send_message(user_id, "Нажмите кнопку, чтобы вызвать человека", reply_markup=markup)

    def handle_button_press(self, message):
        if message.text == "Вызвать клиента":
            self.handle_button_action(message)


    def handle_button_action(self, message):
        if self.no_admin == 0 or self.no_admin == 1:
            return
        exists = ServiceCollection.Repository.check_client
        if exists != 0:
            client = ServiceCollection.Repository.call_client()
            ServiceCollection.Repository.update_client(client[0])
            self.info_user = client[0]
            self.bot.send_message(message.chat.id, f"Абитуриент: {client[1]}\nНомер: {client[0]}", reply_markup=self.send_inline_button())
            # 
        else:
            self.bot.send_message(message.chat.id, "Больше нет клиентов")


    def process_message(self, message):
        table_info = ', '.join(str(i) for i in self.information)
        self.bot.send_message(message.chat.id, f"Вы можете приступить к работе! Ваш стол № {table_info}")


    def send_inline_button(self):
        markup = InlineKeyboardMarkup()
            
        button1 = InlineKeyboardButton(text="Не пришел", callback_data="no")
        button2 = InlineKeyboardButton(text="Сдал", callback_data="yes")
            
        markup.add(button1, button2)
        return markup

    def handle_no_action(self, id):
        ServiceCollection.Repository.dont_come_client(id)

    def handle_yes_action(self, id):
        ServiceCollection.Repository.come_client(id)
        

