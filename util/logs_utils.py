from bot import bot
from api.api import get_admin_ids


def send_logs_to_admins(data: str):
    admin_telegram_ids = get_admin_ids()
    for telegram_id in admin_telegram_ids:
        try:
            bot.send_message(telegram_id, f"<b>Admin logs</b>\n"
                                          f"{data}",
                             parse_mode='HTML')
        except Exception as _:
            pass
