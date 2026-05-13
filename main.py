import telebot
from telebot import types

# الإعدادات الأساسية - محمد المصري
API_TOKEN = '8747899384:AAHAFrAC4LTbYDw8Rp_oHU6fi34E2qlRqKc'
ADMIN_ID = 7729719430 
CHANNEL_ID = "@almasrestore"
CHANNEL_LINK = "https://t.me/almasrestore"
OWNER_USER = "@mohamedalmasre99"

bot = telebot.TeleBot(API_TOKEN)

# 1. نظام الاشتراك الإجباري الاحترافي
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

# 2. واجهة البداية (Start) مع تأثيرات
@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("اضغط هنا للاشتراك وتفعيل البوت 📢", url=CHANNEL_LINK)
        markup.add(btn)
        bot.send_message(message.chat.id, "⚠️ **عذراً يا بطل!**\n\nلا يمكنك استخدام البوت قبل الاشتراك في قناة المتجر الرسمية.\n\nاشترك ثم أرسل /start مجدداً.", reply_markup=markup, parse_mode="Markdown")
        return

    # القائمة الرئيسية بأزرار شفافة واحترافية
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🎮 شحن ببجي", callback_data="pubg")
    btn2 = types.InlineKeyboardButton("🔥 فري فاير", callback_data="ff")
    btn3 = types.InlineKeyboardButton("📸 رشق انستا", callback_data="insta")
    btn4 = types.InlineKeyboardButton("📱 أرقام وهمية", callback_data="nums")
    btn5 = types.InlineKeyboardButton("👤 حسابي", callback_data="me")
    btn6 = types.InlineKeyboardButton("📞 المطور", url=f"https://t.me/mohamedalmasre99")
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    welcome_msg = (
        f"🚀 **مرحباً بك في عالم Turbo Store**\n\n"
        f"أهلاً بك يا {message.from_user.first_name} في المتجر الأسرع والأضمن.\n"
        "إليك قائمة الخدمات المتوفرة حالياً 👇"
    )
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup, parse_mode="Markdown")

# 3. معالجة ضغط الأزرار (تأثيرات الانتقال)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "pubg":
        bot.answer_callback_query(call.id, "جاري تحميل أسعار الشدات...")
        text = "🎮 **أسعار شدات ببجي (UC):**\n\n• 60 UC -> 5000 نقطة\n• 325 UC -> 25000 نقطة\n\nللطلب تواصل مع: @mohamedalmasre99"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown")
    
    elif call.data == "insta":
        bot.answer_callback_query(call.id, "قسم خدمات الإنستغرام")
        text = "📸 **خدمات الرشق المتاحة:**\n\n• 1000 متابع -> 2500 نقطة\n• 5000 متابع -> 10000 نقطة\n\nالدعم فوري ومضمون ✅"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown")

# 4. لوحة تحكم الإدارة (السرية)
@bot.message_handler(commands=['admin'])
def admin(message):
    if message.from_user.id == ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 إذاعة للكل", callback_data="broadcast"))
        markup.add(types.InlineKeyboardButton("⚙️ إعدادات المتجر", callback_data="settings"))
        bot.send_message(message.chat.id, "🛠 **لوحة تحكم المالك (محمد المصري)**", reply_markup=markup, parse_mode="Markdown")

bot.polling()
