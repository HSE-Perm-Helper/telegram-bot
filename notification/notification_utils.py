from aiogram.utils.keyboard import InlineKeyboardBuilder

from schedule import schedule_utils
from schedule.schedule_type import ScheduleType
from util.utils import format_output_array


def get_difference_schedule(schedules):
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


def get_markup_schedule(schedules) -> InlineKeyboardBuilder:
    keyword = InlineKeyboardBuilder()
    for schedule in schedules:
        keyword.row(schedule_utils.get_button_by_schedule_info(schedule, False))
    return keyword
