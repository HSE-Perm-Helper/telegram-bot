import api
from threading import Thread
import time


def run():
    thread_checker_schedule_updates = Thread(target=check_schedule_updates, args=())
    thread_checker_schedule_updates.start()


def check_schedule_updates():
    while True:
        api.check_new_schedule()
        time.sleep(300)
