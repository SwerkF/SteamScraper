import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# === Setup ===
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# === Extraction ===
driver.get("https://steamdb.info/charts/")
time.sleep(3)

games = []
seen = set()

# Trouver les liens des jeux populaires
links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/app/'][href$='/charts/']")

for link in links:
    name = link.text.strip()
    href = link.get_attribute("href").strip()
    if name and href and href not in seen:
        games.append({
            "game_name": name,
            "url": href
        })
        seen.add(href)
    if len(games) >= 100:
        break

driver.quit()

# === Sauvegarde JSON ===
os.makedirs("data", exist_ok=True)
output_path = os.path.join("data", "top_games.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(games, f, ensure_ascii=False, indent=4)

print(f"✅ {len(games)} jeux enregistrés dans {output_path}")
