import asyncio
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from config import *

client = TelegramClient("user_session", API_ID, API_HASH)

@client.on(events.NewMessage(chats=CHANNEL1))
async def handle_channel(event):
    try:
        # Send full post to Bot-1
        await client.send_message(BOT1_USERNAME, event.message)
        await asyncio.sleep(SAFE_DELAY)

    except FloodWaitError as e:
        await asyncio.sleep(e.seconds)

@client.on(events.NewMessage(from_users=BOT1_USERNAME))
async def handle_bot1_reply(event):
    if not event.video:
        return

    try:
        # Send ONLY video to your bot
        await client.send_file(
            YOUR_BOT_USERNAME,
            event.video,
            caption=None
        )
        await asyncio.sleep(SAFE_DELAY)

    except FloodWaitError as e:
        await asyncio.sleep(e.seconds)

async def main():
    await client.start()
    print("User bridge running...")
    await client.run_until_disconnected()

asyncio.run(main())
