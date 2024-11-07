import enum


class NotificationType(enum.Enum):
    SCHEDULE_ADDED = "SCHEDULE_ADDED"
    SCHEDULE_CHANGED = "SCHEDULE_CHANGED_FOR_USER"
    UPCOMING_LESSONS = "UPCOMING_LESSONS"
    SERVICE_WARNING = "SERVICE_WARNING"
    NONE = "NONE"

    @classmethod
    def _missing_(cls, value):
        return cls.NONE
