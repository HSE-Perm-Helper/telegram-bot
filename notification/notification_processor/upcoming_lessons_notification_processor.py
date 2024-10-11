import traceback

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

import constants.constant
from bot import bot
from notification.base_notification import BaseNotification
from notification.base_notification_processor import BaseNotificationProcessor
from notification.notification_type import NotificationType
from schedule import schedule_utils
from schedule.schedule_utils import get_pair_count, group_lessons_by_pair_number, get_lessons_without_header
from settings.setting_code import SettingCode
from util.utils import get_notification_disable_button


class UpcomingLessonsNotificationProcessor(BaseNotificationProcessor):
    async def process(self, notifications: list[BaseNotification]) -> None:
        for notification in notifications:
            try:

                payload = notification.payload
                users = payload["users"]

                schedule = payload["targetSchedule"]
                lessons = schedule["lessons"]
                markup = InlineKeyboardBuilder()

                markup.row(types.InlineKeyboardButton(
                    text="Получить на всю неделю 👀",
                    callback_data=schedule_utils.get_callback_for_schedule(schedule_info=schedule,
                                                                           need_delete_message=False)[0]))

                grouped_lessons = await group_lessons_by_pair_number(lessons)
                pair_count = await get_pair_count(grouped_lessons)

                base_message = f"<b>Напоминаю, завтра у тебя {constants.constant.count_pairs_dict[str(pair_count)]}</b>"
                base_message += "\n\n"

                lessons_message = await get_lessons_without_header(grouped_lessons)

                for user in users:
                    try:
                        message = base_message + lessons_message
                        await bot.send_message(user, message, parse_mode="HTML",
                                               reply_markup=markup.as_markup())
                    except Exception as e:
                        print(e)
                        pass
            except Exception as e:
                traceback.print_exc()
                pass

    async def get_notification_type(self) -> NotificationType:
        return NotificationType.UPCOMING_LESSONS
