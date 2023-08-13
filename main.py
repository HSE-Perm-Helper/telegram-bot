import telebot
from telebot import types

import requests
import json_parsing

bot = telebot.TeleBot('6348506696:AAGHBhAGBYF0I0iHFuzBuPYYdgEYHumg3bQ')

# -----------  Данные пользователя  ------------- #

user_data_list = [0] * 3  # Данные для идентификации пользователя, 1 - курс, 2 - направление, 3 - группа

# -----------  Тексты для сообщений бота  ------------- #



# -----------  --------------------------  ------------- #

# Создание кнопок выбора программы
def get_course(message):
    text_hello = "Давай познакомися! На каком курсе ты учишься?"
    markup = types.InlineKeyboardMarkup()
    for i in range(len(json_parsing.courses)):
        markup.add(types.InlineKeyboardButton(json_parsing.courses[i], callback_data="course_" + str(json_parsing.courses[i])))

    bot.send_message(message.chat.id, text_hello, reply_markup=markup)

    @bot.callback_query_handler(lambda c: c.data.startswith('course_'))
    def course_query_handler(callback_query: types.CallbackQuery):
        data = int(callback_query.data.replace("course_", ""))
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        user_data_list[0] = data
        get_program(message)

# Создание кнопок выбора программы
def get_program(message):
    text_get_course = "Ты выбрал " + str(user_data_list[0]) + " курс! На каком направлении ты учишься?"
    markup = types.InlineKeyboardMarkup()
    for i in range(len(json_parsing.programs)):
        markup.add(types.InlineKeyboardButton(json_parsing.programs[i], callback_data="program_" + str(json_parsing.programs[i])))

    bot.send_message(message.chat.id, text_get_course, reply_markup=markup)

    @bot.callback_query_handler(lambda c: c.data.startswith('program_'))
    def program_query_handler(callback_query: types.CallbackQuery):
        data = callback_query.data.replace("program_", "")
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        user_data_list[1] = data
        get_group(message)

# Создание кнопок выбора группы
def get_group(message):
    text_get_group = "Отлично, ты выбрал " + str(user_data_list[1]) + " направление! Теперь давай выберем группу!"
    markup = types.InlineKeyboardMarkup()
    for i in range(len(json_parsing.groups)):
        markup.add(types.InlineKeyboardButton(json_parsing.groups[i], callback_data="group_" + str(json_parsing.groups[i])))

    bot.send_message(message.chat.id, text_get_group, reply_markup=markup)

    @bot.callback_query_handler(lambda c: c.data.startswith('group_'))
    def program_query_handler(callback_query: types.CallbackQuery):
        data = callback_query.data.replace("group_", "")
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        user_data_list[2] = data
        print(user_data_list)
        bot.send_message(message.chat.id, str(user_data_list))

@bot.message_handler(commands=['start'])
def get_menu(message):
    user_data_list = [0] * 3
    get_course(message)

#Получить файл расписание

# @bot.callback_query_handler(func=lambda callback: callback.data == "course")
# def callback_message(callback):
#     bot.delete_message(callback.message.chat.id, callback.message.message_id)



bot.polling(none_stop=True)
