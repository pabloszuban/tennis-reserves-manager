from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Browser initial configuration
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Go to the MiBA login page
driver.get("https://formulario-sigeci.buenosaires.gob.ar/InicioTramiteComun?idPrestacion=3154")

wait = WebDriverWait(driver, 20)

# Wait for the page to load and the login button to be clickable
btn_ingresar_mail = wait.until(EC.element_to_be_clickable((
    By.XPATH,
    "//p[text()='Ingresar con CUIL / email']"
)))
btn_ingresar_mail.click()

# Wait for the email and password input to be present
email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
password_input = driver.find_element(By.NAME, "password")

# Complete the email and password fields
email_input.send_keys("pablo.szuban@ib.edu.ar")
password_input.send_keys("Passwordmiba1.")

# Click the login button
btn_ingresar = driver.find_element(By.XPATH, "//button[contains(., 'Ingresar')]")
btn_ingresar.click()

# Wait for the page to load the most recent reservations
btn_mas_proximo = wait.until(EC.element_to_be_clickable((
    By.XPATH,
    "//div[@data-start='primeros']//a[contains(text(), 'Comenzar')]"
)))
btn_mas_proximo.click()

# Wait for the page to load and the "Ver como lista" button to be clickable
btn_ver_lista = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[text()='Ver como lista']")))
btn_ver_lista.click()

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "listBody"))
)

# Get all radio buttons for date and place
radio_buttons = driver.find_elements(By.CSS_SELECTOR, 'input[name="dateAndPlace"]')

results = []

for radio in radio_buttons:
    if not radio.is_displayed():
        continue  # if any radio is not visible, skip it
    
    # Scroll
    driver.execute_script("arguments[0].scrollIntoView(true);", radio)
    time.sleep(0.3)

    # Click the radio button
    radio.click()
    time.sleep(1)

    # Wait for the hours section to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "hoursBody"))
    )

    # Extract date and place attributes
    date = radio.get_attribute("data-date")
    court = radio.get_attribute("data-placename")

    # Get all hour inputs
    hour_inputs = driver.find_elements(By.CSS_SELECTOR, '#hoursBody input[name="hour"]')
    times = [h.get_attribute("data-hour") for h in hour_inputs]

    results.append({
        "date": date,
        "court": court,
        "times": times
    })

# Show results
for item in results:
    print(f"{item['date']} - {item['court']}: {', '.join(item['times'])}")