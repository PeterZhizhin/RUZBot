import telegram
import re
import UserData
from User import User
import logging
logger = logging.getLogger("BotLogic")

bot = telegram.Bot("134496856:AAEJKACPo9RYAiZd5Q_GtXE9NGEDx5-e84o")
lastUpdate = 0

# user_id -- User class
users = {}


def __check_user(user):
    if user.id not in users:
        users[user.id] = User(user)


def __process_update(update_query):
    global lastUpdate
    lastUpdate = max(lastUpdate, update_query.update_id)
    message = update_query.message
    __check_user(message.from_user)
    users[message.from_user.id].process_update(message.text)


def start():
    User.init_users(bot)
    global lastUpdate
    for last in bot.getUpdates(lastUpdate+1):
        lastUpdate = max(lastUpdate, last.update_id)


def update():
    for last in bot.getUpdates(lastUpdate+1):
        __process_update(last)


def destroy():
    UserData.destroy()