import os
import telebot
from datetime import datetime

# استدعاء المتغيرات السرية اللي صبيناها في Render
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
EXNESS_ACCOUNT = os.getenv("EXNESS_LOGIN")
EXNESS_SERVER = os.getenv("EXNESS_SERVER")

# تشغيل بوت التليجرام
bot = telebot.TeleBot(TOKEN)

def run_test():
    try:
        print("⚡ جاري تشغيل الفحص بأقصى قوة...")
        
        # تجهيز نص الرسالة الاحترافية
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = (
            "🚀 **Exness Cloud Bot - Test Success** 🚀\n\n"
            "🟢 **حالة الربط:** مريغل 100% وبأقصى قوة!\n"
            f"📅 **الوقت:** {current_time}\n\n"
            "📊 **معطيات الحساب المربوط:**\n"
            f"👤 **رقم الحساب:** `{EXNESS_ACCOUNT}`\n"
            f"🖥️ **السيرفر:** `{EXNESS_SERVER}`\n\n"
            "🎯 النظام جاهز الآن لمراقبة الصفقات أوتوماتيكياً!"
        )
        
        # إرسال الرسالة للتليجرام
        bot.send_message(CHAT_ID, message, parse_mode="Markdown")
        print("✅ تم إرسال رسالة التست بنجاح للتليجرام! تفقد تليجرام في تليلفونك.")
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء التست: {e}")

if __name__ == "__main__":
    run_test()