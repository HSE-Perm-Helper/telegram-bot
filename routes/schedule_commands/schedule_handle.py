from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api import timetable_service
from bot import bot
from callback.callback import check_callback, extract_data_from_callback
from callback.schedule_callback import TimetableCallback
from decorator.decorators import typing_action
from message.schedule_messages import SCHEDULE_NOT_FOUND_ANYMORE, NO_LESSONS_IN_SCHEDULE
from schedule.schedule_type import ScheduleType
from schedule.schedule_utils import get_button_by_timetable_info, group_lessons_by_key, \
    get_timetable_header_by_timetable_info, get_pair_count, group_lessons_by_pair_number, get_lessons_without_header, \
    get_lesson_message_header
from util.utils import get_day_of_week_from_date, get_day_of_week_from_slug, do_or_nothing

router = Router()

@router.message(Command('schedule', 'расписание'))
@router.message(lambda F: F.text == ('schedule' or 'расписание'))
@typing_action
async def get_settings(message):
    await get_text_schedule(message)


# Обработка сообщения получения текстового расписания
@router.message(lambda
                        F: F.text == "Получить текстовое расписание 💼" or F.text == "💼 Расписание на неделю")
@typing_action
async def callback_message(message, state: FSMContext):
    await state.clear()

    await get_text_schedule(message)


@router.message(Command("base_schedule"))
@router.message(lambda F: F.text == "Получить расписание на модуль 🗓" or F.text == "🗓 Расписание на модуль")
@typing_action
async def get_base_schedule(message: types.Message, state: FSMContext):
    await state.clear()

    await bot.delete_message(message.chat.id, message.message_id)
    timetable_json = await timetable_service.get_timetables(message.chat.id)

    timetables = list(filter(lambda timetable: timetable["scheduleType"] == ScheduleType.QUARTER_SCHEDULE.value,
                             timetable_json))
    if len(timetables) == 0:
        await message.answer(text="Пока расписания на модуль нет! 🎉🎊")
    else:
        timetable = timetables[0]
        response_schedule = await timetable_service.get_timetable(message.chat.id, timetable["id"])
        await schedule_sending(message, response_schedule)


# Получение текстового расписания
async def get_text_schedule(message):
    await message.delete()
    timetable_json = await timetable_service.get_timetables(message.chat.id)

    if timetable_json is None:
        await message.answer(text='Для тебя почему-то нет расписания 🤷\nНастрой группу заново '
                                  'командой /settings!')
    else:
        timetables_dict = list(filter(lambda schedule: schedule["scheduleType"] != ScheduleType.QUARTER_SCHEDULE.value,
                                     timetable_json))

        if len(timetables_dict) == 1:
            timetable = timetables_dict[0]
            response = await timetable_service.get_timetable(message.chat.id, timetable["id"])
            await schedule_sending(message, response)
        elif len(timetables_dict) == 0:
            await message.answer(text="Расписания пока нет, отдыхай! 😎")
        else:
            text_message = "🔵 Выбери расписание, которое ты хочешь увидеть:"
            markup = InlineKeyboardBuilder()

            for timetable in timetables_dict:
                markup.row(get_button_by_timetable_info(timetable, True)),

            await message.answer(text=text_message, reply_markup=markup.as_markup())


# Формирование расписания
async def schedule_sending(message: types.Message, schedule_dict):
    schedule_type = schedule_dict["scheduleType"]
    is_session = False
    if schedule_type == ScheduleType.SESSION_SCHEDULE.value:
        is_session = True

    temp_lessons = schedule_dict['lessons']

    if len(temp_lessons) == 0:
        await message.answer(text=NO_LESSONS_IN_SCHEDULE, parse_mode='HTML')
        return

    else:
        text_for_message = f"<b>{get_timetable_header_by_timetable_info(schedule_dict)}</b>\n\n"

        header_message = await message.answer(text_for_message, parse_mode='HTML')

        if schedule_type == ScheduleType.QUARTER_SCHEDULE.value:
            temp_lessons = group_lessons_by_key(temp_lessons,
                                                lambda l: get_day_of_week_from_slug(l["time"]["dayOfWeek"]))
        else:
            temp_lessons = group_lessons_by_key(temp_lessons,
                                                lambda l: f'{get_day_of_week_from_date(l["time"]["date"])}'
                                                          f', {l["time"]["date"]}')
        for day, lessons in temp_lessons.items():
            text_for_message = await get_lessons_as_string(day, is_session, lessons)
            await message.answer(text=text_for_message, parse_mode='HTML', disable_notification=True, disable_web_page_preview=True)

        await do_or_nothing(bot.unpin_all_chat_messages, message.chat.id)
        await bot.pin_chat_message(message.chat.id, message_id=header_message.message_id, disable_notification=True)


async def get_lessons_as_string(day, is_session, lessons):
    lesson_list = await group_lessons_by_pair_number(lessons)
    count_pairs = await get_pair_count(lesson_list)
    count_pairs = str(count_pairs)
    text_for_message = await get_lesson_message_header(count_pairs, day, is_session)
    text_for_message += await get_lessons_without_header(lesson_list)
    return text_for_message


@router.callback_query(lambda c: check_callback(c, TimetableCallback.TIMETABLE_CHOICE.value))
async def callback_message(callback_query: types.CallbackQuery):
    data = extract_data_from_callback(TimetableCallback.TIMETABLE_CHOICE.value, callback_query.data)
    id = data[0]
    need_delete_message = True if len(data) > 1 and data[1] == "True" else False

    if need_delete_message:
        await callback_query.message.delete()

    timetable_json = await timetable_service.get_timetable(callback_query.message.chat.id, id)

    if not need_delete_message and timetable_json is None:
        await callback_query.answer(text=SCHEDULE_NOT_FOUND_ANYMORE, show_alert=True)

        keyboard: list[list[types.InlineKeyboardButton]] = callback_query.message.reply_markup.inline_keyboard
        new_keyboard: list[list[types.InlineKeyboardButton]] = []
        for row in keyboard:
            filtered_row = list(filter(lambda button: button.callback_data != callback_query.data, row))
            if len(filtered_row) > 0:
                new_keyboard.append(filtered_row)

        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                            message_id=callback_query.message.message_id,
                                            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=new_keyboard))
        return

    await bot.answer_callback_query(callback_query.id)
    schedule_dict = timetable_json
    await schedule_sending(callback_query.message, schedule_dict)
