from notification.base_notification import BaseNotification
from notification.notification_type import NotificationType


class BaseNotificationProcessor:
    async def process(self, notifications: list[BaseNotification]) -> None:
        raise NotImplementedError

    async def get_notification_type(self) -> NotificationType:
        raise NotImplementedError
