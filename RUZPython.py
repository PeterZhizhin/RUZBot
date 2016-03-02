from Lesson import Lesson
from datetime import timedelta
# from httplib2 import Http
from simplejson import loads, dumps
import BotLogic
import logging
import requests
logger = logging.getLogger("RUZPython")
__base_URL = "http://ruz.hse.ru/RUZService.svc/personlessons?fromdate={}&todate={}&email={}"
__date_format = "%Y.%m.%d"
got_wrong_from_ruz = "Got not a lesson from ruz\n"


def init():
    logger.info("Initializing HTTP socket for RUZ")


def get_this_week_timetable(email, date):
    start = date - timedelta(days=date.weekday())
    end = start + timedelta(days=6)
    return get_timetable(email, start, end)


def get_week_ahead_timetable(email, date):
    start = date
    end = start + timedelta(days=6)
    return get_timetable(email,start,end)


def get_timetable(email, start, end):
    logger.info("Getting timetable for " + email)
    try:
	    response = requests.get(__base_URL.format(start.strftime(__date_format),
                                                         end.strftime(__date_format),
                                                         email), timeout=3)
    except requests.exceptions.Timeout:
        return None
    if response is None or response.status_code != 200:
        logger.error("RUZ Server doesn't response correctly")
        return None
    logger.info("Got timetable " + email)
    json = response.json()
    try:
        return Lesson.split_days(Lesson(lesson) for lesson in json)
    except:
        log = dumps(json, indent=' '*4, sort_keys=True, ensure_ascii=False)
        logger.error("Got none from RUZ. Got: "+log)
        BotLogic.send_admin_alert(got_wrong_from_ruz+log)
        return None


if __name__ == "__main__":
    import datetime
    table = get_this_week_timetable("pnzhizhin@edu.hse.ru", datetime.date.today())
    import pdb
    pdb.set_trace()
