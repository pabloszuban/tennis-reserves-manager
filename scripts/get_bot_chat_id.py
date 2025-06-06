import asyncio
from telegram import Bot

BOT_TOKEN = "7764497640:AAFOgJ2b98rbD3T_S-OrJymAD2SoH7KrGkQ"
bot = Bot(token=BOT_TOKEN)

async def main():
    updates = await bot.get_updates()
    print(updates)
    if updates:
        print("chat_id:", updates[-1].message.chat.id)
    else:
        print("No new messages, please send a message to the bot and try again.")

asyncio.run(main())
