from sqlite3 import connect
import logging
logger = logging.getLogger("UserData")
__connection = connect('users.db')
__cursor = __connection.cursor()
__cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT);")
logger.info("SQLite inited")


def get_email(user_id):
    __cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
    return __cursor.fetchone()[0]


def set_email(user_id, mail):
    __cursor.execute("UPDATE users SET email = ? WHERE id = ?", (mail, user_id))
    __connection.commit()


def add_user(user_id, email="None"):
    __cursor.execute("INSERT INTO users (id, email) VALUES (?, ?)",
                              (user_id, email))
    __connection.commit()


def check_user_exists(user_id):
    return not __cursor.execute("SELECT * FROM users WHERE id = ? LIMIT 1", (user_id,)).fetchone() is None


def destroy():
    __connection.close()