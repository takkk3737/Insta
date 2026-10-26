import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import yt_dlp

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "YOUR_BOT_TOKEN"

async def handle_instagram_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    if "instagram.com" not in url:
        await update.message.reply_text("الرجاء إرسال رابط انستغرام صالح (صورة أو فيديو).")
        return

    await update.message.reply_text("⏳ جاري تحميل المحتوى من انستغرام، يرجى الانتظار...")

    ydl_opts = {
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        if file_path.endswith(('.mp4', '.mov', '.mkv', '.webm')):
            with open(file_path, 'rb') as video_file:
                await update.message.reply_video(video=video_file, caption="تم التنزيل بنجاح 📥")
        else:
            with open(file_path, 'rb') as photo_file:
                await update.message.reply_photo(photo=photo_file, caption="تم التنزيل بنجاح 📥")

        os.remove(file_path)

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("❌ حدث خطأ أثناء محاولة تحميل المحتوى. تأكد أن الحساب ليس خاصاً (Private).")

if __name__ == '__main__':
    os.makedirs('downloads', exist_ok=True)
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_instagram_link))
    print("🤖 البوت يعمل الآن...")
    application.run_polling()
