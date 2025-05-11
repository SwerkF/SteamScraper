import json
import time
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# === Charger les URLs ===
with open("data/steam_store_links.json", "r", encoding="utf-8") as f:
    games = json.load(f)

# === Setup Chrome ===
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# === Résultats ===
results = {}
errors = []

# === Fonction extraction config d'un bloc ===
def extract_config_from_block(block):
    lis = block.find_elements(By.CSS_SELECTOR, "ul.bb_ul > li")
    config = {}
    for li in lis:
        text = li.text.strip()
        if not text or text.lower().startswith("minimale") or text.lower().startswith("recommandée"):
            continue
        match = re.match(r'^\s*([^:]+):\s*(.+)', text)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            config[key] = value
    return config

# === Scraper principal ===
for i, (game_name, url) in enumerate(list(games.items())[:5]):  # test
    print(f"🔍 {i+1}. {game_name} — {url}")
    driver.get(url)
    time.sleep(3)

    # Accepter cookies si présent
    try:
        cookie_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "acceptAllButton"))
        )
        driver.execute_script("arguments[0].click();", cookie_btn)
        print("✅ Cookies acceptés.")
        time.sleep(1)
    except:
        print("⚠️ Pas de popup cookies détectée.")

    game_data = {}

    try:
        sysreq_block = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.game_page_autocollapse.sys_req"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", sysreq_block)
        time.sleep(2)

        # Cas avec onglets (multi-OS)
        tabs = driver.find_elements(By.CSS_SELECTOR, "div.sysreq_tab[data-os]")
        os_list = [tab.get_attribute("data-os") for tab in tabs]

        if os_list:
            for os_type in os_list:
                try:
                    tab_elem = driver.find_element(By.CSS_SELECTOR, f"div.sysreq_tab[data-os='{os_type}']")
                    driver.execute_script("arguments[0].scrollIntoView(true);", tab_elem)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", tab_elem)
                    time.sleep(1)

                    block = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, f"div.game_area_sys_req.sysreq_content[data-os='{os_type}']"))
                    )
                    config = extract_config_from_block(block)
                    if config:
                        game_data[os_type] = config
                        print(f"➡️ Config minimale extraite pour {os_type}")
                except Exception as e:
                    print(f"⚠️ Erreur avec {os_type} pour {game_name} : {e}")
        else:
            # Cas sans onglet (typiquement Windows seul)
            try:
                block = driver.find_element(By.CSS_SELECTOR, "div.game_area_sys_req_leftCol")
                config = extract_config_from_block(block)
                if config:
                    game_data["win"] = config
                    print(f"➡️ Config minimale extraite (bloc unique)")
            except Exception as e:
                print(f"❌ Aucun bloc détecté : {e}")

    except Exception as e:
        print(f"❌ Section config non trouvée pour {game_name} : {e}")
        errors.append({"game": game_name, "url": url, "reason": str(e)})
        continue

    if game_data:
        results[game_name] = game_data

    time.sleep(10)

driver.quit()

# === Sauvegarde ===
os.makedirs("data", exist_ok=True)

with open("data/steam_sysreqs.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

with open("data/steam_sysreqs_errors.json", "w", encoding="utf-8") as f:
    json.dump(errors, f, indent=4, ensure_ascii=False)

print("✅ Terminé. Résultats enregistrés dans 'data/steam_sysreqs.json'")
