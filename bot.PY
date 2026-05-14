import telebot
import random
import time 
from telebot import types
import sqlite3


bot = telebot.TeleBot("...") # токен

conn = sqlite3.connect('TgCurency.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        money INTEGER,
        luck REAL
    )
''')
conn.commit()

# Функция: получить данные юзера
def get_user(user_id):
    cursor.execute('SELECT money, luck FROM users WHERE user_id = ?', (user_id,))
    return cursor.fetchone()

# Функция: сохранить/обновить данные юзера
def update_user(user_id, money, luck):
    cursor.execute('INSERT OR REPLACE INTO users (user_id, money, luck) VALUES (?, ?, ?)', (user_id, money, luck))
    conn.commit()
# -----------------------------

@bot.message_handler(commands=['start'])
def babushka_priekhala(message):
    user_id = message.from_user.id
    
    if get_user(user_id) is None:
        update_user(user_id, 20, 0.75)

    markup1 = types.InlineKeyboardMarkup() 
    btn1 = types.InlineKeyboardButton("Да", callback_data='yes')
    markup1.add(btn1)
    
    # Это единственное новое сообщение, с которого начинается диалог
    bot.send_message(message.chat.id, "Здарова c8rVRs, все таки снова депаешь?", reply_markup=markup1)

@bot.callback_query_handler(func=lambda call: call.data == "yes")
def answer_yes(call):
    markup2 = types.InlineKeyboardMarkup() 
    btn2 = types.InlineKeyboardButton("По крупному", callback_data='crupnyi')
    btn3 = types.InlineKeyboardButton("По мелочи", callback_data='melochy') 
    markup2.add(btn2, btn3)
    
    # Изменяем текущее сообщение
    bot.edit_message_text("Ну понятно, по крупному или так по мелочи?", call.message.chat.id, call.message.message_id, reply_markup=markup2)

@bot.callback_query_handler(func=lambda call: call.data == "melochy")
def answer_melochy(call):
    bot.answer_callback_query(call.id, "У нас так не принято")
    
    # Изменяем сообщение, убираем кнопку "По мелочи", оставляем только правильный вариант
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("По крупному", callback_data='crupnyi')
    markup.add(btn)
    bot.edit_message_text("У нас так не принято! Давай по крупному:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "crupnyi")
def answer_crupnyi(call):
    markup4 = types.InlineKeyboardMarkup()  
    btn4 = types.InlineKeyboardButton("Крутим!", callback_data='KRUTIM!') 
    markup4.add(btn4)
    bot.edit_message_text("Крути, раз хочется", call.message.chat.id, call.message.message_id, reply_markup=markup4)
    
@bot.callback_query_handler(func=lambda call: call.data == "KRUTIM!")
def spin(call):
    bot.answer_callback_query(call.id)

    user_id = call.from_user.id
    user_data = get_user(user_id)
    
    if not user_data:
        update_user(user_id, 20, 0.75)
        money, luck = 20, 0.75
    else:
        money, luck = user_data
    
    if money <= 0:
        bot.edit_message_text("Ты все проебал 💀", call.message.chat.id, call.message.message_id)
        return

    W = 24 
    StartPossition = 0.0
    StartSpeed = random.uniform(0.10, 0.20)
    LeftWinzone, rightWinzone = random.randint(5, 10), random.randint(14, 20)
    
    # Вместо send_message редактируем текущее сообщение, убирая кнопки на время прокрута
    bot.edit_message_text("🎰 Начинаем...", call.message.chat.id, call.message.message_id)

    for i in range(15):
        StartPossition = (StartPossition + StartSpeed) % 1.0
        StartSpeed *= 0.90
        Possition = int(StartPossition * W)
        
        bar = ["█" if LeftWinzone <= j < rightWinzone else "—" for j in range(W)]
        bar[min(Possition, W-1)] = "◆"
        
        frame = f"<code>[{''.join(bar)}]\n"
        frame += f"0.0{' ' * (W-5)}1.0\n"
        frame += f"{' ' * (Possition+1)}▲ {StartPossition:.2f}</code>\n"
        frame += f"\nКрутим{'.' * (i % 4 + 1)}"
        
        try:
            # Анимация в том же самом сообщении
            bot.edit_message_text(frame, call.message.chat.id, call.message.message_id, parse_mode='HTML')
        except: 
            pass
        time.sleep(0.12)

    Possition = int(StartPossition * W)
    win = LeftWinzone <= Possition < rightWinzone
    
    luck += -0.075 if win else 0.05
    money += 1 if win else -1
    
    # Сохраняем
    update_user(user_id, money, luck)
    
    res_symbol = "🎉 ПОБЕДА!" if win else "💀 МИМО..."
    
    bar = ["█" if LeftWinzone <= j < rightWinzone else "—" for j in range(W)]
    bar[min(Possition, W-1)] = "◆"
    final_text = f"<code>[{''.join(bar)}]\n"
    final_text += f"{' ' * (Possition+1)}▲ {StartPossition:.2f}</code>\n\n"
    final_text += f"{res_symbol}\nБаланс: {money}\n\nЕщё разок?"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Крутить еще!", callback_data='KRUTIM!'))
    
    # Финальный результат и кнопка "Крутить еще" появляются в этом же сообщении
    bot.edit_message_text(final_text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)

print("работаем")

bot.infinity_polling()
