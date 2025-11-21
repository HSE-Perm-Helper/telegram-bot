from typing import Callable, Dict, Any, Awaitable

import requests
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update, Message, CallbackQuery
from structlog import get_logger

from exception.service_unavailable_exception import ServiceUnavailableException
from exception.user_not_found_exception import UserNotFoundException
from message.common_messages import EXCEPTION_MESSAGE, UNREGISTERED_USER_EXCEPTION, CONNECTION_ERROR
from middleware.utils import get_user_id_from_update, send_message


class ExceptionHandlerMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        event: Update
        user_id = await get_user_id_from_update(event)
        try:
            return await handler(event, data)
        except ServiceUnavailableException as e:
            await send_message(user_id, event, e.__str__())
        except UserNotFoundException as e:
            await send_message(user_id, event, UNREGISTERED_USER_EXCEPTION)
        except requests.exceptions.ConnectionError as e:
            await send_message(user_id, event, CONNECTION_ERROR)
        except Exception as e:
            await send_message(user_id, event, EXCEPTION_MESSAGE.format(event.update_id))
            if event.message is not None:
                payload = f"text='{event.message.text}'"
            elif event.callback_query is not None:
                payload = f"data='{event.callback_query.data}'"
            else:
                payload = ""

            get_logger().exception(f"Error when handling update {payload}", exc_info=e)
