from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from api.api import get_today_lessons as get_lessons
from decorator.decorators import exception_handler, typing_action
from routes.schedule_commands.schedule_handle import get_lessons_as_string
from schedule.schedule_type import ScheduleType
from util.utils import get_day_of_week_from_date

router = Router()

@exception_handler
@typing_action
@router.message(F.text == "📅 На сегодня")
@router.message(Command("today"))
async def get_today_lessons(message: Message, state: FSMContext):
    await state.clear()

    lessons = await get_lessons(message.chat.id)
    await message.delete()

    if len(lessons) == 0:
        await message.answer("Сегодня у тебя нет пар 😎")
        return

    is_session = lessons[0]["parentScheduleType"] == ScheduleType.SESSION_SCHEDULE.value

    day = f'{get_day_of_week_from_date(lessons[0]["time"]["date"])}, {lessons[0]["time"]["date"]}'

    text_for_message = await get_lessons_as_string(day, is_session, lessons)

    await message.answer(text=text_for_message, parse_mode='HTML', disable_notification=True)