import random

from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from api import api
from bot import bot
from message.schedule_messages import SCHEDULE_NOT_FOUND_ANYMORE, NO_LESSONS_IN_SCHEDULE
from schedule.schedule_type import ScheduleType
from schedule.schedule_utils import get_button_by_schedule_info, group_lessons_by_key, \
    get_schedule_header_by_schedule_info
from util.utils import get_day_of_week_from_date, get_day_of_week_from_slug, answer_callback
from constants import constant
from callback.callback import check_callback, extract_data_from_callback
from callback.schedule_callback import ScheduleCallback
from decorator.decorators import typing_action, exception_handler
import routes.command_handle.commands as commands

router = Router()


def get_menu(message):
    text_schedule = ("<b>Команды для работы:</b>\n\n"
                     "🔹 /settings — <i>Изменение информации о себе</i>\n\n"
                     "🔹 /menu — <i>Получить меню для работы</i>\n\n"
                     "🔹 /help — <i>Вывод помощи</i>\n\n"
                     "🔹 /schedule_handle — <i>Получить расписание</i>\n\n"
                     "🔹 /base_schedule — <i>Получить расписание на модуль</i>\n\n"
                     "❗ При удалении этого сообщения кнопки выбора расписания пропадут. "
                     "Чтобы их вернуть, введи /menu еще раз! 🙂")

    keyboard_markup_up = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup_down = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # add_schedule_calendar_button = types.KeyboardButton("Добавить обновляемый календарь")
    get_schedule_text_button = types.KeyboardButton(text="Получить текстовое расписание 💼")
    get_base_schedule_text_button = types.KeyboardButton(text="Получить расписание на модуль 🗓")
    # get_deadlines_button = types.KeyboardButton("Проверить дедлайны")
    # keyboard_markup_up.row(add_schedule_calendar_button)
    keyboard_markup_up.row(get_schedule_text_button)
    keyboard_markup_up.row(get_base_schedule_text_button)
    keyboard_markup_up.row_width = 4

    message.answer(text_schedule,
                   reply_markup=keyboard_markup_up, parse_mode='HTML')


# Получение расписания для календаря
def get_schedule(message):
    bot.delete_message(message.chat.id, message.message_id)
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

    message.answer(text=text_get_schedule, reply_markup=markup)


# Получение текстового расписания
def get_text_schedule(message):
    bot.delete_message(message.chat.id, message.message_id)
    schedule_json = api.get_schedules()

    if schedule_json['error'] is True:
        message.answer(text='Для тебя почему-то нет расписания 🤷\nНастрой группу заново '
                            'командой /settings!')
    else:
        schedules_dict = list(filter(lambda schedule: schedule["scheduleType"] != ScheduleType.QUARTER_SCHEDULE.value,
                                     schedule_json['response']))

        if len(schedules_dict) == 1:
            schedule = schedules_dict[0]
            start = schedule["start"]
            end = schedule["end"]
            schedule_sending(message, api.get_schedule(message.chat.id, start, end)["response"])
        elif len(schedules_dict) == 0:
            message.answer(text="Расписания пока нет, отдыхай! 😎")
        else:
            text_message = "🔵 Выбери расписание, которое ты хочешь увидеть:"
            markup = InlineKeyboardBuilder()

            for schedule in schedules_dict:
                markup.add(get_button_by_schedule_info(schedule, True)),

            message.answer(text=text_message, reply_markup=markup)


