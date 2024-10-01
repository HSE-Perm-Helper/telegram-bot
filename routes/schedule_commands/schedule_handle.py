from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api import api
from bot import bot
from callback.callback import check_callback, extract_data_from_callback
from callback.schedule_callback import ScheduleCallback
from decorator.decorators import typing_action, exception_handler
from message.schedule_messages import SCHEDULE_NOT_FOUND_ANYMORE, NO_LESSONS_IN_SCHEDULE
from schedule.schedule_type import ScheduleType
from schedule.schedule_utils import get_button_by_schedule_info, group_lessons_by_key, \
    get_schedule_header_by_schedule_info, get_pair_count, group_lessons_by_pair_number, get_lessons_without_header, \
    get_lesson_message_header
from util.utils import get_day_of_week_from_date, get_day_of_week_from_slug

router = Router()


@router.message(Command('schedule', 'расписание'))
@router.message(lambda F: F.text == ('schedule' or 'расписание'))
@typing_action
@exception_handler
async def get_settings(message):
    await get_text_schedule(message)


# Обработка сообщения получения текстового расписания
@router.message(lambda
                        F: F.text == "Получить текстовое расписание 💼" or F.text == "💼 Расписание на неделю")
@typing_action
@exception_handler
async def callback_message(message):
    await get_text_schedule(message)


# @router.message(Command('schedule'))
# @typing_action
# @exception_handler
# @required_admin
# async def get_remote_schedule(message):
#     await bot.delete_message(message.chat.id, message.message_id)
#     keyword = InlineKeyboardBuilder()
#     link = await api.get_remote_schedule_link(message.chat.id)
#     keyword.add(types.InlineKeyboardButton(text="Добавить расписание в календарь", url=link))
#     await message.answer(text="Чтобы добавить расписание в свой календарь тебе всего лишь нужно нажать на кнопку и "
#                               "выбрать календарь, который ты используешь."
#                               "И всё. Твое расписание у тебя на устройстве!", reply_markup=keyword)


@router.message(Command("base_schedule"))
@router.message(lambda F: F.text == "Получить расписание на модуль 🗓" or F.text == "🗓 Расписание на модуль")
@typing_action
@exception_handler
async def get_base_schedule(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    schedules_json = await api.get_schedules()
    schedules = list(filter(lambda schedule: schedule["scheduleType"] == ScheduleType.QUARTER_SCHEDULE.value,
                            schedules_json['response']))
    if len(schedules) == 0:
        await message.answer(text="Пока расписания на модуль нет! 🎉🎊")
    else:
        schedule = schedules[0]
        response_schedule = await api.get_schedule(message.chat.id, schedule["start"], schedule["end"])
        await schedule_sending(message, response_schedule["response"])


# Получение расписания для календаря
async def get_schedule(message):
    await message.delete()
    text_get_schedule = "🔵 Выбери способ получения расписания:"

    markup = InlineKeyboardBuilder()
    # markup.add(types.InlineKeyboardButton("Добавить автообновляемый календарь",
    #                                       url="webcal://https://hse-schedule-bot.xenforo-studio.ru/api/files/user_files/db625264-0a6c-4b25-b074-4f2f290e76fe/schedule.ics"))
    markup.add(types.InlineKeyboardButton(text="Добавить автообновляемый календарь",
                                          callback_data="add_calendar"))
    markup.add(types.InlineKeyboardButton(text="Получить расписание файлом .ics",
                                          callback_data="get_file"))
    # markup.add(types.InlineKeyboardButton("Отправлять расписание текстом",
    #                                       callback_data="get_text_schedule"))

    await message.answer(text=text_get_schedule, reply_markup=markup)


# Получение текстового расписания
async def get_text_schedule(message):
    await message.delete()
    schedule_json = await api.get_schedules()

    if schedule_json['error'] is True:
        await message.answer(text='Для тебя почему-то нет расписания 🤷\nНастрой группу заново '
                                  'командой /settings!')
    else:
        schedules_dict = list(filter(lambda schedule: schedule["scheduleType"] != ScheduleType.QUARTER_SCHEDULE.value,
                                     schedule_json['response']))

        if len(schedules_dict) == 1:
            schedule = schedules_dict[0]
            start = schedule["start"]
            end = schedule["end"]
            response = await api.get_schedule(message.chat.id, start, end)
            await schedule_sending(message, response["response"])
        elif len(schedules_dict) == 0:
            await message.answer(text="Расписания пока нет, отдыхай! 😎")
        else:
            text_message = "🔵 Выбери расписание, которое ты хочешь увидеть:"
            markup = InlineKeyboardBuilder()

            for schedule in schedules_dict:
                markup.row(get_button_by_schedule_info(schedule, True)),

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
        text_for_message = f"<b>{get_schedule_header_by_schedule_info(schedule_dict)}</b>\n\n"

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
            await message.answer(text=text_for_message, parse_mode='HTML', disable_notification=True)

        await bot.unpin_all_chat_messages(message.chat.id)
        await bot.pin_chat_message(message.chat.id, message_id=header_message.message_id, disable_notification=True)


async def get_lessons_as_string(day, is_session, lessons):
    lesson_list = await group_lessons_by_pair_number(lessons)
    count_pairs = await get_pair_count(lesson_list)
    count_pairs = str(count_pairs)
    text_for_message = await get_lesson_message_header(count_pairs, day, is_session)
    text_for_message += await get_lessons_without_header(lesson_list)
    return text_for_message


# Пользователем выбрано расписание для отправки
@typing_action
@router.callback_query(lambda c: check_callback(c, ScheduleCallback.TEXT_SCHEDULE_CHOICE.value))
@exception_handler
async def callback_message(callback_query: types.CallbackQuery):
    data = extract_data_from_callback(ScheduleCallback.TEXT_SCHEDULE_CHOICE.value, callback_query.data)
    start = data[0]
    end = data[1]
    need_delete_message = data[2]

    if need_delete_message == "True":
        await callback_query.message.delete()

    schedule_json = await api.get_schedule(callback_query.message.chat.id, start, end)

    if need_delete_message == "False" and schedule_json["error"]:
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
    schedule_dict = schedule_json['response']
    await schedule_sending(callback_query.message, schedule_dict)
