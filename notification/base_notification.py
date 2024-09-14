import dataclasses

from notification.notification_type import NotificationType


@dataclasses.dataclass
class BaseNotification:
    id: str
    date: str
    notification_type: NotificationType
    payload: dict
