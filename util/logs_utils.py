from api.user_service import get_admin_ids, get_service_admin_ids
from bot import bot


async def send_logs_to_admins(data: str):
    admin_telegram_ids = await get_admin_ids()
    for telegram_id in admin_telegram_ids:
        try:
            await bot.send_message(telegram_id, f"<b>Admin logs</b>\n"
                                                f"{data}",
                                   parse_mode='HTML')
        except Exception as _:
            pass


async def send_logs_to_service_admins(data: str):
    admin_telegram_ids = await get_service_admin_ids()
    for telegram_id in admin_telegram_ids:
        try:
            await bot.send_message(telegram_id, f"<b>Service admin logs</b>\n"
                                                f"{data}",
                                   parse_mode='HTML')
        except Exception as _:
            pass