# scraper.py
from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv

load_dotenv()

MIBA_EMAIL = os.getenv("MIBA_EMAIL")
MIBA_PASSWORD = os.getenv("MIBA_PASSWORD")
MIBA_URL = os.getenv("MIBA_URL", "https://formulario-sigeci.buenosaires.gob.ar/InicioTramiteComun?idPrestacion=3154")

async def get_available_courts():
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(MIBA_URL)

        await page.click("text=Ingresar con CUIL / email")
        await page.fill("input[name='email']", MIBA_EMAIL)
        await page.fill("input[name='password']", MIBA_PASSWORD)
        await page.click("button:has-text('Ingresar')")

        await page.click("text=Comenzar")
        await page.click("label:text('Ver como lista')")
        await page.wait_for_selector("#listBody")

        radios = await page.query_selector_all('input[name="dateAndPlace"]')

        for radio in radios:
            visible = await radio.is_visible()
            if not visible:
                continue

            await radio.scroll_into_view_if_needed()
            await radio.click()
            await page.wait_for_selector("#hoursBody")

            date = await radio.get_attribute("data-date")
            court = await radio.get_attribute("data-placename")
            hour_inputs = await page.query_selector_all('#hoursBody input[name="hour"]')
            times = [await h.get_attribute("data-hour") for h in hour_inputs]

            results.append({
                "date": date,
                "court": court,
                "times": times
            })

        await browser.close()
    return results
