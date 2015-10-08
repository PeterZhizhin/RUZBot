from sqlite3 import connect
import logging
logger = logging.getLogger("UserData")


def init():
    global __connection
    global __cursor
    logger.debug("Creating cursor")
    __connection = connect('users.db')
    logger.debug("Creating connection")
    __cursor = __connection.cursor()
    __cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT);")
    logger.info("SQLite inited")


def get_email(user_id):
    logger.info("Getting email from DB")
    __cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
    return __cursor.fetchone()[0]


def set_email(user_id, mail):
    logger.info("Committing email adress")
    __cursor.execute("UPDATE users SET email = ? WHERE id = ?", (mail, user_id))
    __connection.commit()


def add_user(user_id, email="None"):
    logger.info("Inserting new user!")
    __cursor.execute("INSERT INTO users (id, email) VALUES (?, ?)",
                              (user_id, email))
    __connection.commit()


def check_user_exists(user_id):
    logger.info("Checking is user exists")
    return not __cursor.execute("SELECT * FROM users WHERE id = ? LIMIT 1", (user_id,)).fetchone() is None


def destroy():
    logger.info("Destroying connection")
    __connection.close()
