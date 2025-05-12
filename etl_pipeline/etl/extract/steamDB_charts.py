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
jeux_a_exclure = ["Spacewar", "Source SDK Base 2007"]

# Trouver les liens des jeux populaires
links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/app/'][href$='/charts/']")

for link in links:
    name = link.text.strip()
    href = link.get_attribute("href").strip()
    # Vérifier si le jeu n'est pas dans la liste des jeux à exclure
    if name and href and href not in seen and name not in jeux_a_exclure:
        games.append({
            "game_name": name,
            "url": href
        })
        seen.add(href)
    # Continuer jusqu'à avoir 100 jeux (+ 1 pour le premier qui sera retiré)
    if len(games) >= 101:
        break

# Si on n'a pas atteint 100 jeux, continuer à chercher
if len(games) < 101:
    print(f"Besoin de plus de jeux. Actuellement {len(games)}")
    # Faire défiler la page pour charger plus de contenu si nécessaire
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # Rechercher plus de liens
    additional_links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/app/'][href$='/charts/']")
    for link in additional_links:
        name = link.text.strip()
        href = link.get_attribute("href").strip()
        if name and href and href not in seen and name not in jeux_a_exclure:
            games.append({
                "game_name": name,
                "url": href
            })
            seen.add(href)
        if len(games) >= 11:
            break

driver.quit()

# Supprimer le premier élément de la liste s'il existe
if games:
    premier_jeu = games[0]["game_name"]
    games.pop(0)
    print(f"Suppression du premier jeu: {premier_jeu}")

# === Sauvegarde JSON ===
os.makedirs("data", exist_ok=True)
output_path = os.path.join("data", "top_games.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(games, f, ensure_ascii=False, indent=4)

print(f"{len(games)} jeux enregistrés dans {output_path} pour traitement ultérieur")
print(f"Les jeux suivants ont été exclus du scraping: {', '.join(jeux_a_exclure)}")
