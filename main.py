import telebot

bot = telebot.TeleBot('6348506696:AAGHBhAGBYF0I0iHFuzBuPYYdgEYHumg3bQ')

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Я бот шедуля!')

bot.polling(none_stop=True)