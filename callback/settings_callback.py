import enum


class SettingsCallback(enum.Enum):
    SET_GROUP = "SET_GROUP_SETTINGS"
    NOTIFICATION_SETTINGS = "NOTIFICATION_SETTINGS"
    DONE_SETTINGS = "DONE_SETTINGS"
    OFF_NOTIFICATION = "OFF_NOTIFICATION"
