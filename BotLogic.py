import telegram
import UserData
from User import User
import logging
import config
logger = logging.getLogger("BotLogic")
# Server token
# token = "134496856:AAEJKACPo9RYAiZd5Q_GtXE9NGEDx5-e84o"
# Dev token
token = "134144850:AAH1DoOjDIXc27JZuKIl2xs_wjFPpKBNui0"
admin_id = 93894659


def __check_user(user):
    if user.id not in users:
        users[user.id] = User(user)


def __process_update(update_query):
    global lastUpdate
    lastUpdate = max(lastUpdate, update_query.update_id)
    message = update_query.message
    logger.info("Processing update from user {} {}".format(message.from_user.id,
                                                           message.from_user.username))
    __check_user(message.from_user)
    users[message.from_user.id].process_update(message.text, message.date)


def start():
    logger.info("Initializing bot")

    global bot
    global users
    bot = telegram.Bot(token)
    # user_id -- User class
    users = {}

    global lastUpdate
    lastUpdate = 0
    User.init_users(bot)
    updates = bot.getUpdates(lastUpdate+1)
    logger.info("Disabling unhandled updates {}".format(len(updates)))
    for last in updates:
        lastUpdate = max(lastUpdate, last.update_id)


def update():
    for last in bot.getUpdates(lastUpdate+1):
        __process_update(last)


def send_admin_alert(message):
    try:
        bot.sendMessage(chat_id=admin_id, text=message)
    except:
        logger.critical("Send message to admin failed.")

