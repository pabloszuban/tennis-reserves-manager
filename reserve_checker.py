from scraper import get_available_courts
from telegram import Bot
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS").split(",") 
INTERVAL = int(os.getenv("INTERVAL", "43200"))
MIBA_URL = os.getenv("MIBA_URL", "https://formulario-sigeci.buenosaires.gob.ar/InicioTramiteComun?idPrestacion=3154")

bot = Bot(token=BOT_TOKEN)

from datetime import datetime

def format_msg(courts):
    dias = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }
    msg = "🎾 ¡Canchas disponibles!\n\n"
    for court in courts:
        date = court["date"]
        dt = datetime.strptime(date, "%Y-%m-%d")
        day_name = dias[dt.strftime("%A")]
        court_name = court["court"].replace(" - Polideportivo Parque Patricios", "")
        time = ", ".join(court["times"])
        msg += f"📅 <b>{day_name} {date}</b> - 📍 {court_name}: ⏰ {time}\n"
    msg += f"\n👉 Reservá tu turno acá: {MIBA_URL}"
    return msg

async def send_telegram_message(mensaje, chat_id):
    await bot.send_message(chat_id, text=mensaje, parse_mode="HTML")

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
