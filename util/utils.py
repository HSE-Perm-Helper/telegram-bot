import datetime
from typing import Callable

from aiogram.types import InlineKeyboardButton

import callback.callback
from callback.settings_callback import SettingsCallback
from settings.setting_code import SettingCode

days_of_week_list = ['Понедельник',
                     'Вторник',
                     'Среда',
                     'Четверг',
                     'Пятница',
                     'Суббота',
                     'Воскресенье']

days_of_week_slug = {
    "MONDAY": days_of_week_list[0],
    "TUESDAY": days_of_week_list[1],
    "WEDNESDAY": days_of_week_list[2],
    "THURSDAY": days_of_week_list[3],
    "FRIDAY": days_of_week_list[4],
    "SATURDAY": days_of_week_list[5],
    "SUNDAY": days_of_week_list[6]
}


def format_output_array(array: list[str]):
    if len(array) == 0:
        return ""
    if array[0] is not str:
        array = list(map(str, array))
    if len(array) == 1:
        return array[0]
    output = ", ".join(array[0: len(array) - 1])
    return f"{output} и {array[-1]}"


def get_day_of_week_from_date(date_string: str) -> str:
    day_, month, year = date_string.split('.')
    day_ = int(day_)
    month = int(month)
    year = int(year)
    date = datetime.datetime(year, month, day_)
    day_of_the_week = days_of_week_list[date.isoweekday() - 1]
    return day_of_the_week


def get_day_of_week_from_slug(slug: str) -> str:
    return days_of_week_slug.get(slug.upper(), "N/a")


async def get_notification_disable_button(setting_code: SettingCode) -> InlineKeyboardButton:
    callback_data = callback.callback.insert_data_to_callback(SettingsCallback.OFF_NOTIFICATION.value,
                                                              [setting_code.value])
    return InlineKeyboardButton(text="Не хочу получать такие уведомления 🥸",
                                callback_data=callback_data)


async def do_or_nothing(function: Callable, *args):
    try:
        await function(*args)
    except Exception as e:
        pass
