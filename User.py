import UserData
import RUZPython
import logging
import re
import datetime
from Lesson import Lesson

class User():

    logger = logging.getLogger("UserClass")

    class NoneBot:

        def sendMessage(self, chat_id=None, user_id=None, text=None):
            User.logger.critical("BOT WAS NOT SETTED UP FOR USERS")
    bot = NoneBot()

    command_re = re.compile("/([^\s]*) *([^\s].*)?")
    email_re = re.compile("[A-Za-z_0-9]+@edu\.hse\.ru")
    one_day_delta = datetime.timedelta(days=1)

    helloMessage = """Бот Telegram для РУЗ ВШЭ
    Доступные команды:
    /start — Напечатать это сообщение.
    /setemail — Поменять E-Mail для РУЗ.
    /getemail — Вывести текущий E-Mail.
    /gettmrw — Расписание на завтра.
    /gettoday — Расписание на сегодня.
    /getleft — Оставшиеся сегодня пары.
    """
    wrongCommandMessage = "К сожалению, команда недоступна. Наберите /start для помощи."
    noEmailMessage = "E-Mail ещё не задан. Задайте его командой /setemail"
    wrongEmailMessage = "Пожалуйста, проверьте E-Mail. Он должен соответствовать \"<адрес>@edu.hse.ru\"."
    email_help_message = "Для того чтобы ввести E-Mail для бота нужно набрать:\n/setemail " \
                         "<адрес>@edu.hse.ru\nНапример: /setemail vnpupkin@edu.hse.ru"
    yourEmailMessage = "Текущий E-Mail: {}."
    mailChangedMessage = "E-Mail был заменен на {}."
    noLessonsMessage = "На сегодня занятий больше нет."
    noLessonsTomorrow = "На завтра занятий нет."
    noWeekLessons = "На неделю занятий нет.\nМожет стоит проверить E-mail?\nТекущий: {}"
    updatingTimetableFromRUZ = "Обновление расписания. Это может занять некоторое время."

    def __get_timetable(self, force=False, need_notification=False):
        """
        Безопасное получение расписания.
        При необходимости совершает запрос в РУЗ
        и обновляет недельное расписание
        """
        if force or self.__timetable is None or\
                    self.__next_update_needed <= datetime.datetime.now():
            self.__next_update_needed = datetime.datetime.now() + User.one_day_delta
            self.__assert_if_none_mail()
            if self.__email is None:
                return
            if need_notification:
                User.bot.sendMessage(chat_id=self.__id, text=User.updatingTimetableFromRUZ)
            self.__timetable = RUZPython.get_week_timetable(self.__email, self.__last_update_time)
        if self.__timetable is None or len(self.__timetable) == 0:
            self.__no_week_table()

    def __get_today_lessons(self):
        self.__get_timetable(need_notification=True)
        if self.__timetable is not None:
            # Выделяем сегодняшний день в расписании
            for day in self.__timetable:
                if day[0].date == self.__last_update_time.date():
                    return day
        return None

    def __get_tomorrow_lessons(self):
        self.__get_timetable(need_notification=True)
        if self.__timetable is not None:
            tomorrow = self.__last_update_time.date() + User.one_day_delta
            for day in self.__timetable:
                if day[0].date == tomorrow:
                    return day
        return None

    def __print_lessons(self, lessons, no_lessons_message=noLessonsMessage):
        lessons = Lesson.get_printable_lessons(lessons)
        User.bot.sendMessage(chat_id=self.__id,
                             text=lessons if lessons else no_lessons_message)

    def __get_today(self, params=None):
        User.logger.info("User {} getting today lessons".format(self.__username))
        self.__print_lessons(self.__get_today_lessons(), no_lessons_message=User.noLessonsMessage)

    def __get_tomorrow(self, params=None):
        User.logger.info("User {} getting tomorrow lessons".format(self.__username))
        self.__print_lessons(self.__get_tomorrow_lessons(), no_lessons_message=User.noLessonsTomorrow)

    def __get_left(self, params=None):
        User.logger.info("User {} getting left lessons".format(self.__username))
        lessons = self.__get_today_lessons()
        if lessons is not None:
            lessons = [lesson for lesson in self.__get_today_lessons() if
                       lesson.end >= self.__last_update_time.time()]
        self.__print_lessons(lessons)

    def __print_hello(self, params=None):
        User.logger.info("Processing hello message for {}".format(self.__username))
        User.bot.sendMessage(chat_id=self.__id, text=User.helloMessage)

    def __wrong_command(self, params=None):
        User.logger.info("Processing wrong command message for {}".format(self.__username))
        User.bot.sendMessage(chat_id=self.__id, text=User.wrongCommandMessage)

    def __assert_if_none_mail(self):
        if self.__email is None:
            User.logger.info("User {} didn't set mail".format(self.__username))
            User.bot.sendMessage(chat_id=self.__id, text=User.noEmailMessage)

    def __get_email(self, params=None):
        self.__assert_if_none_mail()
        if self.__email is not None:
            User.logger.info("Send mail address for {}".format(self.__username))
            User.bot.sendMessage(chat_id=self.__id,
                                 text=User.yourEmailMessage.format(self.__email))

    def __wrong_email(self, mail):
        User.logger.info("Mail {} for {} is wrong".format(mail, self.__username))
        User.bot.sendMessage(chat_id=self.__id, text=User.wrongEmailMessage)

    def __email_help(self):
        User.logger.info("Printing help for user {}".format(self.__username))
        User.bot.sendMessage(chat_id=self.__id, text=User.email_help_message)

    def __no_week_table(self):
        User.logger.info("No timetable for {}".format(self.__username))
        User.bot.sendMessage(chat_id=self.__id, text=User.noWeekLessons.format(self.__email))

    def __set_email(self, params):
        User.logger.info("Setting mail for {}".format(self.__username))
        if params is None or params == "":
            self.__email_help()
            return

        if User.email_re.match(params.strip()) is None:
            self.__wrong_email(params.strip())
            return
        mail = params.strip()
        UserData.set_email(self.__id, mail)
        User.bot.sendMessage(chat_id=self.__id,
                             text=User.mailChangedMessage.format(mail))
        self.__email = mail
        self.__get_timetable(force=True)

    @staticmethod
    def init_users(bot):
        User.bot = bot

    def __init__(self, user):
        self.__last_update_time = None
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

        # Получаем расписание только по безопасному запросу
        self.__timetable = None
        # Время обновления в цикле обновим
        self.__last_update_time = None
        # Мы не обновляли расписание ещё и нам его нужно сейчас обновить
        self.__next_update_needed = datetime.datetime.now()

        self.commandExec = {'start': self.__print_hello,
                            'setemail': self.__set_email,
                            'getemail': self.__get_email,
                            'gettoday': self.__get_today,
                            'getleft': self.__get_left,
                            'gettmrw': self.__get_tomorrow}

    def __send_message(self, text):
        User.bot.sendMessage(chat_id=self.__id,
                             text=text)

    def process_update(self, message_text, date):
        self.__last_update_time = date
        match = User.command_re.match(message_text)
        if match is None:
            self.__wrong_command()
            return
        command, params = match.groups()
        if command not in self.commandExec:
            self.__wrong_command()
            return
        self.commandExec[command](params)

