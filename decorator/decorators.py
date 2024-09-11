import traceback
from functools import wraps

import aiogram

from bot import bot
from util.users_utils import is_admin

from message.common_messages import EXCEPTION_MESSAGE


def typing_action(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if len(args) > 0 and isinstance(args[0], aiogram.types.Message):
            chat_id = args[0].chat.id
        elif len(args) > 0 and isinstance(args[0], aiogram.types.CallbackQuery):
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
                if isinstance(arg, aiogram.types.Message):
                    bot.send_message(arg.chat.id, EXCEPTION_MESSAGE)
                    break
                elif isinstance(arg, aiogram.types.CallbackQuery):
                    bot.send_message(arg.message.chat.id, EXCEPTION_MESSAGE)
                    break

    return wrapper


def required_admin(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, aiogram.types.Message):
                if not is_admin(arg.chat.id):
                    return
                else:
                    func(*args, **kwargs)
                return
            elif isinstance(arg, aiogram.types.CallbackQuery):
                if not is_admin(arg.message.chat.id):
                    return
                else:
                    func(*args, **kwargs)
                return

    return wrapper
