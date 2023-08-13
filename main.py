import telebot
from telebot import types

import requests
import json_parsing

bot = telebot.TeleBot('6348506696:AAGHBhAGBYF0I0iHFuzBuPYYdgEYHumg3bQ')

# -----------  Данные пользователя  ------------- #

user_data_list = [0] * 4  # Данные для идентификации пользователя, 1 - курс, 2 - направление, 3 - группа

# -----------  Тексты для сообщений бота  ------------- #



# -----------  --------------------------  ------------- #

# Создание кнопок выбора курса
def get_course(message):
    text_hello = "Давай познакомися! На каком курсе ты учишься?"
    markup = types.InlineKeyboardMarkup()
    for i in range(len(json_parsing.courses)):
        markup.add(types.InlineKeyboardButton(json_parsing.courses[i], callback_data="course_" + str(json_parsing.courses[i])))

    bot.send_message(message.chat.id, text_hello, reply_markup=markup)


# Создание кнопок выбора программы
def get_program(message):
    text_get_course = "Ты выбрал " + str(user_data_list[0]) + " курс! На каком направлении ты учишься?"
    markup = types.InlineKeyboardMarkup()
    for i in range(len(json_parsing.programs)):
        markup.add(types.InlineKeyboardButton(json_parsing.programs[i], callback_data="program_" + str(json_parsing.programs[i])))
    markup.add(types.InlineKeyboardButton("<- Назад", callback_data="back_to_course"))

    bot.send_message(message.chat.id, text_get_course, reply_markup=markup)


# Создание кнопок выбора группы
def get_group(message):
    text_get_group = "Отлично, ты выбрал " + str(user_data_list[1]) + " направление! Теперь давай выберем группу!"
    markup = types.InlineKeyboardMarkup()
    for i in range(len(json_parsing.groups)):
        markup.add(types.InlineKeyboardButton(json_parsing.groups[i], callback_data="group_" + str(json_parsing.groups[i])))
    markup.add(types.InlineKeyboardButton("<- Назад", callback_data="back_to_program"))

    bot.send_message(message.chat.id, text_get_group, reply_markup=markup)

# Создание кнопок выбора подгруппы

def get_subgroup(message):
    text_get_subgroup = str(user_data_list[2]) + " - твоя группа. Осталось определиться с подгруппой!"
    markup = types.InlineKeyboardMarkup()
    for i in range(len(json_parsing.subgroups)):
        markup.add(types.InlineKeyboardButton(json_parsing.subgroups[i], callback_data="subgroup_" + str(json_parsing.subgroups[i])))
    markup.add(types.InlineKeyboardButton("<- Назад", callback_data="back_to_group"))

    bot.send_message(message.chat.id, text_get_subgroup, reply_markup=markup)

def get_confirmation(message):
    text_confirmation = ("Отлично! Теперь давай проверим, всё ли верно:\n" +
                         f"{user_data_list[0]} - курс\n{user_data_list[1]} - направление\n"
                         f"{user_data_list[2]} - группа\n{user_data_list[3]} - подгруппа.\n\nВсе верно?")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Все верно!", callback_data="start_working"))
    markup.add(types.InlineKeyboardButton("Редактировать", callback_data="back_to_start"))
    markup.add(types.InlineKeyboardButton("<- Назад", callback_data="back_to_subgroup"))

    bot.send_message(message.chat.id, text_confirmation, reply_markup=markup)

@bot.message_handler(commands=['start'])
def get_menu(message):
    user_data_list = [0] * 4
    get_course(message)

@bot.callback_query_handler(lambda c: c.data.startswith('course_'))
def course_query_handler(callback_query: types.CallbackQuery):
    data = int(callback_query.data.replace("course_", ""))
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    user_data_list[0] = data
    get_program(callback_query.message)


@bot.callback_query_handler(lambda c: c.data.startswith('program_'))
def program_query_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.replace("program_", "")
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    user_data_list[1] = data
    get_group(callback_query.message)


@bot.callback_query_handler(lambda c: c.data.startswith('group_'))
def group_query_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.replace("group_", "")
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    user_data_list[2] = data
    get_subgroup(callback_query.message)

@bot.callback_query_handler(lambda c: c.data.startswith('subgroup_'))
def subgroup_query_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.replace("subgroup_", "")
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    user_data_list[3] = data
    get_confirmation(callback_query.message)

@bot.callback_query_handler(lambda c: c.data.startswith('back_to_'))
def program_query_handler(callback_query: types.CallbackQuery):
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    if callback_query.data == 'back_to_program':
        get_program(callback_query.message)
    elif callback_query.data == 'back_to_group':
        get_group(callback_query.message)
    elif callback_query.data == 'back_to_subgroup':
        get_subgroup(callback_query.message)
    else:
        get_course(callback_query.message)

@bot.callback_query_handler(func=lambda callback: callback.data == "start_working")
def callback_message(callback):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

#Получить файл расписание





bot.polling(none_stop=True)
