from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Remote
import time
import random


def scrape_avito():
    # ====== FIX: Remote Selenium (Docker) ======
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = Remote(
        command_executor="http://localhost:4444/wd/hub",
        options=options
    )

    data = []
    seen_links = set()

    base_url = "https://www.avito.ma/fr/maroc/appartements-%C3%A0_louer?price=5000-&rooms=1&spare_rooms=1&bathrooms=1&size=-&has_price=true"

    for page in range(1, 100):
        print(f"Scraping page {page}...")

        driver.get(base_url + "&page=" + str(page))
        time.sleep(random.uniform(3, 6))

        cards = driver.find_elements(By.CSS_SELECTOR, "a.sc-1jge648-0.jZXrfL")

        # stop if no data
        if len(cards) == 0:
            print("No more data, stopping...")
            break

        for c in cards:
            try:
                lien = c.get_attribute("href")
            except:
                lien = None

            if not lien or lien in seen_links:
                continue

            seen_links.add(lien)

            try:
                titre = c.find_element(By.CSS_SELECTOR, "p.sc-1x0vz2r-0.iHApav").text
            except:
                titre = None

            try:
                prix = c.find_element(By.XPATH, ".//span[contains(@class,'kohQqr')]").text
            except:
                prix = None

            try:
                ville = c.find_element(By.XPATH, ".//p[contains(text(),'Appartements dans')]").text
            except:
                ville = None

            try:
                surface = c.find_element(By.CSS_SELECTOR, "span[title='Surface totale']").text
            except:
                surface = None

            try:
                chambres = c.find_element(By.CSS_SELECTOR, "span[title='Chambres']").text
            except:
                chambres = None

            try:
                sdb = c.find_element(By.CSS_SELECTOR, "span[title='Salle de bain']").text
            except:
                sdb = None

            try:
                etage = c.find_element(By.CSS_SELECTOR, "span[title='Étage']").text
            except:
                etage = None

            data.append({
                "titre": titre,
                "prix": prix,
                "ville": ville,
                "surface": surface,
                "chambres": chambres,
                "salle_de_bain": sdb,
                "etage": etage,
                "lien": lien
            })

    driver.quit()
    return data