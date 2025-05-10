import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
# options.add_argument("--headless")  # Décommente si tu veux tourner sans interface
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://steamdb.info/charts/")
time.sleep(3)

# Tous les liens de jeux (href = /app/{appid}/charts/)
links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/app/'][href$='/charts/']")

games = []
seen = set()

for link in links:
    name = link.text.strip()
    href = link.get_attribute("href").strip()
    if name and href and href not in seen:
        games.append({"game_name": name, "url": href})
        seen.add(href)
    if len(games) >= 100:
        break

# Sauvegarde CSV
with open("top_games.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["game_name", "url"])
    writer.writeheader()
    for game in games:
        writer.writerow(game)

driver.quit()
print(f"✅ {len(games)} jeux enregistrés dans top_games.csv")