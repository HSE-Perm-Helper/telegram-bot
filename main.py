import random

import telebot
from telebot import types

import api
import scheduler

# ---------------------------------  Настройка бота  ----------------------------------- #

bot = telebot.TeleBot('6348506696:AAGHBhAGBYF0I0iHFuzBuPYYdgEYHumg3bQ')
bot.can_join_groups = False        # Запрет на приглашения в группы (ему пофиг)


# ---------------------------------  Функции  ----------------------------------- #


# Создание кнопок выбора курса
def get_course(message, is_new_user):
    text_hello = "Давай познакомися! На каком курсе ты учишься?"
    courses = api.get_courses()
    markup = types.InlineKeyboardMarkup()
    for i in range(len(courses)):
        markup.add(types.InlineKeyboardButton(courses[i],
                                              callback_data=f"course_{courses[i]}"
                                                            f"^{is_new_user}"))

    bot.send_message(message.chat.id,
                     text_hello,
                     reply_markup=markup)


# Создание кнопок выбора программы
def get_program(message, data):
    number_course, is_new_user = data.split('^')
    number_course = int(number_course)
    text_get_course = f"Ты выбрал {number_course} курс! На каком направлении ты учишься?"

    programs = api.get_programs(number_course)

    markup = types.InlineKeyboardMarkup()
    for i in range(len(programs)):
        markup.add(types.InlineKeyboardButton(programs[i],
                                              callback_data=f"program_{programs[i]}"
                                                            f"^{number_course}"
                                                            f"^{is_new_user}"))
    markup.add(types.InlineKeyboardButton("<- Назад",
                                          callback_data=f"back_to_start{is_new_user}"))

    bot.send_message(message.chat.id,
                     text_get_course,
                     reply_markup=markup)


# Создание кнопок выбора группы
def get_group(message, data):
    number_program, number_course, is_new_user = data.split('^')

    text_get_group = f"Отлично, ты выбрал {number_program} направление! Теперь давай выберем группу!"

    groups = api.get_groups(number_course,
                            number_program)

    markup = types.InlineKeyboardMarkup()
    for i in range(len(groups)):
        markup.add(types.InlineKeyboardButton(groups[i],
                                              callback_data=f"group_{groups[i]}"
                                                            f"^{number_program}"
                                                            f"^{number_course}"
                                                            f"^{is_new_user}"))
    markup.add(types.InlineKeyboardButton("<- Назад",
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
        markup.add(types.InlineKeyboardButton(subgroups[i],
                                              callback_data=f"subgroup_{subgroups[i]}"
                                                            f"^{number_group}"
                                                            f"^{number_program}"
                                                            f"^{number_course}"
                                                            f"^{is_new_user}"))
    markup.add(types.InlineKeyboardButton("Нет подгруппы",
                                              callback_data=f"subgroup_None"
                                                            f"^{number_group}"
                                                            f"^{number_program}"
                                                            f"^{number_course}"
                                                            f"^{is_new_user}"))
    markup.add(types.InlineKeyboardButton("<- Назад",
                                          callback_data=f"back_to_group{number_program}"
                                                        f"^{number_course}"
                                                        f"^{is_new_user}"))

    bot.send_message(message.chat.id,
                     text_get_subgroup,
                     reply_markup=markup)


# Создание кнопок для подтверждения выбора
def get_confirmation(message, data):
    number_subgroup, number_group, number_program, number_course, is_new_user = data.split('^')
    if number_subgroup == "None":
        text_confirmation = ("Отлично! Теперь давай проверим, всё ли верно:\n" +
                             f"{number_course} - курс\n"
                             f"{number_program} - направление\n"
                             f"{number_group} - группа"
                             f"\n\nВсе верно?")
    else:
        text_confirmation = ("Отлично! Теперь давай проверим, всё ли верно:\n" +
                             f"{number_course} - курс\n"
                             f"{number_program} - направление\n"
                             f"{number_group} - группа\n"
                             f"{number_subgroup} - подгруппа.\n\nВсе верно?")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Все верно!",
                                          callback_data=f"start_working{number_course}"
                                                        f"^{number_program}"
                                                        f"^{number_group}"
                                                        f"^{number_subgroup}"
                                                        f"^{message.chat.id}"
                                                        f"^{is_new_user}"))
    markup.add(types.InlineKeyboardButton("Редактировать",
                                          callback_data=f"back_to_start"
                                                        f"^{is_new_user}"))
    markup.add(types.InlineKeyboardButton("<- Назад",
                                          callback_data=f"back_to_subgroup{number_group}"
                                                        f"^{number_program}"
                                                        f"^{number_course}"
                                                        f"^{is_new_user}"))

    bot.send_message(message.chat.id,
                     text_confirmation,
                     reply_markup=markup)


