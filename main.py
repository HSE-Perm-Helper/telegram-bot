import random

from telebot import types

import api
from worker import workers
from bot import bot
from callback.callback import check_callback, extract_data_from_callback
from callback.schedule_callback import ScheduleCallback
from decorator.decorators import typing_action, exception_handler, required_admin
from message.schedule_messages import SCHEDULE_NOT_FOUND_ANYMORE, NO_LESSONS_IN_SCHEDULE
from message.common_messages import SUCCESS_REGISTER
from schedule.schedule import ScheduleType
from schedule.schedule_utils import get_button_by_schedule_info, group_lessons_by_key, get_schedule_header_by_schedule_info
from util.users_utils import send_message_to_users
from util.utils import is_admin, get_day_of_week_from_date, get_day_of_week_from_slug, answer_callback

# ---------------------------------  Настройка бота  ----------------------------------- #

bot.can_join_groups = False  # Запрет на приглашения в группы (ему пофиг)
version = "1.10.0-beta"

# ---------------------------------  Данные  ----------------------------------- #

type_of_lessons_dict = {
    'LECTURE': 'лекция 😴',
    'SEMINAR': 'семинар 📗',
    'COMMON_MINOR': 'Майнор Ⓜ',
    'ENGLISH': 'английский 🆎',
    'EXAM': 'экзамен ☠️',
    'INDEPENDENT_EXAM': 'независимый экзамен ☠️☠️',
    'TEST': 'зачёт ☠️',
    'PRACTICE': 'практика 💼',
    'MINOR': 'Майнор Ⓜ',
    'COMMON_ENGLISH': 'английский 🆎',
    'STATEMENT': 'ведомость 📜',
    'ICC': 'МКД 📙',
    'UNDEFINED_AED': 'ДОЦ по выбору 📕',
    'AED': 'ДОЦ 📕',
    'CONSULT': 'консультация 🗿',
    'EVENT': 'мероприятие'
}

type_of_program_dict = {
    'МБ': 'Международный бакалавриат по бизнесу и экономике',
    'РИС': 'Разработка информационных систем для бизнеса',
    'И': 'История',
    'ИЯ': 'Иностранные языки',
    'Ю': 'Юриспруденция',
    'УБ': 'Управление бизнесом',
    'Э': 'Экономика',
    'ПИ': 'Программная инженерия',
    'БИ': 'Бизнес-информатика'
}

number_of_pair_dict = {
    '8:10': '1-ая пара',
    '9:40': '2-ая пара',
    '11:30': '3-ая пара',
    '13:10': '4-ая пара',
    '15:00': '5-ая пара',
    '16:40': '6-ая пара',
    '18:20': '7-ая пара',
    '20:10': '8-ая пара'
}

count_pairs_dict = {
    '1': '1 пара 🥳',
    '2': '2 пары 🙂',
    '3': '3 пары 😐',
    '4': '4 пары 😟',
    '5': '5 пар 😨',
    '6': '6 пар 😱',
    '7': '7 пар 😵',
    '8': '8 пар ☠'
}

emojies_for_course = ['📒', '📓', '📔', '📕', '📗', '📘', '📙']
emojies_for_programs = ['🌶', '🍑', '🍉', '🍏', '🍍', '🥭', '🍆', '🍐', '🍋', '🍇', '🍒', '🥝', '🥥']
emojies_for_groups = ['⚪', '🔴', '🟡', '🟢', '🟣', '🟤', '🔵', '⚫']
emojies_for_subgroups = ['🌁', '🌃', '🌄', '🌅', '🌆', '🌇', '🌉']


# emojies_for_number_of_pair = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']


# ---------------------------------  Функции  ----------------------------------- #


# Рандомный номер эмодзи для быстрого получения из списка
def rand_emj(count):
    return random.randint(0, count - 1)


# Создание кнопок выбора курса
def get_course(message, is_new_user: bool):
    if is_new_user:
        text_hello = "Давай познакомися! 👋 На каком курсе ты учишься?"
    else:
        text_hello = "Немного изменим данные. ✏ На каком курсе ты учишься?"
    courses = api.get_courses()
    markup = types.InlineKeyboardMarkup()
    random.shuffle(emojies_for_course)
    for i in range(len(courses)):
        emoji_for_button = f"{emojies_for_course[i]} {courses[i]} курс"
        markup.add(types.InlineKeyboardButton(emoji_for_button,
                                              callback_data=f"course_{courses[i]}"
                                                            f"^{is_new_user}"))

    bot.send_message(message.chat.id,
                     text_hello,
                     reply_markup=markup)


