
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load referral data
def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except:
        return {"referrals": {}, "ref_count": {}}

# Save referral data
def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)

data = load_data()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    args = context.args

    if args:
        referrer_id = args[0]
        if referrer_id == user_id:
            await update.message.reply_text("❌ You cannot refer yourself!")
        elif user_id in data["referrals"]:
            await update.message.reply_text("⚠️ You were already referred!")
        else:
            data["referrals"][user_id] = referrer_id
            data["ref_count"][referrer_id] = data["ref_count"].get(referrer_id, 0) + 1
            save_data(data)
            await update.message.reply_text(f"✅ You were referred by user {referrer_id}")
    else:
        await update.message.reply_text("👋 Welcome! Share your referral link!")

async def myref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    ref_link = f"https://t.me/YOUR_BOT_USERNAME?start={user_id}"
    ref_count = data["ref_count"].get(user_id, 0)

    await update.message.reply_text(f"🔗 Your referral link:\n{ref_link}\n👥 Total referrals: {ref_count}")

app = ApplicationBuilder().token("8077195764:AAHXz19t-1xgJsyLjc0DLaCv_BZZdliJbCc").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("myref", myref))

print("✅ Bot is running...")
app.run_polling()
