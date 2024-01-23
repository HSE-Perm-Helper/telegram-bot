from bot import bot

admins_telegram_id = [
    646596194,
    774471737
]


def send_logs_to_admins(data: str):
    for telegram_id in admins_telegram_id:
        try:
            bot.send_message(telegram_id, data)
        except Exception as _:
            pass
