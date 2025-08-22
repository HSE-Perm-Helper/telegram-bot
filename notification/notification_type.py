import enum


class NotificationType(enum.Enum):
    SCHEDULE_ADDED = "SCHEDULE_ADDED"
    SCHEDULE_CHANGED = "SCHEDULE_CHANGED_FOR_USER"
    UPCOMING_LESSONS = "UPCOMING_LESSONS"
    NONE = "NONE"

    @classmethod
    def _missing_(cls, value):
        return cls.NONE
