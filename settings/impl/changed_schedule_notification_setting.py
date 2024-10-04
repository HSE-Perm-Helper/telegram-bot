from settings.base_setting import BaseSetting
from settings.setting_code import SettingCode


class ChangedScheduleNotificationSetting(BaseSetting):
    def __init__(self):
        super().__init__(
            title="Уведомления об измененном расписании",
            code=SettingCode.CHANGED_SCHEDULE_NOTIFICATION,
            api_code="isEnabledChangedScheduleNotifications"
        )
