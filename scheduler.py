from notifications import check_new_schedule
from threading import Thread
import time
import bot


def run():
    thread_checker_schedule_updates = Thread(target=check_schedule_updates, args=())
    thread_checker_schedule_updates.start()
    bot.scheduler.send_message(774471737, "Поток запущен!")


def check_schedule_updates():
    while True:
        check_new_schedule()
        time.sleep(300)
