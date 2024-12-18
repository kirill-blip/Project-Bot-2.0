import telebot
from admin_manager import AdminManager
from service_collection import ServiceCollection
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


class AdminBot:
    def __init__(self, token: str):
        self.bot = telebot.TeleBot(token)
        self.attempts = {}
        self.information = []
        self.no_admin = 0
        self.info_user = ""
        self.waiting_for_button = False
        
        self.admin_manager = AdminManager()

        self.bot.message_handler(commands=["start"])(self.handle_start_command)
        self.bot.message_handler(commands=["reset_attempts"])(self.handle_reset_command)
        self.bot.message_handler(func=self.handle_password_input)(self.process_message)
        self.bot.message_handler(func=self.handle_button_press)(
            self.call_client
        )

        self.bot.message_handler(func=lambda message: self.waiting_for_button)(
            self.warn_user_to_press_button
        )

        self.bot.callback_query_handler(func=lambda call: call.data in ["no", "yes"])(
            self.handle_inline_button_action
        )

        self.bot.polling(none_stop=True)

    def handle_inline_button_action(self, call):
        if call.data == "no":
            self.handle_no_action(call.message.chat.id, self.info_user)
        elif call.data == "yes":
            self.handle_yes_action(call.message.chat.id, self.info_user)

        self.bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )
        self.bot.answer_callback_query(call.id)
        self.waiting_for_button = False

    def handle_start_command(self, message):
        user_id = message.chat.id

        user_exists = ServiceCollection.Repository.check_user_admin(user_id)

        if user_exists:
            return False
        else:
            ServiceCollection.Repository.add_user_admin(user_id)

        self.attempts[user_id] = 3
        self.bot.send_message(
            message.chat.id, "❗️ *Обратите внимание* ❗️. После *трёх* неправильных попыток *Вы не сможете больше войти.*", parse_mode="Markdown"
        )
        self.bot.send_message(
            message.chat.id, "Введите пароль для входа. Ваше количество попыток 3."
        )
        
    def handle_reset_command(self, message):
        user_id = message.chat.id
        user_exists = ServiceCollection.Repository.check_user_admin(user_id)
        
        if user_exists:
            self.attempts[user_id] = 3
            self.bot.send_message(
                message.chat.id, "Количество попыток сброшено до 3."
            )
        else:
            self.bot.send_message(
                message.chat.id, "Вы не являетесь администратором."
            )

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
                self.bot.send_message(user_id, "Этот стол уже занят.")
            else:
                result = ServiceCollection.Repository.get_name_and_table_number(password)
                ServiceCollection.Repository.update_status_admin(user_id, result[0][1])
                
                self.information.append(result[0][1])
                
                self.bot.send_message(
                    user_id, f"Пароль верный! Добро пожаловать {result[0][0]}."
                )
                
                self.send_button(user_id)
                del self.attempts[user_id]
                self.no_admin += 2
                
                return True
        else:
            self.attempts[user_id] -= 1
            if self.attempts[user_id] > 0:
                self.bot.send_message(
                    user_id,
                    f"Неверный пароль. Осталось попыток: {self.attempts[user_id]}.",
                )
            else:
                self.bot.send_message(user_id, "Вы исчерпали количество попыток.")
                self.no_admin = 1
                return False

    def send_button(self, user_id):
        if self.no_admin != 2:
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            button = KeyboardButton("Вызвать клиента")
            update_button = KeyboardButton("Обновить информацию о столе")
            add_admin_button = KeyboardButton("Добавить администратора")
            markup.add(button)
            markup.add(update_button)
            markup.add(add_admin_button)

            self.bot.send_message(
                chat_id=user_id, text="Нажмите кнопку, чтобы вызвать человека.", reply_markup=markup
            )

    def handle_button_press(self, message):
        if ServiceCollection.Repository.check_user_admin(message.chat.id) == False:
            self.bot.send_message(message.chat.id, "Вы не являетесь больше администратором.")
            return
        
        if message.text == "Вызвать клиента":
            self.call_client(message)
        elif message.text == "Обновить информацию о столе" and self.no_admin not in [0, 1]:
            text = "Чтобы обновить информацию о столе, надо воспользоваться:\n\t`/update_table_info 'номер стола' 'имя' 'фамилия' 'пароль'`.\n\n*Пример*:\n\t`/update_table_info 1 Иван Иванов 1234`"
            self.bot.send_message(chat_id=message.chat.id, text=text, parse_mode="Markdown")
        elif message.text == "Добавить администратора" and self.no_admin not in [0, 1]:
            text = "Чтобы добавить администратора, надо воспользоваться:\n\t<code>/add_admin 'номер стола' 'имя' 'фамилия' 'пароль'</code>.\n\n<b>Пример</b>:\n\t<code>/add_admin 1 Иван Иванов 1234</code>"
            self.bot.send_message(chat_id=message.chat.id, text=text, parse_mode="HTML")
        elif message.text.count("/update_table_info") == 1:
            self.update_table_info(message)
        elif message.text.count("/add_admin") == 1:
            self.add_admin(message)
            
        print(message.text)

    def add_admin(self, message):
        if self.no_admin in [0, 1]:
            return
        
        text = message.text.split()
        
        try:
            table_number = text[1]
            name = text[2]
            last_name = text[3]
            password = text[4]
            
            print(table_number, name, last_name, password)
            
            print(ServiceCollection.Repository.check_table_number(table_number))
            
            if ServiceCollection.Repository.check_table_number(table_number):
                self.bot.send_message(chat_id=message.chat.id, text="Стол с таким номером уже существует.")
                return
            
            if ServiceCollection.Repository.check_password_admin(password):
                self.bot.send_message(chat_id=message.chat.id, text="Пароль уже занят.")
                return
            
            ServiceCollection.Repository.add_admin(table_number, name, last_name, password)
            
            self.bot.send_message(chat_id=message.chat.id, text="Администратор *успешно* добавлен.", parse_mode="Markdown")
        except:
            self.bot.send_message(chat_id=message.chat.id, text="Введите все данные.")
            return

    def update_table_info(self, message):
        if self.no_admin in [0, 1]:
            return
        
        text = message.text.split()
        
        table_number = text[1]
        name = text[2]
        surname = text[3]
        password = ""
        
        try:
            password = text[4]
            
            if ServiceCollection.Repository.check_password_admin(password):
                self.bot.send_message(chat_id=message.chat.id, text="Пароль уже занят.")
                return
        except:
            pass
        
        ServiceCollection.Repository.update_table_info(table_number, name, surname, password)
        
        self.bot.send_message(chat_id=message.chat.id, text="Информация о столе *успешно* обновлена.", parse_mode="Markdown")

    def call_client(self, message):
        if self.no_admin in [0, 1]:
            return
        
        exists = ServiceCollection.Repository.is_client_waiting()
        
        if self.admin_manager.is_busy(message.chat.id):
            self.bot.delete_message(message.chat.id, message.message_id)
            self.warn_user_to_press_button(message)
            return
        
        if exists != 0:
            self.admin_manager.set_is_busy_admin(message.chat.id, True)
            
            client = ServiceCollection.Repository.call_client()
            table_number = ServiceCollection.Repository.get_table_number(message.chat.id)
            
            ServiceCollection.Repository.update_client(table_number, client[0])
            
            self.info_user = client[0]
            
            self.bot.send_message(
                message.chat.id,
                f"*Талона {client[0]}*\nАбитуриент: {client[1]}\nНомер телефона: {client[2]}",
                reply_markup=self.send_inline_button(), parse_mode="Markdown",
            )
        else:
            self.bot.send_message(message.chat.id, "На сегодня записей больше нет.")

    def process_message(self, message):
        table_info = ServiceCollection.Repository.get_table_number(message.chat.id)
        
        self.bot.send_message(
            message.chat.id, f"Вы можете приступить к работе! Ваш стол № {table_info}."
        )

    def send_inline_button(self):
        markup = InlineKeyboardMarkup()

        button1 = InlineKeyboardButton(text="Не пришел", callback_data="no")
        button2 = InlineKeyboardButton(text="Пришел", callback_data="yes")

        markup.add(button1, button2)
        return markup

    def handle_no_action(self, admin_chat_id:int, id):
        self.admin_manager.set_is_busy_admin(admin_chat_id, False)
        ServiceCollection.Repository.cancel_entry(id)

    def handle_yes_action(self, admin_chat_id:int, id):
        self.admin_manager.set_is_busy_admin(admin_chat_id, False)
        ServiceCollection.Repository.accept_entry(id)

    def warn_user_to_press_button(self, message):
        self.bot.send_message(
            message.chat.id,
            "Пожалуйста, нажмите одну из кнопок: 'Пришел' или 'Не пришел', прежде чем продолжить.",
        )
