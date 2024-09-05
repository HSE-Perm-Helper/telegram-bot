from telebot import types

from schedule.schedule_type import ScheduleType
from callback.schedule_callback import ScheduleCallback
from callback.callback import insert_data_to_callback

emojies_for_week_color = ['🟥', '🟪', '🟦', '🟩', '🟧', '🟨']


def get_button_text_by_schedule_info(schedule_info: dict, start: str, end: str) -> str:
    schedule_type = schedule_info["scheduleType"]
    match schedule_type:
        case ScheduleType.COMMON_SCHEDULE.value:
            number = schedule_info["number"]
            return f"Неделя {number}, {start} — {end}"
        case ScheduleType.SESSION_SCHEDULE.value:
            return f"Сессия, {start} — {end}"
        case ScheduleType.QUARTER_SCHEDULE.value:
            number = schedule_info["number"]
            return f"Базовое расписание на {number} модуль"
    return "N/a"


def get_schedule_header_by_schedule_info(schedule_info: dict) -> str:
    schedule_type = schedule_info["scheduleType"]
    match schedule_type:
        case ScheduleType.COMMON_SCHEDULE.value:
            number = schedule_info["number"]
            emoji_index = number % len(emojies_for_week_color)
            emoji = emojies_for_week_color[emoji_index]
            return f"{emoji} Расписание на {number} неделю {emoji}"
        case ScheduleType.SESSION_SCHEDULE.value:
            return f"🍀 Расписание на сессию 🍀"
        case ScheduleType.QUARTER_SCHEDULE.value:
            number = schedule_info["number"]
            return f"🗓 Расписание на {number} модуль 🗓"
    return "N/a"


def get_button_by_schedule_info(schedule_info: dict, need_delete_message: bool) -> types.InlineKeyboardButton:
    start = schedule_info["start"]
    end = schedule_info["end"]
    data = insert_data_to_callback(ScheduleCallback.TEXT_SCHEDULE_CHOICE.value, [start, end, need_delete_message])
    return types.InlineKeyboardButton(get_button_text_by_schedule_info(schedule_info, start, end),
                                      callback_data=data)


def group_lessons_by_key(lessons: list[dict], key_func) -> dict[str, list[dict]]:
    lessons_by_key = {}
    for lesson in lessons:
        key = key_func(lesson)
        if key not in lessons_by_key:
            lessons_by_key[key] = []
        lessons_by_key[key].append(lesson)
    return lessons_by_key
