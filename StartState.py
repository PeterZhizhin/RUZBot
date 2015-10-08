class StartStateImpl:
    start_message = "Для продолжения мне необходим ваш корпоративный E-mail"\
        "Адрес вида: <адрес>@edu.hse.ru (без кавычек)"
    thank_you = "Спасибо за ваш адрес. Продолжаем."

    def __init__(self):
        pass

    def enter_state(self, message, user):
        user.send_message(StartStateImpl.start_message)

    def exit_state(self, message, user):
        user.send_message(StartStateImpl.thank_you)

    def update_state(self, message, user):
        pass


class StartState(StartStateImpl):
    obj = None

    def __new__(cls, *args, **kwargs):
        if cls.obj is None:
            cls.obj = StartStateImpl()
        return cls.obj