# Создание кнопок выбора программы
def get_program(message, data):
    number_course, is_new_user = data.split('^')
    number_course = int(number_course)
    text_get_course = f"Ты выбрал {number_course} курс! 🎉 На каком направлении ты учишься?"

    programs = api.get_programs(number_course)

    markup = types.InlineKeyboardMarkup()
    random.shuffle(emojies_for_programs)
    for i in range(len(programs)):
        if programs[i] in type_of_program_dict.keys():
            emoji_for_button = (f"{emojies_for_programs[i]} "
                                f"{type_of_program_dict[programs[i]]}")
        else:
            emoji_for_button = (f"{emojies_for_programs[i]}"
                                f"{programs[i]}")
        markup.add(types.InlineKeyboardButton(emoji_for_button,
                                              callback_data=f"program_{programs[i]}"
                                                            f"^{number_course}"
                                                            f"^{is_new_user}"))
    markup.add(types.InlineKeyboardButton("⬅ Назад",
                                          callback_data=f"back_to_start{is_new_user}"))

    bot.send_message(message.chat.id,
                     text_get_course,
                     reply_markup=markup)


# Создание кнопок выбора группы
def get_group(message, data):
    program, course, is_new_user = data.split('^')
    if program in type_of_program_dict.keys():
        text_get_group = f"Отлично, ты выбрал: \n{type_of_program_dict[program]} 😎\nТеперь давай выберем группу!"
    else:
        text_get_group = f"Отлично, ты выбрал {program} направление! 😎\nТеперь давай выберем группу!"

    groups = api.get_groups(course,
                            program)

    markup = types.InlineKeyboardMarkup()
    random.shuffle(emojies_for_groups)
    for i in range(len(groups)):
        emoji_for_button = f"{emojies_for_groups[i]} {groups[i]}"
        markup.add(types.InlineKeyboardButton(emoji_for_button,
                                              callback_data=f"group_{groups[i]}"
                                                            f"^{program}"
                                                            f"^{course}"
                                                            f"^{is_new_user}"))
    markup.add(types.InlineKeyboardButton("⬅ Назад",
                                          callback_data=f"back_to_program{course}"
                                                        f"^{is_new_user}"))

    bot.send_message(message.chat.id,
                     text_get_group,
                     reply_markup=markup)


# Создание кнопок выбора подгруппы
def get_subgroup(message, data):
    group, program, course, is_new_user = data.split('^')

    text_get_subgroup = f"{group} — твоя группа. Осталось определиться с подгруппой!"

    subgroups = api.get_subgroups(course,
                                  program,
                                  group)
    markup = types.InlineKeyboardMarkup()
    for i in range(len(subgroups)):
        emoji_for_button = f"{emojies_for_subgroups[rand_emj(len(emojies_for_subgroups))]} {subgroups[i]}"
        markup.add(types.InlineKeyboardButton(emoji_for_button,
                                              callback_data=f"subgroup_{subgroups[i]}"
                                                            f"^{group}"
                                                            f"^{program}"
                                                            f"^{course}"
                                                            f"^{is_new_user}"))
    markup.add(types.InlineKeyboardButton("🚫 Нет подгруппы",
                                          callback_data=f"subgroup_None"
                                                        f"^{group}"
                                                        f"^{program}"
                                                        f"^{course}"
                                                        f"^{is_new_user}"))
    markup.add(types.InlineKeyboardButton("⬅ Назад",
                                          callback_data=f"back_to_group{program}"
                                                        f"^{course}"
                                                        f"^{is_new_user}"))

    bot.send_message(message.chat.id,
                     text_get_subgroup,
                     reply_markup=markup)


