from aiogram.types import Update


async def send_message(user_id: int, update: Update, text: str):
    await update.bot.send_message(chat_id=user_id, text=text, parse_mode="Markdown")


async def get_user_id_from_update(update: Update) -> int:
    if update.message is not None:
        return update.message.from_user.id
    elif update.callback_query is not None:
        return update.callback_query.from_user.id
