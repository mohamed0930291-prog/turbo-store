import telebot
from telebot import types

# إعدادات البوت الأساسية
API_TOKEN = 'هنا_ضع_توكن_بوتك_الذي_أخذته_من_بوت_فاذر'
ADMIN_ID = 7729719430
CHANNEL_ID = "@almasrestore"
CHANNEL_LINK = "https://t.me/almasrestore"

bot = telebot.TeleBot(API_TOKEN)

# قاعدة بيانات وهمية (يتم تحديثها من لوحة التحكم)
prices = {
    "pubg": 5000,
    "insta": 2000,
    "freefire": 4500
}

# دالة التحقق من الاشتراك الإجباري
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

# لوحة التحكم (للمالك فقط)
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("تعديل أسعار ببجي", callback_data="edit_pubg")
        btn2 = types.InlineKeyboardButton("تعديل أسعار انستا", callback_data="edit_insta")
        btn3 = types.InlineKeyboardButton("إحصائيات البوت", callback_data="stats")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, "أهلاً بك يا محمد في لوحة تحكم Turbo Store 🚀", reply_markup=markup)

# القائمة الرئيسية
@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("اشترك هنا أولاً ✅", url=CHANNEL_LINK)
        markup.add(btn)
        bot.send_message(message.chat.id, "عذراً! يجب عليك الاشتراك في قناة المتجر لتتمكن من استخدام البوت.", reply_markup=markup)
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛒 خدمات الشحن", "👤 حسابي", "📞 الدعم الفني")
    bot.send_message(message.chat.id, "أهلاً بك في متجر تيربو - Turbo Store ⚡\nاختر من القائمة أدناه:", reply_markup=markup)

# التعامل مع الخدمات
@bot.message_handler(func=lambda message: message.text == "🛒 خدمات الشحن")
def services(message):
    text = f"قائمة الخدمات الحالية:\n\n"
    text += f"🔹 شدات ببجي (60 UC): {prices['pubg']} نقطة\n"
    text += f"🔹 متابعين انستا (1000): {prices['insta']} نقطة\n"
    text += f"🔹 جواهر فري فاير: {prices['freefire']} نقطة\n\n"
    text += "لطلب أي خدمة، تواصل مع الإدارة مباشرة."
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: message.text == "📞 الدعم الفني")
def support(message):
    bot.send_message(message.chat.id, "للتواصل مع المالك محمد المصري: @mohamedalmasre99")

print("البوت يعمل الآن بنجاح...")
bot.polling()
