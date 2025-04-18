from datetime import datetime, timedelta

import pytz
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from api.schedule_service import get_tomorrow_lessons as get_lessons
from decorator.decorators import typing_action
from routes.schedule_commands.schedule_handle import get_lessons_as_string
from schedule.schedule_type import ScheduleType
from util.utils import get_day_of_week_from_date

router = Router()


@typing_action
@router.message(F.text == "➡️ На завтра")
@router.message(Command("tomorrow"))
async def get_tomorrow_lessons(message: Message, state: FSMContext):
    await state.clear()

    await message.delete()
    lessons = await get_lessons(message.chat.id)

    if len(lessons) == 0:
        date = datetime.now(pytz.timezone("Asia/Yekaterinburg")) + timedelta(days=1)
        if date.weekday() == 6:
            date += timedelta(days=1)

        days_of_week = ['понедельник',
                        'вторник',
                        'среду',
                        'четверг',
                        'пятницу',
                        'субботу',
                        'Воскресенье']

        day_of_week = days_of_week[date.weekday()].lower()

        await message.answer(f"На {day_of_week} у тебя нет пар 😎")
        # await message.answer(f"На {day_of_week} у тебя нет пар 🃏") # halloween
        return

    is_session = lessons[0]["parentScheduleType"] == ScheduleType.SESSION_SCHEDULE.value

    day = f'{get_day_of_week_from_date(lessons[0]["time"]["date"])}, {lessons[0]["time"]["date"]}'

    text_for_message = await get_lessons_as_string(day, is_session, lessons)

    await message.answer(text=text_for_message, parse_mode='HTML', disable_notification=True)
