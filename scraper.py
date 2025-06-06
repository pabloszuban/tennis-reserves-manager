# scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from dotenv import load_dotenv
import os

load_dotenv()

MIBA_EMAIL = os.getenv("MIBA_EMAIL")
MIBA_PASSWORD = os.getenv("MIBA_PASSWORD")
MIBA_URL = os.getenv("MIBA_URL", "https://formulario-sigeci.buenosaires.gob.ar/InicioTramiteComun?idPrestacion=3154")

def get_available_courts():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(MIBA_URL)
    wait = WebDriverWait(driver, 20)

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Ingresar con CUIL / email']"))).click()
        wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(MIBA_EMAIL)
        driver.find_element(By.NAME, "password").send_keys(MIBA_PASSWORD)
        driver.find_element(By.XPATH, "//button[contains(., 'Ingresar')]").click()

        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-start='primeros']//a[contains(text(), 'Comenzar')]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//label[text()='Ver como lista']"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "listBody")))

        radio_buttons = driver.find_elements(By.CSS_SELECTOR, 'input[name="dateAndPlace"]')
        results = []

        for radio in radio_buttons:
            if not radio.is_displayed():
                continue
            driver.execute_script("arguments[0].scrollIntoView(true);", radio)
            time.sleep(0.3)
            try:
                radio.click()
            except:
                continue
            time.sleep(1)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "hoursBody")))

            date = radio.get_attribute("data-date")
            court = radio.get_attribute("data-placename")
            hour_inputs = driver.find_elements(By.CSS_SELECTOR, '#hoursBody input[name="hour"]')
            times = [h.get_attribute("data-hour") for h in hour_inputs]

            results.append({
                "date": date,
                "court": court,
                "times": times
            })

        return results

    finally:
        driver.quit()
