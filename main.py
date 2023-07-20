import telebot
from telebot import types
import json

bot = telebot.TeleBot('6348506696:AAGHBhAGBYF0I0iHFuzBuPYYdgEYHumg3bQ')

@bot.message_handler(commands=['start'])
def get_menu(message):
    # bot.delete_message(message.chat.id, message.message_id)
    button_course_1 = types.InlineKeyboardButton('1', url='https://google.com')
    button_course_2 = types.InlineKeyboardButton('2', url='https://google.com')
    button_course_3 = types.InlineKeyboardButton('3', url='https://google.com')
    button_course_4 = types.InlineKeyboardButton('4', url='https://google.com')

    markup = types.InlineKeyboardMarkup()
    markup.add(button_course_1)
    markup.add(button_course_2)
    markup.add(button_course_3)
    markup.add(button_course_4)

    bot.send_message(message.chat.id, 'Давай познакомися! На каком курсе ты учишься?', reply_markup=markup)
# def main(message):
#     bot.send_message(message.chat.id, 'Привет! Скоро я смогу рассылать расписание, но пока я в разработке!')


bot.polling(none_stop=True)

