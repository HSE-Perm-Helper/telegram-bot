from settings.base_setting import BaseSetting
from settings.setting_code import SettingCode


class ComingLessonsNotificationSetting(BaseSetting):
    def __init__(self):
        super().__init__(
            title="Уведомления о предстоящих парах",
            code=SettingCode.COMING_LESSONS_NOTIFICATION,
            api_code="isEnabledComingLessonsNotifications"
        )