import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from message.common_messages import EXCEPTION_MESSAGE


class ExceptionHandlerMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        event: Update
        try:
            return await handler(event, data)
        except Exception as e:
            user_id = None
            if event.message is not None:
                user_id = event.message.from_user.id
                await event.message.answer(EXCEPTION_MESSAGE)
            elif event.callback_query is not None:
                user_id = event.callback_query.from_user.id
                await event.callback_query.message.answer(EXCEPTION_MESSAGE)

            logging.error(f"Handling with error for user with id {user_id}", exc_info=e)
