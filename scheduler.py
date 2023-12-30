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
    new_year = datetime.datetime.now().replace(minute=now.minute + 1)

    delta = (new_year - now).total_seconds()

    time.sleep(delta)

    # users = api.get_user_ids()
    bot.send_message(646596194, f"current datetime hour {datetime.datetime.now().hour}")
    # for user in users:
    #     bot.send_message(user, f"Test new year congratulations!")
