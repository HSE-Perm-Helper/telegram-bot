import uuid
import time

from structlog import get_logger
from structlog.contextvars import (
    bind_contextvars,
    clear_contextvars
)

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from middleware.utils import get_user_id_from_update


class TracingMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        event: Update
        user_id = await get_user_id_from_update(event)

        request_id = str(uuid.uuid4())

        bind_contextvars(request_id=request_id, user_id=user_id, update_id=event.update_id)

        start_time = time.monotonic()
        try:
            get_logger().info(f"Handled update with id: {event.update_id}")
            return await handler(event, data)
        finally:
            duration_sec = time.monotonic() - start_time
            execution_time = round(duration_sec, 4)
            get_logger().info(f"Handler execution time for update id {event.update_id} is {execution_time} seconds")
            clear_contextvars()