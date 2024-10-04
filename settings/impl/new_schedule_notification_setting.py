from settings.base_setting import BaseSetting
from settings.setting_code import SettingCode


class NewScheduleNotificationSetting(BaseSetting):
    def __init__(self):
        super().__init__(
            title="Уведомления о новом расписании",
            code=SettingCode.NEW_SCHEDULE_NOTIFICATION,
            api_code="isEnabledNewScheduleNotifications"
        )
