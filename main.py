import random
import datetime
import telebot
from telebot import types

import api
import scheduler

# ---------------------------------  Настройка бота  ----------------------------------- #

bot = telebot.TeleBot('6348506696:AAGHBhAGBYF0I0iHFuzBuPYYdgEYHumg3bQ')
bot.can_join_groups = False        # Запрет на приглашения в группы (ему пофиг)


# ---------------------------------  Данные  ----------------------------------- #

days_of_week = ['Понедельник',
                'Вторник',
                'Среда',
                'Четверг',
                'Пятница',
                'Суббота',
                'Воскресенье']

type_of_lessons = {
    'LECTURE' : 'лекция 😴',
    'SEMINAR' : 'семинар 📗',
    'COMMON_MINOR' : 'Майнор Ⓜ',
    'ENGLISH' : 'английский 🆎',
}

type_of_program = {
    'МБ' : 'Международный бакалавриат по бизнесу и экономике',
    'РИС' : 'Разработка информационных систем для бизнеса',
    'И' : 'История',
    'ИЯ' : 'Лингвистика',
    'Ю' : 'Юриспруденция',
    'УБ' : 'Управление бизнесом',
    'Э' : 'Экономика',
    'ПИ' : 'Программная инженерия',
    'БИ' : 'Бизнес-информатика'
}

emojies_for_course = ['📒', '📓', '📔', '📕', '📗',  '📘', '📙']
emojies_for_programs = ['💶', '💵', '💷', '💸',  '💪', '💻', '💼', '📊', '🥇', '🤡', '☠', '💩', '♿']
emojies_for_groups = ['⚪', '🔴', '🟡', '🟢', '🟣',  '🟤', '🔵', '⚫']
emojies_for_subgroups = ['🌁', '🌃', '🌄', '🌅', '🌆',  '🌇', '🌉']

# ---------------------------------  Функции  ----------------------------------- #

# Рандомный номер эмодзи для быстрого получения из списка
def rand_emj(count):
    return random.randint(0, count - 1)

# Создание кнопок выбора курса
def get_course(message, is_new_user):
    if is_new_user == "True":
        text_hello = "Давай познакомися! 👋 На каком курсе ты учишься?"
    else:
        text_hello = "Немного изменим данные. ✏ На каком курсе ты учишься?"
    courses = api.get_courses()
    markup = types.InlineKeyboardMarkup()
    for i in range(len(courses)):
        emoji_for_button = f"{emojies_for_course[rand_emj(len(emojies_for_course))]} {courses[i]}"
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
    for i in range(len(programs)):
        if programs[i] in type_of_program.keys():
            emoji_for_button = f"{emojies_for_programs[rand_emj(len(emojies_for_programs))]} {type_of_program[programs[i]]}"
        else:
            emoji_for_button = f"{emojies_for_programs[rand_emj(len(emojies_for_programs))]} {programs[i]}"
        markup.add(types.InlineKeyboardButton(emoji_for_button,
                                              callback_data=f"program_{programs[i]}"
                                                            f"^{number_course}"
                                                            f"^{is_new_user}"))
    markup.add(types.InlineKeyboardButton("🔙 Назад",
                                          callback_data=f"back_to_start{is_new_user}"))

    bot.send_message(message.chat.id,
                     text_get_course,
                     reply_markup=markup)


# Создание кнопок выбора группы
def get_group(message, data):
    number_program, number_course, is_new_user = data.split('^')
    if number_program in type_of_program.keys():
        text_get_group = f"Отлично, ты выбрал: \n{type_of_program[number_program]} 😎\nТеперь давай выберем группу!"
    else:
        text_get_group = f"Отлично, ты выбрал {number_program} направление! 😎\nТеперь давай выберем группу!"


    groups = api.get_groups(number_course,
                            number_program)

    markup = types.InlineKeyboardMarkup()
    for i in range(len(groups)):
        emoji_for_button = f"{emojies_for_groups[rand_emj(len(emojies_for_groups))]} {groups[i]}"
        markup.add(types.InlineKeyboardButton(emoji_for_button,
                                              callback_data=f"group_{groups[i]}"
                                                            f"^{number_program}"
                                                            f"^{number_course}"
                                                            f"^{is_new_user}"))
    markup.add(types.InlineKeyboardButton("🔙 Назад",
                                          callback_data=f"back_to_program{number_course}"
                                                        f"^{is_new_user}"))

    bot.send_message(message.chat.id,
                     text_get_group,
                     reply_markup=markup)


