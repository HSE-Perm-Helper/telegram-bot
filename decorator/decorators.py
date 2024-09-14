import traceback
from functools import wraps

import aiogram

from bot import bot
from message.common_messages import EXCEPTION_MESSAGE
from util.users_utils import is_admin


def typing_action(func):
    @wraps(func)
    async def decorator(*args, **kwargs):
        if len(args) > 0 and isinstance(args[0], aiogram.types.Message):
            chat_id = args[0].chat.id
        elif len(args) > 0 and isinstance(args[0], aiogram.types.CallbackQuery):
            chat_id = args[0].message.chat.id
        else:
            chat_id = None

        if chat_id:
            await bot.send_chat_action(chat_id, 'typing')
        return await func(*args, **kwargs)

    return decorator


def exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            for arg in args:
                if isinstance(arg, aiogram.types.Message):
                    await bot.send_message(arg.chat.id, EXCEPTION_MESSAGE)
                    break
                elif isinstance(arg, aiogram.types.CallbackQuery):
                    await bot.send_message(arg.message.chat.id, EXCEPTION_MESSAGE)
                    break

    return wrapper


def required_admin(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, aiogram.types.Message):
                if not await is_admin(arg.chat.id):
                    return
                else:
                    return await func(*args, **kwargs)
            elif isinstance(arg, aiogram.types.CallbackQuery):
                if not await is_admin(arg.message.chat.id):
                    return
                else:
                    return await func(*args, **kwargs)

    return wrapper