# Создание кнопок для подтверждения выбора
def get_confirmation(message, data):
    subgroup, group, program, course, is_new_user = data.split('^')

    '''Заводим новую переменную номера группы, чтобы в сообщение выводилось полное название направления'''
    if program in type_of_program_dict.keys():
        program_for_message = type_of_program_dict[program]
    else:
        program_for_message = program

    '''Два различных варианта вывода информации — с подгруппой и без нее'''
    if subgroup == "None":
        text_confirmation = ("Отлично! ✅ Теперь давай проверим, всё ли верно:\n" +
                             f"{course}-й курс,\n"
                             f"{program_for_message},\n"
                             f"{group} — группа,"
                             f"\n\nВсе верно?")
    else:
        text_confirmation = ("Отлично! ✅ Теперь давай проверим, всё ли верно:\n" +
                             f"{course}-й курс,\n"
                             f"{program_for_message},\n"
                             f"{group} — группа,\n"
                             f"{subgroup} — подгруппа.\n\nВсе верно?")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Все верно! 🎉🎊",
                                          callback_data=f"start_working{course}"
                                                        f"^{program}"
                                                        f"^{group}"
                                                        f"^{subgroup}"
                                                        f"^{message.chat.id}"
                                                        f"^{is_new_user}"))
    markup.add(types.InlineKeyboardButton("Начать сначала ✏",
                                          callback_data=f"back_to_start"
                                                        f"{is_new_user}"))
    markup.add(types.InlineKeyboardButton("⬅ Назад",
                                          callback_data=f"back_to_subgroup{group}"
                                                        f"^{program}"
                                                        f"^{course}"
                                                        f"^{is_new_user}"))

    bot.send_message(message.chat.id,
                     text_confirmation,
                     reply_markup=markup)


# Вывод меню для выбора способа получения расписания
def get_menu(message):
    text_schedule = ("<b>Команды для работы:</b>\n\n"
                     "🔹 /settings — <i>Изменение информации о себе</i>\n\n"
                     "🔹 /menu — <i>Получить меню для работы</i>\n\n"
                     "🔹 /help — <i>Вывод помощи</i>\n\n"
                     "🔹 /schedule — <i>Получить расписание</i>\n\n"
                     "🔹 /base_schedule — <i>Получить расписание на модуль</i>\n\n"
                     "❗ При удалении этого сообщения кнопки выбора расписания пропадут. "
                     "Чтобы их вернуть, введи /menu еще раз! 🙂")

    keyboard_markup_up = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup_down = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # add_schedule_calendar_button = types.KeyboardButton("Добавить обновляемый календарь")
    get_schedule_text_button = types.KeyboardButton("Получить текстовое расписание 💼")
    get_base_schedule_text_button = types.KeyboardButton("Получить расписание на модуль 🗓")
    # get_deadlines_button = types.KeyboardButton("Проверить дедлайны")
    # keyboard_markup_up.row(add_schedule_calendar_button)
    keyboard_markup_up.row(get_schedule_text_button)
    keyboard_markup_up.row(get_base_schedule_text_button)
    keyboard_markup_up.row_width = 4

    bot.send_message(message.chat.id,
                     text_schedule,
                     reply_markup=keyboard_markup_up, parse_mode='HTML')


# Получение расписания для календаря
def get_schedule(message):
    bot.delete_message(message.chat.id, message.message_id)
    text_get_schedule = "🔵 Выбери способ получения расписания:"

    markup = types.InlineKeyboardMarkup()
    # markup.add(types.InlineKeyboardButton("Добавить автообновляемый календарь",
    #                                       url="webcal://https://hse-schedule-bot.xenforo-studio.ru/api/files/user_files/db625264-0a6c-4b25-b074-4f2f290e76fe/schedule.ics"))
    markup.add(types.InlineKeyboardButton("Добавить автообновляемый календарь",
                                          callback_data="add_calendar"))
    markup.add(types.InlineKeyboardButton("Получить расписание файлом .ics",
                                          callback_data="get_file"))
    # markup.add(types.InlineKeyboardButton("Отправлять расписание текстом",
    #                                       callback_data="get_text_schedule"))

    bot.send_message(message.chat.id,
                     text_get_schedule,
                     reply_markup=markup)


