from threading import Thread
from worker.notifications_send_worker import NotificationsSendWorker
from worker.backend_health_check_worker import BackendCheckHealthWorker

workers: list[Thread] = [
    NotificationsSendWorker(),
    BackendCheckHealthWorker()
]


def run_workers():
    for worker in workers:
        worker.start()

# def send_new_year_congratulations():
#     now = datetime.datetime.now()
#     new_year = datetime.datetime.now().replace(year=2023, month=12, day=31, hour=18, minute=59, second=50)
#
#     delta = (new_year - now).total_seconds()
#
#     time.sleep(delta)
#
#     users = api.get_user_ids()
#
#     for user in users:
#         try:
#             msg = """
#             <b>Благодарим Вас за пользование нашим ботом от лица команды разработчиков🙏</b>
#
# Несмотря на то, что изначально бот был представлен ограниченному кругу лиц, с каждым днем Вас все больше и больше, что не может не радовать!🤩🤩🤩 Поэтому со своей стороны мы постепенно будем расширять функционал бота, чтобы он был более полезен для Вас!
# По секрету сообщаем, что скоро выйдет крупное обновление🤭🙃 Мы его очень ждем и надеемся, что Вы тоже
#
# Желаем Вам в Новом году хорошо отдохнуть на каникулах🤪😎 и не терять стипу в периоды экзаменов (а тем, кто потерял, вернуть ее). И в целом, будьте счастливы. 🥳🥳🥳
#
# <b>С Новым Годом, друзья!!!🥳🎄</b>
#             """
#             bot.send_message(user, msg, parse_mode='HTML')
#         except Exception:
#             continue
