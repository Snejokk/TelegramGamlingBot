import telebot
from telebot import types

bot = telebot.TeleBot("8579200627:AAH9mvT43WNnIMxmPF0XfAnVoGsQic8rVRs")

@bot.message_handler(commands=['start'])
def babushka_priekhala(message): # Назвали функцию "бабушка приехала"
    bot.send_message(message.chat.id, "Hi, im a gambler bot")
    types.InlineKeyboardMarkup(row_width=3)

bot.infinity_polling()