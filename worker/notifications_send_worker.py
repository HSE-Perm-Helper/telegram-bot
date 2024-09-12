import asyncio
import enum
import traceback

from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot import bot
from schedule import schedule_utils
from schedule.schedule_type import ScheduleType
from util.logs_utils import send_logs_to_admins
from util.utils import get_request, delete_request, format_output_array

router = Router()


class NotificationType(enum.Enum):
    SCHEDULE_ADDED = "SCHEDULE_ADDED"
    SCHEDULE_CHANGED = "SCHEDULE_CHANGED_FOR_USER"


class NotificationsSendWorker:
    def __init__(self):
        super().__init__()

    def get_difference(self, schedules):
        quarter_schedule = []
        common_schedule = []
        session_schedule = []
        difference = []
        for schedule in schedules:
            scheduleType = schedule["scheduleType"]
            match scheduleType:
                case ScheduleType.QUARTER_SCHEDULE.value:
                    quarter_schedule.append(schedule)
                case ScheduleType.COMMON_SCHEDULE.value:
                    common_schedule.append(schedule)
                case ScheduleType.SESSION_SCHEDULE.value:
                    session_schedule.append(schedule)
        if len(quarter_schedule) > 0:
            difference.append("базовое расписание")
        if len(common_schedule) > 0:
            weeks = []
            for schedule in common_schedule:
                weeks.append(schedule["number"])
            merged_weeks = format_output_array(weeks)
            difference.append(f"расписание на {merged_weeks} неделю")
        if len(session_schedule) > 0:
            difference.append("расписание на сессию")
        return format_output_array(difference)

    def get_markup(self, schedules) -> InlineKeyboardBuilder:
        keyword = InlineKeyboardBuilder()
        for schedule in schedules:
            keyword.row(schedule_utils.get_button_by_schedule_info(schedule, False))
        return keyword

    async def check_new_notifications(self):
        try:
            notifications_response = await get_request(path="/notifications")
            new_schedule: dict[int, list] = {}
            schedule_changing: dict[int, list] = {}
            notifications_data = notifications_response.json()
            if notifications_response.status_code == 200:
                if len(notifications_data['response']) != 0:
                    for notification in notifications_data['response']:
                        notification_type = notification['notificationType']
                        users = notification["users"]

                        match notification_type:
                            case NotificationType.SCHEDULE_ADDED.value:
                                for user in users:
                                    if user not in new_schedule:
                                        new_schedule[user] = []
                                    new_schedule[user].append(notification["targetSchedule"])

                            case NotificationType.SCHEDULE_CHANGED.value:
                                for user in users:
                                    if user not in schedule_changing:
                                        schedule_changing[user] = []
                                    schedule_changing[user].append(notification["targetSchedule"])

                    for telegram_id, schedules in schedule_changing.items():
                        difference = self.get_difference(schedules)
                        markup = self.get_markup(schedules)
                        try:
                            await bot.send_message(telegram_id, f"🟣Твоё {difference} было изменено!🟣\n",
                                                   reply_markup=markup.as_markup())
                        except Exception as e:
                            print(e)
                            pass

                    for telegram_id, schedules in new_schedule.items():
                        difference = self.get_difference(schedules)
                        markup = self.get_markup(schedules)
                        try:
                            await bot.send_message(telegram_id, f"🟣Было добавлено {difference}!🟣\n",
                                                   reply_markup=markup.as_markup())
                        except Exception as e:
                            print(e)
                            pass

                delete_events = await delete_request(path="/notifications", json=notifications_data['response'])

            else:
                await send_logs_to_admins(
                    f"Проверка уведомлений вернула код {notifications_response.status_code}, вместо OK")
        except Exception as e:
            await send_logs_to_admins(f"Произошла ошибка при попытке отправить запрос новых уведомлений на сервер!\n"
                                      f"Стэктрейс: \n"
                                      f"{traceback.format_exc()}")

    async def run(self):
        while True:
            await self.check_new_notifications()
            await asyncio.sleep(300)
