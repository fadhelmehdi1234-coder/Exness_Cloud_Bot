# -*- coding: utf-8 -*-
# تفعيل السيرفر الجبار 2026
from flask import Flask, request, jsonify
import telebot

BOT_TOKEN = "8904786325:AAGi9BEdKX7r4g1BAuwoyrKPlChwhlMQpTA"
ALLOWED_CHAT_ID = 8709813670

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

RISK_SETTINGS = {
    "demo_days": 21,
    "start_balance": 100.0,
}

@app.route('/')
def home():
    return "🚀 Exness Bot Server is Active!"

@app.route('/telegram-webhook', methods=['POST'])
def telegram_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return jsonify({"status": "error"}), 403

@bot.message_handler(commands=['status'])
def send_status(message):
    if message.chat.id != ALLOWED_CHAT_ID: return
    bot.reply_to(message, "🟢 السيرفر شغال في السحاب ومستعد 100% يا مهندس!")

@bot.message_handler(commands=['balance'])
def send_balance(message):
    if message.chat.id != ALLOWED_CHAT_ID: return
    bot.reply_to(message, f"💰 الرصيد الحالي: ${RISK_SETTINGS['start_balance']} USD")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
