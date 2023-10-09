import bot
from api import base_url
from api import headers

import requests


def check_new_schedule():
    request = requests.get(
        url=f"{base_url}/events",
        headers=headers,
        verify=False)
    response = request.json()
    if request.status_code == 200:
        if len(response['response']) != 0:
            for event in response['response']:
                match event['eventType']:
                    case "SCHEDULE_ADDED_EVENT":
                        user_list = event["users"]
                        for telegram_id in user_list:
                            bot.scheduler.send_message(telegram_id, f"Было добавлено новое расписание 😎👍.\n"
                                                                    f"Получи его командой /schedule !")
                    case "SCHEDULE_CHANGED_FOR_USER_EVENT":
                        user_list = event["users"]
                        for telegram_id in user_list:
                            bot.scheduler.send_message(telegram_id, f"Твое расписание было изменено 🫣.\n"
                                                                    f"Получи его командой /schedule !")
                            bot.scheduler.send_message(774471737, f"Для {telegram_id} было изменено расписание.\n")
        response_for_delete = requests.delete(
            url=f"{base_url}/events?clear",
            headers=headers,
            json=response['response'],
            verify=False)
    else:
        print("Возникли проблемы с получением ивентов")