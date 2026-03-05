import telebot
import random
import time 
from telebot import types

bot = telebot.TeleBot("8579200627:AAGnudJwoMdIxwp_xniN42lNRNnALCXPGcM")

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
    bot.edit_message_text("Ну понятно, по крупному или так по мелочи?", call.message.chat.id, call.message.message_id, reply_markup=markup2)

@bot.callback_query_handler(func=lambda call: call.data == "melochy")
def answer_melochy(call):
    bot.answer_callback_query(call.id, "У нас так не принято")

@bot.callback_query_handler(func=lambda call: call.data == "crupnyi")
def answer_crupnyi(call):
    markup4 = types.InlineKeyboardMarkup()  
    btn4= types.InlineKeyboardButton("Крутим!", callback_data='KRUTIM!') 
    markup4.add(btn4)
    bot.edit_message_text("Крути, раз хочеться", call.message.chat.id, call.message.message_id, reply_markup=markup4)
    
@bot.callback_query_handler(func=lambda call: call.data == "KRUTIM!")
def spin(call):
    global money, luck, DepValueHowMany
    
    if money <= 0:
        bot.edit_message_text("Ты все проебал", call.message.chat.id, call.message.message_id)
        return

    W = 24 
    StartPossition = 0.0
    StartSpeed = random.uniform(0.10, 0.20)
    LeftWinzone, rightWinzone = random.randint(5, 10), random.randint(14, 20)
    
    msg = bot.send_message(call.message.chat.id, "🎰 Начинаем...")


    for i in range(15):
        StartPossition = (StartPossition + StartSpeed) % 1.0
        StartSpeed *= 0.90
        Possition = int(StartPossition * W)
        
        bar = ["█" if LeftWinzone <= j < rightWinzone else "—" for j in range(W)]
        bar[min(Possition, W-1)] = "◆"
        
        # Формируем текст кадра
        frame = f"<code>[{''.join(bar)}]\n"
        frame += f"0.0{' ' * (W-5)}1.0\n"
        frame += f"{' ' * (Possition+1)}▲ {StartPossition:.2f}</code>\n"
        frame += f"\nКрутим{'.' * (i % 4 + 1)}"
        
        try:
            bot.edit_message_text(frame, call.message.chat.id, msg.message_id, parse_mode='HTML')
        except: pass
        time.sleep(0.12)


    Possition = int(StartPossition * W)
    win = LeftWinzone <= Possition < rightWinzone
    

    luck += -0.075 if win else 0.05
    DepValueHowMany += 1
    money += 1 if win else -1
    
    res_symbol = "🎉 ПОБЕДА!" if win else "💀 МИМО..."
    
    # Финальный кадр
    bar = ["█" if LeftWinzone <= j < rightWinzone else "—" for j in range(W)]
    bar[min(Possition, W-1)] = "◆"
    final_text = f"<code>[{''.join(bar)}]\n"
    final_text += f"{' ' * (Possition+1)}▲ {StartPossition:.2f}</code>\n\n"
    final_text += f"{res_symbol}\nБаланс: {money}"
    
    bot.edit_message_text(final_text, call.message.chat.id, msg.message_id, parse_mode='HTML')
    

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Крутить еще!", callback_data='KRUTIM!'))
    bot.send_message(call.message.chat.id, "Ещё разок?", reply_markup=markup)

print("работаем")

bot.infinity_polling()