# Создание кнопок выбора подгруппы
def get_subgroup(message, data):
    number_group, number_program, number_course, is_new_user = data.split('^')

    text_get_subgroup = f"{number_group} - твоя группа. Осталось определиться с подгруппой!"

    subgroups = api.get_subgroups(number_course,
                                  number_program,
                                  number_group)
    markup = types.InlineKeyboardMarkup()
    for i in range(len(subgroups)):
        emoji_for_button = f"{emojies_for_subgroups[rand_emj(len(emojies_for_subgroups))]} {subgroups[i]}"
        markup.add(types.InlineKeyboardButton(emoji_for_button,
                                              callback_data=f"subgroup_{subgroups[i]}"
                                                            f"^{number_group}"
                                                            f"^{number_program}"
                                                            f"^{number_course}"
                                                            f"^{is_new_user}"))
    markup.add(types.InlineKeyboardButton("🚫 Нет подгруппы",
                                              callback_data=f"subgroup_None"
                                                            f"^{number_group}"
                                                            f"^{number_program}"
                                                            f"^{number_course}"
                                                            f"^{is_new_user}"))
    markup.add(types.InlineKeyboardButton("🔙 Назад",
                                          callback_data=f"back_to_group{number_program}"
                                                        f"^{number_course}"
                                                        f"^{is_new_user}"))

    bot.send_message(message.chat.id,
                     text_get_subgroup,
                     reply_markup=markup)


# Создание кнопок для подтверждения выбора
def get_confirmation(message, data):
    number_subgroup, number_group, number_program, number_course, is_new_user = data.split('^')

    '''Заводим новую переменную номера группы, чтобы в сообщение выводилось полное название направления'''
    if number_program in type_of_program.keys():
        number_program_for_message = type_of_program[number_program]
    else:
        number_program_for_message = number_program

    '''Два различных варианта вывода информации - с подгруппой и без нее'''
    if number_subgroup == "None":
        text_confirmation = ("Отлично! ✅ Теперь давай проверим, всё ли верно:\n" +
                             f"{number_course} - курс\n"
                             f"{number_program_for_message},\n"
                             f"{number_group} - группа"
                             f"\n\nВсе верно?")
    else:
        text_confirmation = ("Отлично! ✅ Теперь давай проверим, всё ли верно:\n" +
                             f"{number_course} - курс\n"
                             f"{number_program_for_message},\n"
                             f"{number_group} - группа\n"
                             f"{number_subgroup} - подгруппа.\n\nВсе верно?")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Все верно! 🎉🎊",
                                          callback_data=f"start_working{number_course}"
                                                        f"^{number_program}"
                                                        f"^{number_group}"
                                                        f"^{number_subgroup}"
                                                        f"^{message.chat.id}"
                                                        f"^{is_new_user}"))
    markup.add(types.InlineKeyboardButton("Редактировать ✏",
                                          callback_data=f"back_to_start"
                                                        f"^{is_new_user}"))
    markup.add(types.InlineKeyboardButton("🔙 Назад",
                                          callback_data=f"back_to_subgroup{number_group}"
                                                        f"^{number_program}"
                                                        f"^{number_course}"
                                                        f"^{is_new_user}"))

    bot.send_message(message.chat.id,
                     text_confirmation,
                     reply_markup=markup)


def get_menu(message):
    text_schedule = ("<b>Команды для работы:</b>\n\n"
                 "🔹 /settings - <i>Изменение информации о себе</i>\n\n"
                 "🔹 /menu - <i>Получить меню для работы</i>\n\n"
                 "🔹 /help - <i>Вывод помощи</i>\n\n"
                     "❗ При удалении этого сообщения кнопки выбора расписания пропадут. "
                     "Чтобы их вернуть, введи /menu еще раз! 🙂")

    keyboard_markup_up = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup_down = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_schedule_calendar_button = types.KeyboardButton("Добавить обновляемый календарь")
    get_schedule_text_button = types.KeyboardButton("Получить текстовое расписание")
    # get_deadlines_button = types.KeyboardButton("Проверить дедлайны")
    keyboard_markup_up.row(add_schedule_calendar_button)
    keyboard_markup_up.row(get_schedule_text_button)
    keyboard_markup_up.row_width = 4

    bot.send_message(message.chat.id,
                     text_schedule,
                     reply_markup=keyboard_markup_up, parse_mode='HTML')



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

def get_text_schedule(message):
    bot.delete_message(message.chat.id, message.message_id)
    schedule_json = api.get_schedule(message.chat.id)

    if schedule_json['error'] is True:
        bot.send_message(message.chat.id, 'Для тебя почему-то нет расписания 🤷\nНастрой группу заново '
                                                   'командой /settings!')
    else:
        schedule_dict = schedule_json['response']
        text_message = "🔵 Выбери неделю, за которую хочешь видеть расписание:"
        markup = types.InlineKeyboardMarkup()
        for week in schedule_dict:
            markup.add(types.InlineKeyboardButton(f"Неделя {week['weekNumber']}, "
                                                  f"{week['weekStart']} - {week['weekEnd']}",
                                                  callback_data=f"number_of_week_schedule{week['weekNumber']}"))
        bot.send_message(message.chat.id,
                         text_message,
                         reply_markup=markup)

