import traceback
from traceback import print_exc

from aiogram.enums import ParseMode

from bot import bot
from notification import notification_utils
from notification.base_notification import BaseNotification
from notification.base_notification_processor import BaseNotificationProcessor
from notification.notification_type import NotificationType
from schedule.schedule_type import ScheduleType
from util.utils import format_output_array


def _get_name_by_schedule_type(schedule_type: ScheduleType, number: int) -> str:
    d = {
        ScheduleType.COMMON_SCHEDULE: f"{number} неделю",
        ScheduleType.QUARTER_SCHEDULE: "модуль",
        ScheduleType.SESSION_SCHEDULE: "сессию"
    }

    return d[schedule_type]


def _get_plural_name_day_of_week(day: str) -> str:
    days = {
        "MONDAY": "понедельник",
        "TUESDAY": "вторник",
        "WEDNESDAY": "среду",
        "THURSDAY": "четверг",
        "FRIDAY": "пятницу",
        "SATURDAY": "субботу",
        "SUNDAY": "воскресенье"
    }

    return days[day]


class ScheduleChangedNotificationProcessor(BaseNotificationProcessor):
    async def process(self, notifications: list[BaseNotification]) -> list[BaseNotification]:
        processed_notifications = []
        for notification in notifications:
            try:
                payload = notification.payload
                schedule = payload["targetSchedule"]
                users = payload["users"]
                schedule_type = ScheduleType(schedule["scheduleType"])
                number = schedule["number"]
                days = list(map(lambda day: f"<b>{_get_plural_name_day_of_week(day)}</b>", payload["differentDays"]))

                message = (f"{notification_utils.NOTIFICATION_EMOJI} В расписании на <b>{_get_name_by_schedule_type(schedule_type, number)}</b>"
                           f" появились изменения на {format_output_array(days)}")

                keyboard = notification_utils.get_markup_schedule([schedule])

                for user in users:
                    try:
                        await bot.send_message(user, message, reply_markup=keyboard.as_markup(), parse_mode=ParseMode.HTML)
                    except Exception as e:
                        print(e)

                processed_notifications.append(notification)
            except Exception as e:
                traceback.print_exc()

        return processed_notifications

    async def get_notification_type(self) -> NotificationType:
        return NotificationType.SCHEDULE_CHANGED

