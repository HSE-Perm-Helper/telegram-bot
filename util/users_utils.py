from api import api
from bot import bot


def send_message_to_users(text: str, users: list[int]):
    for user in users:
        try:
            bot.send_message(user, text=text, parse_mode='HTML')
        except Exception as e:
            pass


def is_admin(telegram_id: int) -> bool:
    """
    Check user is admin
    :param telegram_id user telegram id
    :return True if user is admin
    """
    admins = api.get_admin_ids()
    return telegram_id in admins
