import asyncio
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from config import *

# Create client session
client = TelegramClient(
    session="user_session",
    api_id=API_ID,
    api_hash=API_HASH
)

# =========================
# CHANNEL-1 → BOT-1
# =========================
@client.on(events.NewMessage(chats=CHANNEL1))
async def handle_channel(event):
    try:
        print("🔥 New post detected in Channel-1")

        # Send FULL post (media + caption) to Bot-1
        await client.send_file(
            BOT1_USERNAME,
            event.message
        )

        await asyncio.sleep(SAFE_DELAY)

    except FloodWaitError as e:
        print(f"⏳ FloodWait while sending to Bot-1: {e.seconds}s")
        await asyncio.sleep(e.seconds)

    except Exception as e:
        print("❌ Error in handle_channel:", e)


# =========================
# BOT-1 → USER → YOUR BOT
# =========================
@client.on(events.NewMessage(from_users=BOT1_USERNAME))
async def handle_bot1_reply(event):
    try:
        # Ignore non-video replies
        if not event.video:
            return

        # Ignore messages sent by ourselves
        if event.out:
            return

        print("🎥 Video received from Bot-1")

        # Send ONLY the video (no caption) to your bot
        await client.send_file(
            YOUR_BOT_USERNAME,
            event.video,
            caption=None
        )

        await asyncio.sleep(SAFE_DELAY)

    except FloodWaitError as e:
        print(f"⏳ FloodWait while sending to Your Bot: {e.seconds}s")
        await asyncio.sleep(e.seconds)

    except Exception as e:
        print("❌ Error in handle_bot1_reply:", e)


# =========================
# MAIN LOOP
# =========================
async def main():
    await client.start()
    print("✅ User bridge running and listening...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 User bridge stopped manually")
