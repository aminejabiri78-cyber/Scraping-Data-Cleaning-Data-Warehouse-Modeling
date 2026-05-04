from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import pandas as pd


def scrape_avito():
    driver = webdriver.Chrome()
    data = []
    seen_links = set()

    base_url = "https://www.avito.ma/fr/maroc/appartements-%C3%A0_louer?price=5000-&rooms=1&spare_rooms=1&bathrooms=1&size=-&has_price=true"

    for page in range(1,50):
        print(f"Scraping page {page}...")

        driver.get(base_url + "&page=" + str(page))
        time.sleep(random.uniform(2,5))

        cards = driver.find_elements(By.CSS_SELECTOR, "a.sc-1jge648-0.jZXrfL")

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