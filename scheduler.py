import datetime

import api
from notifications import check_new_schedule
from threading import Thread
import time
from bot import bot


def run_check_events_update():
    thread_checker_schedule_updates = Thread(target=check_schedule_updates, args=(), name='scheduler')
    thread_checker_schedule_updates.start()


def run_new_year_congratulations():
    thread_new_year_congratulations = Thread(target=send_new_year_congratulations, args=(), name='new-year'
                                                                                                 '-congratulations')
    thread_new_year_congratulations.start()


def check_schedule_updates():
    while True:
        check_new_schedule()
        time.sleep(300)


def send_new_year_congratulations():
    now = datetime.datetime.now()
    new_year = datetime.datetime.now().replace(year=2023, month=12, day=31, hour=18, minute=59, second=50)

    delta = (new_year - now).total_seconds()

    time.sleep(delta)

    users = api.get_user_ids()

    for user in users:
        try:
            msg = """
            <b>Благодарим Вас за пользование нашим ботом от лица команды разработчиков🙏</b>

Несмотря на то, что изначально бот был представлен ограниченному кругу лиц, с каждым днем Вас все больше и больше, что не может не радовать!🤩🤩🤩 Поэтому со своей стороны мы постепенно будем расширять функционал бота, чтобы он был более полезен для Вас!
По секрету сообщаем, что скоро выйдет крупное обновление🤭🙃 Мы его очень ждем и надеемся, что Вы тоже 

Желаем Вам в Новом году хорошо отдохнуть на каникулах🤪😎 и не терять стипу в периоды экзаменов (а тем, кто потерял, вернуть ее). И в целом, будьте счастливы. 🥳🥳🥳

<b>С Новым Годом, друзья!!!🥳🎄</b>
            """
            bot.send_message(user, msg, parse_mode='HTML')
        except Exception:
            continue
