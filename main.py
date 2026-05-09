import telebot
from telebot import types
import json
import os

# --- الإعدادات (تأكد من التوكن والأيدي) ---
TOKEN = '8747899384:AAHAFrAC4LTbYDw8Rp_oHU6fi34E2qlRqKc'
ADMIN_ID = 6363657393 
bot = telebot.TeleBot(TOKEN)

# اسم قاعدة البيانات
DB_FILE = "almasri_database.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {}

def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

# --- لوحة المفاتيح الرئيسية ---
def main_menu():
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(
        types.InlineKeyboardButton("📈 رشق متابعين", callback_data="smm"),
        types.InlineKeyboardButton("🎮 شحن ألعاب", callback_data="games"),
        types.InlineKeyboardButton("📱 أرقام وهمية", callback_data="nums"),
        types.InlineKeyboardButton("💰 جمع نقاط", callback_data="invite"),
        types.InlineKeyboardButton("👤 حسابي", callback_data="me"),
        types.InlineKeyboardButton("💳 شحن رصيد", callback_data="pay")
    )
    return m

# --- الأوامر ---
@bot.message_handler(commands=['start'])
def start(message):
    db = load_db()
    uid = str(message.from_user.id)
    
    # نظام الإحالة
    if uid not in db:
        db[uid] = {"points": 0, "name": message.from_user.first_name, "orders": 0}
        args = message.text.split()
        if len(args) > 1 and args[1] in db:
            db[args[1]]["points"] += 100
            bot.send_message(args[1], "✅ حصلت على 100 نقطة من إحالة جديدة!")
    
    save_db(db)
    bot.send_message(message.chat.id, f"🚀 أهلاً بك في **𝑨𝒍 𝒎𝒂𝒔𝒓𝒆 | 𝒔𝒕𝒐𝒓𝒆**\nرصيدك: {db[uid]['points']} نقطة", reply_markup=main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def calls(call):
    db = load_db()
    uid = str(call.from_user.id)
    
    if call.data == "me":
        pts = db[uid]['points']
        bot.edit_message_text(f"👤 **معلوماتك:**\n🆔: `{uid}`\n💰 رصيدك: {pts}\n📦 طلباتك: {db[uid]['orders']}", call.message.chat.id, call.message.message_id, reply_markup=main_menu(), parse_mode="Markdown")
    
    elif call.data == "invite":
        link = f"https://t.me/{bot.get_me().username}?start={uid}"
        bot.send_message(call.message.chat.id, f"🔗 **رابط دعوتك:**\n`{link}`\n\nشارك الرابط وخذ 100 نقطة على كل شخص!")

    elif call.data == "pay":
        bot.send_message(call.message.chat.id, "💳 للشحن تواصل مع المدير: @M7MD_ALMASRI")

    bot.answer_callback_query(call.id)

# --- لوحة تحكم الإدارة (فقط لك) ---
@bot.message_handler(commands=['add'])
def add_points(message):
    if message.from_user.id == ADMIN_ID:
        try:
            # الأمر يكون: /add 123456 1000
            _, target_id, amount = message.text.split()
            db = load_db()
            if target_id in db:
                db[target_id]["points"] += int(amount)
                save_db(db)
                bot.reply_to(message, f"✅ تم إضافة {amount} نقطة للمستخدم {target_id}")
            else:
                bot.reply_to(message, "❌ المستخدم غير موجود.")
        except:
            bot.reply_to(message, "⚠️ الطريقة: /add [ID] [النقاط]")

print("⚡ (بلاك تفعيل النظام): الكود جاهز للرفع...")
bot.infinity_polling()
