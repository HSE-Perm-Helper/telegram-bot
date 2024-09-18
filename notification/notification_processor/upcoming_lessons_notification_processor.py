import traceback

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

import constants.constant
from bot import bot
from notification import notification_utils
from notification.base_notification import BaseNotification
from notification.base_notification_processor import BaseNotificationProcessor
from notification.notification_type import NotificationType
from routes.schedule_handle.schedule_handle import get_lessons_without_header
from schedule import schedule_utils


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

                markup.row(types.InlineKeyboardButton(text="Не хочу получать такие уведомления 🥸", callback_data="no"))

                lessons_message = "<b>Завтра у тебя нет пар 😎</b>"

                if len(lessons) > 0:
                    lessons_message = f"<b>Завтра у тебя {constants.constant.count_pairs_dict[str(len(lessons))]}</b>"
                    lessons_message += "\n\n"
                    lessons_message += await get_lessons_without_header([lessons])

                for user in users:
                    try:
                        await bot.send_message(user, f"{notification_utils.NOTIFICATION_EMOJI} Напоминание о парах")
                        await bot.send_message(user, lessons_message, parse_mode="HTML", reply_markup=markup.as_markup(),
                                               disable_notification=True)
                    except Exception as e:
                        print(e)
                        pass
            except Exception as e:
                traceback.print_exc()
                pass

    async def get_notification_type(self) -> NotificationType:
        return NotificationType.UPCOMING_LESSONS
