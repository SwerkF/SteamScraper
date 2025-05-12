import os
import time
import json
import random
import ssl
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ssl._create_default_https_context = ssl._create_unverified_context

# Charger la liste des jeux depuis JSON
with open("data/top_games.json", "r", encoding="utf-8") as f:
    games = json.load(f)

# Limite pour test
urls = [g["url"] for g in games][:100]

# Setup navigateur
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = uc.Chrome(options=options)

# Résultats
games_data = []
steam_store_links = {}
errors = []

# Fonction d’attente pour le titre
def wait_for_game_title(timeout=15):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='name']"))
        )
    except:
        return None

# Fonction utilitaire pour extraire les champs du tableau
def get_cell_value(label):
    try:
        return driver.find_element(By.XPATH, f"//tr[td[contains(text(), '{label}')]]/td[2]").text.strip()
    except:
        return None

# Scraping boucle
for i, url in enumerate(urls):
    try:
        driver.get(url)
        time.sleep(5)

        name_elem = wait_for_game_title()
        if not name_elem:
            try:
                label = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "label.cb-lb"))
                )
                checkbox = label.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                time.sleep(2)
                checkbox.click()
                print("CAPTCHA résolu.")
            except Exception as e:
                print(f"CAPTCHA non résolu : {e}")
            name_elem = wait_for_game_title(timeout=30)

        if not name_elem:
            print(f"Échec sur {url}")
            errors.append({"url": url, "reason": "Titre non chargé"})
            continue

        name = name_elem.text.strip()
        app_id = get_cell_value("App ID")
        developer = get_cell_value("Developer")
        publisher = get_cell_value("Publisher")
        supported_systems = get_cell_value("Supported Systems")
        technologies = get_cell_value("Technologies")
        release_date = get_cell_value("Release Date")

        try:
            image_elem = driver.find_element(By.CSS_SELECTOR, "img.app-logo[itemprop='image']")
            image_url = image_elem.get_attribute("src")
        except:
            image_url = None

        try:
            store_link = driver.find_element(By.XPATH, "//a[contains(@href, 'store.steampowered.com/app')]")
            store_url = store_link.get_attribute("href")
        except:
            store_url = None

        game_data = {
            "name": name,
            "image_url": image_url,
            "app_id": app_id,
            "developer": developer,
            "publisher": publisher,
            "supported_systems": supported_systems,
            "technologies": technologies,
            "release_date": release_date,
            "store_url": store_url
        }

        games_data.append(game_data)
        steam_store_links[name] = store_url

        print(f"{i+1}/{len(urls)} - {name}")
        time.sleep(60)  # pause longue

    except Exception as e:
        print(f"Erreur sur {url} : {e}")
        errors.append({"url": url, "reason": str(e)})
        continue

driver.quit()

# === Sauvegardes JSON ===
os.makedirs("data", exist_ok=True)

with open("data/games_data.json", "w", encoding="utf-8") as f:
    json.dump(games_data, f, indent=4, ensure_ascii=False)

with open("data/steam_store_links.json", "w", encoding="utf-8") as f:
    json.dump(steam_store_links, f, indent=4, ensure_ascii=False)

with open("data/games_errors.json", "w", encoding="utf-8") as f:
    json.dump(errors, f, indent=4, ensure_ascii=False)

print("\nTerminé : données enregistrées dans le dossier data/ pour traitement ultérieur")
