import telebot
from telebot import types

import requests


bot = telebot.TeleBot('6348506696:AAGHBhAGBYF0I0iHFuzBuPYYdgEYHumg3bQ')

# -----------  Тексты для сообщений бота  ------------- #

# Выбор курса:
first = '1'
second = '2'
third = '3'
four = '4'
five = '5'

# Выбор направления:
superheroes = 'РИС'
program_engineers = 'ПИ'
business_informatics = 'БИ'
international_bachelor = 'МБ'
history = 'И'
jurists = 'Ю'
economics = 'Э'
languages = 'ИЯ'
business_management = 'УБ'

# Номер группы:


# -----------  Данные пользователя  ------------- #

user_data_list = []   # Данные для идентификации пользователя, 1 - курс, 2 - направление, 3 - группа

# -----------  --------------------------  ------------- #

@bot.message_handler(commands=['start'])
def get_menu(message):
    # bot.delete_message(message.chat.id, message.message_id)
    button_course_1 = types.InlineKeyboardButton(first, callback_data=first)
    button_course_2 = types.InlineKeyboardButton(second, callback_data=second)
    button_course_3 = types.InlineKeyboardButton(third, callback_data=third)
    button_course_4 = types.InlineKeyboardButton(four, callback_data=four)
    button_course_5 = types.InlineKeyboardButton(five, callback_data=five)

    markup = types.InlineKeyboardMarkup()
    markup.add(button_course_1)
    markup.add(button_course_2)
    markup.add(button_course_3)
    markup.add(button_course_4)
    markup.add(button_course_5)

    bot.send_message(message.chat.id, 'Давай познакомися! На каком курсе ты учишься?', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
        if callback.data == first:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)

        elif callback.data == second:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)

        elif callback.data == third:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)

        elif callback.data == four:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)

        elif callback.data == five:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)



bot.polling(none_stop=True)