# Получение текстового расписания
def get_text_schedule(message):
    bot.delete_message(message.chat.id, message.message_id)
    schedule_json = api.get_schedules()

    if schedule_json['error'] is True:
        bot.send_message(message.chat.id, 'Для тебя почему-то нет расписания 🤷\nНастрой группу заново '
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
            bot.send_message(message.chat.id,
                             "Расписания пока нет, отдыхай! 😎")
        else:
            text_message = "🔵 Выбери расписание, которое ты хочешь увидеть:"
            markup = types.InlineKeyboardMarkup()

            for schedule in schedules_dict:
                markup.add(get_button_by_schedule_info(schedule, True)),

            bot.send_message(message.chat.id,
                             text_message,
                             reply_markup=markup)


def get_lesson_as_string(lesson):
    text_for_message = ''
    '''Если вид пары — майнор'''
    if lesson['lessonType'] == 'COMMON_MINOR':
        text_for_message = f"{type_of_lessons_dict[lesson['lessonType']]}\n"

    else:
        '''Вычисляем время пары'''
        time_of_pair = f"{lesson['time']['startTime']} — {lesson['time']['endTime']}"

        if lesson['time']['startTime'] is not None and lesson['time']['endTime'] != None:
            '''Добавляем в сообщение номер пары'''
            text_for_message += f"<b>{number_of_pair_dict[lesson['time']['startTime']]}</b> — "

            '''Добавляем в сообщение название пары и ее тип'''
            if lesson['lessonType'] in type_of_lessons_dict.keys():
                text_for_message += (f"{lesson['subject']} — "
                                     f"{type_of_lessons_dict[lesson['lessonType']]}\n")

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
def schedule_sending(message, schedule_dict):
    schedule_type = schedule_dict["scheduleType"]
    is_session = False
    if schedule_type == ScheduleType.SESSION_SCHEDULE.value:
        is_session = True

    temp_lessons = schedule_dict['lessons']

    if len(temp_lessons) == 0:
        bot.send_message(message.chat.id, NO_LESSONS_IN_SCHEDULE, parse_mode='HTML')
        return

    else:
        text_for_message = f"<b>{get_schedule_header_by_schedule_info(schedule_dict)}</b>\n\n"

        bot.send_message(message.chat.id, text_for_message, parse_mode='HTML')
        if schedule_type == ScheduleType.QUARTER_SCHEDULE.value:
            temp_lessons = group_lessons_by_key(temp_lessons,
                                                lambda l: get_day_of_week_from_slug(l["time"]["dayOfWeek"]))
        else:
            temp_lessons = group_lessons_by_key(temp_lessons,
                                                lambda l: f'{get_day_of_week_from_date(l["time"]["date"])}'
                                                          f', {l["time"]["date"]}')
        for day, lessons in temp_lessons.items():
            last_pair = number_of_pair_dict[lessons[- 1]["time"]['startTime']]
            lessons_list_count = int(last_pair.replace('-ая пара', ''))

            lesson_list: list[None | list[dict]] = [None] * lessons_list_count

            ''' Тут я делаю проход по парам за день, в нем расставляю в массиве пары
                Потом иду по этому массиву и проверяю, 0 там или словарь. Если словарь - раскрываю его
                Иначе вывожу сообщение "Окно" '''

            for lesson in lessons:
                pair_index_string = number_of_pair_dict[lesson["time"]["startTime"]]
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
                                     f"{count_pairs_dict[count_pairs]}</b>\n\n")

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
            bot.send_message(message.chat.id, text_for_message, parse_mode='HTML')


# ---------------------------------  Обработка команд  ----------------------------------- #


# Обработка команды /start и /registration
@bot.message_handler(commands=['start', 'старт', 'поехали', 'registration', 'регистрация'])
@bot.message_handler(func=lambda message: message.text == ('start' or 'старт' or 'поехали'
                                                           or 'registration' or 'регистрация'))
@typing_action
@exception_handler
def get_registration(message):
    if api.check_registration_user(message.chat.id):
        get_menu(message)
    else:
        get_course(message, True)


# Обработка команды /help
@bot.message_handler(commands=['help', 'помощь', 'помоги'])
@bot.message_handler(func=lambda message: message.text == ('help' or 'помощь' or 'помоги'))
@typing_action
@exception_handler
def get_help(message):
    bot.delete_message(message.chat.id, message.message_id)
    text_help = ("<b>Вот, что я могу:</b>\n\n"
                 "🔹 /start — <i>Начало работы. Производится выбор курса, направления, группы и подгруппы</i>\n\n"
                 "🔹 /settings — <i>Изменение информации о себе</i>\n\n"
                 "🔹 /menu — <i>Получить меню для работы</i>\n\n"
                 "🔹 /schedule — <i>Получить расписание</i>\n\n"
                 "Канал для обратной связи — <b>@hse_perm_helper_feedback</b>\n"
                 "Будем рады твоему отзыву или предложению!\n\n"
                 f"Версия <i>{version}</i>")
    bot.send_message(message.chat.id, text_help, parse_mode='HTML')


# Обработка команды /menu
@bot.message_handler(commands=['menu', 'меню'])
@bot.message_handler(func=lambda message: message.text == ('menu' or 'меню'))
@typing_action
@exception_handler
def start_working(message):
    bot.delete_message(message.chat.id, message.message_id)
    get_menu(message)


