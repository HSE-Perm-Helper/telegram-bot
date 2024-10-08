from bot import bot
from notification import notification_utils
from notification.base_notification import BaseNotification
from notification.base_notification_processor import BaseNotificationProcessor
from notification.notification_type import NotificationType
from settings.setting_code import SettingCode
from util.utils import get_notification_disable_button


class ScheduleAddedNotificationProcessor(BaseNotificationProcessor):
    async def process(self, notifications: list[BaseNotification]) -> None:
        new_schedule: dict[int, list] = {}
        for notification in notifications:
            payload = notification.payload
            users = payload["users"]

            for user in users:
                if user not in new_schedule:
                    new_schedule[user] = []
                new_schedule[user].append(payload["targetSchedule"])

        for telegram_id, schedules in new_schedule.items():
            difference = notification_utils.get_difference_schedule(schedules)
            markup = notification_utils.get_markup_schedule(schedules)
            markup.row(await get_notification_disable_button(SettingCode.NEW_SCHEDULE_NOTIFICATION))

            try:
                await bot.send_message(telegram_id, f"{notification_utils.NOTIFICATION_EMOJI} Добавлено {difference}!",
                                       reply_markup=markup.as_markup())
            except Exception as e:
                print(e)
                pass

    async def get_notification_type(self) -> NotificationType:
        return NotificationType.SCHEDULE_ADDED
