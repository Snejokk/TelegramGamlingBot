import telebot
from telebot import types

bot = telebot.TeleBot("8579200627:AAH9mvT43WNnIMxmPF0XfAnVoGsQic8r")

@bot.message_handler(commands=['start'])
def babushka_priekhala(message): # Назвали функцию "бабушка приехала"
    bot.send_message(message.chat.id, "Hi, im a gambler bot VRs")
    
    markup = types.InlineKeyboardMarkup() 

    btn1 = types.InlineKeyboardButton("Да", callback_data='yes')
    markup.add(btn1)
    bot.send_message(message.chat.id, "Настя крутыщка", reply_markup=markup)

bot.infinity_polling()