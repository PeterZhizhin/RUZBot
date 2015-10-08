#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import BotLogic
import UserData
import RUZPython
from time import sleep
import traceback
import logging

alertMsg = "Critical error. Restarting server.\n"


def main_program():
    logger.info("Application started")
    UserData.init()
    RUZPython.init()
    BotLogic.start()
    while True:
        BotLogic.update()
        sleep(0.5)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.getLogger("telegram.bot").setLevel(logging.WARNING)
    fh = logging.FileHandler('bot.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    while True:
        try:
            main_program()
        except KeyboardInterrupt:
            break
        except:
            trace = traceback.format_exc()
            logger.critical(trace)
            BotLogic.send_admin_alert(alertMsg+trace)
            UserData.destroy()

