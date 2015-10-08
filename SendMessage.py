import telegram
from sqlite3 import connect

# token = "134496856:AAEJKACPo9RYAiZd5Q_GtXE9NGEDx5-e84o"
# token = "134144850:AAH1DoOjDIXc27JZuKIl2xs_wjFPpKBNui0"
# bot = telegram.Bot(token)
__connection = connect('users.db')
__cursor = __connection.cursor()

message = "А вот бот и обновился! Во много раз улучшена стабильность и доавлена такая необходимая функция, как получения расписания на завтра. Попробуйте: /gettmrw"

if __name__ == "__main__":
    ids = __cursor.execute("SELECT id FROM users WHERE email != 'None'").fetchall()
    for id in ids:
        print("Sending message to {}".format(id[0]))
        bot.sendMessage(chat_id=id[0], text=message)
