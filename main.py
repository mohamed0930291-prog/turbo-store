import telebot
from telebot import types

# الإعدادات المحدثة لـ Turbo Store
API_TOKEN = '8747899384:AAHAFrAC4LTbYDw8Rp_oHU6fi34E2qlRqKc'
ADMIN_ID = 7729719430
CHANNEL_ID = "@almasrestore"
CHANNEL_LINK = "https://t.me/almasrestore"
OWNER_USER = "@mohamedalmasre99"

bot = telebot.TeleBot(API_TOKEN)

# دالة التحقق من الاشتراك
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return True

@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("اشترك في القناة ✅", url=CHANNEL_LINK)
        markup.add(btn)
        bot.send_message(message.chat.id, "أهلاً بك! يرجى الاشتراك في قناة المتجر أولاً لتفعيل البوت.", reply_markup=markup)
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛒 خدمات الشحن والرشق", "👤 حسابي")
    markup.add("📞 الدعم الفني (محمد المصري)")
    bot.send_message(message.chat.id, f"أهلاً بك يا محمد المصري في Turbo Store ⚡\nالبوت شغال الآن بالتوكن الجديد!", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📞 الدعم الفني (محمد المصري)")
def support(message):
    bot.send_message(message.chat.id, f"للتواصل المباشر مع المالك:\n{OWNER_USER}")

@bot.message_handler(func=lambda message: message.text == "🛒 خدمات الشحن والرشق")
def services(message):
    text = (
        "⚡ **خدمات Turbo Store المتاحة:**\n\n"
        "🎮 **ببجي موبايل (UC):** 60 شدة بـ 5000 نقطة\n"
        "📸 **إنستقرام:** 1000 متابع بـ 2500 نقطة\n\n"
        "لطلب خدمة، تواصل مع المالك مباشرة."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

print("Turbo Store is Online with New Token...")
bot.polling()
