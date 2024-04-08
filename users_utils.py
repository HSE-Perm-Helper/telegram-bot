from bot import bot
from api import get_user_ids


def send_message_to_all_users(text):
    users = get_user_ids()
    for user in users:
        bot.send_message(user, text=text, parse_mode='HTML')
