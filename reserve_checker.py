from scraper import get_available_courts
from telegram import Bot
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS").split(",") 
INTERVAL = int(os.getenv("INTERVAL", "43200"))

bot = Bot(token=BOT_TOKEN)

def format_msg(courts):
    mensaje = "🎾 ¡Canchas disponibles!\n\n"
    for court in courts:
        date = court["date"]
        court_name = court["court"].replace(" - Polideportivo Parque Patricios", "")
        time = ", ".join(court["times"])
        mensaje += f"📅 {date} - 📍 {court_name}: ⏰ {time}\n"
    return mensaje

async def send_telegram_message(mensaje, chat_id):
    await bot.send_message(chat_id, text=mensaje)

async def main():
    print("⏳ Searching for availability...")
    while True:
        courts = await get_available_courts()
        if courts:
            mensaje = format_msg(courts)
            print("✅ Found available courts, sending Telegram Message...")
            for chat_id in CHAT_IDS:
                await send_telegram_message(mensaje, chat_id)
        else:
            print("❌ No available courts.")
        await asyncio.sleep(INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
