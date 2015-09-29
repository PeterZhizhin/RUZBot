from httplib2 import Http
from simplejson import loads
import logging
from Lesson import Lesson
logger = logging.getLogger("RUZPython")
__http = Http(".cache")
__base_URL = "http://ruz.hse.ru/RUZService.svc/personlessons?fromdate={}&todate={}&email={}"
__date_format = "%Y.%m.%d"


def printable_next_lessons(email, date):
    res = "\n---------\n".join(str(lesson) for lesson in get_next_lessons(email, date))
    return None if res == "" else res


def get_next_lessons(email,date):
    return Lesson.get_next_lessons(get_timetable_json(email, date), date.time())


def get_timetable_json(email, date):
    logger.info("Getting timetable")
    date = date.strftime(__date_format)
    response, content = __http.request(__base_URL.format(date, date, email))
    logger.info("Got timetable")
    if response is None or response['status'] != '200':
        logger.error("RUZ Server doesn't response correctly")
        return None
    json = loads(content)
    for lesson in json:
        yield Lesson(lesson)
    logger.info("Parsed")


if __name__ == "__main__":
    pass