# ---------------------------------  Обработка команд  ----------------------------------- #


# Обработка команды /start и /registration
@bot.message_handler(commands=['start', 'старт', 'поехали', 'registration', 'регистрация'])
@bot.message_handler(func= lambda message: message.text == ('start' or 'старт' or 'поехали'
                                           or 'registration' or 'регистрация'))
def get_registration(message):
    bot.delete_message(message.chat.id, message.message_id)
    get_course(message, True)


# Обработка команды /help
@bot.message_handler(commands=['help', 'помощь', 'помоги'])
@bot.message_handler(func= lambda message: message.text == ('help' or 'помощь' or 'помоги'))
def get_help(message):
    bot.delete_message(message.chat.id, message.message_id)
    text_help = ("<b>Вот, что я могу:</b>\n\n"
                 "🔹 /start - <i>Начало работы. Производится выбор курса, направления, группы и подгруппы</i>\n\n"
                 "🔹 /settings - <i>Изменение информации о себе</i>\n\n"
                 "🔹 /menu - <i>Получить меню для работы</i>\n\n"
                 "🔹 /help - <i>Вывод помощи</i>")
    bot.send_message(message.chat.id, text_help, parse_mode='HTML')


# Обработка команды /menu
@bot.message_handler(commands=['menu', 'меню'])
@bot.message_handler(func= lambda message: message.text == ('menu' or 'меню'))
def start_working(message):
    bot.delete_message(message.chat.id, message.message_id)
    get_menu(message)


# Леха, удали это потом, это наш стажёр так шутит
# Обработка команды /gay
@bot.message_handler(commands=['gay', 'гей'])
@bot.message_handler(func= lambda message: message.text == ('gay' or 'гей'))
def who_is_gay(message):
    bot.delete_message(message.chat.id, message.message_id)
    if random.randint(0, 9) < 5:
        bot.send_message(message.chat.id, "Денис Малинин гей 👬")
    else:
        bot.send_message(message.chat.id, "Данил Кунакбаев гей 👬")


# Обработка команды /settings
@bot.message_handler(commands=['settings', 'настройки'])
@bot.message_handler(func= lambda message: message.text == ('settings' or 'настройки'))
def get_settings(message):
    bot.delete_message(message.chat.id, message.message_id)
    get_course(message, False)



@bot.message_handler(func= lambda message: message.text == "Добавить обновляемый календарь")
def callback_message(message):
    get_schedule(message)

@bot.message_handler(func= lambda message: message.text == "Получить текстовое расписание")
def callback_message(message):
    get_text_schedule(message)

# @bot.message_handler(func= lambda message: message.text == "Получить расписание")
# def callback_message(message):
#     get_schedule(message)


# @bot.message_handler(func= lambda message: message.text == "Проверить дедлайны")
# def callback_message(message):
#     bot.send_message(message.chat.id, "Скоро будет!")


# ---------------------------------  Обработка событий  ----------------------------------- #


# Обработка события нажатия на кнопку выбора курса
@bot.callback_query_handler(lambda c: c.data.startswith('course_'))
def course_query_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.replace("course_", "")
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    get_program(callback_query.message, data)


# Обработка события нажатия на кнопку выбора программы
@bot.callback_query_handler(lambda c: c.data.startswith('program_'))
def program_query_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.replace("program_", "")
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    get_group(callback_query.message, data)


# Обработка события нажатия на кнопку выбора группы
@bot.callback_query_handler(lambda c: c.data.startswith('group_'))
def group_query_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.replace("group_", "")
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    get_subgroup(callback_query.message, data)


# Обработка события нажатия на кнопку выбора подгруппы
@bot.callback_query_handler(lambda c: c.data.startswith('subgroup_'))
def subgroup_query_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.replace("subgroup_", "")
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    get_confirmation(callback_query.message, data)


# Обработка события возврата на предыдущий выбор

@bot.callback_query_handler(lambda c: c.data.startswith('back_to_'))
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
        get_course(callback_query.message, data)



