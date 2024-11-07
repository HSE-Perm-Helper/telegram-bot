import asyncio
import traceback

from aiogram import Router

from api.utils import get_request, delete_request
from notification.base_notification import BaseNotification
from notification.notification_manager import NotificationManager
from notification.notification_type import NotificationType
from util.logs_utils import send_logs_to_admins
from venv import is_prod

router = Router()


class NotificationsSendWorker:
    notification_manager = NotificationManager()
    NOTIFICATIONS_URL = "/v2/notifications"

    def __init__(self):
        super().__init__()

    async def check_new_notifications(self):
        try:
            notifications_response = await get_request(path=self.NOTIFICATIONS_URL)

            if notifications_response.status_code != 200:
                await send_logs_to_admins(
                    f"Проверка уведомлений вернула код {notifications_response.status_code}, вместо OK")
                return

            data = notifications_response.json()

            notifications = list(filter(lambda notification: notification.notification_type != NotificationType.NONE, map(lambda notify:
                                     BaseNotification(id=notify["id"],
                                                      date=notify["date"],
                                                      payload=notify["payload"],
                                                      notification_type=NotificationType(notify["notificationType"])),
                                     data)))

            notifications = await self.notification_manager.process(notifications)

            deleting_notifications_id = list(map(lambda notification: {"id": notification.id}, notifications))
            if is_prod:
                await delete_request(path=self.NOTIFICATIONS_URL, json=deleting_notifications_id)

        except Exception as e:
            traceback.print_exc()
            await send_logs_to_admins(f"Произошла ошибка при попытке отправить запрос новых уведомлений на сервер!\n"
                                      f"Стэктрейс: \n"
                                      f"{traceback.format_exc()}")

    async def run(self):
        await self.notification_manager.init_processors()

        while True:
            await self.check_new_notifications()
            await asyncio.sleep(300)
