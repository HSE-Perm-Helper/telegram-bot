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


class UpcomingLessonsNotificationProcessor(BaseNotificationProcessor):
    async def process(self, notifications: list[BaseNotification]) -> list[BaseNotification]:
        processed_notifications = []
        for notification in notifications:
            try:

                payload = notification.payload
                users = payload["users"]

                lessons = payload["lessons"]
                # markup = InlineKeyboardBuilder()
                #
                # markup.row(types.InlineKeyboardButton(
                #     text="Получить на всю неделю 👀",
                #     callback_data=schedule_utils.get_callback_for_timetable(timetable_info=schedule,
                #                                                             need_delete_message=False)[0]))

                grouped_lessons = await group_lessons_by_pair_number(lessons)
                pair_count = await get_pair_count(grouped_lessons)

                base_message = f"<b>Напоминаю, завтра у тебя {constants.constant.count_pairs_dict[str(pair_count)]}</b>"
                base_message += "\n\n"

                lessons_message = await get_lessons_without_header(grouped_lessons)

                for user in users:
                    try:
                        message = base_message + lessons_message
                        await bot.send_message(user, message, parse_mode="HTML")
                    except Exception as e:
                        pass

                processed_notifications.append(notification)
            except Exception as e:
                traceback.print_exc()

        return processed_notifications

    async def get_notification_type(self) -> NotificationType:
        return NotificationType.UPCOMING_LESSONS
