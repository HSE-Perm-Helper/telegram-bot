import threading
import time
import traceback

from utils import get_request, delete_request
from bot import bot
from logs_utils import send_logs_to_admins


class NotificationsSendWorker(threading.Thread):
    def __init__(self):
        super().__init__()

    def check_new_notifications(self):
        try:
            notifications_response = get_request(path="/notifications")
            new_schedule_set = set()
            schedule_changing_set = set()
            notifications_data = notifications_response.json()
            if notifications_response.status_code == 200:
                if len(notifications_data['response']) != 0:
                    for notification in notifications_data['response']:
                        event_type = notification['notificationType']
                        user_list = notification["users"]
                        # week_number = event["weekNumber"]

                        match event_type:
                            case "SCHEDULE_ADDED":
                                for user in user_list:
                                    new_schedule_set.add(user)

                            case "SCHEDULE_CHANGED_FOR_USER":
                                for user in user_list:
                                    schedule_changing_set.add(user)

                    for telegram_id in schedule_changing_set:
                        try:
                            bot.send_message(telegram_id, f"🟣Твое расписание было изменено!🟣\n")
                        except Exception as e:
                            pass

                    for telegram_id in new_schedule_set:
                        try:
                            bot.send_message(telegram_id, f"🟣Было добавлено новое расписание!🟣\n")
                        except Exception as e:
                            pass


                delete_events = delete_request(path="/events", json=notifications_data['response'])

            else:
                send_logs_to_admins(f"Проверка уведомлений вернула код ${notifications_response.status_code}, вместо OK")
        except Exception as e:
            send_logs_to_admins(f"Произошла ошибка при попытке отправить запрос новых уведомлений на сервер!\n"
                                f"Стэктрейс: \n"
                                f"{traceback.format_exc()}")

    def run(self):
        while True:
            self.check_new_notifications()
            time.sleep(300)
