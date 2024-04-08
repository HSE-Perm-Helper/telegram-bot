from bot import bot


def send_message_to_users(text: str, users: list[int]):
    for user in users:
        try:
            bot.send_message(user, text=text, parse_mode='HTML')
        except Exception as e:
            pass
