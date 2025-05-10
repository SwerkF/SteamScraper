import csv
import time
import json
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Lecture des URLs depuis le fichier CSV
with open("top_games.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    urls = [row["url"] for row in reader][:5]

# Setup navigateur furtif
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = uc.Chrome(options=options)

# Fichiers CSV
fields = ["Name", "App ID", "Developer", "Publisher", "Supported Systems", "Technologies", "Release Date"]
success_file = open("games_data.csv", "w", newline="", encoding="utf-8")
success_writer = csv.DictWriter(success_file, fieldnames=fields)
success_writer.writeheader()

failed_file = open("games_failed.csv", "w", newline="", encoding="utf-8")
failed_writer = csv.writer(failed_file)
failed_writer.writerow(["url", "reason"])

steam_store_links = {}

def wait_for_game_title(timeout=15):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='name']"))
        )
    except:
        return None

# Boucle sur les URLs
for i, url in enumerate(urls):
    try:
        driver.get(url)
        time.sleep(5)

        name_elem = wait_for_game_title()

        if not name_elem:
            print(f"🛡️ CAPTCHA probable sur {url}")
            try:
                label = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "label.cb-lb"))
                )
                checkbox = label.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                time.sleep(2)
                checkbox.click()
                print("✅ CAPTCHA résolu.")
            except Exception as e:
                print(f"⚠️ CAPTCHA : échec du clic – {e}")
            name_elem = wait_for_game_title(timeout=30)

        if not name_elem:
            print(f"❌ Échec après tentative CAPTCHA – {url}")
            failed_writer.writerow([url, "Titre non chargé"])
            continue

        name = name_elem.text.strip()

        def get_cell_value(label):
            try:
                return driver.find_element(By.XPATH, f"//tr[td[contains(text(), '{label}')]]/td[2]").text.strip()
            except:
                return None

        app_id = get_cell_value("App ID")
        developer = get_cell_value("Developer")
        publisher = get_cell_value("Publisher")
        supported_systems = get_cell_value("Supported Systems")
        technologies = get_cell_value("Technologies")
        release_date = get_cell_value("Release Date")

        # Recherche du lien vers le Steam Store
        try:
            store_link = driver.find_element(By.XPATH, "//a[contains(@href, 'store.steampowered.com/app')]")
            store_url = store_link.get_attribute("href")
            steam_store_links[name] = store_url
        except:
            steam_store_links[name] = None

        data = {
            "Name": name,
            "App ID": app_id,
            "Developer": developer,
            "Publisher": publisher,
            "Supported Systems": supported_systems,
            "Technologies": technologies,
            "Release Date": release_date
        }

        success_writer.writerow(data)
        print(f"✅ {i+1}/{len(urls)} - {name}")

        time.sleep(60)

    except Exception as e:
        print(f"❌ Erreur sur {url} : {e}")
        failed_writer.writerow([url, str(e)])
        continue

driver.quit()
success_file.close()
failed_file.close()

# Sauvegarde du dictionnaire dans un fichier JSON
with open("steam_store_links.json", "w", encoding="utf-8") as f:
    json.dump(steam_store_links, f, ensure_ascii=False, indent=4)

print("\n📁 Terminé : données dans 'games_data.csv' et liens store dans 'steam_store_links.json'")