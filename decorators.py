import traceback
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


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            for arg in args:
                if isinstance(arg, telebot.types.Message):
                    bot.send_message(arg.chat.id, "Что-то пошло не так 🤷\n"
                                                  "Попробуй еще раз или чуть позже")
                    break
                elif isinstance(arg, telebot.types.CallbackQuery):
                    bot.send_message(arg.message.chat.id, "Что-то пошло не так 🤷\n"
                                                          "Попробуй еще раз или зайди чуть позже")
                    break
    return wrapper
