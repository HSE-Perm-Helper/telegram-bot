from notification.base_notification import BaseNotification
from notification.base_notification_processor import BaseNotificationProcessor
from notification.notification_processor.schedule_added_notification_processor import ScheduleAddedNotificationProcessor
from notification.notification_processor.schedule_changed_notification_processor import \
    ScheduleChangedNotificationProcessor
from notification.notification_type import NotificationType
from util.utils import delete_request


class NotificationManager:
    processors: dict[NotificationType, BaseNotificationProcessor] = {}

    async def init_processors(self):
        await self.add_processor(ScheduleAddedNotificationProcessor())
        await self.add_processor(ScheduleChangedNotificationProcessor())

    async def add_processor(self, processor: BaseNotificationProcessor):
        self.processors[await processor.get_notification_type()] = processor

    async def get_processor_by_type(self, notification_type: NotificationType) -> BaseNotificationProcessor:
        return self.processors.get(notification_type)

    async def process(self, notifications: list[BaseNotification]) -> None:
        grouped_by_type = {}
        for notification in notifications:
            notification_type = notification.notification_type
            if notification_type not in grouped_by_type:
                grouped_by_type[notification_type] = [notification]
            else:
                grouped_by_type[notification_type].append(notification)

        for type, notifications in grouped_by_type.items():
            processor = await self.get_processor_by_type(type)
            await processor.process(notifications)

        deleting_notifications_id = list(filter(lambda notification: notification.id, notifications))
        await delete_request(path="/notifications", json=deleting_notifications_id)
