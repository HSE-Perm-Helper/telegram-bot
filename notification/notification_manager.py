import traceback

from notification.base_notification import BaseNotification
from notification.base_notification_processor import BaseNotificationProcessor
from notification.notification_processor.schedule_added_notification_processor import ScheduleAddedNotificationProcessor
from notification.notification_processor.schedule_changed_notification_processor import \
    ScheduleChangedNotificationProcessor
from notification.notification_processor.service_warning_notification_processor import \
    ServiceWarningNotificationProcessor
from notification.notification_processor.upcoming_lessons_notification_processor import \
    UpcomingLessonsNotificationProcessor
from notification.notification_type import NotificationType


class NotificationManager:
    processors: dict[NotificationType, BaseNotificationProcessor] = {}

    async def init_processors(self):
        await self.add_processor(ScheduleAddedNotificationProcessor())
        await self.add_processor(ScheduleChangedNotificationProcessor())
        await self.add_processor(UpcomingLessonsNotificationProcessor())
        await self.add_processor(ServiceWarningNotificationProcessor())

    async def add_processor(self, processor: BaseNotificationProcessor):
        self.processors[await processor.get_notification_type()] = processor

    async def get_processor_by_type(self, notification_type: NotificationType) -> BaseNotificationProcessor:
        return self.processors.get(notification_type)

    async def process(self, notifications: list[BaseNotification]) -> list[BaseNotification]:
        grouped_by_type = {}
        processed_notifications = []
        for notification in notifications:
            notification_type = notification.notification_type
            if notification_type not in grouped_by_type:
                grouped_by_type[notification_type] = [notification]
            else:
                grouped_by_type[notification_type].append(notification)

        for type, notifications in grouped_by_type.items():
            processor = await self.get_processor_by_type(type)
            try:
                processed_notifications.append(*await processor.process(notifications))
            except Exception as e:
                traceback.print_exc()

        return processed_notifications
