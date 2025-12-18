import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import yt_dlp

BOT_TOKEN = "8324087844:AAGyDnaIW6w2VtxT6B-D9MdueeVvGwK2QCI"
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def download_youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not ("youtube.com" in url or "youtu.be" in url):
        await update.message.reply_text("❌ أرسل رابط يوتيوب صحيح")
        return

    await update.message.reply_text("⏳ جاري التحميل بأعلى جودة...")

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # أفضل جودة فيديو وصوت
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'quiet': True,
        'merge_output_format': 'mp4',           # دمج الفيديو والصوت
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        filesize = os.path.getsize(filename) / (1024 * 1024)  # بالميغابايت

        if filesize < 50:
            await update.message.reply_video(
                video=open(filename, 'rb'),
                caption=f"✅ تم التحميل بنجاح ({int(filesize)} MB)"
            )
        else:
            await update.message.reply_text(
                f"⚠️ حجم الفيديو كبير جدًا ({int(filesize)} MB) ولا يمكن إرساله مباشرة.\n"
                f"يمكنك تحميله من هنا: {info.get('webpage_url')}"
            )

        os.remove(filename)

    except Exception as e:
        print(e)
        await update.message.reply_text("❌ فشل التحميل")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_youtube))
    app.run_polling()

if __name__ == "__main__":
    main()
