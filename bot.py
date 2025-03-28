import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
import yt_dlp
import requests

# Tokenni Railway Environment Variables orqali o‘rnating
TOKEN = os.getenv("BOT_TOKEN")

# Logging sozlamalari
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start buyrug‘i
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Salom! Men YouTube va Instagram’dan media yuklab bera olaman.")

# YouTube video yuklash
async def download_youtube(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    await update.message.reply_text("Video yuklanmoqda...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    with open("video.mp4", "rb") as video:
        await update.message.reply_video(video)
    
    os.remove("video.mp4")

# Instagram video yuklash
async def download_instagram(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    await update.message.reply_text("Instagram video yuklanmoqda...")

    response = requests.get(url)
    with open("insta_video.mp4", "wb") as f:
        f.write(response.content)

    with open("insta_video.mp4", "rb") as video:
        await update.message.reply_video(video)
    
    os.remove("insta_video.mp4")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex(r"youtube\.com|youtu\.be"), download_youtube))
    app.add_handler(MessageHandler(filters.Regex(r"instagram\.com"), download_instagram))

    app.run_polling()

if __name__ == "__main__":
    main()
