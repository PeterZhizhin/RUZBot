import UserData
import RUZPython
import logging
import re
import telegram


class User():

    bot = None
    logger = logging.getLogger("UserClass")

    command_re = re.compile("/([^\s]*) *([^\s].*)?")
    email_re = re.compile("[A-Za-z0-9]+@edu\.hse\.ru")
    helloMessage = """Бот Telegram для РУЗ ВШЭ
    Доступные команды:
    /start -- Напечатать это сообщение.
    /setemail EMAIL -- Поменять E-Mail чтобы получать сообщения (bla-bla-bla@edu.hse.ru).
    /getemail -- Вывести текущий E-Mail.
    /gettoday -- Получить расписание на сегодня.
    """
    wrongCommandMessage = "К сожалению, команда недоступна. Наберите /start для помощи."
    noEmailMessage = "E-Mail ещё не задан. Задайте его командой /setemail EMAIL."
    wrongEmailMessage = "Пожалуйста, проверьте E-Mail. Он должен соответствовать \"<адрес>@edu.hse.ru\"."
    yourEmailMessage = "Ваш текущий E-Mail: {}."
    mailChangedMessage = "Ваш E-Mail был заменен на {}."
    noLessonsMessage = "На сегодня занятий больше нет."

    def __get_today(self, message, params=None):
        mail = User.__get_mail_safe(message)
        if mail:
            lessons = RUZPython.printable_next_lessons(mail, message.date)
            User.bot.sendMessage(chat_id=self.__id,
                                 text=lessons if lessons else User.noLessonsMessage)

    def __print_hello(self, message, params=None):
        User.logger.info("Processing hello message for {}".format(message.from_user.username))
        User.bot.sendMessage(chat_id=message.from_user.id, text=User.helloMessage)

    def __wrong_command(self, message, params=None):
        User.logger.info("Processing wrong command message for {}".format(message.from_user.username))
        User.bot.sendMessage(chat_id=message.from_user.id, text=User.wrongCommandMessage)

    def __get_mail_safe(self, message):
        mail = UserData.get_email(message.from_user.id)
        if mail == "None":
            User.logger.info("User {} didn't set mail".format(message.from_user.username))
            User.bot.sendMessage(chat_id=message.from_user.id, text=User.noEmailMessage)
            return False
        return mail

    def __get_email(self, message, params=None):
        mail = self.__get_mail_safe(message)
        if mail:
            User.logger.info("Send mail address for {}".format(message.from_user.username))
            User.bot.sendMessage(chat_id=message.from_user.id,
                            text=User.yourEmailMessage.format(mail))

    def __wrong_email(self, message):
        User.logger.info("Mail for {} is wrong".format(message.from_user.username))
        User.bot.sendMessage(chat_id=message.from_user.id, text=User.wrongEmailMessage)

    def __set_email(self, message, params):
        User.logger.info("Setting mail for {}".format(message.from_user.username))
        if params is None or User.email_re.match(params.strip()) is None:
            self.__wrong_email(message)
            return
        mail = params.strip()
        UserData.set_email(message.from_user.id, mail)
        User.bot.sendMessage(chat_id=message.from_user.id,
                        text=User.mailChangedMessage.format(mail))

    @staticmethod
    def init_users(bot):
        User.bot = bot

    def __init__(self, user):
        self.__id = user.id
        self.__username = user.username

        if not UserData.check_user_exists(self.__id):
            User.logger.info("Adding new user {} with id {}".format(self.__username, self.__id))
            UserData.add_user(self.__id)
            self.__email = None
        else:
            self.__email = UserData.get_email(self.__id)
            if self.__email == "None":
                self.__email = None

        self.commandExec = {'start': self.__print_hello,
                            'setemail': self.__set_email,
                            'getemail': self.__get_email,
                            'gettoday': self.__get_today}

    def __send_message(self, text):
        User.bot.sendMessage(chat_id=self.__id,
                             text=text)

    def process_update(self, message_text):
        pass
