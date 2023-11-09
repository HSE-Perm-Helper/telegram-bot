from notifications import check_new_schedule
from threading import Thread
import time


def run_check_events_update():
    thread_checker_schedule_updates = Thread(target=check_schedule_updates, args=(), name='scheduler')
    thread_checker_schedule_updates.start()


def check_schedule_updates():
    while True:
        check_new_schedule()
        time.sleep(300)