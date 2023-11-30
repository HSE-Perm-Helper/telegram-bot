from bot import bot
from api import base_url, headers

import requests


def check_new_schedule():
    # ID axt: 877810534
    # for i in range(1):
    #     bot.send_message(877810534, f"🔵░░░░░░░░░░█▀▀░░█░\n"
    #                                     f"░░░░░░▄▀▀▀▀░░░░░█▄▄░\n"
    #                                     f"░░░░░░█░█░░░░░░░░░░▐\n"
    #                                     f"░░░░░░▐▐░░░░░░░░░▄░▐\n"
    #                                     f"░░░░░░█░░░░░░░░▄▀▀░▐\n"
    #                                     f"░░░░▄▀░░░░░░░░▐░▄▄▀░\n"
    #                                     f"░░▄▀░░░▐░░░░░█▄▀░▐░░\n"
    #                                     f"░░█░░░▐░░░░░░░░▄░█░░\n"
    #                                     f"░░░█▄░░▀▄░░░░▄▀▐░█░░\n"
    #                                     f"░░░█▐▀▀▀░▀▀▀▀░░▐░█░░\n"
    #                                     f"░░▐█▐▄░░▀░░░░░░▐░█▄▄\n"
    #                                     f"░░расписание обновлено▀░░🔵\n")
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
                event_type = event['eventType']
                user_list = event["users"]
                match event_type:

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
            if telegram_id == 877810534:
                for i in range(20):
                    bot.send_message(telegram_id, f"░░░░░░░░░░█▀▀░░█░\n"
                                                f"░░░░░░▄▀▀▀▀░░░░░█▄▄░\n"
                                                f"░░░░░░█░█░░░░░░░░░░▐\n"
                                                f"░░░░░░▐▐░░░░░░░░░▄░▐\n"
                                                f"░░░░░░█░░░░░░░░▄▀▀░▐\n"
                                                f"░░░░▄▀░░░░░░░░▐░▄▄▀░\n"
                                                f"░░▄▀░░░▐░░░░░█▄▀░▐░░\n"
                                                f"░░█░░░▐░░░░░░░░▄░█░░\n"
                                                f"░░░█▄░░▀▄░░░░▄▀▐░█░░\n"
                                                f"░░░█▐▀▀▀░▀▀▀▀░░▐░█░░\n"
                                                f"░░▐█▐▄░░▀░░░░░░▐░█▄▄\n"
                                                f"░░расписание обновлено▀░░\n")
            else:
                bot.send_message(telegram_id, f"🟣 Твое расписание было изменено! 🟣\n")

        except Exception:
            print(f'Уведомление об изменениях не было отправлено пользователю {telegram_id}. '
                  f'Возможно, он заблокал бота. Ошибка: {Exception}')

    for telegram_id in new_schedule_set:
        try:
            if telegram_id == 877810534:
                for i in range(20):
                    bot.send_message(telegram_id, f"░░░░░░░░░░█▀▀░░█░\n"
                                                f"░░░░░░▄▀▀▀▀░░░░░█▄▄░\n"
                                                f"░░░░░░█░█░░░░░░░░░░▐\n"
                                                f"░░░░░░▐▐░░░░░░░░░▄░▐\n"
                                                f"░░░░░░█░░░░░░░░▄▀▀░▐\n"
                                                f"░░░░▄▀░░░░░░░░▐░▄▄▀░\n"
                                                f"░░▄▀░░░▐░░░░░█▄▀░▐░░\n"
                                                f"░░█░░░▐░░░░░░░░▄░█░░\n"
                                                f"░░░█▄░░▀▄░░░░▄▀▐░█░░\n"
                                                f"░░░█▐▀▀▀░▀▀▀▀░░▐░█░░\n"
                                                f"░░▐█▐▄░░▀░░░░░░▐░█▄▄\n"
                                                f"░░расписание обновлено▀░░\n")
            else:
                bot.send_message(telegram_id, f"🟣 Было добавлено новое расписание! 🟣\n")

        except Exception:
            print(f'Уведомление о новом расписании не было отправлено пользователю {telegram_id}. '
                  f'Возможно, он заблокал бота. Ошибка: {Exception}')

    response_for_delete = requests.delete(
        url=f"{base_url}/events",
        headers=headers,
        json=response['response'],
        verify=False)
