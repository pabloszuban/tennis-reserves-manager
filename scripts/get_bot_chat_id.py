import asyncio
from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

async def main():
    updates = await bot.get_updates()
    print(updates)
    if updates:
        print("chat_id:", updates[-1].message.chat.id)
    else:
        print("No new messages, please send a message to the bot and try again.")

asyncio.run(main())
