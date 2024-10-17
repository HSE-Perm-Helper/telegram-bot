from api import user_service
from bot import bot


async def send_message_to_users(text: str, users: list[int]):
    for user in users:
        try:
            await bot.send_message(user, text=text, parse_mode='HTML')
        except Exception as e:
            pass


async def is_admin(telegram_id: int) -> bool:
    """
    Check user is admin
    :param telegram_id user telegram id
    :return True if user is admin
    """
    admins = await user_service.get_admin_ids()
    return telegram_id in admins