# Обработка события нажатия на кнопку подтверждения данных
@bot.callback_query_handler(lambda c: c.data.startswith("start_working"))
def callback_message(callback_query: types.CallbackQuery):
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = callback_query.data.replace('start_working', "")
    list_data = data.split("^")
    is_new_user = list_data[len(list_data) - 1]
    if is_new_user == "True":
        is_error = api.registration_user(data)
    else:
        is_error = api.edit_user(data)

    if not is_error:
        get_menu(callback_query.message)

    else:
        bot.send_message(callback_query.message.chat.id, "⚠ Произошла ошибка при внесении данных. 😔 "
                                                         "Возможно, ты уже зарегистрирован 🙃\n"
                                                         "Для изменения данных о себе введи команду "
                                                         "/settings !")


# # Отправить расписание текстом
# @bot.callback_query_handler(func=lambda callback: callback.data == "get_text_schedule")
# def callback_message(callback):
#     bot.delete_message(callback.message.chat.id, callback.message.message_id)
#     schedule_json = api.get_schedule(callback.message.chat.id)
#
#     if schedule_json['error'] is True:
#         bot.send_message(callback.message.chat.id, 'Для тебя почему-то нет расписания :(\nНастрой группу заново '
#                                                    'командой /settings!')
#     else:
#         schedule_dict = schedule_json['response']
#         text_message = "Выбери неделю, за которую хочешь видеть расписание:"
#         markup = types.InlineKeyboardMarkup()
#         for week in schedule_dict:
#             markup.add(types.InlineKeyboardButton(f"Неделя {week['weekNumber']}, "
#                                                   f"{week['weekStart']} - {week['weekEnd']}",
#                                                   callback_data=f"number_of_week_schedule{week['weekNumber']}"))
#         bot.send_message(callback.message.chat.id,
#                          text_message,
#                          reply_markup=markup)


# Добавить автообновляемый календарь
@bot.callback_query_handler(func=lambda callback: callback.data == "add_calendar")
def callback_message(callback):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    schedule = open('./schedule.ics', 'r', encoding='utf-8')
    bot.send_message(callback.message.chat.id, "Инструкция по установке:\n\n"
                                               "1. Скачай файл ниже;\n"
                                               "2. Запусти его;\n"
                                               "3. Прими изменения для используемого тобой календаря.")
    bot.send_document(callback.message.chat.id, schedule)



# Пользователем выбрано расписание для отправки
@bot.callback_query_handler(lambda c: c.data.startswith("number_of_week_schedule"))
def callback_message(callback_query: types.CallbackQuery):
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = callback_query.data.replace('number_of_week_schedule', "")
    data = int(data)
    schedule_json = api.get_schedule(callback_query.message.chat.id)
    schedule_dict = schedule_json['response']
    for week in schedule_dict:
        if week['weekNumber'] == data:
            lessons = week['lessons']
            if lessons != []:
                for day in lessons:
                    keys = day.keys()
                    for key in keys:

                        '''Определение дня недели'''
                        date_string = key
                        day_, month, year = date_string.split('.')
                        day_ = int(day_)
                        month = int(month)
                        year = int(year)
                        date = datetime.datetime(year, month, day_)
                        day_of_the_week = days_of_week[date.isoweekday() - 1]
                        '''Конец определения дня недели'''

                        text_for_message = f"<u><b>{day_of_the_week}, {date_string}</b></u>\n\n"

                        daily_schedule_list = day[key]
                        for lesson in daily_schedule_list:
                            if lesson['lessonType'] == 'COMMON_MINOR':
                                text_for_message += type_of_lessons[lesson['lessonType']]
                            else:
                                text_for_message += (f"{lesson['subject']} - "
                                                     f"<u>{type_of_lessons[lesson['lessonType']]}</u> \n")

                                text_for_message += (f"<b>{lesson['startTime']} - {lesson['endTime']}</b> ")

                                if lesson['isOnline']:
                                    if lesson['link'] == None:
                                        text_for_message += (f"Дистанционная пара, ссылка отсутствует \n")
                                    else:
                                        text_for_message += (f"Дистанционная пара, ссылка:\n"
                                                             f"{lesson['link']}")
                                else:
                                    text_for_message += (f"Корпус {lesson['building']}, аудитория {lesson['office']} \n")

                                text_for_message += (f"Преподаватель - <i>{lesson['lecturer']}</i> \n\n")
                        bot.send_message(callback_query.message.chat.id, text_for_message, parse_mode='HTML')

# Команды бота в списке

bot.set_my_commands([
    types.BotCommand('help', 'Помощь с работой бота'),
    types.BotCommand('settings', 'Изменить данные о себе'),
    types.BotCommand('menu', 'Вызвать меню'),
], scope=types.BotCommandScopeDefault())


# Модульное расписание - показывать или нет (расписание на модуль), сделать заготовку настройки
# Придумать, как будет выводиться расписание

# Запуск запланированных задач в отдельном потоке
scheduler.run()

# Безостановочная работа бота

bot.polling(none_stop=True)