def get_lesson_as_string(lesson):
    text_for_message = ''
    '''Если вид пары — майнор'''
    if lesson['lessonType'] == 'COMMON_MINOR':
        text_for_message = f"{constant.type_of_lessons_dict[lesson['lessonType']]}\n"

    else:
        '''Вычисляем время пары'''
        time_of_pair = f"{lesson['time']['startTime']} — {lesson['time']['endTime']}"

        if lesson['time']['startTime'] is not None and lesson['time']['endTime'] != None:
            '''Добавляем в сообщение номер пары'''
            text_for_message += f"<b>{constant.number_of_pair_dict[lesson['time']['startTime']]}</b> — "

            '''Добавляем в сообщение название пары и ее тип'''
            if lesson['lessonType'] in constant.type_of_lessons_dict.keys():
                text_for_message += (f"{lesson['subject']} — "
                                     f"{constant.type_of_lessons_dict[lesson['lessonType']]}\n")

            '''Добавляем в сообщение время пары'''
            text_for_message += (f"<b>{time_of_pair}</b> ")

        '''Проверяем, дистант или очная'''
        if lesson['isOnline']:

            '''- Если дистант, добавляем ссылки'''
            if lesson['links'] is None:
                text_for_message += (f"Дистанционная пара, ссылки отсутствуют \n")

            else:
                text_for_message += (f"Дистанционная пара, ссылки:\n")
                for link in lesson['links']:
                    text_for_message += (f"{link}\n")

        else:
            if lesson['places'] is not None:
                if len(lesson['places']) == 1:
                    place = lesson['places'][0]
                    text_for_message += (
                        f"Корпус {place['building']}, аудитория {place['office']} \n")
                else:
                    text_for_message += f'несколько мест:\n'
                    for place in lesson['places']:
                        '''- Иначе добавляем номер корпуса и аудиторию'''
                        text_for_message += (
                            f"Корпус {place['building']}, аудитория {place['office']} \n")

        if lesson['lecturer'] is not None:
            '''Добавляем преподавателя пары'''
            text_for_message += (f"Преподаватель — <i>{lesson['lecturer']}</i> \n")

        '''Проверяем наличие дополнительной информации к паре'''
        if lesson['additionalInfo'] is not None:
            for addInfo in lesson['additionalInfo']:
                text_for_message += (f"\n<i>Доп.информация: — {addInfo}</i> \n")

        text_for_message += "\n"
    return text_for_message


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

        header_message = bot.send_message(message.chat.id, text_for_message, parse_mode='HTML')

        if schedule_type == ScheduleType.QUARTER_SCHEDULE.value:
            temp_lessons = group_lessons_by_key(temp_lessons,
                                                lambda l: get_day_of_week_from_slug(l["time"]["dayOfWeek"]))
        else:
            temp_lessons = group_lessons_by_key(temp_lessons,
                                                lambda l: f'{get_day_of_week_from_date(l["time"]["date"])}'
                                                          f', {l["time"]["date"]}')
        for day, lessons in temp_lessons.items():
            last_pair = constant.number_of_pair_dict[lessons[- 1]["time"]['startTime']]
            lessons_list_count = int(last_pair.replace('-ая пара', ''))

            lesson_list: list[None | list[dict]] = [None] * lessons_list_count

            ''' Тут я делаю проход по парам за день, в нем расставляю в массиве пары
                Потом иду по этому массиву и проверяю, 0 там или словарь. Если словарь - раскрываю его
                Иначе вывожу сообщение "Окно" '''

            for lesson in lessons:
                pair_index_string = constant.number_of_pair_dict[lesson["time"]["startTime"]]
                pair_index = int(pair_index_string.replace('-ая пара', '')) - 1

                if lesson_list[pair_index] is None:
                    lesson_list[pair_index] = []

                lesson_list[pair_index].append(lesson)

            count_pairs = 0
            for pair in lesson_list:
                if pair:
                    count_pairs += 1

            count_pairs = str(count_pairs)

            text_for_message = ""

            if is_session:
                text_for_message += f"<b>{day}</b>\n\n"
            else:
                text_for_message += (f"<b>{day} — "
                                     f"{constant.count_pairs_dict[count_pairs]}</b>\n\n")

            '''Проходим по всем парам в данный день'''

            is_pairs_start = False
            number_of_pair = 0
            for lessons_inner in lesson_list:
                if not is_pairs_start:
                    if lessons_inner:
                        is_pairs_start = True
                if not lessons_inner:
                    if is_pairs_start:
                        text_for_message += f"<b>{number_of_pair + 1}-ая пара</b>"
                        text_for_message += f" - ОКНО 🪟\n\n"

                else:
                    for lesson in lessons_inner:
                        text_for_message += get_lesson_as_string(lesson)
                number_of_pair += 1
            await message.answer(text=text_for_message, parse_mode='HTML')

        bot.unpin_all_chat_messages(message.chat.id)
        bot.pin_chat_message(message.chat.id, message_id=header_message.message_id, disable_notification=True)


# Пользователем выбрано расписание для отправки
@typing_action
@router.callback_query(lambda c: check_callback(c, ScheduleCallback.TEXT_SCHEDULE_CHOICE.value))
@exception_handler
async def callback_message(callback_query: types.CallbackQuery):

    await bot.answer_callback_query(callback_query.id)

    data = extract_data_from_callback(ScheduleCallback.TEXT_SCHEDULE_CHOICE.value, callback_query.data)
    start = data[0]
    end = data[1]
    need_delete_message = data[2]
    if need_delete_message == "True":
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    schedule_json = api.get_schedule(callback_query.message.chat.id, start, end)
    if need_delete_message == "False" and schedule_json["error"]:
        answer_callback(bot, callback_query, text=SCHEDULE_NOT_FOUND_ANYMORE, show_alert=True)

        keyboard = callback_query.message.reply_markup.keyboard
        new_keyboard = []
        for row in keyboard:
            filtered_row = list(filter(lambda button: button.callback_data != callback_query.data, row))
            if len(filtered_row) > 0:
                new_keyboard.append(filtered_row)

        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                      message_id=callback_query.message.message_id,
                                      reply_markup=types.InlineKeyboardMarkup(keyboard=new_keyboard))
        return
    schedule_dict = schedule_json['response']
    await schedule_sending(callback_query.message, schedule_dict)


@typing_action
@router.callback_query(lambda c: c.data.startswith("mailing_course"))
@exception_handler
async def callback_message(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = callback_query.data.replace('mailing_course_', "")
    course = None
    if data != "all":
        course = int(data)
    await bot.send_message(callback_query.message.chat.id,
                     "Введите сообщение для рассылки: ")
    bot.register_next_step_handler(callback_query.message, commands.send_mail, course=course)

