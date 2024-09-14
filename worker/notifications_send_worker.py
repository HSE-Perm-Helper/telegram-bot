import asyncio
import traceback

from aiogram import Router

from notification.base_notification import BaseNotification
from notification.notification_manager import NotificationManager
from notification.notification_type import NotificationType
from util.logs_utils import send_logs_to_admins
from util.utils import get_request

router = Router()


class NotificationsSendWorker:
    notification_manager = NotificationManager()

    def __init__(self):
        super().__init__()

    async def check_new_notifications(self):
        try:
            notifications_response = await get_request(path="/test/notifications/notifications")

            if notifications_response.status_code != 200:
                await send_logs_to_admins(
                    f"Проверка уведомлений вернула код {notifications_response.status_code}, вместо OK")
                return

            notifications = list(map(lambda notify:
                                     BaseNotification(id=notify["id"],
                                                      date=notify["date"],
                                                      payload=notify["payload"],
                                                      notification_type=NotificationType(notify["notificationType"])),
                                     notifications_response.json()))

            await self.notification_manager.process(notifications)

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
