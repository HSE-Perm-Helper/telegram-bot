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
                        pass
                    case "SCHEDULE_CHANGED_FOR_USER_EVENT":
                        user_list = event["users"]
                        for telegram_id in user_list:
                            bot.scheduler.send_message(774471737, f"Для {telegram_id} было изменено расписание.\n"
                                                                  f"Получи его командой /schedule !")