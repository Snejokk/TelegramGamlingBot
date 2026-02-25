import telebot
import random

from telebot import types

bot = telebot.TeleBot("8579200627:AAH9mvT43WNnIMxmPF0XfAnVoGsQi")

luck = 0.75
money = 20
DepValueHowMany = 0

@bot.message_handler(commands=['start'])
def babushka_priekhala(message):
    markup1 = types.InlineKeyboardMarkup() 

    btn1 = types.InlineKeyboardButton("Да", callback_data='yes')
    markup1.add(btn1)

    bot.send_message(message.chat.id, "Здарова c8rVRs, все таки снова депаешь?", reply_markup=markup1)

@bot.callback_query_handler(func=lambda call: call.data == "yes")
def answer_yes(call):
    markup2 = types.InlineKeyboardMarkup() 

    btn2 = types.InlineKeyboardButton("По крупному", callback_data='crupnyi')
    markup2.add(btn2)

    btn3 = types.InlineKeyboardButton("По мелочи", callback_data='melochy') 
    markup2.add(btn3)

    bot.send_message(call.message.chat.id, "Ну понятно, по крупному или так по мелочи?", reply_markup=markup2)

@bot.callback_query_handler(func=lambda call: call.data == "melochy")
def answer_crupnyi(call):
    bot.send_message(call.message.chat.id, "У нас так не принято")

@bot.callback_query_handler(func=lambda call: call.data == "crupnyi")
def answer_crupnyi(call):
    
    markup4 = types.InlineKeyboardMarkup()  

    btn4= types.InlineKeyboardButton("Крутим!", callback_data='KRUTIM!') 
    markup4.add(btn4)

    bot.send_message(call.message.chat.id, "Крути, раз хочеться", reply_markup=markup4)
    
@bot.callback_query_handler(func=lambda call: call.data == "KRUTIM!")
def spin(call):
    global money, luck, DepValueHowMany # 3. Добавил money и DepValueHowMany в глобальные
    
    if money > 0:
        win = random.random() < luck
        luck += -0.075 if win else 0.05
        
        DepValueHowMany += 1
        
        if win:
            money += 1
        else:
            money += -1
            
        res = "+" if win else "-"
        # 4. Исправил massage на call.message.chat.id
        bot.send_message(call.message.chat.id, f"{res}\nБаланс: {money}")
    else:
        bot.send_message(call.message.chat.id, "Ты все проебал")

bot.infinity_polling()  