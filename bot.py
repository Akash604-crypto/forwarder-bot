import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

# ---------- CONFIG ----------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL1_ID = int(os.environ.get("CHANNEL1_ID"))
CHANNEL2_ID = int(os.environ.get("CHANNEL2_ID"))

# ---------- HANDLER ----------
async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = update.channel_post

    if not post:
        return

    # ✅ ONLY process posts coming from Channel-1
    if post.chat.id != CHANNEL1_ID:
        return

    # ✅ If post has a video → send ONLY video to Channel-2
    if post.video:
        await context.bot.send_video(
            chat_id=CHANNEL2_ID,
            video=post.video.file_id,
            caption=None
        )

    # ❌ Ignore images, captions, text, documents, etc.

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.Chat(CHANNEL1_ID),
            handle_channel_post
        )
    )

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
