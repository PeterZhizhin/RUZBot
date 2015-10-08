from httplib2 import Http
from simplejson import loads, dumps
import logging
from Lesson import Lesson
from datetime import timedelta
import BotLogic
logger = logging.getLogger("RUZPython")
__base_URL = "http://ruz.hse.ru/RUZService.svc/personlessons?fromdate={}&todate={}&email={}"
__date_format = "%Y.%m.%d"
got_wrong_from_ruz = "Got not a lesson from ruz"

def init():
    logger.info("Initializing HTTP socket for RUZ")
    global __http
    __http = Http(".cache")


def get_week_timetable(email, date):
    start = date - timedelta(days=date.weekday())
    end = start + timedelta(days=6)
    return get_timetable(email, start, end)


def get_timetable(email, start, end):
    logger.info("Getting timetable for " + email)
    response, content = __http.request(__base_URL.format(start.strftime(__date_format),
                                                         end.strftime(__date_format),
                                                         email))
    if response is None or response['status'] != '200':
        logger.error("RUZ Server doesn't response correctly")
        return None
    logger.info("Got timetable " + email)
    json = loads(content)
    try:
        return Lesson.split_days(Lesson(lesson) for lesson in json)
    except:
        logger.error("Got none from RUZ. Got: "+dumps(json, indent=' '*4, sort_keys=True))
        BotLogic.send_admin_alert(got_wrong_from_ruz)
        return None


if __name__ == "__main__":
    import datetime
    table = get_week_timetable("pnzhizhin@edu.hse.ru", datetime.date.today())
    pass
