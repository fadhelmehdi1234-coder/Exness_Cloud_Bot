# -*- coding: utf-8 -*-
import os
import sys

# 1. التثبيت التلقائي للمكتبات لضمان عمل السيرفر بدون مشاكل
try:
    import telebot
except ImportError:
    os.system(f"{sys.executable} -m pip install pyTelegramBotAPI")
    import telebot

try:
    from flask import Flask, request, jsonify
except ImportError:
    os.system(f"{sys.executable} -m pip install flask")
    from flask import Flask, request, jsonify

# 2. إعدادات البوت والسيرفر
BOT_TOKEN = "8904786325:AAGi9BEdKX7r4g1BAuwoyrKPlChwhlMQpTA"
ALLOWED_CHAT_ID = 8709813670

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

RISK_SETTINGS = {
    "demo_days": 21,
    "start_balance": 100.0,  # الرصيد الحالي
}

@app.route('/')
def home():
    return "🚀 Exness Bot Server is Active!"

# 3. استقبال تحديثات التليجرام عبر الـ Webhook
@app.route('/telegram-webhook', methods=['POST'])
def telegram_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return jsonify({"status": "error"}), 403

# 4. الأوامر الأساسية
@bot.message_handler(commands=['status'])
def send_status(message):
    if message.chat.id != ALLOWED_CHAT_ID: return
    bot.reply_to(message, "🟢 السيرفر شغال في السحاب ومستعد 100% يا مهندس!")

@bot.message_handler(commands=['balance'])
def send_balance(message):
    if message.chat.id != ALLOWED_CHAT_ID: return
    bot.reply_to(message, f"💰 الرصيد الحالي: ${RISK_SETTINGS['start_balance']} USD")

# 5. أمر حاسبة المخاطر واللوت الذكية (الجديد 🔥)
@bot.message_handler(commands=['calc', 'calculate'])
def calculate_risk(message):
    if message.chat.id != ALLOWED_CHAT_ID: return
    
    try:
        # تقسيم الرسالة لمعرفة المعطيات (مثال: /calc gold sl=30 risk=2)
        args = message.text.split()
        if len(args) < 4:
            bot.reply_to(message, "⚠️ **طريقة الاستخدام غلط يا غول!**\n\nاكتبها هكا بالظبط:\n`/calc اسم_الزوج sl=الستوب risk=النسبة`\n\n*مثال:* `/calc gold sl=30 risk=2`", parse_mode="Markdown")
            return
        
        pair = args[1].upper()
        sl_pips = float(args[2].lower().replace("sl=", ""))
        risk_percent = float(args[3].lower().replace("risk=", ""))
        
        balance = RISK_SETTINGS['start_balance']
        
        # حساب المبلغ الأقصى للمخاطرة بالدولار
        risk_amount = balance * (risk_percent / 100.0)
        
        # تحديد قيمة النقطة حسب الزوج (الذهب والعملات تختلف قليلاً)
        if "GOLD" in pair or "XAU" in pair:
            pip_value_standard = 10.0  # الذهب النقطة بـ 10$ في اللوت الستاندرد
        else:
            pip_value_standard = 10.0  # العملات الرئيسية (EURUSD, GBPUSD..) النقطة بـ 10$
            
        # معادلة حساب اللوت الذكية
        # Lot = Risk Amount / (SL in Pips * Pip Value)
        lot_size = risk_amount / (sl_pips * pip_value_standard)
        lot_size = round(lot_size, 2) # تقريب لرقمان بعد الفاصلة (ميكرو لوت)
        
        if lot_size < 0.01:
            lot_size = 0.01 # أقل لوت ممكن في إكسنس
            
        response_text = (
            f"📊 **حاسبة المخاطر الذكية لـ {pair}:**\n"
            f"----------------------------------\n"
            f"💰 الرصيد الحالي: `${balance}`\n"
            f"📉 الستوب لوز (SL): `{sl_pips} Pips`\n"
            f"🛑 المخاطرة المسموحة ({risk_percent}%): `${risk_amount:.2f} USD`\n"
            f"----------------------------------\n"
            f"🎯 **الـ Lot Size المناسب لصفقتك هو:**\n"
            f"🔥 `Lot: {lot_size}` 🔥\n\n"
            f"ادخل اللوت هذا في المنصة وانت مرتاح ومحمي!"
        )
        bot.reply_to(message, response_text, parse_mode="Markdown")
        
    except Exception as e:
        bot.reply_to(message, "⚠️ حدث خطأ في الحساب، تأكد من إدخال الأرقام بشكل صحيح! مثال: `/calc gold sl=40 risk=1`", parse_mode="Markdown")

# 6. تشغيل السيرفر بالبورت المتوافق مع Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)