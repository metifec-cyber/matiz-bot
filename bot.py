import os
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = os.environ.get("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "بات جست‌وجوی خودرو آماده‌ست 🚗\n\n"
        "فعلاً نسخه آزمایشی هستیم.\n"
        "به‌زودی فیلترهای قیمت، مدل، کارکرد و شهر رو اضافه می‌کنیم."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "دستورات فعلی:\n"
        "/start - شروع\n"
        "/help - راهنما"
    )


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN تنظیم نشده است.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
