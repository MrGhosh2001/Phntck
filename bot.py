import requests
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ================= CONFIG =================
BOT_TOKEN = "8866257893:AAFTsQR3byevFzxEQgabW8CXR0HjpmSsSeo"   # 👈 Apna bot token daalein
API_URL = "http://rajfflivebot.onrender.com/pub/rajfflive/api"
API_KEY = "RAJBOTSOFC"

# ==========================================

# Start Message — ONLY Spoiler (Black Quote/Expandable)
FORCE_JOIN_TEXT = (
    "<blockquote expandable>"
    "sᴇɴᴅ ᴀɴʏ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ᴛᴏ sᴇᴀʀᴄʜ ᴅᴇᴛᴀɪʟs🔥"
    "</blockquote>"
)


def get_join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴊᴏɪɴ", url=JOIN_LINK)]
    ])


def get_result_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=DEV_LINK)]
    ])


# ============ /start COMMAND ============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        FORCE_JOIN_TEXT,
        parse_mode="HTML",
        reply_markup=get_join_keyboard()
    )


# ============ MAIN NUMBER HANDLER ============
async def num_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.isdigit() or len(text) != 10:
        await update.message.reply_text("❌ ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ 10 ᴅɪɢɪᴛ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ")
        return

    msg = await update.message.reply_text("🔍 sᴇᴀʀᴄʜɪɴɢ... ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ")

    try:
        res = requests.get(
            API_URL,
            params={"num": text, "key": API_KEY},
            timeout=30
        )
        data = res.json()
    except Exception as e:
        await msg.edit_text(f"❌ ᴇʀʀᴏʀ: {e}")
        return

    pretty = json.dumps(data, indent=2, ensure_ascii=False)

    LIMIT = 4000
    parts = [pretty[i:i + LIMIT] for i in range(0, len(pretty), LIMIT)]

    try:
        await msg.edit_text(
            f"```json\n{parts[0]}\n```",
            parse_mode="Markdown",
            reply_markup=get_result_keyboard()
        )
        for part in parts[1:]:
            await update.message.reply_text(
                f"```json\n{part}\n```",
                parse_mode="Markdown",
                reply_markup=get_result_keyboard()
            )
    except Exception as e:
        try:
            await msg.edit_text(pretty, reply_markup=get_result_keyboard())
        except Exception:
            await update.message.reply_text(
                f"❌ sᴇɴᴅ ᴇʀʀᴏʀ: {e}",
                reply_markup=get_result_keyboard()
            )


# ============ MAIN ============
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, num_info))

    print("✅ Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
