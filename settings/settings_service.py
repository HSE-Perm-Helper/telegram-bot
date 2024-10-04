import api.api
from settings.base_setting import BaseSetting
from settings.impl.changed_schedule_notification_setting import ChangedScheduleNotificationSetting
from settings.impl.coming_lessons_notification_setting import ComingLessonsNotificationSetting
from settings.impl.new_schedule_notification_setting import NewScheduleNotificationSetting
from settings.setting_code import SettingCode


class SettingsService:
    __settings: dict[SettingCode, BaseSetting] = {}

    def __init__(self):
        self.__settings[SettingCode.CHANGED_SCHEDULE_NOTIFICATION] = ChangedScheduleNotificationSetting()
        self.__settings[SettingCode.NEW_SCHEDULE_NOTIFICATION] = NewScheduleNotificationSetting()
        self.__settings[SettingCode.COMING_LESSONS_NOTIFICATION] = ComingLessonsNotificationSetting()

    async def toggle_setting(self, id: int, code: SettingCode, new_value: bool):
        setting = await self.get_setting_by_code(code)
        await api.api.edit_user_settings(id, setting.api_code, new_value)

    async def get_settings(self, id: int, codes: list[SettingCode]) -> list[(BaseSetting, bool)]:
        l = []
        settings = await api.api.get_user_settings(id)

        for code in codes:
            setting = self.__settings[code]
            l.append((setting, settings[setting.api_code]))

        return l

    async def get_setting_by_code(self, code: SettingCode) -> BaseSetting:
        return self.__settings[code]


settings_service = SettingsService()