def get_menu(message):
    text_schedule = ("Вот, что я могу:\n"
                 "/start - Начало работы. Производится выбор курса, направления, группы и подгруппы\n"
                 "/registration - Начало работы. Производится выбор курса, направления, группы и подгруппы\n"
                 "/help - Вывод помощи")

    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    get_schedule_button = types.KeyboardButton("Получить расписание")
    get_deadlines_button = types.KeyboardButton("Проверить дедлайны")
    keyboard_markup.row(get_deadlines_button, get_schedule_button)
    keyboard_markup.row_width = 5

    bot.send_message(message.chat.id,
                     text_schedule,
                     reply_markup=keyboard_markup)



def get_file(message):
    text_get_schedule = "Выбери способ получения расписания:"

    markup = types.InlineKeyboardMarkup()
    # markup.add(types.InlineKeyboardButton("Добавить автообновляемый календарь",
    #                                       url="webcal://https://hse-schedule-bot.xenforo-studio.ru/api/files/user_files/db625264-0a6c-4b25-b074-4f2f290e76fe/schedule.ics"))
    markup.add(types.InlineKeyboardButton("Добавить автообновляемый календарь",
                                          callback_data="add_calendar"))
    markup.add(types.InlineKeyboardButton("Получить расписание файлом",
                                          callback_data="get_file"))
    markup.add(types.InlineKeyboardButton("Отправлять расписание текстом",
                                          callback_data="get_text_schedule"))

    bot.send_message(message.chat.id,
                     text_get_schedule,
                     reply_markup=markup)

# ---------------------------------  Обработка команд  ----------------------------------- #


# Обработка команды /start и /registration
@bot.message_handler(commands=['start', 'старт', 'поехали', 'registration', 'регистрация'])
@bot.message_handler(func= lambda message: message.text == ('start' or 'старт' or 'поехали'
                                           or 'registration' or 'регистрация'))
def get_registration(message):
    get_course(message, True)


# Обработка команды /help
@bot.message_handler(commands=['help', 'помощь', 'помоги'])
@bot.message_handler(func= lambda message: message.text == ('help' or 'помощь' or 'помоги'))
def get_help(message):
    text_help = ("Вот, что я могу:\n"
                 "/start - Начало работы. Производится выбор курса, направления, группы и подгруппы\n"
                 "/registration - Начало работы. Производится выбор курса, направления, группы и подгруппы\n"
                 "/help - Вывод помощи")
    bot.send_message(message.chat.id, text_help)


# Обработка команды /menu
@bot.message_handler(commands=['menu', 'меню'])
@bot.message_handler(func= lambda message: message.text == ('menu' or 'меню'))
def start_working(message):
    get_menu(message)


# Леха, удали это потом, это наш стажёр так шутит
# Обработка команды /gay
@bot.message_handler(commands=['gay', 'гей'])
@bot.message_handler(func= lambda message: message.text == ('gay' or 'гей'))
def who_is_gay(message):
    if random.randint(0, 9) < 5:
        bot.send_message(message.chat.id, "Денис Малинин гей")
    else:
        bot.send_message(message.chat.id, "Данил Кунакбаев гей")


# Обработка команды /settings
@bot.message_handler(commands=['settings', 'настройки'])
@bot.message_handler(func= lambda message: message.text == ('settings' or 'настройки'))
def get_settings(message):
    get_course(message, False)



@bot.message_handler(func= lambda message: message.text == "Получить расписание")
def callback_message(message):
    get_file(message)



@bot.message_handler(func= lambda message: message.text == "Проверить дедлайны")
def callback_message(message):
    bot.send_message(message.chat.id, "Скоро будет!")

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
        bot.send_message(callback_query.message.chat.id, "Произошла ошибка при внесении данных. Повторите попытку")


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


# Команды бота в списке

bot.set_my_commands([
    types.BotCommand('start', 'Начало работы бота'),
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