# Обработка команды /settings
@bot.message_handler(commands=['settings', 'настройки'])
@bot.message_handler(func=lambda message: message.text == ('settings' or 'настройки'))
@typing_action
@exception_handler
def get_settings(message):
    bot.delete_message(message.chat.id, message.message_id)
    get_course(message, False)


# Обработка команды /schedule
@bot.message_handler(commands=['schedule', 'расписание'])
@bot.message_handler(func=lambda message: message.text == ('schedule' or 'расписание'))
@typing_action
@exception_handler
def get_settings(message):
    get_text_schedule(message)


# Обработка сообщения добавления календаря
# @bot.message_handler(func= lambda message: message.text == "Добавить обновляемый календарь")
# def callback_message(message):
#     get_schedule(message)


# Обработка сообщения получения текстового расписания
@bot.message_handler(func=lambda
        message: message.text == "Получить текстовое расписание 💼" or message.text == "Получить текстовое расписание")
@typing_action
@exception_handler
def callback_message(message):
    get_text_schedule(message)


@bot.message_handler(commands=['remote_schedule'])
@typing_action
@exception_handler
def get_remote_schedule(message):
    if not is_admin(message.chat.id):
        return
    bot.delete_message(message.chat.id, message.message_id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    link = api.get_remote_schedule_link(message.chat.id)
    markup.add(types.InlineKeyboardButton(text="Добавить расписание в календарь", url=link))
    bot.send_message(message.chat.id,
                     text="Чтобы добавить расписание в свой календарь тебе всего-лишь нужно нажать на кнопку и выбрать календарь, который ты используешь."
                          "И всё. Твое расписание у тебя на устройстве!", reply_markup=markup)


# Обработка команды /mailing
@bot.message_handler(commands=["mailing"])
@exception_handler
@required_admin
def mailing_to_all(message: types.Message):
    courses = api.get_courses()
    markup = types.InlineKeyboardMarkup()
    text = "Выберите курсы, в которые необходимо сделать рассылку:"
    for i in range(len(courses)):
        emoji_for_button = f"{emojies_for_course[i]} {courses[i]} курс"
        markup.add(types.InlineKeyboardButton(emoji_for_button,
                                              callback_data=f"mailing_course_{courses[i]}"))
    markup.add(types.InlineKeyboardButton("Всем",
                                          callback_data=f"mailing_course_all"))

    bot.send_message(message.chat.id,
                     text,
                     reply_markup=markup)


@bot.message_handler(commands=["base_schedule"])
@bot.message_handler(func=lambda message: message.text == "Получить расписание на модуль 🗓")
@typing_action
@exception_handler
def get_base_schedule(message: types.Message):
    bot.delete_message(message.chat.id, message.message_id)
    schedules_json = api.get_schedules()
    schedules = list(filter(lambda schedule: schedule["scheduleType"] == ScheduleType.QUARTER_SCHEDULE.value,
                            schedules_json['response']))
    if len(schedules) == 0:
        bot.send_message(message.chat.id,
                         "Пока расписания на модуль нет! 🎉🎊")
    else:
        schedule = schedules[0]
        response_schedule = api.get_schedule(message.chat.id, schedule["start"], schedule["end"])
        schedule_sending(message, response_schedule["response"])


def send_mail(message: types.Message, course: int = None):
    bot.send_message(message.chat.id, "Рассылка успешно отправлена!")
    if not course:
        users = api.get_user_ids()
    else:
        users = api.get_user_ids_by_course(course)
    send_message_to_users(message.html_text, users)


# ---------------------------------  Обработка событий  ----------------------------------- #


# Обработка события нажатия на кнопку выбора курса
@typing_action
@bot.callback_query_handler(lambda c: c.data.startswith('course_'))
@exception_handler
def course_query_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.replace("course_", "")
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

    get_program(callback_query.message, data)


# Обработка события нажатия на кнопку выбора программы
@typing_action
@bot.callback_query_handler(lambda c: c.data.startswith('program_'))
@exception_handler
def program_query_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.replace("program_", "")
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    get_group(callback_query.message, data)


# Обработка события нажатия на кнопку выбора группы
@typing_action
@bot.callback_query_handler(lambda c: c.data.startswith('group_'))
@exception_handler
def group_query_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.replace("group_", "")
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    get_subgroup(callback_query.message, data)


# Обработка события нажатия на кнопку выбора подгруппы
@typing_action
@bot.callback_query_handler(lambda c: c.data.startswith('subgroup_'))
@exception_handler
def subgroup_query_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.replace("subgroup_", "")
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    get_confirmation(callback_query.message, data)


# Обработка события возврата на предыдущий выбор
@typing_action
@bot.callback_query_handler(lambda c: c.data.startswith('back_to_'))
@exception_handler
def program_query_handler(callback_query: types.CallbackQuery):
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

    if callback_query.data.startswith('back_to_program'):
        data = callback_query.data.replace('back_to_program', "")
        get_program(callback_query.message, data)
    elif callback_query.data.startswith('back_to_group'):
        data = callback_query.data.replace('back_to_group', "")
        get_group(callback_query.message, data)
    elif callback_query.data.startswith('back_to_subgroup'):
        data = callback_query.data.replace('back_to_subgroup', "")
        get_subgroup(callback_query.message, data)
    elif callback_query.data.startswith('back_to_start'):
        data = callback_query.data.replace('back_to_start', "")
        get_course(callback_query.message, data == "True")


# Обработка события нажатия на кнопку подтверждения данных
@typing_action
@bot.callback_query_handler(lambda c: c.data.startswith("start_working"))
@exception_handler
def callback_message(callback_query: types.CallbackQuery):
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = callback_query.data.replace('start_working', "")
    course, program, group, subgroup, telegram_id, is_new_user = data.split("^")

    if subgroup != "None":
        subgroup = int(subgroup)
    else:
        subgroup = 0

    if is_new_user == "True":
        is_success = api.registration_user(telegram_id=telegram_id,
                                           group=group,
                                           subgroup=subgroup)
    else:
        is_success = api.edit_user(telegram_id=telegram_id,
                                   group=group,
                                   subgroup=subgroup)

    if is_success:
        answer_callback(bot, callback_query, text=SUCCESS_REGISTER)
        get_menu(callback_query.message)

    else:
        bot.send_message(callback_query.message.chat.id, "⚠ Произошла ошибка при внесении данных. 😔 "
                                                         "Возможно, ты уже зарегистрирован 🙃\n"
                                                         "Для изменения данных о себе введи команду "
                                                         "/settings !")


# Пользователем выбрано расписание для отправки
@typing_action
@bot.callback_query_handler(lambda c: check_callback(c, ScheduleCallback.TEXT_SCHEDULE_CHOICE.value))
@exception_handler
def callback_message(callback_query: types.CallbackQuery):
    data = extract_data_from_callback(ScheduleCallback.TEXT_SCHEDULE_CHOICE.value, callback_query.data)
    start = data[0]
    end = data[1]
    need_delete_message = data[2]
    if need_delete_message == "True":
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    schedule_json = api.get_schedule(callback_query.message.chat.id, start, end)
    if need_delete_message == "False" and schedule_json["error"]:
        answer_callback(bot, callback_query, text=SCHEDULE_NOT_FOUND_ANYMORE, show_alert=True)

        keyboard = callback_query.message.reply_markup.keyboard
        new_keyboard = []
        for row in keyboard:
            filtered_row = list(filter(lambda button: button.callback_data != callback_query.data, row))
            if len(filtered_row) > 0:
                new_keyboard.append(filtered_row)

        bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                      message_id=callback_query.message.message_id,
                                      reply_markup=types.InlineKeyboardMarkup(keyboard=new_keyboard))
        return
    schedule_dict = schedule_json['response']
    schedule_sending(callback_query.message, schedule_dict)


@typing_action
@bot.callback_query_handler(lambda c: c.data.startswith("mailing_course"))
@exception_handler
def callback_message(callback_query: types.CallbackQuery):
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = callback_query.data.replace('mailing_course_', "")
    course = None
    if data != "all":
        course = int(data)
    bot.send_message(callback_query.message.chat.id,
                     "Введите сообщение для рассылки: ")
    bot.register_next_step_handler(callback_query.message, send_mail, course=course)


# Команды бота в списке
bot.set_my_commands([
    types.BotCommand('help', 'Помощь с работой бота'),
    types.BotCommand('settings', 'Изменить данные о себе'),
    types.BotCommand('menu', 'Вызвать меню'),
    types.BotCommand('schedule', 'Получить расписание'),
    types.BotCommand('base_schedule', 'Получить расписание на модуль'),
], scope=types.BotCommandScopeDefault())

# Модульное расписание - показывать или нет (расписание на модуль), сделать заготовку настройки

# Запуск запланированных задач в отдельном потоке
if __name__ == "__main__":
    workers.run_workers()

# Безостановочная работа бота
bot.infinity_polling(timeout=10, long_polling_timeout=5)
