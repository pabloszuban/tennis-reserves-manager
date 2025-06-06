# 🎾 Tennis Court Availability Bot (Buenos Aires, Argentina)

This bot automatically checks for tennis court availability on the [MiBA SIGeCi system](https://formulario-sigeci.buenosaires.gob.ar/) and sends alerts to a Telegram chat if courts are available.

## 🚀 Features

- Scrapes available tennis court dates and times from MiBA (City of Buenos Aires, Polideportivo Parque Patricios).
- Sends Telegram notifications when courts are found.
- Runs periodically, configurable via environment variables.
- Deployable to [Railway](https://railway.app/) or any Python-capable environment.

---

## 🧰 Requirements

- Python 3.9+
- [Playwright](https://playwright.dev/python/)
- A Telegram Bot (via [@BotFather](https://t.me/BotFather))
- A Telegram chat ID to receive alerts
- (Optional) [Railway](https://railway.app/) account for cloud deployment

## 🛠️ Local Setup

```bash
git clone https://github.com/your-username/tennis-court-bot.git
cd tennis-court-bot
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
playwright install
```

## 📁 Environment Variables

Create a .env file in the root directory:

Create a `.env` file in the project root with the following variables:

```env
MIBA_EMAIL=your_email@example.com
MIBA_PASSWORD=your_password
MIBA_URL=https://formulario-sigeci.buenosaires.gob.ar/InicioTramiteComun?idPrestacion=3154
BOT_TOKEN=your_telegram_bot_token
CHAT_IDS=123456789,987654321
INTERVAL=43200  # Optional: Interval in seconds between checks (default is 43200 seconds = 12 hours)
```

## ▶️ Run Locally

```bash
bash start.sh
```

This will start the bot and continuously check for court availability at your defined interval.

## ☁️ Deploy to Railway (Optional)

Push your repo to GitHub.

Create a new project on Railway and link your GitHub repo.

Set the environment variables in Railway using your .env values.

Configure the Start Command in Railway to:

```bash
bash start.sh
```

Railway will install dependencies and run the bot automatically.

📦 Project Structure

```bash
tennis-court-bot/
├── reserve_checker.py # Main script that runs the bot loop
├── scraper.py # Web scraping logic using Playwright
├── start.sh # Bootstrap script for Railway or local usage
├── .env # Environment variables (not committed)
├── requirements.txt # Python dependencies
```

## 📬 Telegram Alert Format

```text
🎾 Available Courts!

📅 2025-06-10 - 📍 Parque Patricios: ⏰ 08:00, 09:00, 10:00
```

## 🧪 Tested With

macOS / Linux

Railway deployment (Linux environment)

Python 3.10+

Chromium (via Playwright)

## 🤝 Contributing

Feel free to open issues or submit PRs to improve the bot! Suggestions welcome 🙌

## 📣 Disclaimer

This bot is not affiliated with the Government of Buenos Aires or MiBA. Use it responsibly.
