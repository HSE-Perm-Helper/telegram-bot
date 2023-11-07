import bot
from api import base_url
from api import headers

import requests

def check_new_schedule():
    request = requests.get(
        url=f"{base_url}/events",
        headers=headers,
        verify=False)
    new_schedule_set = set()
    schedule_changing_set = set()
    response = request.json()
    if request.status_code == 200:
        if len(response['response']) != 0:
            for event in response['response']:
                eventType = event['eventType']
                user_list = event["users"]
                match eventType:

                    case "SCHEDULE_ADDED_EVENT":
                        for user in user_list:
                            new_schedule_set.add(user)

                    case "SCHEDULE_CHANGED_FOR_USER_EVENT":
                        for user in user_list:
                            schedule_changing_set.add(user)


    else:
        print("Возникли проблемы с получением ивентов")

    for telegram_id in schedule_changing_set:
        try:
            # if telegram_id == 774471737 or telegram_id == 646596194:
            #     bot.scheduler.send_message(telegram_id, f"Твое расписание было изменено 🫣\n"
            #                                             f"Получи его командой /schedule !")

            # bot.scheduler.send_message(telegram_id, f"Твое расписание было изменено 🫣\n"
            #                                         f"Получи его командой /schedule !")

            bot.scheduler.send_message(774471737, f"Расписание {telegram_id} было изменено 🫣\n")

        except Exception:
            print(f'Уведомление об изменениях не было отправлено пользователю {telegram_id}. '
                  f'Возможно, он заблокал бота. Ошибка: {Exception}')

    for telegram_id in new_schedule_set:
        try:
            # if telegram_id == 774471737 or telegram_id == 646596194:
            #     bot.scheduler.send_message(telegram_id, f"Было добавлено новое расписание 😎👍\n"
            #                                             f"Получи его командой /schedule !")

            # bot.scheduler.send_message(telegram_id, f"Было добавлено новое расписание 😎👍\n"
            #                                         f"Получи его командой /schedule !")

            bot.scheduler.send_message(774471737, f"Расписание для {telegram_id} обновилось! 🫣\n")

        except Exception:
            print(f'Уведомление о новом расписании не было отправлено пользователю {telegram_id}. '
                  f'Возможно, он заблокал бота. Ошибка: {Exception}')

    # response_for_delete = requests.delete(
    #     url=f"{base_url}/events?clear",
    #     headers=headers,
    #     json=response['response'],
    #     verify=False)