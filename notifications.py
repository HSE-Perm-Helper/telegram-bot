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
                eventType = event['eventType']
                user_set = set()
                user_list = event["users"]
                for user in user_list:
                    user_set.add(user)
                match eventType:
                    case "SCHEDULE_ADDED_EVENT":
                        for telegram_id in user_set:
                            try:
                                bot.scheduler.send_message(telegram_id, f"Было добавлено новое расписание 😎👍\n"
                                                                        f"Получи его командой /schedule !")
                            except Exception:
                                print(f'Уведомление о новом расписании не было отправлено пользователю {telegram_id}. '
                                      f'Возможно, он заблокал бота. Ошибка: {Exception}')

                    case "SCHEDULE_CHANGED_FOR_USER_EVENT":
                        for telegram_id in user_set:
                            try:
                                bot.scheduler.send_message(774471737, f"Для {telegram_id} было изменено расписание.\n")
                                bot.scheduler.send_message(telegram_id, f"Твое расписание было изменено 🫣\n"
                                                                        f"Получи его командой /schedule !")
                            except Exception:
                                print(f'Уведомление об изменениях не было отправлено пользователю {telegram_id}. '
                                      f'Возможно, он заблокал бота. Ошибка: {Exception}')

        response_for_delete = requests.delete(
            url=f"{base_url}/events?clear",
            headers=headers,
            json=response['response'],
            verify=False)
    else:
        print("Возникли проблемы с получением ивентов")