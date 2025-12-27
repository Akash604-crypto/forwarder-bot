import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL2_ID = int(os.environ["CHANNEL2_ID"])

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if not msg or not msg.video:
        return

    await context.bot.send_video(
        chat_id=CHANNEL2_ID,
        video=msg.video.file_id,
        caption=None
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    print("Your bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
