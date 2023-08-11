import telebot
from telebot import types

import requests
import json_parsing

bot = telebot.TeleBot('6348506696:AAGHBhAGBYF0I0iHFuzBuPYYdgEYHumg3bQ')

# -----------  Данные пользователя  ------------- #

user_data_list = [0] * 3  # Данные для идентификации пользователя, 1 - курс, 2 - направление, 3 - группа

# -----------  Тексты для сообщений бота  ------------- #

text_hello = "Давай познакомися! На каком курсе ты учишься?"


# -----------  --------------------------  ------------- #
# print(json_parsing.courses)
# print(json_parsing.groups)
# print(json_parsing.subgroups)
# print(json_parsing.programs)

# Создание кнопок выбора курса
def get_course(message):
    markup = types.InlineKeyboardMarkup()
    for i in range(len(json_parsing.courses)):
        markup.add(types.InlineKeyboardButton(json_parsing.courses[i], callback_data=json_parsing.courses[i]))

    bot.send_message(message.chat.id, text_hello, reply_markup=markup)

    @bot.callback_query_handler(get_course(message))
    def callback_message(callback):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        user_data_list[0] = callback.data
        get_program(message)


def get_program(message):
    text_get_course = "Ты выбрал " + str(user_data_list[0]) + " курс! На каком направлении ты учишься?"
    markup = types.InlineKeyboardMarkup()
    for i in range(len(json_parsing.programs)):
        markup.add(types.InlineKeyboardButton(json_parsing.programs[i], callback_data=json_parsing.programs[i]))

    bot.send_message(message.chat.id, text_get_course, reply_markup=markup)

    @bot.callback_query_handler(func=lambda callback: True)
    def callback_message(callback):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        user_data_list[1] = callback.data
        get_group(message)


def get_group(message):
    text_get_group = "Отлично, ты выбрал " + str(user_data_list[1]) + " направление! Теперь давай выберем группу!"
    markup = types.InlineKeyboardMarkup()
    for i in range(len(json_parsing.groups)):
        markup.add(types.InlineKeyboardButton(json_parsing.groups[i], callback_data=json_parsing.groups[i]))

    bot.send_message(message.chat.id, text_get_group, reply_markup=markup)

    @bot.callback_query_handler(func=lambda callback: True)
    def callback_message(callback):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        user_data_list[2] = callback.data
        print(user_data_list)


@bot.message_handler(commands=['start'])
def get_menu(message):
    user_data_list = [0] * 3
    get_course(message)


# @bot.callback_query_handler(func=lambda callback: True)
# def callback_message(callback):
#     bot.delete_message(callback.message.chat.id, callback.message.message_id)
#     user_data_list[0] = callback.data


bot.polling(none_stop=True)
