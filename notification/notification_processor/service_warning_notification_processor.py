from notification.base_notification import BaseNotification
from notification.base_notification_processor import BaseNotificationProcessor
from notification.notification_type import NotificationType
from util.logs_utils import send_logs_to_service_admins


class ServiceWarningNotificationProcessor(BaseNotificationProcessor):
    async def process(self, notifications: list[BaseNotification]) -> None:
        for notification in notifications:
            try:
                payload = notification.payload
                message = payload["message"]

                await send_logs_to_service_admins(message)
            except Exception as e:
                pass


    async def get_notification_type(self) -> NotificationType:
        return NotificationType.SERVICE_WARNING
