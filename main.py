import telebot
from telebot import types

# --- الإعدادات الثابتة (بلاك تفعيل النظام) ---
API_TOKEN = '7748443916:AAH5Z_p0qM0Xw_D0m-l_o3V6q-YI2Lp78i8' # توكن بوتك
ADMIN_ID = 7729719430 # آيدي محمد المصري
CHANNEL_ID = "@almasrestore" # معرف القناة
CHANNEL_LINK = "https://t.me/almasrestore" # رابط القناة
OWNER_USER = "@mohamedalmasre99" # يوزر التواصل الجديد

bot = telebot.TeleBot(API_TOKEN)

# دالة التحقق من الاشتراك الإجباري
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return True # إذا في مشكلة بالصلاحيات يكمل عشان ما يعلق البوت

# أمر البدء
@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("اشترك في قناة المتجر أولاً ✅", url=CHANNEL_LINK)
        markup.add(btn)
        bot.send_message(message.chat.id, f"أهلاً بك في Turbo Store ⚡\n\nعذراً يا بطل، يجب عليك الاشتراك في القناة لتتمكن من استخدام خدماتنا.", reply_markup=markup)
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛒 خدمات الشحن والرشق", "👤 حسابي")
    markup.add("📞 الدعم الفني (محمد المصري)")
    bot.send_message(message.chat.id, f"أهلاً بك يا {message.from_user.first_name} في متجر تيربو 🚀\nكل ما تحتاجه من خدمات رقمية في مكان واحد.", reply_markup=markup)

# لوحة التحكم للمالك فقط
@bot.message_handler(commands=['admin'])
def admin(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "أهلاً بك يا محمد في لوحة تحكم الإدارة. قريباً سنضيف أزرار التحكم بالأسعار من هنا.")
    else:
        bot.send_message(message.chat.id, "هذا الأمر مخصص للمالك فقط.")

# الدعم الفني
@bot.message_handler(func=lambda message: message.text == "📞 الدعم الفني (محمد المصري)")
def support(message):
    bot.send_message(message.chat.id, f"للتواصل مع المالك محمد المصري مباشرة:\n{OWNER_USER}")

# خدمات الشحن
@bot.message_handler(func=lambda message: message.text == "🛒 خدمات الشحن والرشق")
def services(message):
    text = (
        "⚡ **خدمات Turbo Store المتاحة:**\n\n"
        "🎮 **ببجي موبايل (UC):**\n- 60 شدة: 5000 نقطة\n\n"
        "📸 **إنستقرام:**\n- 1000 متابع: 2500 نقطة\n\n"
        "💬 **أرقام وهمية:**\n- تفعيل تليجرام/واتساب (مجاناً للمشتركين الجدد)\n\n"
        "لطلب أي خدمة، تواصل مع المالك مباشرة عبر زر الدعم الفني."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

print("Turbo Store is Online...")
bot.polling()
