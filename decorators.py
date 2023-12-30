from functools import wraps

import telebot

from bot import bot


def typing_action(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if len(args) > 0 and isinstance(args[0], telebot.types.Message):
            chat_id = args[0].chat.id
        elif len(args) > 0 and isinstance(args[0], telebot.types.CallbackQuery):
            chat_id = args[0].message.chat.id
        else:
            chat_id = None

        if chat_id:
            bot.send_chat_action(chat_id, 'typing')
        return func(*args, **kwargs)
    return decorator
