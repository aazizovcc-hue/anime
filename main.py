import asyncio
import logging
import os
import tempfile
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from youtube_upload import upload_video

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID_RAW = os.getenv("OWNER_TELEGRAM_ID", "").strip()
OWNER_ID = int(OWNER_ID_RAW) if OWNER_ID_RAW.isdigit() else None
logging.basicConfig(level=logging.INFO)


def authorized(update: Update) -> bool:
    return OWNER_ID is None or (update.effective_user and update.effective_user.id == OWNER_ID)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not authorized(update):
        return
    await update.message.reply_text(
        "🎬 YouTube Auto Uploader tayyor!\n"
        "Videoni yuboring. Captionning 1-qatori — video nomi,\n"
        "keyingi qatorlari — description. Caption bo'lmasa, fayl nomi ishlatiladi."
    )


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not authorized(update):
        return
    message = update.effective_message
    video = message.video or message.document
    if not video:
        return
    if message.document and not (message.document.mime_type or "").startswith("video/"):
        await message.reply_text("Video fayl yuboring (video format).")
        return

    caption = message.caption or ""
    lines = caption.splitlines()
    filename = getattr(message.document, "file_name", None) or "Telegram video"
    fallback_title = os.path.splitext(filename)[0]
    title = lines[0].strip() if lines and lines[0].strip() else fallback_title
    description = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
    status_msg = await message.reply_text("📥 Video qabul qilindi. Yuklashga tayyorlanyapti…")
    video_path = None
    try:
        tg_file = await context.bot.get_file(video.file_id)
        suffix = os.path.splitext(filename)[1] if filename else ".mp4"
        if not suffix or len(suffix) > 10:
            suffix = ".mp4"
        fd, video_path = tempfile.mkstemp(suffix=suffix)
        os.close(fd)
        await tg_file.download_to_drive(video_path)
        await status_msg.edit_text("🚀 YouTube kanaliga yuklanyapti…")
        url = await asyncio.to_thread(upload_video, video_path, title, description)
        await status_msg.edit_text(f"✅ YouTube'ga yuklandi!\n\n🎬 {title}\n🔗 {url}")
    except Exception:
        logging.exception("Video upload failed")
        await status_msg.edit_text("❌ Uploadda xatolik yuz berdi. Terminal logini tekshiring.")
    finally:
        if video_path and os.path.exists(video_path):
            os.remove(video_path)


def main():
    if not BOT_TOKEN:
        raise RuntimeError(".env ichida TELEGRAM_BOT_TOKEN ko'rsatilmagan")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.ALL, handle_video))
    print("Bot ishga tushdi — Ctrl+C bilan to'xtating")
    app.run_polling()


if __name__ == "__main__":
    main()
