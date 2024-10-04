import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from exception.service_unavailable_exception import ServiceUnavailableException
from message.common_messages import EXCEPTION_MESSAGE


class ExceptionHandlerMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        event: Update
        try:
            return await handler(event, data)
        except ServiceUnavailableException as e:
            await self.send_message(event, e.__str__())
            
        except Exception as e:
            user_id = self.get_user_id_from_update(event)

            await self.send_message(event, EXCEPTION_MESSAGE)
            logging.error(f"Handling with error for user with id {user_id}", exc_info=e)


    async def send_message(self, update: Update, text: str):
        user_id = await self.get_user_id_from_update(update)
        await update.bot.send_message(chat_id=user_id, text=text)


    async def get_user_id_from_update(self, update: Update) -> int:
        if update.message is not None:
            return update.message.from_user.id
        elif update.callback_query is not None:
            return update.callback_query.from_user.id
